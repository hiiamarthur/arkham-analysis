from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum

from ..card import PlayerCard
from ..card.faction import Faction
from ..card.card_type import CardType
from ..difficulty import Difficulty
from ..scenario import Scenario


class ArchetypeType(Enum):
    COMBAT = "combat"
    INVESTIGATION = "investigation"
    SUPPORT = "support"
    SURVIVAL = "survival"
    ECONOMY = "economy"
    BALANCED = "balanced"
    COMBO = "combo"
    CONTROL = "control"


# @dataclass
# class InvestigatorStats:
#     """Core investigator statistics"""

#     health: int
#     sanity: int
#     willpower: int
#     intellect: int
#     combat: int
#     agility: int
#     deck_size: int
#     unique_ability: str
#     elder_sign_ability: str


@dataclass
class MetaContext:
    """Current meta context for analysis"""

    current_tier: int  # 1-5 tier ranking
    popularity_score: float  # 0-1 how often played
    win_rate: float  # 0-1 overall win rate
    meta_shift_trend: float  # -1 to 1, trending up/down
    counter_strategies: List[str]
    popular_combos: List[List[str]]  # card codes


class Investigator:
    """Advanced investigator class for card strength analysis"""

    def __init__(
        self,
        code: str,
        name: str,
        faction: Faction,
        stats: InvestigatorStats,
        deck: List[PlayerCard],
        meta_context: Optional[MetaContext] = None,
    ):
        self.code = code
        self.name = name
        self.faction = faction
        self.stats = stats
        self.deck = deck
        self.meta_context = meta_context or MetaContext(
            current_tier=3,
            popularity_score=0.5,
            win_rate=0.5,
            meta_shift_trend=0.0,
            counter_strategies=[],
            popular_combos=[],
        )

        # Calculated properties
        self._stat_distribution = None
        self._archetype_scores = None
        self._deck_analysis = None

    # =============================================================================
    # STAT ANALYSIS (Uses DB data + calculations)
    # =============================================================================

    @property
    def stat_distribution(self) -> Dict[str, float]:
        """Normalized stat spread for comparison - DB data + calculation"""
        if self._stat_distribution is None:
            total_stats = sum(
                [
                    self.stats.willpower,
                    self.stats.intellect,
                    self.stats.combat,
                    self.stats.agility,
                ]
            )
            self._stat_distribution = {
                "willpower": self.stats.willpower / total_stats,
                "intellect": self.stats.intellect / total_stats,
                "combat": self.stats.combat / total_stats,
                "agility": self.stats.agility / total_stats,
                "total": total_stats,
            }
        return self._stat_distribution

    def calculate_stat_efficiency(self) -> Dict[str, float]:
        """Cost-to-stat ratios - DB data + calculation"""
        return {
            "willpower_efficiency": self.stats.willpower / self.stats.deck_size,
            "intellect_efficiency": self.stats.intellect / self.stats.deck_size,
            "combat_efficiency": self.stats.combat / self.stats.deck_size,
            "agility_efficiency": self.stats.agility / self.stats.deck_size,
        }

    def analyze_stat_breakpoints(self) -> Dict[str, List[int]]:
        """Critical stat thresholds - DB data + calculation"""
        return {
            "willpower_breakpoints": [3, 4, 5],  # Common test difficulties
            "intellect_breakpoints": [3, 4, 5],
            "combat_breakpoints": [3, 4, 5],
            "agility_breakpoints": [3, 4, 5],
            "current_breakpoints": {
                "willpower": self._get_breakpoint_level(self.stats.willpower),
                "intellect": self._get_breakpoint_level(self.stats.intellect),
                "combat": self._get_breakpoint_level(self.stats.combat),
                "agility": self._get_breakpoint_level(self.stats.agility),
            },
        }

    def _get_breakpoint_level(self, stat: int) -> int:
        """Determine which breakpoint level the stat reaches"""
        if stat >= 5:
            return 3
        elif stat >= 4:
            return 2
        elif stat >= 3:
            return 1
        else:
            return 0

    # =============================================================================
    # DECK ANALYSIS (Uses DB data + calculations)
    # =============================================================================

    def analyze_deck_composition(self) -> Dict[str, Any]:
        """Deck composition analysis - DB data + calculation"""
        if self._deck_analysis is None:
            card_types = {}
            factions = {}
            costs = []
            xp_costs = []

            for card in self.deck:
                # Count by type
                card_type = card.card_type.value
                card_types[card_type] = card_types.get(card_type, 0) + 1

                # Count by faction
                faction = card.faction.value
                factions[faction] = factions.get(faction, 0) + 1

                # Collect costs
                if hasattr(card, "cost") and card.cost is not None:
                    costs.append(card.cost)
                if hasattr(card, "xp") and card.xp is not None:
                    xp_costs.append(card.xp)

            self._deck_analysis = {
                "card_type_distribution": card_types,
                "faction_distribution": factions,
                "average_cost": sum(costs) / len(costs) if costs else 0,
                "total_xp": sum(xp_costs),
                "deck_size": len(self.deck),
                "consistency_score": self._calculate_consistency_score(card_types),
            }
        return self._deck_analysis

    def _calculate_consistency_score(self, card_types: Dict[str, int]) -> float:
        """Calculate deck consistency - calculation only"""
        if not card_types:
            return 0.0

        # Higher consistency = more focused deck
        total_cards = sum(card_types.values())
        max_type_count = max(card_types.values())
        return max_type_count / total_cards

    def calculate_action_economy(self) -> Dict[str, float]:
        """Action efficiency metrics - DB data + calculation"""
        action_cards = [card for card in self.deck if hasattr(card, "actions")]
        free_actions = [
            card for card in action_cards if getattr(card, "actions", 0) == 0
        ]

        return {
            "total_action_cards": len(action_cards),
            "free_action_ratio": (
                len(free_actions) / len(action_cards) if action_cards else 0
            ),
            "action_efficiency": len(free_actions) / len(self.deck) if self.deck else 0,
        }

    # =============================================================================
    # ARCHETYPE ANALYSIS (Uses DB data + calculations)
    # =============================================================================

    @property
    def archetype_scores(self) -> Dict[ArchetypeType, float]:
        """How well investigator fits different archetypes - DB data + calculation"""
        if self._archetype_scores is None:
            scores = {}

            # Combat score based on combat stat and combat cards
            combat_cards = [card for card in self.deck if "combat" in card.traits]
            scores[ArchetypeType.COMBAT] = (
                self.stats.combat * 0.3 + len(combat_cards) / len(self.deck) * 0.7
            )

            # Investigation score
            investigation_cards = [
                card for card in self.deck if "investigation" in card.traits
            ]
            scores[ArchetypeType.INVESTIGATION] = (
                self.stats.intellect * 0.3
                + len(investigation_cards) / len(self.deck) * 0.7
            )

            # Support score based on support cards
            support_cards = [card for card in self.deck if "support" in card.traits]
            scores[ArchetypeType.SUPPORT] = len(support_cards) / len(self.deck)

            # Economy score based on resource generation
            economy_cards = [card for card in self.deck if "economy" in card.traits]
            scores[ArchetypeType.ECONOMY] = len(economy_cards) / len(self.deck)

            # Balanced score (inverse of specialization)
            specialization = max(scores.values()) if scores else 0
            scores[ArchetypeType.BALANCED] = 1.0 - specialization

            self._archetype_scores = scores
        return self._archetype_scores

    def get_primary_archetype(self) -> ArchetypeType:
        """Get the primary archetype - calculation only"""
        scores = self.archetype_scores
        return max(scores.items(), key=lambda x: x[1])[0]

    # =============================================================================
    # SCENARIO MATCHUP ANALYSIS (Uses DB data + calculations)
    # =============================================================================

    def evaluate_scenario_matchup(self, scenario: Scenario) -> Dict[str, Any]:
        """Evaluate how well investigator matches scenario - DB data + calculation"""
        context = scenario.get_scenario_context()

        # Calculate matchup scores
        time_pressure_score = self._calculate_time_pressure_matchup(context)
        investigation_score = self._calculate_investigation_matchup(context)
        combat_score = self._calculate_combat_matchup(context)

        return {
            "overall_matchup": (
                time_pressure_score + investigation_score + combat_score
            )
            / 3,
            "time_pressure_matchup": time_pressure_score,
            "investigation_matchup": investigation_score,
            "combat_matchup": combat_score,
            "recommended_strategy": self._get_recommended_strategy(context),
            "risk_factors": self._identify_risk_factors(context),
        }

    def _calculate_time_pressure_matchup(self, context: Dict[str, float]) -> float:
        """Calculate time pressure matchup - calculation only"""
        time_pressure = context.get("time_pressure", 0.5)
        action_efficiency = self.calculate_action_economy()["action_efficiency"]
        return 1.0 - abs(time_pressure - action_efficiency)

    def _calculate_investigation_matchup(self, context: Dict[str, float]) -> float:
        """Calculate investigation matchup - calculation only"""
        investigation_heavy = context.get("investigation_heavy", 0.5)
        intellect_score = self.stats.intellect / 5.0  # Normalize to 0-1
        return 1.0 - abs(investigation_heavy - intellect_score)

    def _calculate_combat_matchup(self, context: Dict[str, float]) -> float:
        """Calculate combat matchup - calculation only"""
        combat_heavy = context.get("combat_heavy", 0.5)
        combat_score = self.stats.combat / 5.0  # Normalize to 0-1
        return 1.0 - abs(combat_heavy - combat_score)

    def _get_recommended_strategy(self, context: Dict[str, float]) -> str:
        """Get recommended strategy - calculation only"""
        if context.get("time_pressure", 0.5) > 0.7:
            return "Prioritize speed and action economy"
        elif context.get("investigation_heavy", 0.5) > 0.7:
            return "Focus on investigation tools and intellect"
        elif context.get("combat_heavy", 0.5) > 0.7:
            return "Pack combat cards and damage dealing"
        else:
            return "Balanced approach with flexibility"

    def _identify_risk_factors(self, context: Dict[str, float]) -> List[str]:
        """Identify potential risk factors - calculation only"""
        risks = []

        if (
            context.get("time_pressure", 0.5) > 0.7
            and self.calculate_action_economy()["action_efficiency"] < 0.3
        ):
            risks.append("Low action efficiency for time-pressured scenario")

        if context.get("investigation_heavy", 0.5) > 0.7 and self.stats.intellect < 3:
            risks.append("Low intellect for investigation-heavy scenario")

        if context.get("combat_heavy", 0.5) > 0.7 and self.stats.combat < 3:
            risks.append("Low combat for combat-heavy scenario")

        return risks

    # =============================================================================
    # CARD RECOMMENDATION (Uses DB data + calculations)
    # =============================================================================

    def get_recommended_card_types(self) -> List[Tuple[CardType, float]]:
        """Get recommended card types with scores - DB data + calculation"""
        archetype = self.get_primary_archetype()

        recommendations = []

        if archetype == ArchetypeType.COMBAT:
            recommendations.extend(
                [
                    (CardType.ASSET, 0.9),  # Weapons
                    (CardType.EVENT, 0.7),  # Combat events
                    (CardType.SKILL, 0.5),  # Combat skills
                ]
            )
        elif archetype == ArchetypeType.INVESTIGATION:
            recommendations.extend(
                [
                    (CardType.ASSET, 0.8),  # Investigation tools
                    (CardType.EVENT, 0.6),  # Investigation events
                    (CardType.SKILL, 0.7),  # Investigation skills
                ]
            )
        else:
            recommendations.extend(
                [(CardType.ASSET, 0.6), (CardType.EVENT, 0.6), (CardType.SKILL, 0.6)]
            )

        return recommendations

    def calculate_deck_optimization_score(self, cards: List[PlayerCard]) -> float:
        """Calculate how well cards synergize - DB data + calculation"""
        if not cards:
            return 0.0

        # Basic synergy scoring based on traits and types
        synergy_score = 0.0
        total_combinations = 0

        for i, card1 in enumerate(cards):
            for card2 in cards[i + 1 :]:
                total_combinations += 1
                if self._cards_synergize(card1, card2):
                    synergy_score += 1

        return synergy_score / total_combinations if total_combinations > 0 else 0.0

    def _cards_synergize(self, card1: PlayerCard, card2: PlayerCard) -> bool:
        """Check if two cards synergize - DB data + calculation"""
        # Simple synergy check based on shared traits
        shared_traits = set(card1.traits) & set(card2.traits)
        return len(shared_traits) > 0

    # =============================================================================
    # META ANALYSIS (Uses DB data + calculations)
    # =============================================================================

    def calculate_meta_performance(self) -> Dict[str, float]:
        """Calculate meta performance metrics - DB data + calculation"""
        return {
            "tier_score": self.meta_context.current_tier / 5.0,
            "popularity_score": self.meta_context.popularity_score,
            "win_rate": self.meta_context.win_rate,
            "trend_score": (self.meta_context.meta_shift_trend + 1)
            / 2,  # Normalize -1,1 to 0,1
            "overall_meta_score": (
                self.meta_context.current_tier / 5.0 * 0.3
                + self.meta_context.popularity_score * 0.2
                + self.meta_context.win_rate * 0.3
                + (self.meta_context.meta_shift_trend + 1) / 2 * 0.2
            ),
        }

    def get_counter_meta_strategies(self) -> List[str]:
        """Get counter-meta strategies - DB data + calculation"""
        strategies = []

        if self.meta_context.current_tier < 3:
            strategies.append("Consider alternative investigators")

        if self.meta_context.win_rate < 0.5:
            strategies.append("Focus on deck optimization")

        if self.meta_context.meta_shift_trend < -0.3:
            strategies.append("Adapt to meta shifts")

        return strategies

    # =============================================================================
    # UTILITY METHODS
    # =============================================================================

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "code": self.code,
            "name": self.name,
            "faction": self.faction.value,
            "stats": {
                "health": self.stats.health,
                "sanity": self.stats.sanity,
                "willpower": self.stats.willpower,
                "intellect": self.stats.intellect,
                "combat": self.stats.combat,
                "agility": self.stats.agility,
                "deck_size": self.stats.deck_size,
            },
            "abilities": {
                "unique": self.stats.unique_ability,
                "elder_sign": self.stats.elder_sign_ability,
            },
            "analysis": {
                "stat_distribution": self.stat_distribution,
                "archetype_scores": {
                    k.value: v for k, v in self.archetype_scores.items()
                },
                "primary_archetype": self.get_primary_archetype().value,
                "deck_composition": self.analyze_deck_composition(),
                "action_economy": self.calculate_action_economy(),
                "meta_performance": self.calculate_meta_performance(),
            },
            "meta_context": {
                "tier": self.meta_context.current_tier,
                "popularity": self.meta_context.popularity_score,
                "win_rate": self.meta_context.win_rate,
                "trend": self.meta_context.meta_shift_trend,
            },
        }

    def __str__(self) -> str:
        return f"Investigator({self.name}, {self.faction.value})"

    def __repr__(self) -> str:
        return (
            f"Investigator(code={self.code}, name={self.name}, faction={self.faction})"
        )
