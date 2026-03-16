import { DOCUMENT } from '@angular/common';
import { Inject, Injectable } from '@angular/core';
import { Meta, Title } from '@angular/platform-browser';

export type SeoMetaInput = {
  title?: string;
  description?: string;
  image?: string;
  canonicalUrl?: string;
  robots?: string;
  noIndex?: boolean;
};

const BASE_URL = 'https://arkham-analysis.arthurlau.dev';
const DEFAULT_IMAGE = `${BASE_URL}/favicon.svg`;

@Injectable({ providedIn: 'root' })
export class SeoService {
  private readonly defaultTitle = 'Arkham Analysis';
  private readonly defaultDescription =
    'Arkham Horror: The Card Game analytics — deck statistics, card analysis, and scenario threat assessment.';

  constructor(
    private readonly title: Title,
    private readonly meta: Meta,
    @Inject(DOCUMENT) private readonly document: Document,
  ) {}

  update(input: SeoMetaInput): void {
    const computedTitle = input.title ? `${input.title} · ${this.defaultTitle}` : this.defaultTitle;
    const computedDescription = input.description ?? this.defaultDescription;
    const robots = input.noIndex ? 'noindex,nofollow' : (input.robots ?? 'index,follow');
    const image = input.image ?? DEFAULT_IMAGE;
    const canonical = this.getCanonicalUrl(input);

    this.title.setTitle(computedTitle);
    this.setName('description', computedDescription);
    this.setName('robots', robots);

    // Open Graph
    this.setProperty('og:site_name', this.defaultTitle);
    this.setProperty('og:type', 'website');
    this.setProperty('og:title', computedTitle);
    this.setProperty('og:description', computedDescription);
    this.setProperty('og:image', image);
    this.setProperty('og:image:width', '512');
    this.setProperty('og:image:height', '512');
    if (canonical) this.setProperty('og:url', canonical);

    // Twitter — summary_large_image shows the image prominently in tweets
    this.setName('twitter:card', 'summary_large_image');
    this.setName('twitter:title', computedTitle);
    this.setName('twitter:description', computedDescription);
    this.setName('twitter:image', image);

    // Canonical link tag
    if (canonical) this.setCanonicalLink(canonical);

    // Per-page WebPage JSON-LD for structured data
    if (canonical) this.updatePageJsonLd(computedTitle, computedDescription, canonical);
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
    const href = this.document?.location?.href;
    if (!href) return null;
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

  private updatePageJsonLd(title: string, description: string, url: string): void {
    const id = 'page-json-ld';
    let scriptEl = this.document.getElementById(id) as HTMLScriptElement | null;
    if (!scriptEl) {
      scriptEl = this.document.createElement('script');
      scriptEl.type = 'application/ld+json';
      scriptEl.id = id;
      this.document.head.appendChild(scriptEl);
    }
    scriptEl.textContent = JSON.stringify({
      '@context': 'https://schema.org',
      '@type': 'WebPage',
      '@id': url,
      'name': title,
      'description': description,
      'url': url,
      'isPartOf': { '@id': `${BASE_URL}/#website` },
      'publisher': { '@id': `${BASE_URL}/#organization` },
    });
  }
}
