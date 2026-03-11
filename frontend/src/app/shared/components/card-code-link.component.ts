import { Component, Input, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Router } from '@angular/router';
import { CardModalService } from '../../services/card-modal.service';

@Component({
  selector: 'app-card-code-link',
  standalone: true,
  imports: [CommonModule],
  template: `
    <span
      class="card-code-link"
      (click)="onClick()"
      [title]="'Click to view ' + cardCode + ' details'">
      <ng-content>{{cardCode}}</ng-content>
    </span>
  `,
  styles: [`
    .card-code-link {
      cursor: pointer;
      color: #60a5fa;
      font-family: 'JetBrains Mono', monospace;
      font-weight: 600;
      text-decoration: none;
      border-bottom: 1px dashed rgba(96, 165, 250, 0.3);
      transition: all 0.3s;
      display: inline-block;
      padding: 0.125rem 0.25rem;
      border-radius: 0.25rem;
    }

    .card-code-link:hover {
      background: rgba(96, 165, 250, 0.1);
      border-bottom-color: #60a5fa;
      transform: translateY(-1px);
    }

    .card-code-link:active {
      transform: translateY(0);
    }
  `]
})
export class CardCodeLinkComponent {
  @Input({ required: true }) cardCode!: string;

  private cardModalService = inject(CardModalService);
  private router = inject(Router);

  onClick(): void {
    if (!this.cardCode) return;

    // Check if we're on the analysis page
    const currentUrl = this.router.url;
    if (currentUrl.startsWith('/analysis')) {
      // Navigate to /analysis/{code} to change URL
      this.router.navigate(['/analysis', this.cardCode]);
    } else {
      // On other pages (investigators, etc.), open modal
      this.cardModalService.openCardModal(this.cardCode);
    }
  }
}
