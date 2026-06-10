import { Injectable, signal, inject } from '@angular/core';
import { firstValueFrom } from 'rxjs';
import { CardService, CardResponse } from '../../services/card.service';

export interface TooltipAnchor {
  x: number;
  y: number;
}

@Injectable({ providedIn: 'root' })
export class CardTooltipService {
  private cardService = inject(CardService);
  private cache = new Map<string, CardResponse>();
  private pendingCode: string | null = null;

  isVisible = signal(false);
  card = signal<CardResponse | null>(null);
  loading = signal(false);
  anchor = signal<TooltipAnchor | null>(null);

  async showTooltip(code: string, x: number, y: number): Promise<void> {
    if (!code) return;

    this.pendingCode = code;
    this.anchor.set({ x, y });

    if (this.cache.has(code)) {
      if (this.pendingCode === code) {
        this.card.set(this.cache.get(code)!);
        this.loading.set(false);
        this.isVisible.set(true);
      }
      return;
    }

    this.loading.set(true);
    this.card.set(null);
    this.isVisible.set(true);

    try {
      const data = await firstValueFrom(this.cardService.getCard(code));
      if (this.pendingCode === code) {
        this.cache.set(code, data);
        this.card.set(data);
      }
    } catch {
      if (this.pendingCode === code) this.isVisible.set(false);
    } finally {
      if (this.pendingCode === code) this.loading.set(false);
    }
  }

  hideTooltip(): void {
    this.pendingCode = null;
    this.isVisible.set(false);
    this.card.set(null);
    this.loading.set(false);
  }
}
