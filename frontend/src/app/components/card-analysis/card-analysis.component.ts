import { Component, signal, computed, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, FormArray } from '@angular/forms';
import { AnalysisService, CardAnalysisRequest, AnalysisResponse } from '../../services/analysis.service';
import { DataTableComponent, TableColumn, TableConfig } from '../../shared/components/data-table.component';
import { CardService, CardResponse, CardStatsResponse } from '../../services/card.service';
import { AppStateService } from '../../services/app-state.service';
import { ArkhamIconsPipe } from '../../shared/pipes/arkham-icons.pipe';

interface Card {
  code: string;
  name: string;
  type: string;
  class: string;
  cost: number | null;
  faction: string;
  pack: string;
  xp?: number;
  flavor?: string;
  skillWillpower?: number;
  skillIntellect?: number;
  skillCombat?: number;
  skillAgility?: number;
  skillWild?: number;
  text?: string;
  traits?: string | Array<{ name: string }>;
  slot?: string;
  health?: number;
  sanity?: number;
  // Enhanced stats
  usageRate?: number;
  winRateWithCard?: number;
  averageTimePlayed?: string;
  topInvestigators?: { name: string; usageRate: number; winRate: number }[];
  synergyCards?: { code: string; name: string; synergyScore: number }[];
  deckInclusionRate?: number;
  performanceByDifficulty?: { difficulty: string; winRate: number }[];
  performanceByCampaign?: { campaign: string; winRate: number }[];
  versatilityScore?: number;
  economyRating?: number;
  impactRating?: number;
  consistencyRating?: number;
}

@Component({
  selector: 'app-card-analysis',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, DataTableComponent, ArkhamIconsPipe],
  templateUrl: './card-analysis.component.html',
  styleUrl: './card-analysis.component.css'
})
export class CardAnalysisComponent implements OnInit {
  analysisForm: FormGroup;

  // Expose Math to template
  Math = Math;

  // Tab management
  activeTab = signal<'browser' | 'gpt-analysis'>('browser');

  // Signals for reactive state management
  loading = signal(false);
  results = signal<AnalysisResponse | null>(null);
  error = signal<string | null>(null);
  analysisType = signal<'strength' | 'synergies' | 'timing'>('strength');

  // Card browser
  selectedCard = signal<Card | null>(null);
  cards = signal<Card[]>([]);
  cardsLoading = signal(false);

  // Card stats modal
  showStatsModal = signal(false);
  selectedCardStats = signal<CardStatsResponse | null>(null);
  selectedCardDetails = signal<CardResponse | null>(null);
  statsLoading = signal(false);

  // Expandable sections
  topInvestigatorsExpanded = signal(true);
  usageTrendExpanded = signal(true);

  // Pagination
  currentPage = signal(1);
  pageSize = signal(25);
  totalResults = signal(0);
  hasNextPage = signal(false);
  hasPrevPage = signal(false);

  // Basic search filters
  searchQuery = signal('');
  searchFaction = signal('');
  searchType = signal('');
  searchTrait = signal('');
  searchMinCost = signal<number | undefined>(undefined);
  searchMaxCost = signal<number | undefined>(undefined);

  // Advanced filters (collapsible)
  showAdvancedFilters = signal(false);
  searchText = signal('');
  searchFlavor = signal('');
  searchSlot = signal('');
  searchIsUnique = signal<boolean | undefined>(undefined);
  searchPermanent = signal<boolean | undefined>(undefined);
  searchMinWillpower = signal<number | undefined>(undefined);
  searchMinIntellect = signal<number | undefined>(undefined);
  searchMinCombat = signal<number | undefined>(undefined);
  searchMinAgility = signal<number | undefined>(undefined);
  searchMinHealth = signal<number | undefined>(undefined);
  searchMinSanity = signal<number | undefined>(undefined);

  // Computed values
  hasResults = computed(() => this.results() !== null);
  hasError = computed(() => this.error() !== null);

  // Form options
  campaigns = [
    { value: 'night_of_the_zealot', label: 'Night of the Zealot' },
    { value: 'dunwich_legacy', label: 'The Dunwich Legacy' },
    { value: 'path_to_carcosa', label: 'The Path to Carcosa' },
    { value: 'forgotten_age', label: 'The Forgotten Age' },
    { value: 'circle_undone', label: 'The Circle Undone' },
    { value: 'dream_eaters', label: 'The Dream-Eaters' },
    { value: 'innsmouth_conspiracy', label: 'The Innsmouth Conspiracy' },
    { value: 'edge_of_the_earth', label: 'Edge of the Earth' }
  ];

  difficulties = [
    { value: 'easy', label: 'Easy' },
    { value: 'standard', label: 'Standard' },
    { value: 'hard', label: 'Hard' },
    { value: 'expert', label: 'Expert' }
  ];

  phases = [
    { value: 'investigation', label: 'Investigation Phase' },
    { value: 'enemy', label: 'Enemy Phase' },
    { value: 'upkeep', label: 'Upkeep Phase' },
    { value: 'mythos', label: 'Mythos Phase' }
  ];

  constructor(
    private fb: FormBuilder,
    private analysisService: AnalysisService,
    private cardService: CardService,
    private appState: AppStateService
  ) {
    this.analysisForm = this.createForm();
  }

  // Access cached traits for dropdown
  availableTraits = computed(() => this.appState.traits());

  ngOnInit(): void {
    // Load all cards when component initializes
    this.loadCards();
  }

  private loadCards(): void {
    this.cardsLoading.set(true);

    // Build search params from current filter values
    const params: any = {
      page: this.currentPage(),
      limit: this.pageSize()
    };

    // Basic filters
    if (this.searchQuery()) params.q = this.searchQuery();
    if (this.searchFaction()) params.faction = this.searchFaction();
    if (this.searchType()) params.card_type = this.searchType();
    if (this.searchTrait()) params.traits = this.searchTrait();
    if (this.searchMinCost() !== undefined) params.min_cost = this.searchMinCost();
    if (this.searchMaxCost() !== undefined) params.max_cost = this.searchMaxCost();

    // Advanced filters
    if (this.searchText()) params.text = this.searchText();
    if (this.searchFlavor()) params.flavor = this.searchFlavor();
    if (this.searchSlot()) params.slot = this.searchSlot();
    if (this.searchIsUnique() !== undefined) params.is_unique = this.searchIsUnique();
    if (this.searchPermanent() !== undefined) params.permanent = this.searchPermanent();
    if (this.searchMinWillpower() !== undefined) params.min_skill_willpower = this.searchMinWillpower();
    if (this.searchMinIntellect() !== undefined) params.min_skill_intellect = this.searchMinIntellect();
    if (this.searchMinCombat() !== undefined) params.min_skill_combat = this.searchMinCombat();
    if (this.searchMinAgility() !== undefined) params.min_skill_agility = this.searchMinAgility();
    if (this.searchMinHealth() !== undefined) params.min_health = this.searchMinHealth();
    if (this.searchMinSanity() !== undefined) params.min_sanity = this.searchMinSanity();

    this.cardService.searchCards(params).subscribe({
      next: (response) => {
        console.log('API Response received:', response);
        console.log('Cards count:', response.cards?.length);
        console.log('Total results:', response.total_results);
        
        // Convert API response to our Card interface - response.cards contains CardSummary[]
        const cards: Card[] = response.cards.map(apiCard => ({
          code: apiCard.code,
          name: apiCard.name,
          type: apiCard.type_code,
          class: apiCard.faction_code,
          cost: apiCard.cost,
          faction: apiCard.faction_code,
          pack: 'Unknown'  // Not in CardSummary, will need to fetch full details when clicked
        }));

        console.log('Converted cards:', cards);
        console.log('Setting cards signal with', cards.length, 'items');
        this.cards.set(cards);
        this.totalResults.set(response.total_results);
        this.hasNextPage.set(response.pagination.has_next);
        this.hasPrevPage.set(response.pagination.has_prev);
        this.cardsLoading.set(false);
        console.log('Cards signal updated, current value:', this.cards().length);
      },
      error: (err) => {
        console.error('Error loading cards:', err);
        console.error('Error details:', {
          status: err.status,
          statusText: err.statusText,
          message: err.message,
          url: err.url
        });
        this.cardsLoading.set(false);
        // Fallback to mock data if API fails
        this.cards.set(this.getMockCards());
        this.totalResults.set(this.getMockCards().length);
      }
    });
  }

  // Trigger search when user clicks search button
  onSearch(): void {
    this.currentPage.set(1); // Reset to page 1 when searching
    this.loadCards();
  }

  // Clear all search filters
  clearSearch(): void {
    // Basic filters
    this.searchQuery.set('');
    this.searchFaction.set('');
    this.searchType.set('');
    this.searchTrait.set('');
    this.searchMinCost.set(undefined);
    this.searchMaxCost.set(undefined);

    // Advanced filters
    this.searchText.set('');
    this.searchFlavor.set('');
    this.searchSlot.set('');
    this.searchIsUnique.set(undefined);
    this.searchPermanent.set(undefined);
    this.searchMinWillpower.set(undefined);
    this.searchMinIntellect.set(undefined);
    this.searchMinCombat.set(undefined);
    this.searchMinAgility.set(undefined);
    this.searchMinHealth.set(undefined);
    this.searchMinSanity.set(undefined);

    this.currentPage.set(1);
    this.loadCards();
  }

  // Toggle advanced filters visibility
  toggleAdvancedFilters(): void {
    this.showAdvancedFilters.update(show => !show);
  }

  // Pagination methods
  goToNextPage(): void {
    if (this.hasNextPage()) {
      this.currentPage.update(page => page + 1);
      this.loadCards();
    }
  }

  goToPrevPage(): void {
    if (this.hasPrevPage()) {
      this.currentPage.update(page => page - 1);
      this.loadCards();
    }
  }

  goToPage(page: number): void {
    this.currentPage.set(page);
    this.loadCards();
  }

  changePageSize(size: number): void {
    this.pageSize.set(size);
    this.currentPage.set(1); // Reset to page 1 when changing page size
    this.loadCards();
  }

  private convertToCard(apiCard: CardResponse): Card {
    return {
      code: apiCard.code,
      name: apiCard.name || 'Unknown',
      type: apiCard.type_name || apiCard.type_code || 'Unknown',
      class: apiCard.faction_name || apiCard.faction_code || 'Neutral',
      cost: apiCard.cost !== undefined ? apiCard.cost : null,
      faction: apiCard.faction_name || apiCard.faction_code || 'Neutral',
      pack: apiCard.pack_name || apiCard.pack_code || 'Unknown',
      skillWillpower: apiCard.skill_willpower,
      skillIntellect: apiCard.skill_intellect,
      skillCombat: apiCard.skill_combat,
      skillAgility: apiCard.skill_agility,
      skillWild: apiCard.skill_wild,
      text: apiCard.text || apiCard.real_text,
      traits: apiCard.traits,
      slot: apiCard.real_slot,
      health: apiCard.health,
      sanity: apiCard.sanity
    };
  }

  private createForm(): FormGroup {
    return this.fb.group({
      // Card codes input
      cardCodes: [''],
      
      // Investigator context
      investigatorCode: [''],
      
      // Campaign context
      campaignContext: this.fb.group({
        campaign: [''],
        difficulty: ['standard'],
        scenarioCode: [''],
        investigatorCount: [1]
      }),
      
      // Game context
      gameContext: this.fb.group({
        currentScenario: [''],
        currentAct: [1],
        currentAgenda: [1],
        doomOnAgenda: [0],
        doomThreshold: [10],
        scenarioDifficulty: ['standard'],
        currentPhase: ['investigation'],
        turnNumber: [1],
        totalDoomInPlay: [0],
        activeInvestigator: [''],
        analysisQuestion: [''],
        availableActions: [''],
        specialRulesActive: [''],
        
        // Investigators array
        investigators: this.fb.array([this.createInvestigatorForm()]),
        
        // Enemies array
        enemiesInPlay: this.fb.array([]),
        
        // Locations array
        locationsInPlay: this.fb.array([])
      }),
      
      // Flags for which context to include
      includeGameContext: [false],
      includeCampaignContext: [false]
    });
  }

  private createInvestigatorForm(): FormGroup {
    return this.fb.group({
      investigatorCode: [''],
      currentHealth: [0],
      maxHealth: [0],
      currentSanity: [0],
      maxSanity: [0],
      currentResources: [0],
      currentActions: [3],
      isEngaged: [false],
      locationCode: ['']
    });
  }

  private createEnemyForm(): FormGroup {
    return this.fb.group({
      enemyCode: [''],
      currentHealth: [0],
      maxHealth: [0],
      locationCode: [''],
      engagedWith: [''],
      isExhausted: [false]
    });
  }

  private createLocationForm(): FormGroup {
    return this.fb.group({
      locationCode: [''],
      status: ['revealed'],
      currentClues: [0],
      investigatorsHere: [''],
      enemiesHere: ['']
    });
  }

  // Form array getters
  get investigators(): FormArray {
    return this.analysisForm.get('gameContext.investigators') as FormArray;
  }

  get enemiesInPlay(): FormArray {
    return this.analysisForm.get('gameContext.enemiesInPlay') as FormArray;
  }

  get locationsInPlay(): FormArray {
    return this.analysisForm.get('gameContext.locationsInPlay') as FormArray;
  }

  // Add/Remove form array items
  addInvestigator(): void {
    this.investigators.push(this.createInvestigatorForm());
  }

  removeInvestigator(index: number): void {
    this.investigators.removeAt(index);
  }

  addEnemy(): void {
    this.enemiesInPlay.push(this.createEnemyForm());
  }

  removeEnemy(index: number): void {
    this.enemiesInPlay.removeAt(index);
  }

  addLocation(): void {
    this.locationsInPlay.push(this.createLocationForm());
  }

  removeLocation(index: number): void {
    this.locationsInPlay.removeAt(index);
  }

  // Analysis methods
  async analyzeCards(): Promise<void> {
    if (!this.analysisForm.valid) {
      this.error.set('Please fill in required fields');
      return;
    }

    this.loading.set(true);
    this.error.set(null);
    this.results.set(null);

    try {
      const request = this.buildAnalysisRequest();
      let response: AnalysisResponse;

      switch (this.analysisType()) {
        case 'strength':
          response = await this.analysisService.analyzeCardStrength(request).toPromise() as AnalysisResponse;
          break;
        case 'synergies':
          response = await this.analysisService.analyzeCardSynergies(request).toPromise() as AnalysisResponse;
          break;
        case 'timing':
          response = await this.analysisService.analyzeCardTiming(request).toPromise() as AnalysisResponse;
          break;
        default:
          throw new Error('Invalid analysis type');
      }

      this.results.set(response);
    } catch (error: any) {
      this.error.set(error.message || 'Analysis failed');
    } finally {
      this.loading.set(false);
    }
  }

  private buildAnalysisRequest(): CardAnalysisRequest {
    const formValue = this.analysisForm.value;
    
    const request: CardAnalysisRequest = {
      card_codes: formValue.cardCodes.split(',').map((code: string) => code.trim()).filter(Boolean),
      investigator_code: formValue.investigatorCode || undefined
    };

    // Add campaign context if enabled
    if (formValue.includeCampaignContext && formValue.campaignContext.campaign) {
      request.campaign_context = {
        campaign: formValue.campaignContext.campaign,
        difficulty: formValue.campaignContext.difficulty,
        scenario_code: formValue.campaignContext.scenarioCode || undefined,
        investigator_count: formValue.campaignContext.investigatorCount
      };
    }

    // Add game context if enabled
    if (formValue.includeGameContext && formValue.gameContext.currentScenario) {
      const gc = formValue.gameContext;
      request.game_context = {
        current_scenario: gc.currentScenario,
        current_act: gc.currentAct,
        current_agenda: gc.currentAgenda,
        doom_on_agenda: gc.doomOnAgenda,
        doom_threshold: gc.doomThreshold,
        scenario_difficulty: gc.scenarioDifficulty,
        current_phase: gc.currentPhase,
        turn_number: gc.turnNumber,
        total_doom_in_play: gc.totalDoomInPlay,
        active_investigator: gc.activeInvestigator,
        analysis_question: gc.analysisQuestion,
        investigators: gc.investigators.filter((inv: any) => inv.investigatorCode),
        enemies_in_play: gc.enemiesInPlay?.filter((enemy: any) => enemy.enemyCode) || [],
        locations_in_play: gc.locationsInPlay?.map((loc: any) => ({
          ...loc,
          investigators_here: loc.investigatorsHere?.split(',').map((s: string) => s.trim()).filter(Boolean) || [],
          enemies_here: loc.enemiesHere?.split(',').map((s: string) => s.trim()).filter(Boolean) || []
        })).filter((loc: any) => loc.locationCode) || [],
        available_actions: gc.availableActions?.split(',').map((s: string) => s.trim()).filter(Boolean) || [],
        special_rules_active: gc.specialRulesActive?.split(',').map((s: string) => s.trim()).filter(Boolean) || []
      };
    }

    return request;
  }

  setAnalysisType(type: 'strength' | 'synergies' | 'timing'): void {
    this.analysisType.set(type);
    this.results.set(null);
    this.error.set(null);
  }

  clearResults(): void {
    this.results.set(null);
    this.error.set(null);
  }

  // Card Browser Methods
  setActiveTab(tab: 'browser' | 'gpt-analysis'): void {
    this.activeTab.set(tab);
  }

  onCardClick(card: Card): void {
    console.log('Card clicked:', card.code, card.name);

    // Fetch both card details and stats from API
    this.statsLoading.set(true);
    this.showStatsModal.set(true);

    console.log('Modal signals set - showStatsModal:', this.showStatsModal(), 'statsLoading:', this.statsLoading());

    // Fetch card details and stats in parallel
    const cardDetails$ = this.cardService.getCard(card.code);
    const cardStats$ = this.cardService.getCardStats(card.code);

    // Use RxJS forkJoin to wait for both requests
    import('rxjs').then(({ forkJoin }) => {
      forkJoin({
        details: cardDetails$,
        stats: cardStats$
      }).subscribe({
        next: (result) => {
          this.selectedCardDetails.set(result.details);
          this.selectedCardStats.set(result.stats);
          this.statsLoading.set(false);
        },
        error: (err) => {
          console.error('Error fetching card data:', err);
          this.statsLoading.set(false);
          // Fall back to enriched card for display
          const enrichedCard = this.enrichCardWithStats(card);
          this.selectedCard.set(enrichedCard);
        }
      });
    });
  }

  closeStatsModal(): void {
    this.showStatsModal.set(false);
    this.selectedCardStats.set(null);
    this.selectedCardDetails.set(null);
  }

  toggleTopInvestigators(): void {
    this.topInvestigatorsExpanded.update(expanded => !expanded);
  }

  toggleUsageTrend(): void {
    this.usageTrendExpanded.update(expanded => !expanded);
  }

  getTopInvestigators(investigatorUsage: { [key: string]: number }): { code: string; rate: number }[] {
    return Object.entries(investigatorUsage)
      .map(([code, rate]) => ({ code, rate }))
      .filter(inv => inv.rate > 0)
      .sort((a, b) => b.rate - a.rate)
      .slice(0, 10);
  }

  getTrendPeriods(trendData: any): { key: string; value: any }[] {
    return Object.entries(trendData)
      .map(([key, value]) => ({ key, value }))
      .sort((a, b) => a.key.localeCompare(b.key));
  }

  getTrendBarHeight(rate: number, allData: any): number {
    const maxRate = Math.max(...Object.values(allData).map((d: any) => d.usage_rate));
    return maxRate > 0 ? (rate / maxRate) * 100 : 0;
  }

  formatPeriod(period: string): string {
    // Format YYYY-MM to MMM'YY
    const [year, month] = period.split('-');
    const monthNames = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    return `${monthNames[parseInt(month) - 1]}'${year.slice(2)}`;
  }

  getInvestigatorName(code: string): string {
    return this.appState.getInvestigatorName(code);
  }

  formatTraits(traits: any): string {
    if (!traits) return '';
    if (typeof traits === 'string') return traits;
    if (Array.isArray(traits)) {
      return traits.map((t: any) => t.name || t).join('. ') + '.';
    }
    return '';
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

  getCardImageUrl(imagesrc: string | undefined): string {
    if (!imagesrc) return '';
    return `https://arkhamdb.com${imagesrc}`;
  }

  get includeCampaignContext(): boolean {
    return this.analysisForm.get('includeCampaignContext')?.value || false;
  }

  private enrichCardWithStats(card: Card): Card {
    // Generate mock enhanced stats based on card properties
    const isPopular = ['Emergency Cache', 'Machete', 'Magnifying Glass', 'Shrivelling', 'Lucky!', 'Ward of Protection'].includes(card.name);

    return {
      ...card,
      usageRate: isPopular ? Math.floor(Math.random() * 20) + 70 : Math.floor(Math.random() * 40) + 30,
      winRateWithCard: Math.floor(Math.random() * 15) + 60,
      averageTimePlayed: `Turn ${Math.floor(Math.random() * 5) + 2}`,
      deckInclusionRate: isPopular ? Math.floor(Math.random() * 20) + 60 : Math.floor(Math.random() * 30) + 20,
      versatilityScore: Math.floor(Math.random() * 30) + 60,
      economyRating: this.getEconomyRating(card),
      impactRating: this.getImpactRating(card),
      consistencyRating: Math.floor(Math.random() * 20) + 70,
      topInvestigators: this.getTopInvestigatorsForCard(card),
      synergyCards: this.getSynergyCardsFor(card),
      performanceByDifficulty: [
        { difficulty: 'Easy', winRate: Math.floor(Math.random() * 15) + 75 },
        { difficulty: 'Standard', winRate: Math.floor(Math.random() * 15) + 65 },
        { difficulty: 'Hard', winRate: Math.floor(Math.random() * 15) + 55 },
        { difficulty: 'Expert', winRate: Math.floor(Math.random() * 20) + 45 }
      ],
      performanceByCampaign: [
        { campaign: 'Night of the Zealot', winRate: Math.floor(Math.random() * 20) + 60 },
        { campaign: 'The Dunwich Legacy', winRate: Math.floor(Math.random() * 20) + 55 },
        { campaign: 'The Path to Carcosa', winRate: Math.floor(Math.random() * 20) + 50 },
        { campaign: 'The Forgotten Age', winRate: Math.floor(Math.random() * 20) + 45 }
      ]
    };
  }

  private getEconomyRating(card: Card): number {
    // Lower cost = better economy
    if (card.cost === 0) return 95;
    if (card.cost === 1) return 85;
    if (card.cost === 2) return 75;
    if (card.cost === 3) return 65;
    return 50;
  }

  private getImpactRating(card: Card): number {
    // Based on card type and properties
    if (card.type === 'Event') return Math.floor(Math.random() * 20) + 70;
    if (card.type === 'Asset') return Math.floor(Math.random() * 20) + 75;
    return Math.floor(Math.random() * 20) + 60;
  }

  private getTopInvestigatorsForCard(card: Card): { name: string; usageRate: number; winRate: number }[] {
    const investigatorsByClass: Record<string, string[]> = {
      'Guardian': ['Roland Banks', 'Zoey Samaras', 'Mark Harrigan'],
      'Seeker': ['Daisy Walker', 'Rex Murphy', 'Minh Thi Phan'],
      'Rogue': ['Skids O\'Toole', 'Jenny Barnes', 'Finn Edwards'],
      'Mystic': ['Agnes Baker', 'Jim Culver', 'Akachi Onyele'],
      'Survivor': ['Wendy Adams', 'Ashcan Pete', 'Stella Clark'],
      'Neutral': ['Roland Banks', 'Daisy Walker', 'Skids O\'Toole']
    };

    const investigators = investigatorsByClass[card.class] || investigatorsByClass['Neutral'];
    return investigators.slice(0, 3).map(name => ({
      name,
      usageRate: Math.floor(Math.random() * 30) + 50,
      winRate: Math.floor(Math.random() * 20) + 60
    }));
  }

  private getSynergyCardsFor(card: Card): { code: string; name: string; synergyScore: number }[] {
    const synergyMap: Record<string, { code: string; name: string }[]> = {
      'Machete': [
        { code: '01016', name: 'Beat Cop' },
        { code: '01088', name: 'Guard Dog' },
        { code: '01017', name: 'Physical Training' }
      ],
      'Magnifying Glass': [
        { code: '01039', name: 'Working a Hunch' },
        { code: '01024', name: 'Dr. Milan Christopher' },
        { code: '01025', name: 'Hyperawareness' }
      ],
      'Shrivelling': [
        { code: '01053', name: 'Ward of Protection' },
        { code: '01033', name: 'Scrying' },
        { code: '01034', name: 'Arcane Studies' }
      ],
      'Lucky!': [
        { code: '01037', name: 'Rabbit\'s Foot' },
        { code: '01080', name: 'Leather Coat' },
        { code: '01076', name: 'Baseball Bat' }
      ]
    };

    const synergies = synergyMap[card.name] || [
      { code: '01020', name: 'Emergency Cache' },
      { code: '02001', name: 'Flashlight' }
    ];

    return synergies.map(s => ({
      ...s,
      synergyScore: Math.floor(Math.random() * 30) + 65
    }));
  }

  closeCardDetail(): void {
    this.selectedCard.set(null);
  }

  analyzeCardWithGPT(card: Card): void {
    // Populate the form with the card code and switch to GPT analysis tab
    this.analysisForm.patchValue({
      cardCodes: card.code
    });
    this.activeTab.set('gpt-analysis');
  }

  // Table configuration for card browser
  cardColumns: TableColumn[] = [
    { key: 'code', label: 'Code', sortable: true, searchable: true, width: '100px' },
    { key: 'name', label: 'Card Name', sortable: true, searchable: true },
    { key: 'type', label: 'Type', sortable: true, filterable: true, width: '120px' },
    { key: 'class', label: 'Class', sortable: true, filterable: true, width: '120px' },
    { key: 'faction', label: 'Faction', sortable: true, filterable: true, width: '120px' },
    { key: 'cost', label: 'Cost', sortable: true, type: 'number', width: '80px' },
    { key: 'pack', label: 'Pack', sortable: true, filterable: true },
    { key: 'traits', label: 'Traits', sortable: true, searchable: true }
  ];

  cardTableConfig: TableConfig = {
    pageSize: 25,
    pageSizeOptions: [10, 25, 50, 100],
    showPagination: false,  // Disabled - using server-side pagination instead
    showSearch: false,  // Disabled - using custom search filters instead
    showColumnToggle: true,
    showFilters: false,  // Disabled - using custom filters instead
    striped: true,
    hoverable: true,
    bordered: true,
    responsive: true
  };

  getFactionColor(faction: string): string {
    const colors: Record<string, string> = {
      'Guardian': '#2b80c5',
      'Seeker': '#ec8b26',
      'Rogue': '#107116',
      'Mystic': '#4e1a45',
      'Survivor': '#cc3038',
      'Neutral': '#5a5a5a'
    };
    return colors[faction] || '#5a5a5a';
  }

  // Mock card data - Replace with actual API call
  private getMockCards(): Card[] {
    return [
      {
        code: '01006',
        name: '.45 Automatic',
        type: 'Asset',
        class: 'Guardian',
        cost: 4,
        faction: 'Guardian',
        pack: 'Core Set',
        skillCombat: 1,
        skillAgility: 1,
        slot: 'Hand',
        traits: 'Item. Weapon. Firearm.',
        text: 'Uses (4 ammo). Spend 1 ammo: Fight. You get +1 combat and deal +1 damage for this attack.'
      },
      {
        code: '01016',
        name: 'Machete',
        type: 'Asset',
        class: 'Guardian',
        cost: 3,
        faction: 'Guardian',
        pack: 'Core Set',
        skillCombat: 1,
        slot: 'Hand',
        traits: 'Item. Weapon. Melee.',
        text: 'While you are engaged with exactly one enemy, Machete gains: "+1 combat and deals +1 damage."'
      },
      {
        code: '01020',
        name: 'Emergency Cache',
        type: 'Asset',
        class: 'Neutral',
        cost: 0,
        faction: 'Neutral',
        pack: 'Core Set',
        traits: 'Supply.',
        text: 'Gain 3 resources.'
      },
      {
        code: '01022',
        name: 'Magnifying Glass',
        type: 'Asset',
        class: 'Seeker',
        cost: 1,
        faction: 'Seeker',
        pack: 'Core Set',
        skillIntellect: 1,
        slot: 'Hand',
        traits: 'Item. Tool.',
        text: 'Exhaust Magnifying Glass: Investigate. You get +1 intellect for this investigation. If you succeed, discover 1 additional clue at this location.'
      },
      {
        code: '01024',
        name: 'Old Book of Lore',
        type: 'Asset',
        class: 'Seeker',
        cost: 3,
        faction: 'Seeker',
        pack: 'Core Set',
        skillWillpower: 1,
        skillIntellect: 1,
        slot: 'Hand',
        traits: 'Item. Tome.',
        text: 'Exhaust Old Book of Lore: Choose an investigator at your location. That investigator draws 1 card. Then, he or she discards 1 card from his or her hand.'
      },
      {
        code: '01027',
        name: 'Lockpicks',
        type: 'Asset',
        class: 'Rogue',
        cost: 3,
        faction: 'Rogue',
        pack: 'Core Set',
        skillIntellect: 1,
        slot: 'Hand',
        traits: 'Item. Tool. Illicit.',
        text: 'Uses (3 supplies). Exhaust Lockpicks: Investigate. Your location\'s shroud value is reduced by 2 for this investigation. If you succeed, discard 1 supply from Lockpicks. If you fail, discard Lockpicks.'
      },
      {
        code: '01030',
        name: 'Burglary',
        type: 'Event',
        class: 'Rogue',
        cost: 1,
        faction: 'Rogue',
        pack: 'Core Set',
        skillIntellect: 2,
        traits: 'Trick.',
        text: 'Investigate. If you succeed, instead of discovering clues, gain 3 resources.'
      },
      {
        code: '01032',
        name: 'Shrivelling',
        type: 'Asset',
        class: 'Mystic',
        cost: 3,
        faction: 'Mystic',
        pack: 'Core Set',
        skillWillpower: 1,
        skillCombat: 1,
        slot: 'Arcane',
        traits: 'Spell.',
        text: 'Uses (4 charges). Spend 1 charge: Fight. You get +2 combat and deal +1 damage for this attack. If a symbol is revealed during this attack, you take 1 horror.'
      },
      {
        code: '01053',
        name: 'Ward of Protection',
        type: 'Event',
        class: 'Mystic',
        cost: 1,
        faction: 'Mystic',
        pack: 'Core Set',
        skillWillpower: 1,
        skillWild: 1,
        traits: 'Spell. Spirit.',
        text: 'Fast. Play when you draw a non-weakness treachery card. Cancel that card\'s revelation effect. Then, take 1 horror.'
      },
      {
        code: '01074',
        name: 'Lucky!',
        type: 'Event',
        class: 'Survivor',
        cost: 1,
        faction: 'Survivor',
        pack: 'Core Set',
        skillAgility: 2,
        traits: 'Fortune.',
        text: 'Fast. Play after a skill test you are performing fails. You get +2 to your skill value for that test. (If this effect causes the test to succeed, the success resolves after the effects for failing the test.)'
      },
      {
        code: '01076',
        name: 'Baseball Bat',
        type: 'Asset',
        class: 'Survivor',
        cost: 2,
        faction: 'Survivor',
        pack: 'Core Set',
        skillCombat: 1,
        slot: 'Hand x2',
        traits: 'Item. Weapon. Melee.',
        text: 'Fight. You get +2 combat for this attack (if the symbol is revealed during this attack, this attack deals +1 damage).'
      },
      {
        code: '02001',
        name: 'Flashlight',
        type: 'Asset',
        class: 'Neutral',
        cost: 2,
        faction: 'Neutral',
        pack: 'Core Set',
        skillIntellect: 1,
        slot: 'Hand',
        traits: 'Item. Tool.',
        text: 'Uses (3 supplies). Exhaust Flashlight: Investigate. Your location gets -2 shroud for this investigation. If you succeed, discard 1 supply from Flashlight.'
      },
      {
        code: '02010',
        name: 'Working a Hunch',
        type: 'Event',
        class: 'Seeker',
        cost: 2,
        faction: 'Seeker',
        pack: 'Core Set',
        skillIntellect: 2,
        traits: 'Insight.',
        text: 'Discover 2 clues at your location.'
      },
      {
        code: '02016',
        name: 'Evidence!',
        type: 'Event',
        class: 'Guardian',
        cost: 1,
        faction: 'Guardian',
        pack: 'Core Set',
        skillIntellect: 2,
        traits: 'Insight.',
        text: 'After you defeat an enemy: Discover 1 clue at your location. (If it is an Elite enemy, discover 1 additional clue.)'
      },
      {
        code: '02023',
        name: 'Elusive',
        type: 'Event',
        class: 'Rogue',
        cost: 2,
        faction: 'Rogue',
        pack: 'Core Set',
        skillAgility: 2,
        traits: 'Tactic.',
        text: 'Fast. Play only during your turn. Disengage from each enemy engaged with you, move to a revealed location with no enemies, and evade each enemy at that location.'
      }
    ];
  }
}