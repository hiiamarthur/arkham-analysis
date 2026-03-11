import { Injectable, signal } from '@angular/core';
import { CardService, CardResponse, CardStatsResponse } from './card.service';
import { forkJoin } from 'rxjs';

@Injectable({
  providedIn: 'root'
})
export class CardModalService {
  // Modal state
  showModal = signal(false);
  selectedCardDetails = signal<CardResponse | null>(null);
  selectedCardStats = signal<CardStatsResponse | null>(null);
  loading = signal(false);

  constructor(private cardService: CardService) {}

  /**
   * Open card modal with details only (no stats API call)
   */
  async openCardModal(cardCode: string): Promise<void> {
    this.loading.set(true);
    this.showModal.set(true);

    try {
      const details = await this.cardService.getCard(cardCode).toPromise();
      if (details) {
        this.selectedCardDetails.set(details);
      }
    } catch (error) {
      console.error('Error loading card details:', error);
    } finally {
      this.loading.set(false);
    }
  }

  /**
   * Close the card modal
   */
  closeModal(): void {
    this.showModal.set(false);
    this.selectedCardDetails.set(null);
    this.selectedCardStats.set(null);
  }
}
