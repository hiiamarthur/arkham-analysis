import { Component, signal, computed, inject, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup } from '@angular/forms';
import { ActivatedRoute } from '@angular/router';
import { AnalysisService, ThreatAssessment } from '../../services/analysis.service';
import { ScenarioService, Scenario, ScenarioContext, Campaign, InvestigatorAnalysis, InvestigatorAnalysisResponse } from '../../services/scenario.service';
import { InvestigatorService, InvestigatorMetadata } from '../../services/investigator.service';
import { ReplacePipe } from '../../pipes/replace.pipe';
import { IconService } from '../../shared/services/icon.service';
import { SafeHtml } from '@angular/platform-browser';
import { SearchableSelectComponent, SelectOption } from '../../shared/components/searchable-select.component';

@Component({
  selector: 'app-threat-assessment',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule, ReplacePipe, SearchableSelectComponent],
  templateUrl: './threat-assessment.component.html',
  styleUrl: './threat-assessment.component.css'
})
export class ThreatAssessmentComponent implements OnInit {
  threatForm: FormGroup;

  // Signals
  loading = signal(false);
  assessment = signal<ThreatAssessment | null>(null);
  error = signal<string | null>(null);
  scenarios = signal<Scenario[]>([]);
  campaigns = signal<Campaign[]>([]);
  selectedScenarioContext = signal<ScenarioContext | null>(null);
  loadingScenarios = signal(false);
  selectedCampaign = signal<string>('');

  // Investigator selection
  availableInvestigators = signal<InvestigatorMetadata[]>([]);
  selectedInvestigatorCodes = signal<string[]>([]);
  investigatorAnalysis = signal<InvestigatorAnalysisResponse | null>(null);
  analysisLoading = signal(false);
  playerCountSignal = signal<number>(2);  // mirrors the playerCount form field

  // Computed values
  canAddInvestigator = computed(() =>
    this.selectedInvestigatorCodes().length < this.playerCountSignal()
  );
  hasAssessment = computed(() => this.assessment() !== null);
  hasError = computed(() => this.error() !== null);
  hasScenarioContext = computed(() => this.selectedScenarioContext() !== null);
  threatLevel = computed(() => {
    let level = 0;

    // Use assessment if available, otherwise use context-based calculation
    const assessmentLevel = this.assessment()?.threat_assessment?.overall_threat_level;
    if (assessmentLevel !== undefined) {
      level = assessmentLevel;
    } else {
      level = this.contextBasedThreat() || 0;
    }

    if (level < 0.2) return { level: 'Low', color: '#28a745', percentage: level * 100 };
    if (level < 0.4) return { level: 'Moderate', color: '#ffc107', percentage: level * 100 };
    if (level < 0.6) return { level: 'High', color: '#fd7e14', percentage: level * 100 };
    if (level < 0.8) return { level: 'Critical', color: '#dc3545', percentage: level * 100 };
    return { level: 'Extreme', color: '#6f42c1', percentage: level * 100 };
  });

  private iconService = inject(IconService);

  constructor(
    private fb: FormBuilder,
    private analysisService: AnalysisService,
    private scenarioService: ScenarioService,
    private investigatorService: InvestigatorService,
    private route: ActivatedRoute
  ) {
    this.threatForm = this.fb.group({
      campaign: [''],
      scenario: ['the_gathering'],
      difficulty: ['standard'],
      playerCount: [2],
      act: [1],
      agenda: [1],
      doomOnAgenda: [0],
      doomThreshold: [5]
    });
  }

  ngOnInit(): void {
    this.loadScenarios();
    this.loadCampaigns();
    this.loadInvestigators();

    // Check for scenario query param (e.g. from dashboard quick links)
    const queryScenario = this.route.snapshot.queryParamMap.get('scenario');
    const defaultScenario = queryScenario || this.threatForm.get('scenario')?.value;
    if (queryScenario) {
      this.threatForm.patchValue({ scenario: queryScenario });
    }
    if (defaultScenario) this.loadScenarioContext(defaultScenario);

    // Watch for scenario changes to back-fill campaign
    this.threatForm.get('scenario')?.valueChanges.subscribe((scenarioCode: string) => {
      if (!scenarioCode) return;
      const scenario = this.scenarios().find(s => s.code === scenarioCode);
      if (scenario && this.threatForm.get('campaign')?.value !== scenario.campaign) {
        this.threatForm.patchValue({ campaign: scenario.campaign }, { emitEvent: false });
        this.selectedCampaign.set(scenario.campaign);
      }
    });

    // Watch for campaign changes to filter scenarios
    this.threatForm.get('campaign')?.valueChanges.subscribe(campaign => {
      this.selectedCampaign.set(campaign);
    });

    // Keep playerCountSignal in sync; trim party if player count drops
    this.threatForm.get('playerCount')?.valueChanges.subscribe((count: number) => {
      this.playerCountSignal.set(count);
      const current = this.selectedInvestigatorCodes();
      if (current.length > count) {
        this.selectedInvestigatorCodes.set(current.slice(0, count));
        this.investigatorAnalysis.set(null);
      }
    });
  }

  async loadScenarios(): Promise<void> {
    this.loadingScenarios.set(true);
    try {
      const scenarios = await this.scenarioService.getScenarios().toPromise();
      if (scenarios) {
        this.scenarios.set(scenarios);
        // Back-fill campaign for the currently selected scenario (handles query-param case)
        const currentScenarioCode = this.threatForm.get('scenario')?.value;
        if (currentScenarioCode && !this.threatForm.get('campaign')?.value) {
          const match = scenarios.find(s => s.code === currentScenarioCode);
          if (match) {
            this.threatForm.patchValue({ campaign: match.campaign }, { emitEvent: false });
            this.selectedCampaign.set(match.campaign);
          }
        }
      }
    } catch (error) {
      console.error('Failed to load scenarios:', error);
    } finally {
      this.loadingScenarios.set(false);
    }
  }

  async loadCampaigns(): Promise<void> {
    try {
      const campaigns = await this.scenarioService.getCampaigns().toPromise();
      if (campaigns) {
        this.campaigns.set(campaigns);
      }
    } catch (error) {
      console.error('Failed to load campaigns:', error);
    }
  }

  async loadScenarioContext(scenarioCode: string, manageLoading = true): Promise<void> {
    if (manageLoading) this.loading.set(true);
    try {
      const difficulty = this.threatForm.get('difficulty')?.value || 'standard';
      const playerCount = this.threatForm.get('playerCount')?.value || 2;
      const context = await this.scenarioService.getScenarioContext(scenarioCode, difficulty, playerCount).toPromise();
      if (context) {
        this.selectedScenarioContext.set(context);

        // Auto-update form with scenario context values
        this.threatForm.patchValue({
          doomThreshold: context.doom_threshold,
          playerCount: context.player_count
        });
        this.playerCountSignal.set(context.player_count);
      }
    } catch (error) {
      console.error('Failed to load scenario context:', error);
      this.error.set('Failed to load scenario data');
    } finally {
      if (manageLoading) this.loading.set(false);
    }
  }

  async loadInvestigators(): Promise<void> {
    try {
      const investigators = await this.investigatorService.getAllInvestigators().toPromise();
      if (investigators) this.availableInvestigators.set(investigators);
    } catch (error) {
      console.error('Failed to load investigators:', error);
    }
  }

  addInvestigator(code: string): void {
    if (!code) return;
    const current = this.selectedInvestigatorCodes();
    if (current.length < this.playerCountSignal() && !current.includes(code)) {
      this.selectedInvestigatorCodes.set([...current, code]);
    }
  }

  removeInvestigator(code: string): void {
    this.selectedInvestigatorCodes.update(codes => codes.filter(c => c !== code));
    // Clear analysis if party changes
    this.investigatorAnalysis.set(null);
  }

  getInvestigatorName(code: string): string {
    return this.availableInvestigators().find(i => i.code === code)?.name ?? code;
  }

  async analyzeInvestigators(): Promise<void> {
    const codes = this.selectedInvestigatorCodes();
    const scenarioCode = this.threatForm.get('scenario')?.value;
    if (!codes.length || !scenarioCode) return;

    this.analysisLoading.set(true);
    try {
      const result = await this.scenarioService.analyzeInvestigatorsVsScenario(
        scenarioCode,
        this.threatForm.get('difficulty')?.value || 'standard',
        this.threatForm.get('playerCount')?.value || 2,
        codes
      ).toPromise();
      if (result) this.investigatorAnalysis.set(result);
    } catch (error) {
      console.error('Investigator analysis failed:', error);
    } finally {
      this.analysisLoading.set(false);
    }
  }

  getStatSuccessRateColor(rate: number): string {
    if (rate >= 0.75) return '#28a745';
    if (rate >= 0.55) return '#ffc107';
    if (rate >= 0.35) return '#fd7e14';
    return '#dc3545';
  }

  getFactionColor(faction: string): string {
    const colors: Record<string, string> = {
      guardian: '#2b80c5', seeker: '#ec8b26', rogue: '#107116',
      mystic: '#4e1a45', survivor: '#cc3038', neutral: '#5a5a5a'
    };
    return colors[faction?.toLowerCase()] ?? '#5a5a5a';
  }

  getStatRates(inv: InvestigatorAnalysis, stat: 'willpower' | 'intellect' | 'combat' | 'agility'): number[] {
    const rates = inv.success_rates[stat];
    return [rates.vs_1, rates.vs_2, rates.vs_3, rates.vs_4, rates.vs_5];
  }

  // Computed signals for filtered scenarios
  filteredScenarios = computed(() => {
    const campaign = this.selectedCampaign();
    const allScenarios = this.scenarios();

    if (!campaign) return allScenarios;
    return allScenarios.filter(s => s.campaign === campaign);
  });

  // SelectOption arrays for searchable selects
  campaignOptions = computed<SelectOption[]>(() =>
    this.campaigns().map(c => ({ value: c.code, label: c.name }))
  );

  scenarioOptions = computed<SelectOption[]>(() =>
    this.filteredScenarios().map(s => ({ value: s.code, label: s.name }))
  );

  difficultyOptions: SelectOption[] = [
    { value: 'easy', label: 'Easy' },
    { value: 'standard', label: 'Standard' },
    { value: 'hard', label: 'Hard' },
    { value: 'expert', label: 'Expert' },
  ];

  investigatorOptions = computed<SelectOption[]>(() =>
    this.availableInvestigators().map(inv => ({
      value: inv.code,
      label: inv.name,
      disabled: this.selectedInvestigatorCodes().includes(inv.code),
    }))
  );

  // Group encounter cards by type with quantities
  groupedEncounterCards = computed(() => {
    const context = this.selectedScenarioContext();
    if (!context?.encounter_cards || context.encounter_cards.length === 0) {
      return null;
    }

    const groups = new Map<string, any[]>();

    // Group cards by type
    context.encounter_cards.forEach(card => {
      const type = card.card_type || 'unknown';
      if (!groups.has(type)) {
        groups.set(type, []);
      }
      groups.get(type)!.push(card);
    });

    // Convert to array and calculate totals
    const typeOrder = ['enemy', 'treachery', 'location', 'act', 'agenda', 'scenario'];
    return Array.from(groups.entries())
      .map(([type, cards]) => ({
        type,
        cards: cards.sort((a, b) => a.name.localeCompare(b.name)),
        totalQuantity: cards.reduce((sum, card) => sum + (card.quantity || 1), 0)
      }))
      .sort((a, b) => {
        const indexA = typeOrder.indexOf(a.type);
        const indexB = typeOrder.indexOf(b.type);
        if (indexA === -1 && indexB === -1) return a.type.localeCompare(b.type);
        if (indexA === -1) return 1;
        if (indexB === -1) return -1;
        return indexA - indexB;
      });
  });

  // Computed signal for threat calculation based on context
  contextBasedThreat = computed(() => {
    const context = this.selectedScenarioContext();
    const form = this.threatForm;
    if (!context || !form) return null;

    const doomOnAgenda = form.get('doomOnAgenda')?.value || 0;
    const doomThreshold = form.get('doomThreshold')?.value || 1;
    const act = form.get('act')?.value || 1;
    const agenda = form.get('agenda')?.value || 1;

    // Doom pressure factor (0-1)
    const doomProgress = Math.min(doomOnAgenda / doomThreshold, 1);

    // Encounter difficulty from context (already 0-1)
    const encounterDifficulty = context.encounter_difficulty || 0;

    // Time pressure from context (already 0-1)
    const timePressure = context.time_pressure || 0;

    // Chaos hostility from context (already 0-1)
    const chaosHostility = context.scenario_context?.chaos_bag_stats?.chaos_hostility || 0;

    // Act/Agenda progression penalty (later acts/agendas = higher threat)
    const progressionFactor = Math.min((act + agenda - 2) * 0.1, 0.3);

    // Enemy density factor
    const enemyDensity = (context.scenario_context?.encounter_wide_stats?.encounter_card_density?.enemy_percentage || 0) / 100;

    // Calculate overall threat based on weighted factors
    const threatLevel = (doomProgress * 0.35) +           // Doom is most critical
                       (encounterDifficulty * 0.2) +     // Base scenario difficulty
                       (timePressure * 0.15) +           // Time pressure
                       (chaosHostility * 0.15) +         // Chaos bag hostility
                       (progressionFactor * 0.1) +       // Game progression
                       (enemyDensity * 0.05);            // Enemy density

    return Math.min(Math.max(threatLevel, 0), 1);
  });

  // Computed threat factors for display
  threatFactors = computed(() => {
    const context = this.selectedScenarioContext();
    const form = this.threatForm;
    if (!context || !form) return null;

    const doomOnAgenda = form.get('doomOnAgenda')?.value || 0;
    const doomThreshold = form.get('doomThreshold')?.value || 1;
    const act = form.get('act')?.value || 1;
    const agenda = form.get('agenda')?.value || 1;

    // Map our calculated factors to the expected interface
    const enemyDensity = (context.scenario_context?.encounter_wide_stats?.encounter_card_density?.enemy_percentage || 0) / 100;
    const avgEnemyDamage = (context.scenario_context?.enemy_stats?.average_enemy_damage || 0) / 5; // Normalized to 0-1
    const avgEnemyHorror = (context.scenario_context?.enemy_stats?.average_enemy_horror || 0) / 5; // Normalized to 0-1

    return {
      doom_pressure: Math.min(doomOnAgenda / doomThreshold, 1),
      enemy_pressure: enemyDensity,
      health_pressure: avgEnemyDamage,
      sanity_pressure: avgEnemyHorror,
      resource_pressure: context.time_pressure || 0
    };
  });

  async assessThreat(): Promise<void> {
    if (!this.threatForm.valid) {
      this.error.set('Please fill in all required fields');
      return;
    }

    this.loading.set(true);
    this.error.set(null);
    this.assessment.set(null);

    try {
      const formValue = this.threatForm.value;

      // Load (or refresh) scenario context for the current scenario + difficulty
      await this.loadScenarioContext(formValue.scenario, false);

      // If we have scenario context, create a mock assessment using our calculations
      const context = this.selectedScenarioContext();
      if (context) {
        const threatLevel = this.contextBasedThreat();
        const factors = this.threatFactors();

        // Only create assessment if we have valid factors
        if (factors) {
          const mockAssessment: ThreatAssessment = {
            success: true,
            threat_assessment: {
              overall_threat_level: threatLevel || 0,
              threat_description: this.getThreatDescription(threatLevel || 0),
              threat_factors: factors
            },
            scenario_info: {
              scenario: formValue.scenario,
              act: formValue.act,
              agenda: formValue.agenda,
              doom_pressure: `${formValue.doomOnAgenda}/${formValue.doomThreshold}`
            }
          };

          this.assessment.set(mockAssessment);
        }
      } else {
        // Fallback to original API call
        const response = await this.analysisService.getThreatAssessment(
          formValue.scenario,
          formValue.act,
          formValue.agenda,
          formValue.doomOnAgenda,
          formValue.doomThreshold
        ).toPromise();

        if (response) {
          this.assessment.set(response);
        }
      }
    } catch (error: any) {
      this.error.set(error.message || 'Threat assessment failed');
    } finally {
      this.loading.set(false);
    }
  }

  clearAssessment(): void {
    this.assessment.set(null);
    this.error.set(null);
  }

  // Quick scenario selection
  onScenarioSelect(scenario: Scenario): void {
    this.threatForm.patchValue({
      scenario: scenario.code
    });
  }

  // Remove preset scenarios as we now use real data

  getFactorClass(value: number): string {
    if (value < 0.2) return 'factor-low';
    if (value < 0.4) return 'factor-moderate';
    if (value < 0.6) return 'factor-high';
    if (value < 0.8) return 'factor-critical';
    return 'factor-extreme';
  }

  getRecommendationIcon(): SafeHtml {
    const level = this.threatLevel().level;
    switch (level) {
      case 'Low': return this.iconService.getIcon('check');
      case 'Moderate': return this.iconService.getIcon('threat');
      case 'High': return this.iconService.getIcon('fire');
      case 'Critical': return this.iconService.getIcon('alert');
      case 'Extreme': return this.iconService.getIcon('skull');
      default: return this.iconService.getIcon('question');
    }
  }

  // Get icon from IconService
  getIcon(iconName: string): SafeHtml {
    return this.iconService.getIcon(iconName);
  }

  // Calculate real-time threat based on current form values
  calculateRealTimeThreat(): void {
    const context = this.selectedScenarioContext();
    if (context) {
      // Trigger recalculation by updating the form
      this.threatForm.updateValueAndValidity();
    }
  }

  getRecommendationTitle(): string {
    const level = this.threatLevel().level;
    switch (level) {
      case 'Low': return 'Stable Situation';
      case 'Moderate': return 'Moderate Pressure';
      case 'High': return 'Dangerous Situation';
      case 'Critical': return 'Critical Emergency';
      case 'Extreme': return 'Extreme Emergency';
      default: return 'Unknown';
    }
  }

  getThreatDescription(level: number): string {
    if (level < 0.2) return 'Situation is manageable with standard play patterns';
    if (level < 0.4) return 'Moderate pressure building, stay alert';
    if (level < 0.6) return 'High threat environment requiring defensive play';
    if (level < 0.8) return 'Critical situation demanding immediate action';
    return 'Extreme danger - survival is the only priority';
  }

  // Encounter deck spoiler gate
  showEncounterCards = signal<boolean>(false);

  toggleEncounterCards(): void {
    this.showEncounterCards.update(v => !v);
  }

  isHiddenFactor(key: string): boolean {
    return ['health_pressure', 'sanity_pressure', 'resource_pressure'].includes(key);
  }

  // Pre-compute token distribution display data to avoid multiple function calls in template
  tokenCompositionDisplay = computed(() => {
    const dist = this.selectedScenarioContext()?.scenario_context?.chaos_bag_stats?.token_distribution;
    if (!dist) return [];
    return Object.entries(dist).map(([key, count]) => {
      const iconName = this.getTokenIconName(key);
      const numericDisplay = iconName ? null : this.getNumericTokenDisplay(key);
      const numericClass = numericDisplay ? this.getNumericTokenClass(numericDisplay) : '';
      return { key, count, iconName, numericDisplay, numericClass };
    });
  });

  // Flatten scenario_token_modifications into a typed array for the template
  scenarioTokenEffects = computed(() => {
    const mods = this.selectedScenarioContext()?.scenario_token_modifications;
    if (!mods) return [];
    return Object.entries(mods).map(([key, value]) => ({ key, value }));
  });

  // Maps class-derived token keys to their numeric display value (+1, 0, -1, etc.)
  getNumericTokenDisplay(key: string): string | null {
    const map: Record<string, string> = {
      plusone: '+1', zero: '0',
      minusone: '-1', minustwo: '-2', minusthree: '-3',
      minusfour: '-4', minusfive: '-5', minussix: '-6',
      minuseight: '-8',
    };
    return map[key.toLowerCase()] ?? null;
  }

  getNumericTokenClass(num: string): string {
    if (num === '+1') return 'numeric-token numeric-token--positive';
    if (num === '0') return 'numeric-token numeric-token--neutral';
    return 'numeric-token numeric-token--negative';
  }

  getTokenIconName(tokenType: string): string | null {
    // Normalize class-derived names (e.g. autofail, eldersign, elderthing)
    // to the underscore-keyed icon names used in arkham-icon-data.ts
    const aliasMap: Record<string, string> = {
      autofail: 'auto_fail',
      eldersign: 'elder_sign',
      elderthing: 'elder_thing',
    };
    const key = tokenType.toLowerCase().replace(/\s+/g, '_');
    const resolved = aliasMap[key] ?? key;
    const specialTokens = ['skull', 'cultist', 'tablet', 'elder_thing', 'auto_fail', 'bless', 'curse', 'frost', 'elder_sign'];
    return specialTokens.includes(resolved) ? resolved : null;
  }

  getRecommendationText(): string {
    const level = this.threatLevel().level;
    const context = this.selectedScenarioContext();

    let baseText = '';
    switch (level) {
      case 'Low':
        baseText = 'The situation is under control. Focus on efficient clue gathering and deck setup. Consider taking some risks for optimal plays.';
        break;
      case 'Moderate':
        baseText = 'Some pressure is building. Balance efficiency with safety. Prepare defensive options and consider faster clue gathering.';
        break;
      case 'High':
        baseText = 'Dangerous situation requires immediate attention. Prioritize survival and threat mitigation. Fast actions and defensive cards are valuable.';
        break;
      case 'Critical':
        baseText = 'Critical emergency! Focus entirely on survival and threat elimination. Play conservatively and use emergency resources.';
        break;
      case 'Extreme':
        baseText = 'Extreme emergency! All-out survival mode. Use any available resources to prevent defeat. Consider desperate measures.';
        break;
      default:
        baseText = 'Unable to determine threat level recommendations.';
    }

    // Add context-specific recommendations
    if (context) {
      const enemyCount = context.scenario_context?.enemy_stats?.enemy_count || 0;
      const avgFight = context.scenario_context?.enemy_stats?.average_enemy_fight || 0;
      const treacheryCount = context.scenario_context?.treachery_stats?.treachery_count || 0;
      const willpowerTests = context.scenario_context?.treachery_stats?.no_of_willpower_test || 0;

      if (enemyCount > 8) {
        baseText += ' High enemy density - prioritize combat solutions or evasion.';
      }
      if (avgFight > 3) {
        baseText += ' Strong enemies present - boost combat stats or use weapons.';
      }
      if (willpowerTests > 5) {
        baseText += ' Heavy willpower testing - protect sanity and boost willpower.';
      }
      if (treacheryCount > 15) {
        baseText += ' Treachery-heavy encounter deck - prepare defensive assets.';
      }
    }

    return baseText;
  }
}