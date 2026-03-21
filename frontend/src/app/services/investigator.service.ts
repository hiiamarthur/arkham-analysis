import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface InvestigatorMetadata {
  code: string;
  name: string;
  faction_code: string | null;
}

export interface CardRanking {
  card_code: string;
  card_name?: string;
  card_xp?: number | null;
  card_subname?: string | null;
  usage_count: number;
  usage_rate: number;
  average_quantity: number;
  min_quantity: number;
  max_quantity: number;
  consistency_score: number;
}

export interface StapleCard extends CardRanking {
  staple_confidence: number;
}

export interface TrendingCard {
  card_code: string;
  card_name?: string;
  card_xp?: number | null;
  card_subname?: string | null;
  old_usage_rate: number;
  new_usage_rate: number;
  change_rate: number;
  trend_strength: number;
}

export interface CardSynergy {
  card1: string;
  card1_name?: string;
  card2: string;
  card2_name?: string;
  co_occurrence_count: number;
  synergy_strength: number;
  card1_usage_rate: number;
  card2_usage_rate: number;
}

export interface DeckArchetype {
  archetype_signature: string[];
  archetype_signature_names?: string[];
  archetype_signature_xp?: (number | null)[];
  archetype_signature_subnames?: (string | null)[];
  deck_count: number;
  percentage: number;
  archetype_id: string;
}

export interface CardPoolEntry {
  code: string;
  name: string;
  subname?: string | null;
  faction_code: string;
  faction2_code?: string | null;
  faction3_code?: string | null;
  type_code: string;
  xp: number;
  cost?: number | null;
  real_slot?: string | null;
  pack_name?: string | null;
  imagesrc?: string | null;
  deck_limit?: number | null;
  is_unique?: boolean | null;
  permanent?: boolean | null;
  traits: string[];
  text?: string | null;
  flavor?: string | null;
  related_cards?: Array<{ code: string; name: string; pack_name: string }> | null;
}

export interface UnderusedGem {
  card_code: string;
  card_name?: string;
  card_xp?: number | null;
  card_subname?: string | null;
  usage_rate: number;
  consistency_score: number;
  gem_potential: number;
}

export interface OverusedCard {
  card_code: string;
  card_name?: string;
  usage_rate: number;
  consistency_score: number;
  overuse_indicator: number;
}

export interface CardEfficiency {
  card_code: string;
  card_name?: string;
  efficiency_score: number;
  usage_rate: number;
  consistency_score: number;
  average_quantity: number;
}

export interface InvestigatorStatsResponse {
  investigator_info: {
    code: string;
    name: string;
    total_decks: number;
    deck_activity_period?: {
      earliest_deck: string;
      latest_deck: string;
      active_months: number;
    };
  };
  card_rankings: CardRanking[];
  staple_cards: StapleCard[];
  rising_cards: TrendingCard[];
  falling_cards: TrendingCard[];
  deck_composition: {
    average_deck_size: number;
    deck_size_range: [number, number];
    most_common_size: number;
    deck_size_consistency: number;
  };
  card_synergies: CardSynergy[];
  deck_archetypes: DeckArchetype[];
  optimization_score: number;
  underused_gems: UnderusedGem[];
  overused_cards: OverusedCard[];
  meta_position: {
    total_decks: number;
    meta_share: number;
    total_decks_analyzed: number;
    activity_level: string;
    deck_innovation_score: number;
  };
  popularity_trends: {
    insufficient_data?: boolean;
    quarterly_deck_counts?: number[];
    trend_direction?: string;
    peak_period?: number;
  };
  deck_diversity: {
    diversity_score: number;
    unique_deck_ratio: number;
    card_variety_score: number;
    total_unique_cards: number;
  };
  card_efficiency_ratings: CardEfficiency[];
  build_recommendations: {
    must_include: string[];
    must_include_names?: string[];
    must_include_xp?: (number | null)[];
    must_include_subnames?: (string | null)[];
    must_include_replacements?: { [slotCode: string]: string[] };
    must_include_replacements_names?: { [slotCode: string]: string[] };
    must_include_replacements_xp?: { [slotCode: string]: (number | null)[] };
    must_include_replacements_subnames?: { [slotCode: string]: (string | null)[] };
    core_recommendations: string[];
    core_recommendations_names?: string[];
    core_recommendations_xp?: (number | null)[];
    core_recommendations_subnames?: (string | null)[];
    hidden_gems: string[];
    hidden_gems_names?: string[];
    hidden_gems_xp?: (number | null)[];
    hidden_gems_subnames?: (string | null)[];
    trending_picks: string[];
    trending_picks_names?: string[];
    trending_picks_xp?: (number | null)[];
    trending_picks_subnames?: (string | null)[];
    build_advice: string[];
    meta_considerations: {
      optimization_priority: string;
      innovation_opportunity: string;
    };
  };
}

@Injectable({
  providedIn: 'root'
})
export class InvestigatorService {
  private apiUrl = `${environment.apiUrl}/cards`;

  constructor(private http: HttpClient) {}

  /**
   * Get all investigators with their codes and names
   */
  getAllInvestigators(): Observable<InvestigatorMetadata[]> {
    return this.http.get<InvestigatorMetadata[]>(`${this.apiUrl}/metadata/investigators`);
  }

  /**
   * Get detailed stats for a specific investigator
   */
  getInvestigatorStats(investigatorCode: string): Observable<InvestigatorStatsResponse> {
    return this.http.get<InvestigatorStatsResponse>(`${this.apiUrl}/investigator/${investigatorCode}/stats`);
  }

  /**
   * Get the full legal card pool for an investigator (based on deck_options)
   */
  getInvestigatorCardPool(investigatorCode: string): Observable<{
    investigator_code: string;
    investigator_name: string;
    deck_restrictions: Array<{ traits: string[]; level?: { min: number; max: number } }>;
    total: number;
    cards: CardPoolEntry[];
  }> {
    return this.http.get<any>(`${this.apiUrl}/investigator/${investigatorCode}/card-pool`);
  }

  /**
   * Get top cards for an investigator with server-side XP filter and limit
   */
  getInvestigatorTopCards(
    investigatorCode: string,
    params: { min_xp?: number | null; max_xp?: number | null; q?: string; limit?: number }
  ): Observable<{ investigator_code: string; cards: CardRanking[]; total: number; filters: any }> {
    const query: Record<string, string> = { limit: String(params.limit ?? 20) };
    if (params.min_xp != null) query['min_xp'] = String(params.min_xp);
    if (params.max_xp != null) query['max_xp'] = String(params.max_xp);
    if (params.q) query['q'] = params.q;
    return this.http.get<any>(`${this.apiUrl}/investigator/${investigatorCode}/top-cards`, { params: query });
  }
}
