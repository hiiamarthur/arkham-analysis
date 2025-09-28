import { Component, signal, computed } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule, ReactiveFormsModule, FormBuilder, FormGroup, FormArray } from '@angular/forms';
import { AnalysisService, CardAnalysisRequest, AnalysisResponse } from '../../services/analysis.service';

@Component({
  selector: 'app-card-analysis',
  standalone: true,
  imports: [CommonModule, FormsModule, ReactiveFormsModule],
  templateUrl: './card-analysis.component.html',
  styleUrl: './card-analysis.component.css'
})
export class CardAnalysisComponent {
  analysisForm: FormGroup;
  
  // Signals for reactive state management
  loading = signal(false);
  results = signal<AnalysisResponse | null>(null);
  error = signal<string | null>(null);
  analysisType = signal<'strength' | 'synergies' | 'timing'>('strength');

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
    private analysisService: AnalysisService
  ) {
    this.analysisForm = this.createForm();
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
}