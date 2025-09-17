from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

from ..investigators.investigators import Investigator, ArchetypeType
from ..Scenario.scenario import Scenario
from ..card.card_type import CardType
from ..difficulty import Difficulty


class MetaTier(Enum):
    S_TIER = 1
    A_TIER = 2
    B_TIER = 3
    C_TIER = 4
    D_TIER = 5


@dataclass
class CardMetaData:
    """Meta data for individual cards"""

    card_code: str
    popularity_score: float  # 0-1 how often played
    win_rate: float  # 0-1 win rate when included
    tier_rating: MetaTier
    synergy_partners: List[str]  # card codes that synergize well
    counter_cards: List[str]  # cards that counter this
    meta_shift_trend: float  # -1 to 1, trending up/down
    last_updated: datetime


@dataclass
class ScenarioMetaData:
    """Meta data for scenarios"""

    scenario_code: str
    difficulty_rating: float  # 0-1 overall difficulty
    popularity_score: float  # 0-1 how often played
    win_rate: float  # 0-1 overall win rate
    preferred_archetypes: List[ArchetypeType]
    counter_strategies: List[str]
    meta_shift_trend: float
    last_updated: datetime


class AnalysisContext:
    """Context class for advanced card strength analysis"""

    def __init__(
        self,
        current_meta: str = "standard",
        difficulty: Difficulty = Difficulty.STANDARD,
        player_count: int = 3,
    ):
        self.current_meta = current_meta
        self.difficulty = difficulty
        self.player_count = player_count
        self.analysis_timestamp = datetime.now()

        # Meta data caches
        self._card_meta_cache: Dict[str, CardMetaData] = {}
        self._scenario_meta_cache: Dict[str, ScenarioMetaData] = {}
        self._tier_lists: Dict[str, List[str]] = {}
        self._synergy_networks: Dict[str, List[str]] = {}

    # =============================================================================
    # CARD VALUE ANALYSIS (Uses DB data + calculations)
    # =============================================================================

    def calculate_card_value_in_context(
        self,
        card_code: str,
        investigator: Investigator,
        scenario: Optional[Scenario] = None,
    ) -> Dict[str, Any]:
        """Calculate contextual card value - DB data + calculation"""
        base_value = self._get_base_card_value(card_code)
        investigator_bonus = self._calculate_investigator_synergy(
            card_code, investigator
        )
        scenario_bonus = (
            self._calculate_scenario_bonus(card_code, scenario) if scenario else 0.0
        )
        meta_bonus = self._calculate_meta_bonus(card_code)

        total_value = base_value + investigator_bonus + scenario_bonus + meta_bonus

        return {
            "base_value": base_value,
            "investigator_synergy": investigator_bonus,
            "scenario_bonus": scenario_bonus,
            "meta_bonus": meta_bonus,
            "total_value": total_value,
            "value_breakdown": {
                "base": base_value / total_value if total_value > 0 else 0,
                "investigator": (
                    investigator_bonus / total_value if total_value > 0 else 0
                ),
                "scenario": scenario_bonus / total_value if total_value > 0 else 0,
                "meta": meta_bonus / total_value if total_value > 0 else 0,
            },
        }

    def _get_base_card_value(self, card_code: str) -> float:
        """Get base card value from DB data - DB data only"""
        # This would query your card database for base stats
        # For now, return a placeholder
        return 5.0  # Placeholder

    def _calculate_investigator_synergy(
        self, card_code: str, investigator: Investigator
    ) -> float:
        """Calculate investigator synergy bonus - DB data + calculation"""
        # Check if card synergizes with investigator's archetype
        archetype = investigator.get_primary_archetype()
        synergy_bonus = 0.0

        # This would check card traits against investigator preferences
        # Placeholder logic
        if archetype == ArchetypeType.COMBAT:
            synergy_bonus += 1.0  # Combat cards get bonus
        elif archetype == ArchetypeType.INVESTIGATION:
            synergy_bonus += 1.0  # Investigation cards get bonus

        return synergy_bonus

    def _calculate_scenario_bonus(self, card_code: str, scenario: Scenario) -> float:
        """Calculate scenario-specific bonus - DB data + calculation"""
        context = scenario.get_scenario_context()
        bonus = 0.0

        # Time pressure bonus
        if context.get("time_pressure", 0.5) > 0.7:
            # Fast cards get bonus
            bonus += 0.5

        # Investigation bonus
        if context.get("investigation_heavy", 0.5) > 0.7:
            # Investigation cards get bonus
            bonus += 0.5

        return bonus

    def _calculate_meta_bonus(self, card_code: str) -> float:
        """Calculate meta bonus - DB data + calculation"""
        meta_data = self._card_meta_cache.get(card_code)
        if not meta_data:
            return 0.0

        # Tier bonus
        tier_bonus = (6 - meta_data.tier_rating.value) * 0.5

        # Popularity bonus
        popularity_bonus = meta_data.popularity_score * 0.3

        # Win rate bonus
        win_rate_bonus = meta_data.win_rate * 0.4

        return tier_bonus + popularity_bonus + win_rate_bonus

    # =============================================================================
    # META ANALYSIS (Uses DB data + calculations)
    # =============================================================================

    def predict_meta_shift(self, timeframe_days: int = 30) -> Dict[str, Any]:
        """Predict meta shifts - DB data + calculation"""
        # Analyze trends in card popularity and win rates
        trending_up = []
        trending_down = []

        for card_code, meta_data in self._card_meta_cache.items():
            if meta_data.meta_shift_trend > 0.3:
                trending_up.append(card_code)
            elif meta_data.meta_shift_trend < -0.3:
                trending_down.append(card_code)

        return {
            "trending_up": trending_up,
            "trending_down": trending_down,
            "predicted_tier_shifts": self._predict_tier_shifts(timeframe_days),
            "confidence": self._calculate_prediction_confidence(),
        }

    def _predict_tier_shifts(self, timeframe_days: int) -> Dict[str, str]:
        """Predict tier shifts - calculation only"""
        predictions = {}

        for card_code, meta_data in self._card_meta_cache.items():
            if meta_data.meta_shift_trend > 0.5:
                predictions[card_code] = "likely_up"
            elif meta_data.meta_shift_trend < -0.5:
                predictions[card_code] = "likely_down"
            else:
                predictions[card_code] = "stable"

        return predictions

    def _calculate_prediction_confidence(self) -> float:
        """Calculate prediction confidence - calculation only"""
        # Simple confidence based on data recency and trend strength
        recent_data = sum(
            1
            for meta in self._card_meta_cache.values()
            if (datetime.now() - meta.last_updated).days < 7
        )
        total_data = len(self._card_meta_cache)

        if total_data == 0:
            return 0.0

        recency_factor = recent_data / total_data
        trend_strength = (
            sum(abs(meta.meta_shift_trend) for meta in self._card_meta_cache.values())
            / total_data
        )

        return (recency_factor + trend_strength) / 2

    def analyze_win_conditions(
        self, investigator: Investigator, scenario: Scenario
    ) -> List[Dict[str, Any]]:
        """Analyze win conditions - DB data + calculation"""
        win_conditions = []

        # Primary win condition based on scenario
        if scenario.is_investigation_heavy():
            win_conditions.append(
                {
                    "type": "investigation",
                    "priority": "high",
                    "description": "Gather clues efficiently",
                    "required_cards": self._get_investigation_cards(investigator),
                }
            )

        if scenario.is_combat_heavy():
            win_conditions.append(
                {
                    "type": "combat",
                    "priority": "high",
                    "description": "Defeat enemies efficiently",
                    "required_cards": self._get_combat_cards(investigator),
                }
            )

        # Secondary win conditions
        win_conditions.append(
            {
                "type": "survival",
                "priority": "medium",
                "description": "Survive until scenario completion",
                "required_cards": self._get_survival_cards(investigator),
            }
        )

        return win_conditions

    def _get_investigation_cards(self, investigator: Investigator) -> List[str]:
        """Get investigation cards for investigator - DB data + calculation"""
        # This would query the database for investigation cards
        # that the investigator can use
        return ["magnifying_glass", "deduction", "working_a_hunch"]

    def _get_combat_cards(self, investigator: Investigator) -> List[str]:
        """Get combat cards for investigator - DB data + calculation"""
        return ["machete", "vicious_blow", "overpower"]

    def _get_survival_cards(self, investigator: Investigator) -> List[str]:
        """Get survival cards for investigator - DB data + calculation"""
        return ["ward_of_protection", "dodge", "elusive"]

    # =============================================================================
    # DECK OPTIMIZATION (Uses DB data + calculations)
    # =============================================================================

    def evaluate_tech_choices(
        self, investigator: Investigator, scenario: Scenario
    ) -> List[Dict[str, Any]]:
        """Evaluate tech choices - DB data + calculation"""
        tech_choices = []

        # Analyze current meta for tech choices
        meta_analysis = self.predict_meta_shift()

        for card_code in meta_analysis["trending_up"]:
            tech_choices.append(
                {
                    "card_code": card_code,
                    "reason": "Meta trending up",
                    "priority": "high",
                    "synergy_score": self._calculate_tech_synergy(
                        card_code, investigator
                    ),
                }
            )

        return tech_choices

    def _calculate_tech_synergy(
        self, card_code: str, investigator: Investigator
    ) -> float:
        """Calculate tech card synergy - DB data + calculation"""
        # This would analyze how well the tech card fits the investigator
        return 0.7  # Placeholder

    def calculate_deck_power_level(
        self, investigator: Investigator
    ) -> Dict[str, float]:
        """Calculate overall deck power level - DB data + calculation"""
        deck_analysis = investigator.analyze_deck_composition()
        meta_performance = investigator.calculate_meta_performance()

        # Combine various factors
        power_level = (
            meta_performance["overall_meta_score"] * 0.4
            + deck_analysis["consistency_score"] * 0.3
            + investigator.calculate_deck_optimization_score(investigator.deck) * 0.3
        )

        return {
            "overall_power": power_level,
            "meta_score": meta_performance["overall_meta_score"],
            "consistency": deck_analysis["consistency_score"],
            "optimization": investigator.calculate_deck_optimization_score(
                investigator.deck
            ),
            "tier_equivalent": self._power_to_tier(power_level),
        }

    def _power_to_tier(self, power_level: float) -> str:
        """Convert power level to tier - calculation only"""
        if power_level >= 0.8:
            return "S"
        elif power_level >= 0.6:
            return "A"
        elif power_level >= 0.4:
            return "B"
        elif power_level >= 0.2:
            return "C"
        else:
            return "D"

    # =============================================================================
    # SYNERGY ANALYSIS (Uses DB data + calculations)
    # =============================================================================

    def analyze_card_synergies(
        self, card_codes: List[str]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """Analyze card synergies - DB data + calculation"""
        synergies = {}

        for i, card1 in enumerate(card_codes):
            card_synergies = []
            for j, card2 in enumerate(card_codes[i + 1 :], i + 1):
                synergy_score = self._calculate_card_synergy(card1, card2)
                if synergy_score > 0.5:  # Threshold for meaningful synergy
                    card_synergies.append(
                        {
                            "partner_card": card2,
                            "synergy_score": synergy_score,
                            "synergy_type": self._get_synergy_type(card1, card2),
                        }
                    )

            synergies[card1] = card_synergies

        return synergies

    def _calculate_card_synergy(self, card1: str, card2: str) -> float:
        """Calculate synergy between two cards - DB data + calculation"""
        # This would analyze card interactions, shared traits, etc.
        # Placeholder logic
        return 0.6  # Placeholder

    def _get_synergy_type(self, card1: str, card2: str) -> str:
        """Get synergy type - DB data + calculation"""
        # This would analyze the type of synergy
        return "combo"  # Placeholder

    # =============================================================================
    # UTILITY METHODS
    # =============================================================================

    def update_meta_data(self, card_code: str, meta_data: CardMetaData):
        """Update card meta data - DB data only"""
        self._card_meta_cache[card_code] = meta_data

    def get_tier_list(
        self, card_type: Optional[CardType] = None
    ) -> List[Dict[str, Any]]:
        """Get tier list - DB data + calculation"""
        if card_type:
            # Filter by card type
            filtered_cards = {
                k: v
                for k, v in self._card_meta_cache.items()
                if self._get_card_type(k) == card_type
            }
        else:
            filtered_cards = self._card_meta_cache

        # Sort by tier and win rate
        sorted_cards = sorted(
            filtered_cards.items(),
            key=lambda x: (x[1].tier_rating.value, -x[1].win_rate),
        )

        return [
            {
                "card_code": card_code,
                "tier": meta_data.tier_rating.name,
                "win_rate": meta_data.win_rate,
                "popularity": meta_data.popularity_score,
                "trend": meta_data.meta_shift_trend,
            }
            for card_code, meta_data in sorted_cards
        ]

    def _get_card_type(self, card_code: str) -> CardType:
        """Get card type from code - DB data only"""
        # This would query the database
        return CardType.ASSET  # Placeholder

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "current_meta": self.current_meta,
            "difficulty": self.difficulty.value,
            "player_count": self.player_count,
            "analysis_timestamp": self.analysis_timestamp.isoformat(),
            "meta_analysis": self.predict_meta_shift(),
            "tier_lists": {
                "overall": self.get_tier_list(),
                "assets": self.get_tier_list(CardType.ASSET),
                "events": self.get_tier_list(CardType.EVENT),
                "skills": self.get_tier_list(CardType.SKILL),
            },
        }
