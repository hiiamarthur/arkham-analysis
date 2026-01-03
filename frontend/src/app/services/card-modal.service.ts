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
   * Open card modal with details and stats
   */
  async openCardModal(cardCode: string): Promise<void> {
    this.loading.set(true);
    this.showModal.set(true);

    try {
      const result = await forkJoin({
        details: this.cardService.getCard(cardCode),
        stats: this.cardService.getCardStats(cardCode)
      }).toPromise();

      if (result) {
        this.selectedCardDetails.set(result.details);
        this.selectedCardStats.set(result.stats);
      }
    } catch (error) {
      console.error('Error loading card data:', error);
      // Try to at least load the card details
      try {
        const details = await this.cardService.getCard(cardCode).toPromise();
        if (details) {
          this.selectedCardDetails.set(details);
        }
      } catch (detailsError) {
        console.error('Error loading card details:', detailsError);
      }
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
