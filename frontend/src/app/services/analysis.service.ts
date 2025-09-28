import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface CardAnalysisRequest {
  card_codes: string[];
  game_context?: GameContext;
  investigator_code?: string;
  campaign_context?: CampaignContext;
}

export interface GameContext {
  current_scenario: string;
  current_act?: number;
  current_agenda?: number;
  doom_on_agenda: number;
  doom_threshold: number;
  scenario_difficulty?: string;
  current_phase?: string;
  turn_number?: number;
  total_doom_in_play?: number;
  investigators: InvestigatorCondition[];
  enemies_in_play?: EnemyInPlay[];
  locations_in_play?: LocationInPlay[];
  active_investigator: string;
  analysis_question: string;
  available_actions?: string[];
  special_rules_active?: string[];
}

export interface InvestigatorCondition {
  investigator_code: string;
  current_health: number;
  max_health: number;
  current_sanity: number;
  max_sanity: number;
  current_resources: number;
  current_actions?: number;
  doom_on_investigator?: number;
  horror_this_round?: number;
  damage_this_round?: number;
  is_engaged?: boolean;
  location_code?: string;
}

export interface EnemyInPlay {
  enemy_code: string;
  current_health: number;
  max_health: number;
  doom_on_enemy?: number;
  location_code?: string;
  engaged_with?: string;
  is_exhausted?: boolean;
}

export interface LocationInPlay {
  location_code: string;
  status: 'revealed' | 'unrevealed' | 'resigned';
  current_clues: number;
  investigators_here: string[];
  enemies_here: string[];
}

export interface CampaignContext {
  campaign: string;
  difficulty: 'easy' | 'standard' | 'hard' | 'expert';
  scenario_code?: string;
  investigator_count?: number;
}

export interface CardInfo {
  code: string;
  name: string;
  type?: string;
  faction?: string;
}

export interface CardAnalysisResult {
  card_info?: CardInfo;
  strength_analysis?: string;
  timing_analysis?: string;
  synergy_analysis?: string;
  error?: string;
}

export interface AnalysisResponse {
  success: boolean;
  message: string;
  analysis?: {
    analysis_type: string;
    context_applied?: {
      has_game_context: boolean;
      has_investigator_context: boolean;
      has_campaign_context: boolean;
    };
    // For strength analysis
    card_analyses?: { [card_code: string]: CardAnalysisResult };
    // For synergy analysis
    cards_analyzed?: string[];
    synergy_analysis?: string;
    // For timing analysis
    timing_analyses?: { [card_code: string]: CardAnalysisResult };
  };
}

export interface ThreatAssessment {
  success: boolean;
  threat_assessment: {
    overall_threat_level: number;
    threat_factors: {
      doom_pressure: number;
      enemy_pressure: number;
      health_pressure: number;
      sanity_pressure: number;
      resource_pressure: number;
    };
    threat_description: string;
  };
  scenario_info: {
    scenario: string;
    act: number;
    agenda: number;
    doom_pressure: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class AnalysisService {
  private apiUrl = environment.apiUrl || 'http://localhost:8000/api/v1';

  constructor(private http: HttpClient) {}

  analyzeCardStrength(request: CardAnalysisRequest): Observable<AnalysisResponse> {
    return this.http.post<AnalysisResponse>(`${this.apiUrl}/analysis/card-strength`, request);
  }

  analyzeCardSynergies(request: CardAnalysisRequest): Observable<AnalysisResponse> {
    return this.http.post<AnalysisResponse>(`${this.apiUrl}/analysis/card-synergies`, request);
  }

  analyzeCardTiming(request: CardAnalysisRequest): Observable<AnalysisResponse> {
    return this.http.post<AnalysisResponse>(`${this.apiUrl}/analysis/card-timing`, request);
  }

  getThreatAssessment(
    scenario: string,
    act: number,
    agenda: number,
    doomOnAgenda: number,
    doomThreshold: number
  ): Observable<ThreatAssessment> {
    const params = {
      scenario,
      act: act.toString(),
      agenda: agenda.toString(),
      doom_on_agenda: doomOnAgenda.toString(),
      doom_threshold: doomThreshold.toString()
    };
    
    return this.http.get<ThreatAssessment>(`${this.apiUrl}/analysis/threat-assessment`, { params });
  }
}