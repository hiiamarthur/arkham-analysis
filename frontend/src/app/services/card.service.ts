import { Injectable } from '@angular/core';
import { HttpClient, HttpParams } from '@angular/common/http';
import { Observable } from 'rxjs';
import { environment } from '../../environments/environment';

export interface CardResponse {
  code: string;
  name: string;
  real_name?: string;
  subname?: string;
  subtype?: string;
  cost?: number;
  text?: string;
  real_text?: string;
  type_code?: string;
  type_name?: string;
  faction_code?: string;
  faction_name?: string;
  pack_code?: string;
  pack_name?: string;
  position?: number;
  quantity?: number;
  is_unique?: boolean;
  exceptional?: boolean;
  permanent?: boolean;
  double_sided?: boolean;
  url?: string;
  imagesrc?: string;
  flavor?: string;
  deck_limit?: number;
  health?: number;
  sanity?: number;
  skill_willpower?: number;
  skill_intellect?: number;
  skill_combat?: number;
  skill_agility?: number;
  skill_wild?: number;
  real_slot?: string;
  illustrator?: string;
  xp?: number;
  traits?: Array<{ name: string }> | string;
  // Investigator stats (only for investigator cards)
  average_deck_size?: number;
  deck_size_min?: number;
  deck_size_max?: number;
  meta_share?: number;
  total_decks?: number;  // Total decks for this investigator
  total_decks_analyzed?: number;  // Total decks in meta
  bonded_cards?: Array<{ code: string; name: string; count: number }>;
  related_card?: string;
}

export interface CardSearchParams {
  // Text search
  q?: string;
  text?: string;
  flavor?: string;

  // Card attributes
  faction?: string;
  card_type?: string;
  subtype?: string;
  traits?: string;
  slot?: string;
  pack_code?: string;
  illustrator?: string;

  // Boolean filters
  is_unique?: boolean;
  permanent?: boolean;
  exceptional?: boolean;

  // Numeric filters
  min_xp?: number;
  max_xp?: number;
  min_cost?: number;
  max_cost?: number;
  min_skill_willpower?: number;
  max_skill_willpower?: number;
  min_skill_intellect?: number;
  max_skill_intellect?: number;
  min_skill_combat?: number;
  max_skill_combat?: number;
  min_skill_agility?: number;
  max_skill_agility?: number;
  min_health?: number;
  max_health?: number;
  min_sanity?: number;
  max_sanity?: number;

  // Pagination
  page?: number;
  limit?: number;
}

export interface CardSummary {
  code: string;
  name: string;
  subname?: string | null;
  faction_code: string;
  type_code: string;
  xp: number | null;
  cost: number | null;
  pack_code: string;
  traits: string[];
  illustrator: string;
}

export interface PaginatedCardResponse {
  cards: CardSummary[];
  pagination: {
    page: number;
    limit: number;
    has_next: boolean;
    has_prev: boolean;
  };
  filters: {
    q?: string;
    faction?: string;
    card_type?: string;
    min_xp?: number;
    max_xp?: number;
    min_cost?: number;
    max_cost?: number;
    pack_code?: string;
    traits?: string;
  };
  total_results: number;
}

export interface InvestigatorUsageData {
  rate: number;
  decks_with_card: number;
  total_decks: number;
}

export interface CardDeckStats {
  popularity: {
    overall_usage_rate: number;
    investigator_usage_rate: { [key: string]: number | InvestigatorUsageData };
    investigator_spread: number;
  };
  trend: {
    trend_data: {
      [key: string]: {
        usage_rate: number;
        total_decks: number;
        decks_with_card: number;
      };
    };
    trend_direction: string;
    change_rate: number;
    periods_analyzed: number;
  };
}

export interface RelatedCardStats {
  code: string;
  name: string;
  pack_name: string;
  pack_code: string;
  imagesrc?: string;
  deck_stats: CardDeckStats | null;
}

export interface CardStatsResponse {
  card_info: {
    code: string;
    name: string;
    type: string;
  };
  /** Stats for this specific card code only */
  deck_stats: CardDeckStats;
  /** Stats combining this card + all reprints (use this as the headline) */
  combined_deck_stats?: CardDeckStats;
  /** Each reprint's independent stats */
  related_cards?: RelatedCardStats[];
  data_source: {
    decks_analyzed: number;
    days_covered: number;
    trend_period: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class CardService {
  private apiUrl = `${environment.apiUrl}/cards`;

  constructor(private http: HttpClient) {}

  /**
   * Search for cards with comprehensive filters and pagination.
   * Returns paginated response from server.
   */
  searchCards(params: CardSearchParams = {}): Observable<PaginatedCardResponse> {
    let httpParams = new HttpParams();

    // Text search parameters
    if (params.q) httpParams = httpParams.set('q', params.q);
    if (params.text) httpParams = httpParams.set('text', params.text);
    if (params.flavor) httpParams = httpParams.set('flavor', params.flavor);

    // Card attribute parameters
    if (params.faction) httpParams = httpParams.set('faction', params.faction);
    if (params.card_type) httpParams = httpParams.set('card_type', params.card_type);
    if (params.subtype) httpParams = httpParams.set('subtype', params.subtype);
    if (params.traits) httpParams = httpParams.set('traits', params.traits);
    if (params.slot) httpParams = httpParams.set('slot', params.slot);
    if (params.pack_code) httpParams = httpParams.set('pack_code', params.pack_code);
    if (params.illustrator) httpParams = httpParams.set('illustrator', params.illustrator);

    // Boolean parameters
    if (params.is_unique !== undefined) httpParams = httpParams.set('is_unique', params.is_unique.toString());
    if (params.permanent !== undefined) httpParams = httpParams.set('permanent', params.permanent.toString());
    if (params.exceptional !== undefined) httpParams = httpParams.set('exceptional', params.exceptional.toString());

    // Numeric range parameters - XP and Cost
    if (params.min_xp !== undefined) httpParams = httpParams.set('min_xp', params.min_xp.toString());
    if (params.max_xp !== undefined) httpParams = httpParams.set('max_xp', params.max_xp.toString());
    if (params.min_cost !== undefined) httpParams = httpParams.set('min_cost', params.min_cost.toString());
    if (params.max_cost !== undefined) httpParams = httpParams.set('max_cost', params.max_cost.toString());

    // Skill icon parameters
    if (params.min_skill_willpower !== undefined) httpParams = httpParams.set('min_skill_willpower', params.min_skill_willpower.toString());
    if (params.max_skill_willpower !== undefined) httpParams = httpParams.set('max_skill_willpower', params.max_skill_willpower.toString());
    if (params.min_skill_intellect !== undefined) httpParams = httpParams.set('min_skill_intellect', params.min_skill_intellect.toString());
    if (params.max_skill_intellect !== undefined) httpParams = httpParams.set('max_skill_intellect', params.max_skill_intellect.toString());
    if (params.min_skill_combat !== undefined) httpParams = httpParams.set('min_skill_combat', params.min_skill_combat.toString());
    if (params.max_skill_combat !== undefined) httpParams = httpParams.set('max_skill_combat', params.max_skill_combat.toString());
    if (params.min_skill_agility !== undefined) httpParams = httpParams.set('min_skill_agility', params.min_skill_agility.toString());
    if (params.max_skill_agility !== undefined) httpParams = httpParams.set('max_skill_agility', params.max_skill_agility.toString());

    // Health and Sanity parameters
    if (params.min_health !== undefined) httpParams = httpParams.set('min_health', params.min_health.toString());
    if (params.max_health !== undefined) httpParams = httpParams.set('max_health', params.max_health.toString());
    if (params.min_sanity !== undefined) httpParams = httpParams.set('min_sanity', params.min_sanity.toString());
    if (params.max_sanity !== undefined) httpParams = httpParams.set('max_sanity', params.max_sanity.toString());

    // Pagination parameters
    if (params.page !== undefined) httpParams = httpParams.set('page', params.page.toString());
    if (params.limit !== undefined) httpParams = httpParams.set('limit', params.limit.toString());

    return this.http.get<PaginatedCardResponse>(`${this.apiUrl}/search`, { params: httpParams });
  }

  /**
   * Get a single card by code
   */
  getCard(cardCode: string): Observable<CardResponse> {
    return this.http.get<CardResponse>(`${this.apiUrl}/${cardCode}`);
  }

  /**
   * Get a specific card by code and return full details
   */
  getCardByCode(cardCode: string): Observable<CardResponse> {
    return this.http.get<CardResponse>(`${this.apiUrl}/${cardCode}`);
  }

  /**
   * Get card statistics including popularity, investigator usage, and trends
   */
  getCardStats(cardCode: string): Observable<CardStatsResponse> {
    return this.http.get<CardStatsResponse>(`${this.apiUrl}/${cardCode}/stats`);
  }
}
