import { Component, signal, computed, OnInit, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute } from '@angular/router';
import { DataTableComponent, TableColumn, TableConfig } from '../../shared/components/data-table.component';
import { InvestigatorService, InvestigatorStatsResponse, CardRanking, StapleCard, TrendingCard, CardSynergy, DeckArchetype, UnderusedGem } from '../../services/investigator.service';
import { CardService, CardResponse } from '../../services/card.service';
import { CardCodeLinkComponent } from '../../shared/components/card-code-link.component';
import { CardModalComponent } from '../../shared/components/card-modal.component';
import { ArkhamSvgIconsService } from '../../shared/services/arkham-svg-icons.service';
import { IconService } from '../../shared/services/icon.service';
import { SafeHtml, DomSanitizer } from '@angular/platform-browser';

interface Investigator {
  code: string;
  name: string;
  faction: string;
  willpower: number;
  intellect: number;
  combat: number;
  agility: number;
  health: number;
  sanity: number;
  deckSize: number;
  deckSizeMin?: number;
  deckSizeMax?: number;
  expansion: string;
  popularity: number;
  totalDecks?: number;
  totalDecksAnalyzed?: number;
  imageUrl?: string;
}

@Component({
  selector: 'app-investigators',
  standalone: true,
  imports: [CommonModule, DataTableComponent, CardCodeLinkComponent, CardModalComponent],
  templateUrl: './investigators.component.html',
  styleUrl: './investigators.component.css'
})
export class InvestigatorsComponent implements OnInit {
  private investigatorService = inject(InvestigatorService);
  private cardService = inject(CardService);
  private arkhamIconsService = inject(ArkhamSvgIconsService);
  private iconService = inject(IconService);
  private sanitizer = inject(DomSanitizer);
  private route = inject(ActivatedRoute);

  // Expose Math to template
  Math = Math;

  // Loading states
  investigatorsLoading = signal<boolean>(true);
  statsLoading = signal<boolean>(false);
  statsNoData = signal<boolean>(false);   // true when investigator has no deck data

  // Selected investigator
  selectedInvestigator = signal<Investigator | null>(null);
  selectedInvestigatorCode = signal<string | null>(null);

  // Faction pre-filter from query param
  factionFilter = signal<string | null>(null);

  // All investigators data
  investigators = signal<Investigator[]>([]);

  // Filtered investigators (by faction query param)
  filteredInvestigators = computed(() => {
    const faction = this.factionFilter();
    if (!faction) return this.investigators();
    return this.investigators().filter(inv => inv.faction.toLowerCase() === faction.toLowerCase());
  });

  // Raw stats response
  investigatorStats = signal<InvestigatorStatsResponse | null>(null);

  ngOnInit() {
    const params = this.route.snapshot.queryParamMap;
    const factionParam = params.get('faction');
    const investigatorParam = params.get('investigator');

    if (factionParam) {
      this.factionFilter.set(factionParam);
    }

    this.loadInvestigators().then(() => {
      if (investigatorParam) {
        const match = this.investigators().find(inv => inv.code === investigatorParam);
        if (match) this.onInvestigatorClick(match);
      }
    });
  }

  async loadInvestigators(): Promise<void> {
    this.investigatorsLoading.set(true);
    try {
      const metadata = await this.investigatorService.getAllInvestigators().toPromise();

      if (metadata) {
        // Fetch full card details for each investigator
        const investigatorPromises = metadata.map(async (meta) => {
          try {
            const cardDetails = await this.cardService.getCard(meta.code).toPromise();
            return this.mapCardToInvestigator(cardDetails!, meta.faction_code || 'Neutral');
          } catch (error) {
            console.error(`Error loading investigator ${meta.code}:`, error);
            return null;
          }
        });

        const investigatorsData = await Promise.all(investigatorPromises);
        this.investigators.set(investigatorsData.filter(inv => inv !== null) as Investigator[]);
      }
    } catch (error) {
      console.error('Error loading investigators:', error);
    } finally {
      this.investigatorsLoading.set(false);
    }
  }

  private mapCardToInvestigator(card: CardResponse, faction: string): Investigator {
    return {
      code: card.code,
      name: card.name,
      faction: this.normalizeFactionName(card.faction_name || faction),
      willpower: card.skill_willpower || 0,
      intellect: card.skill_intellect || 0,
      combat: card.skill_combat || 0,
      agility: card.skill_agility || 0,
      health: card.health || 0,
      sanity: card.sanity || 0,
      deckSize: Math.round(card.average_deck_size || card.deck_limit || 30),
      deckSizeMin: card.deck_size_min,
      deckSizeMax: card.deck_size_max,
      expansion: card.pack_name || 'Unknown',
      popularity: card.meta_share ? Math.round(card.meta_share * 100) : 0,
      totalDecks: card.total_decks,
      totalDecksAnalyzed: card.total_decks_analyzed,
      imageUrl: card.imagesrc ? `https://arkhamdb.com${card.imagesrc}` : undefined
    };
  }

  private normalizeFactionName(faction: string): string {
    const factionMap: Record<string, string> = {
      'guardian': 'Guardian',
      'seeker': 'Seeker',
      'rogue': 'Rogue',
      'mystic': 'Mystic',
      'survivor': 'Survivor',
      'neutral': 'Neutral'
    };
    return factionMap[faction.toLowerCase()] || faction;
  }


  // Table columns for investigators list
  investigatorColumns: TableColumn[] = [
    { key: 'name', label: 'Name', sortable: true, searchable: true, width: '200px' },
    { key: 'faction', label: 'Class', sortable: true, filterable: true, width: '120px' },
    { key: 'willpower', label: 'Willpower', sortable: true, type: 'number', width: '100px' },
    { key: 'intellect', label: 'Intellect', sortable: true, type: 'number', width: '100px' },
    { key: 'combat', label: 'Combat', sortable: true, type: 'number', width: '100px' },
    { key: 'agility', label: 'Agility', sortable: true, type: 'number', width: '100px' },
    { key: 'health', label: 'Health', sortable: true, type: 'number', width: '80px' },
    { key: 'sanity', label: 'Sanity', sortable: true, type: 'number', width: '80px' },
    { key: 'expansion', label: 'Expansion', sortable: true, filterable: true }
  ];

  // Table columns for card rankings
  cardRankingColumns: TableColumn[] = [
    { key: 'card_name', label: 'Card Name', sortable: true, searchable: true, width: '200px' },
    { key: 'usage_count', label: 'Usage Count', sortable: true, type: 'number', width: '120px' },
    { key: 'usage_rate', label: 'Usage Rate', sortable: true, type: 'number', width: '120px', render: (value: number) => `${(value * 100).toFixed(1)}%` },
    { key: 'average_quantity', label: 'Avg Qty', sortable: true, type: 'number', width: '100px' },
    { key: 'consistency_score', label: 'Consistency', sortable: true, type: 'number', width: '120px', render: (value: number) => `${(value * 100).toFixed(1)}%` }
  ];

  // Table columns for staple cards
  stapleCardColumns: TableColumn[] = [
    { key: 'card_name', label: 'Card Name', sortable: true, searchable: true, width: '200px' },
    { key: 'usage_rate', label: 'Usage Rate', sortable: true, type: 'number', width: '120px', render: (value: number) => `${(value * 100).toFixed(1)}%` },
    { key: 'staple_confidence', label: 'Confidence', sortable: true, type: 'number', width: '120px', render: (value: number) => `${(value * 100).toFixed(1)}%` },
    { key: 'average_quantity', label: 'Avg Qty', sortable: true, type: 'number', width: '100px' }
  ];

  // Table columns for card synergies
  synergyColumns: TableColumn[] = [
    { key: 'card1', label: 'Card 1', sortable: true, searchable: true, width: '150px' },
    { key: 'card2', label: 'Card 2', sortable: true, searchable: true, width: '150px' },
    { key: 'co_occurrence_count', label: 'Times Together', sortable: true, type: 'number', width: '140px' },
    { key: 'synergy_strength', label: 'Synergy Strength', sortable: true, type: 'number', width: '150px', render: (value: number) => `${(value * 100).toFixed(1)}%` }
  ];

  // Table config
  tableConfig: TableConfig = {
    pageSize: 10,
    pageSizeOptions: [5, 10, 25, 50],
    showPagination: true,
    showSearch: true,
    showColumnToggle: true,
    showFilters: true,
    striped: true,
    hoverable: true,
    bordered: true,
    responsive: true
  };

  smallTableConfig: TableConfig = {
    pageSize: 10,
    pageSizeOptions: [10, 25, 50],
    showPagination: true,
    showSearch: true,
    showColumnToggle: false,
    showFilters: false,
    striped: true,
    hoverable: true,
    bordered: true,
    responsive: true
  };

  // Event handlers
  async onInvestigatorClick(investigator: Investigator) {
    this.selectedInvestigator.set(investigator);
    this.selectedInvestigatorCode.set(investigator.code);
    this.statsNoData.set(false);

    // Load stats for this investigator
    this.statsLoading.set(true);
    try {
      const raw = await this.investigatorService.getInvestigatorStats(investigator.code).toPromise();
      // Backend returns {investigator_info, error} when no decks exist — not a full stats object.
      // Detect this in TS (not the template) so we avoid accessing missing fields.
      if (!raw || !raw.card_rankings) {
        this.investigatorStats.set(null);
        this.statsNoData.set(true);
      } else {
        this.investigatorStats.set(raw);
      }
    } catch (error) {
      console.error('Error loading investigator stats:', error);
      this.investigatorStats.set(null);
      this.statsNoData.set(true);
    } finally {
      this.statsLoading.set(false);
    }

    // Scroll to details section
    setTimeout(() => {
      document.getElementById('investigator-details')?.scrollIntoView({ behavior: 'smooth' });
    }, 100);
  }

  backToList() {
    this.selectedInvestigator.set(null);
    this.selectedInvestigatorCode.set(null);
    this.investigatorStats.set(null);
    this.statsNoData.set(false);
  }

  getClassColor(className: string): string {
    const colors: Record<string, string> = {
      'Guardian': '#2b80c5',
      'Seeker': '#ec8b26',
      'Rogue': '#107116',
      'Mystic': '#4e1a45',
      'Survivor': '#cc3038',
      'Neutral': '#5a5a5a'
    };
    return colors[className] || '#5a5a5a';
  }

  // Get Arkham game icon as SafeHtml for template
  getIcon(iconName: string): SafeHtml {
    const svg = this.arkhamIconsService.getIcon(iconName);
    return this.sanitizer.bypassSecurityTrustHtml(svg);
  }

  // Custom SVG icons for non-game-specific stats
  getCustomIcon(iconType: string): SafeHtml {
    return this.iconService.getIcon(iconType);
  }

  // Get meta share tooltip text
  getMetaShareTooltip(): string {
    const stats = this.investigatorStats();
    if (!stats) {
      return 'Percentage of all competitive decks using this investigator';
    }
    const totalDecks = stats.meta_position.total_decks;
    const totalAnalyzed = stats.meta_position.total_decks_analyzed;
    return `Percentage of all competitive decks using this investigator (${totalDecks} out of ${totalAnalyzed} total decks)`;
  }

  // Help panel
  showHelp = signal<boolean>(false);

  toggleHelp() {
    this.showHelp.update(v => !v);
  }
}
