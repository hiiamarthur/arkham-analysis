import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { CardModalService } from '../../services/card-modal.service';
import { ArkhamIconsPipe } from '../pipes/arkham-icons.pipe';
import { IconService } from '../services/icon.service';
import { ArkhamSvgIconsService } from '../services/arkham-svg-icons.service';
import { SafeHtml } from '@angular/platform-browser';

@Component({
  selector: 'app-card-modal',
  standalone: true,
  imports: [CommonModule, ArkhamIconsPipe],
  template: `
    <!-- Card Stats Modal -->
    <div class="stats-modal-overlay" *ngIf="cardModalService.showModal()" (click)="cardModalService.closeModal()">
      <div class="stats-modal" (click)="$event.stopPropagation()">
        <button class="close-button" (click)="cardModalService.closeModal()" [innerHTML]="getIcon('close')"></button>

        <!-- Loading State -->
        <div *ngIf="cardModalService.loading()" class="modal-loading">
          <div class="loading-spinner"></div>
          <p>Loading card data...</p>
        </div>

        <!-- Card Content -->
        <div *ngIf="!cardModalService.loading() && cardModalService.selectedCardStats() as stats" class="stats-content">
          <!-- Header -->
          <div class="stats-header">
            <h2>{{stats.card_info.name}}</h2>
            <span class="card-type-badge">{{stats.card_info.type}}</span>
          </div>

          <!-- Overview Stats -->
          <div class="stats-overview-compact">
            <div class="stat-card-compact">
              <span class="stat-icon-compact" [innerHTML]="getIcon('popularity')"></span>
              <div class="stat-content-compact">
                <div class="stat-value-compact">{{ stats.deck_stats.popularity.overall_usage_rate * 100 | number:'1.1-1' }}%</div>
                <div class="stat-label-compact">Usage Rate</div>
              </div>
            </div>
            <div class="stat-card-compact">
              <span class="stat-icon-compact" [innerHTML]="getTrendIcon(stats.deck_stats.trend.trend_direction)"></span>
              <div class="stat-content-compact">
                <div class="stat-value-compact">{{ stats.deck_stats.trend.change_rate * 100 | number:'1.1-1' }}%</div>
                <div class="stat-label-compact">Trend</div>
              </div>
            </div>
            <div class="stat-card-compact">
              <span class="stat-icon-compact" [innerHTML]="getIcon('target')"></span>
              <div class="stat-content-compact">
                <div class="stat-value-compact">{{ stats.deck_stats.popularity.investigator_spread | number:'1.0-0' }}</div>
                <div class="stat-label-compact">Investigator Spread</div>
              </div>
            </div>
            <div class="stat-card-compact">
              <span class="stat-icon-compact" [innerHTML]="getIcon('total-decks')"></span>
              <div class="stat-content-compact">
                <div class="stat-value-compact">{{ stats.data_source.decks_analyzed.toLocaleString() }}</div>
                <div class="stat-label-compact">Decks Analyzed</div>
              </div>
            </div>
          </div>

          <!-- Card Details -->
          <div *ngIf="cardModalService.selectedCardDetails() as details" class="card-details-section-top">
            <div class="card-details-layout-horizontal">
              <!-- Card Image -->
              <div class="card-image-container">
                <img *ngIf="details.imagesrc"
                     [src]="'https://arkhamdb.com' + details.imagesrc"
                     [alt]="details.name"
                     class="card-image"
                     (error)="$any($event.target).style.display='none'">
                <div *ngIf="!details.imagesrc" class="no-image-placeholder">
                  <span class="no-image-icon">🃏</span>
                  <p>No image available</p>
                </div>
              </div>

              <!-- Card Content Column -->
              <div class="card-content-column">
                <!-- Card Stats -->
                <div class="card-stats-grid">
                  <div class="stat-pill" *ngIf="details.cost !== null && details.cost !== undefined">
                    <span class="stat-pill-label">Cost</span>
                    <span class="stat-pill-value">{{details.cost}}</span>
                  </div>
                  <div class="stat-pill" *ngIf="details.xp !== null && details.xp !== undefined">
                    <span class="stat-pill-label">XP</span>
                    <span class="stat-pill-value">{{details.xp}}</span>
                  </div>
                  <div class="stat-pill" *ngIf="details.health">
                    <span class="stat-pill-label">Health</span>
                    <span class="stat-pill-value">{{details.health}}</span>
                  </div>
                  <div class="stat-pill" *ngIf="details.sanity">
                    <span class="stat-pill-label">Sanity</span>
                    <span class="stat-pill-value">{{details.sanity}}</span>
                  </div>
                </div>

                <!-- Skill Icons -->
                <div class="skill-icons-row" *ngIf="details.skill_willpower || details.skill_intellect || details.skill_combat || details.skill_agility">
                  <div class="skill-icon-item" *ngIf="details.skill_willpower">
                    <span class="skill-icon-svg" [innerHTML]="getSkillIcon('willpower')"></span>
                    <span class="skill-value">{{details.skill_willpower}}</span>
                  </div>
                  <div class="skill-icon-item" *ngIf="details.skill_intellect">
                    <span class="skill-icon-svg" [innerHTML]="getSkillIcon('intellect')"></span>
                    <span class="skill-value">{{details.skill_intellect}}</span>
                  </div>
                  <div class="skill-icon-item" *ngIf="details.skill_combat">
                    <span class="skill-icon-svg" [innerHTML]="getSkillIcon('combat')"></span>
                    <span class="skill-value">{{details.skill_combat}}</span>
                  </div>
                  <div class="skill-icon-item" *ngIf="details.skill_agility">
                    <span class="skill-icon-svg" [innerHTML]="getSkillIcon('agility')"></span>
                    <span class="skill-value">{{details.skill_agility}}</span>
                  </div>
                </div>

                <!-- Card Text -->
                <div class="card-text-section" *ngIf="details.real_text || details.text">
                  <div class="card-text" [innerHTML]="(details.real_text || details.text) | arkhamIcons"></div>
                </div>

                <!-- Traits -->
                <div class="traits-row" *ngIf="details.traits">
                  <span class="trait-badge" *ngFor="let trait of getTraitsArray(details.traits)">{{trait}}</span>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  `,
  styleUrls: ['../../../app/components/card-analysis/card-analysis.component.css']
})
export class CardModalComponent {
  cardModalService = inject(CardModalService);
  private iconService = inject(IconService);
  private arkhamSvgIconsService = inject(ArkhamSvgIconsService);

  getIcon(iconName: string): SafeHtml {
    return this.iconService.getIcon(iconName);
  }

  getSkillIcon(skillName: string): SafeHtml {
    // Use colored version for skill icons
    return this.arkhamSvgIconsService.getIcon(`${skillName}-color`);
  }

  getTrendIcon(trendDirection: string): SafeHtml {
    switch (trendDirection) {
      case 'increasing':
        return this.iconService.getIcon('rising');
      case 'decreasing':
        return this.iconService.getIcon('falling');
      default:
        return this.iconService.getIcon('trend');
    }
  }

  getTraitsArray(traits: string | Array<{ name: string }> | undefined): string[] {
    if (!traits) return [];
    if (typeof traits === 'string') {
      return traits.split('.').map(t => t.trim()).filter(t => t.length > 0);
    }
    if (Array.isArray(traits)) {
      return traits.map(t => typeof t === 'string' ? t : t.name);
    }
    return [];
  }
}
