import { DOCUMENT, isPlatformBrowser } from '@angular/common';
import { Inject, Injectable, PLATFORM_ID } from '@angular/core';
import { Meta, Title } from '@angular/platform-browser';

export type SeoMetaInput = {
  title?: string;
  description?: string;
  image?: string;
  canonicalUrl?: string;
  robots?: string;
  noIndex?: boolean;
};

@Injectable({ providedIn: 'root' })
export class SeoService {
  private readonly defaultTitle = 'Arkham Analysis';
  private readonly defaultDescription =
    'Arkham Horror: The Card Game analytics — deck statistics, card analysis, and scenario threat assessment.';

  constructor(
    private readonly title: Title,
    private readonly meta: Meta,
    @Inject(DOCUMENT) private readonly document: Document,
    @Inject(PLATFORM_ID) private readonly platformId: object,
  ) {}

  update(input: SeoMetaInput): void {
    const computedTitle = input.title ? `${input.title} · ${this.defaultTitle}` : this.defaultTitle;
    const computedDescription = input.description ?? this.defaultDescription;
    const robots = input.noIndex ? 'noindex,nofollow' : (input.robots ?? 'index,follow');

    this.title.setTitle(computedTitle);
    this.setName('description', computedDescription);
    this.setName('robots', robots);

    // Open Graph
    this.setProperty('og:site_name', this.defaultTitle);
    this.setProperty('og:type', 'website');
    this.setProperty('og:title', computedTitle);
    this.setProperty('og:description', computedDescription);
    this.setProperty('og:url', this.getCanonicalUrl(input));
    if (input.image) this.setProperty('og:image', input.image);

    // Twitter
    this.setName('twitter:card', 'summary');
    this.setName('twitter:title', computedTitle);
    this.setName('twitter:description', computedDescription);
    if (input.image) this.setName('twitter:image', input.image);

    // Canonical
    const canonical = this.getCanonicalUrl(input);
    if (canonical) this.setCanonicalLink(canonical);
  }

  private setName(name: string, content: string | null | undefined): void {
    if (!content) return;
    this.meta.updateTag({ name, content });
  }

  private setProperty(property: string, content: string | null | undefined): void {
    if (!content) return;
    this.meta.updateTag({ property, content });
  }

  private getCanonicalUrl(input: SeoMetaInput): string | null {
    if (input.canonicalUrl) return input.canonicalUrl;
    if (!isPlatformBrowser(this.platformId)) return null;
    const href = this.document?.location?.href;
    if (!href) return null;
    // Strip hash fragments for canonical
    return href.split('#')[0];
  }

  private setCanonicalLink(url: string): void {
    let linkEl = this.document.querySelector<HTMLLinkElement>('link[rel="canonical"]');
    if (!linkEl) {
      linkEl = this.document.createElement('link');
      linkEl.setAttribute('rel', 'canonical');
      this.document.head.appendChild(linkEl);
    }
    linkEl.setAttribute('href', url);
  }
}

