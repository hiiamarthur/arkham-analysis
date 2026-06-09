import { Component, inject, computed, PLATFORM_ID } from '@angular/core';
import { CommonModule, isPlatformBrowser } from '@angular/common';
import { CardTooltipService } from '../services/card-tooltip.service';
import { CardResponse } from '../../services/card.service';

const TOOLTIP_GAP      = 4;

const INV_TOOLTIP_W    = 280;
const INV_IMG_HEIGHT   = 160;
const INV_TOOLTIP_H    = 230;

const CARD_TOOLTIP_W   = 200;
const CARD_IMG_HEIGHT  = 240;
const CARD_TOOLTIP_H   = 320;

@Component({
  selector: 'app-card-tooltip-overlay',
  standalone: true,
  imports: [CommonModule],
  template: `
    <ng-container *ngIf="tooltipService.isVisible() && !tooltipService.loading() && tooltipService.card() as card">
      <div
        class="ct-tooltip"
        [style.top.px]="position().top"
        [style.left.px]="position().left"
        [style.width.px]="card.type_code === 'investigator' ? ${INV_TOOLTIP_W} : ${CARD_TOOLTIP_W}"
        role="tooltip"
        aria-live="polite">

        <div class="ct-body">
          <img
            class="ct-image"
            [style.height.px]="card.type_code === 'investigator' ? ${INV_IMG_HEIGHT} : ${CARD_IMG_HEIGHT}"
            [src]="imageUrl(card)"
            [alt]="card.name"
            (error)="onImgError($event)"
          />
          <div class="ct-info">
            <div class="ct-name">
              {{ card.name }}
              <span *ngIf="card.subname" class="ct-subname"> · {{ card.subname }}</span>
            </div>
            <div class="ct-meta">
              <span class="ct-type">{{ card.type_name }}</span>
              <span *ngIf="card.xp != null && card.xp > 0" class="ct-xp">{{ card.xp }}XP</span>
              <span *ngIf="card.cost != null && card.type_code !== 'investigator'" class="ct-cost">\${{ card.cost }}</span>
            </div>
            <div *ngIf="traitsStr(card)" class="ct-traits">{{ traitsStr(card) }}</div>
          </div>
        </div>

      </div>
    </ng-container>
  `,
  styles: [`
    .ct-tooltip {
      position: fixed;
      z-index: 9999;
      background: var(--surface-elevated, #16213e);
      border: 1px solid var(--accent-gold, #c9a84c);
      border-radius: 8px;
      box-shadow: 0 12px 40px rgba(0,0,0,0.7);
      overflow: hidden;
      pointer-events: none;
      animation: ct-fade-in 0.12s ease;
    }

    @keyframes ct-fade-in {
      from { opacity: 0; transform: translateY(4px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    .ct-body {
      display: flex;
      flex-direction: column;
    }

    .ct-image {
      width: 100%;
      object-fit: cover;
      object-position: top center;
      display: block;
      border-bottom: 1px solid rgba(255,255,255,0.08);
      flex-shrink: 0;
    }

    .ct-info {
      flex: 1;
      padding: 0.5rem 0.6rem;
      min-width: 0;
      display: flex;
      flex-direction: column;
      gap: 0.15rem;
      justify-content: center;
    }

    .ct-name {
      font-size: 0.78rem;
      font-weight: 700;
      color: var(--text-primary, #e8e0d5);
      line-height: 1.3;
      word-break: break-word;
    }

    .ct-subname {
      font-weight: 400;
      opacity: 0.7;
    }

    .ct-meta {
      display: flex;
      gap: 0.4rem;
      flex-wrap: wrap;
      margin-top: 0.1rem;
    }

    .ct-type {
      font-size: 0.68rem;
      color: var(--text-muted, rgba(255,255,255,0.5));
    }

    .ct-xp {
      font-size: 0.68rem;
      color: var(--accent-gold, #c9a84c);
      font-weight: 600;
    }

    .ct-cost {
      font-size: 0.68rem;
      color: #94a3b8;
    }

    .ct-traits {
      font-size: 0.65rem;
      color: var(--text-muted, rgba(255,255,255,0.4));
      font-style: italic;
      overflow: hidden;
      text-overflow: ellipsis;
      display: -webkit-box;
      -webkit-line-clamp: 2;
      -webkit-box-orient: vertical;
    }

  `],
})
export class CardTooltipOverlayComponent {
  protected tooltipService = inject(CardTooltipService);
  private platformId = inject(PLATFORM_ID);

  imageUrl(card: CardResponse): string {
    if (card.imagesrc) return 'https://arkhamdb.com' + card.imagesrc;
    return `https://arkhamdb.com/bundles/cards/${card.code}.png`;
  }

  onImgError(event: Event): void {
    const img = event.target as HTMLImageElement;
    if (!img.src.endsWith('.jpg')) {
      img.src = img.src.replace(/\.\w+$/, '.jpg');
    } else {
      img.style.display = 'none';
    }
  }

  traitsStr(card: CardResponse): string {
    if (!card.traits) return '';
    if (typeof card.traits === 'string') return card.traits;
    return card.traits.map((t: { name: string }) => t.name).join(', ');
  }

  position = computed(() => {
    const anchor = this.tooltipService.anchor();
    if (!anchor || !isPlatformBrowser(this.platformId)) return { top: 0, left: 0 };

    const isInv = this.tooltipService.card()?.type_code === 'investigator';
    const w = isInv ? INV_TOOLTIP_W : CARD_TOOLTIP_W;
    const h = isInv ? INV_TOOLTIP_H : CARD_TOOLTIP_H;
    const vw = window.innerWidth;
    const vh = window.innerHeight;

    let left = anchor.x + TOOLTIP_GAP;
    if (left + w > vw - 8) left = anchor.x - w - TOOLTIP_GAP;
    left = Math.max(8, Math.min(left, vw - w - 8));

    let top = anchor.y - 8;
    if (top + h > vh - 8) top = Math.max(8, vh - h - 8);

    return { top, left };
  });
}
