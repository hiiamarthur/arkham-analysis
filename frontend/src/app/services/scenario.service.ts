import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Scenario {
  code: string;
  name: string;
  campaign: string;
  campaign_name: string;
}

export interface EncounterCard {
  code: string;
  name: string;
  traits?: string[];
  faction: string;
  text?: string;
  card_type: string;
  quantity: number;
  back_text?: string;
  taboo?: any;
  encounter_code: string;
  victory?: number;
  damage?: number;
  horror?: number;
  fight?: number;
  evade?: number;
  health?: number;
  health_per_investigator?: boolean;
  clues?: number;
  clues_fixed?: boolean;
  shroud?: number;
  is_per_investigator?: boolean;
  imagesrc?: string;
}

export interface ScenarioContext {
  scenario_type: string;
  difficulty: string;
  campaign_type: string;
  player_count: number;
  doom_threshold: number;
  starting_clues: number;
  agenda_advancement_rate: number;
  scenario_context: {
    time_pressure: number;
    encounter_wide_stats: {
      total_encounter_cards: number;
      victory_points_available: number;
      cards_with_victory: number;
      average_victory_per_card: number;
      max_victory_single_card: number;
      doom_cards: number;
      total_doom_on_cards: number;
      cards_by_type: Record<string, number>;
      overall_trait_distribution: Record<string, number>;
      encounter_card_density: {
        enemy_percentage: number;
        treachery_percentage: number;
        location_percentage: number;
      };
    };
    enemy_stats: {
      trait_count: Record<string, number>;
      enemy_count: number;
      max_enemy_health: number;
      max_enemy_fight: number;
      max_enemy_evade: number;
      max_enemy_horror: number;
      max_enemy_damage: number;
      min_enemy_health: number;
      min_enemy_fight: number;
      min_enemy_evade: number;
      min_enemy_horror: number;
      min_enemy_damage: number;
      average_enemy_health: number;
      average_enemy_fight: number;
      average_enemy_evade: number;
      average_enemy_horror: number;
      average_enemy_damage: number;
      enemies_with_dynamic_fight: number;
      enemies_with_dynamic_evade: number;
      enemies_without_fight: number;
      enemies_without_evade: number;
      enemies_without_health: number;
    };
    treachery_stats: {
      trait_count: Record<string, number>;
      treachery_count: number;
      no_of_combat_test: number;
      no_of_intellect_test: number;
      no_of_willpower_test: number;
      no_of_agility_test: number;
      average_combat_test_value: number;
      average_intellect_test_value: number;
      average_willpower_test_value: number;
      average_agility_test_value: number;
      no_of_card_with_surge: number;
      no_of_card_with_peril: number;
      no_of_card_with_attach: number;
    };
    location_stats: {
      trait_count: Record<string, number>;
      no_of_location: number;
      average_clue_per_location: number;
      average_shroud_per_location: number;
      highest_clue: number;
      lowest_clue: number;
      highest_shroud: number;
      lowest_shroud: number;
      total_clues_available: number;
      locations_with_clues: number;
      locations_without_clues: number;
    };
    chaos_bag_stats: {
      total_tokens: number;
      calculable_tokens: number;
      excluded_tokens: {
        elder_sign_count: number;
        auto_fail_count: number;
        note: string;
      };
      token_distribution: Record<string, number>;
      numeric_summary: {
        average_modifier: number;
        positive_tokens: number;
        zero_tokens: number;
        negative_tokens: number;
        most_common_value: number;
        worst_token: number;
        best_token: number;
        calculation_note: string;
      };
      special_tokens: Record<string, number>;
      success_probabilities: Record<string, any>;
      modifier_suggestions: Record<string, any>;
      special_token_effects: Array<{
        token_type: string;
        effect: string;
        value: any;
        count: number;
      }>;
      chaos_hostility: number;
    };
    encounter_difficulty: number;
    doom_threshold: number;
    starting_clues: number;
    agenda_rate: number;
    player_count: number;
  };
  chaos_bag_stats: {
    expected_value: number;
    hostility_rating: number;
    composition: Record<string, number>;
    simulation_ready: boolean;
  };
  special_mechanics: Record<string, boolean>;
  configuration: any;
  rule_calculated_values: any;
  is_time_pressured: boolean;
  is_investigation_heavy: boolean;
  is_combat_heavy: boolean;
  difficulty_multiplier: number;
  encounter_difficulty: number;
  time_pressure: number;
  resource_scarcity: number;
  encounter_cards: EncounterCard[];
  scenario_token_modifications: Record<string, { effect: string; value: any }>;
}

export interface ChaosTokens {
  scenario: {
    code: string;
    name: string;
    campaign: string;
  };
  difficulty: string;
  token_modifications: Record<string, {
    effect: string;
    value: any;
  }>;
  has_modifications: boolean;
}

export interface Campaign {
  code: string;
  name: string;
  scenario_count: number;
  scenarios?: number; // legacy alias
}

export interface InvestigatorSuccessRates {
  vs_1: number;
  vs_2: number;
  vs_3: number;
  vs_4: number;
  vs_5: number;
}

export interface InvestigatorAnalysis {
  rank: number;
  investigator_code: string;
  investigator_name: string;
  faction: string;
  hp: number;
  sanity: number;
  stats: {
    willpower: number;
    intellect: number;
    combat: number;
    agility: number;
  };
  success_rates: {
    willpower: InvestigatorSuccessRates;
    intellect: InvestigatorSuccessRates;
    combat: InvestigatorSuccessRates;
    agility: InvestigatorSuccessRates;
  };
  overall_score: number;
  scenario_fit: {
    investigation_rating: number;
    combat_rating: number;
    evasion_rating: number;
    willpower_rating: number;
  };
}

export interface InvestigatorAnalysisResponse {
  scenario_code: string;
  difficulty: string;
  chaos_bag_summary: {
    expected_value: number;
    hostility_rating: number;
    composition: Record<string, number>;
    simulation_ready: boolean;
  };
  investigator_analyses: InvestigatorAnalysis[];
}

export interface DashboardInvestigator {
  code: string;
  name: string;
  faction: string;
  deck_count: number;
  meta_share: number;
}

export interface DashboardCard {
  code: string;
  name: string;
  type_code: string;
  faction_code: string;
  xp: number;
  deck_count: number;
  inclusion_rate: number;
}

export interface DashboardVersatileCard extends DashboardCard {
  factions: string[];
  faction_count: number;
}

export interface DashboardTrendingInvestigator {
  code: string;
  name: string;
  faction: string;
  recent_decks: number;
  prior_decks: number;
  change_pct: number;
}

export interface DashboardStats {
  meta: { decks_analyzed: number; days: number; generated_at: string; };
  top_investigators: DashboardInvestigator[];
  most_popular_cards: DashboardCard[];
  card_stats: {
    top_assets: DashboardCard[];
    top_events: DashboardCard[];
    top_skills: DashboardCard[];
    top_level_0: DashboardCard[];
    top_upgraded: DashboardCard[];
    most_versatile: DashboardVersatileCard[];
    avg_xp_per_deck: number;
    xp_distribution: Record<string, number>;
  };
  faction_meta_share: Record<string, number>;
  trending: {
    rising: DashboardTrendingInvestigator[];
    falling: DashboardTrendingInvestigator[];
  };
  highlight: {
    most_played_investigator?: DashboardInvestigator;
    dominant_faction?: { faction: string; share: number; };
    runner_up?: DashboardInvestigator;
    total_decks_analyzed?: number;
    avg_xp_per_deck?: number;
  };
}

@Injectable({
  providedIn: 'root'
})
export class ScenarioService {
  private apiUrl = 'http://localhost:8000/v1/scenarios';
  private dashboardUrl = 'http://localhost:8000/v1/dashboard';

  constructor(private http: HttpClient) {}

  getScenarios(): Observable<Scenario[]> {
    return this.http.get<Scenario[]>(this.apiUrl);
  }

  getCampaigns(): Observable<Campaign[]> {
    return this.http.get<Campaign[]>(`${this.apiUrl}/campaigns`);
  }

  getScenarioContext(scenarioCode: string, difficulty = 'standard', playerCount = 2): Observable<ScenarioContext> {
    return this.http.get<ScenarioContext>(`${this.apiUrl}/${scenarioCode}/context?difficulty=${difficulty}&no_of_investigators=${playerCount}`);
  }

  getChaosTokens(scenarioCode: string, difficulty: string = 'standard'): Observable<ChaosTokens> {
    return this.http.get<ChaosTokens>(`${this.apiUrl}/${scenarioCode}/chaos-tokens?difficulty=${difficulty}`);
  }

  getScenarioCards(scenarioCode: string): Observable<any[]> {
    return this.http.get<any[]>(`${this.apiUrl}/${scenarioCode}/cards`);
  }

  getDifficultyComparison(scenarioCode: string): Observable<any> {
    return this.http.get<any>(`${this.apiUrl}/${scenarioCode}/difficulty-comparison`);
  }

  analyzeScenario(scenarioCode: string, params: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/${scenarioCode}/analyze`, params);
  }

  simulateChaosBag(scenarioCode: string, params: any): Observable<any> {
    return this.http.post<any>(`${this.apiUrl}/${scenarioCode}/simulate-chaos-bag`, params);
  }

  getDashboardStats(days = 90): Observable<DashboardStats> {
    return this.http.get<DashboardStats>(`${this.dashboardUrl}?days=${days}`);
  }

  analyzeInvestigatorsVsScenario(
    scenarioCode: string,
    difficulty: string,
    playerCount: number,
    investigatorCodes: string[]
  ): Observable<InvestigatorAnalysisResponse> {
    return this.http.post<InvestigatorAnalysisResponse>(
      `${this.apiUrl}/${scenarioCode}/investigator-analysis`,
      {
        difficulty,
        no_of_investigators: playerCount,
        investigator_codes: investigatorCodes,
      }
    );
  }
}