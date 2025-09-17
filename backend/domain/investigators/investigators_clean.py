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


@dataclass
class InvestigatorStats:
    """Core investigator statistics - ONLY from database"""

    health: int
    sanity: int
    willpower: int
    intellect: int
    combat: int
    agility: int
    deck_size: int
    unique_ability: str
    elder_sign_ability: str


class Investigator:
    """Investigator class with only calculable statistics"""

    def __init__(
        self,
        code: str,
        name: str,
        faction: Faction,
        stats: InvestigatorStats,
        deck: List[PlayerCard],
    ):
        self.code = code
        self.name = name
        self.faction = faction
        self.stats = stats
        self.deck = deck

        # Calculated properties
        self._stat_distribution = None
        self._deck_analysis = None

    # =============================================================================
    # STAT ANALYSIS (Purely calculable from DB data)
    # =============================================================================

    @property
    def stat_distribution(self) -> Dict[str, float]:
        """
        CALCULABLE: Normalized stat spread for comparison

        Logic:
        1. Sum all 4 stats (willpower + intellect + combat + agility)
        2. Each stat's percentage = stat_value / total_stats
        3. This shows which stats the investigator is specialized in

        Example: Roland (3,2,4,2) = 11 total
        - Willpower: 3/11 = 27.3%
        - Intellect: 2/11 = 18.2%
        - Combat: 4/11 = 36.4%
        - Agility: 2/11 = 18.2%
        """
        if self._stat_distribution is None:
            total_stats = sum(
                [
                    self.stats.willpower,
                    self.stats.intellect,
                    self.stats.combat,
                    self.stats.agility,
                ]
            )

            if total_stats == 0:
                # Handle edge case
                self._stat_distribution = {
                    "willpower": 0.25,
                    "intellect": 0.25,
                    "combat": 0.25,
                    "agility": 0.25,
                    "total": 0,
                }
            else:
                self._stat_distribution = {
                    "willpower": self.stats.willpower / total_stats,
                    "intellect": self.stats.intellect / total_stats,
                    "combat": self.stats.combat / total_stats,
                    "agility": self.stats.agility / total_stats,
                    "total": total_stats,
                }
        return self._stat_distribution

    def calculate_stat_efficiency(self) -> Dict[str, float]:
        """
        CALCULABLE: Cost-to-stat ratios

        Logic:
        1. Each stat divided by deck size gives "stat per card slot"
        2. Higher values = more efficient use of deck space
        3. This helps compare investigators with different deck sizes

        Example: Roland (3,2,4,2) with 30-card deck
        - Willpower efficiency: 3/30 = 0.1
        - Combat efficiency: 4/30 = 0.133 (most efficient)
        """
        return {
            "willpower_efficiency": self.stats.willpower / self.stats.deck_size,
            "intellect_efficiency": self.stats.intellect / self.stats.deck_size,
            "combat_efficiency": self.stats.combat / self.stats.deck_size,
            "agility_efficiency": self.stats.agility / self.stats.deck_size,
        }

    def analyze_stat_breakpoints(self) -> Dict[str, Any]:
        """
        CALCULABLE: Critical stat thresholds based on game mechanics

        Logic:
        1. Arkham Horror uses difficulty 0-5 for most tests
        2. Breakpoints are where stats become "good enough" for tests
        3. 3+ = can pass easy tests, 4+ = standard, 5+ = hard
        4. Current level shows which breakpoint the investigator reaches

        Example: Roland with 4 combat
        - Can reliably pass combat tests up to difficulty 4
        - Needs help for difficulty 5+ tests
        """

        def get_breakpoint_level(stat: int) -> int:
            if stat >= 5:
                return 3  # Can handle hard tests
            elif stat >= 4:
                return 2  # Can handle standard tests
            elif stat >= 3:
                return 1  # Can handle easy tests
            else:
                return 0  # Needs help for most tests

        return {
            "breakpoint_levels": {
                "willpower": get_breakpoint_level(self.stats.willpower),
                "intellect": get_breakpoint_level(self.stats.intellect),
                "combat": get_breakpoint_level(self.stats.combat),
                "agility": get_breakpoint_level(self.stats.agility),
            },
            "total_breakpoints": sum(
                [
                    get_breakpoint_level(self.stats.willpower),
                    get_breakpoint_level(self.stats.intellect),
                    get_breakpoint_level(self.stats.combat),
                    get_breakpoint_level(self.stats.agility),
                ]
            ),
        }

    # =============================================================================
    # DECK ANALYSIS (Purely calculable from DB data)
    # =============================================================================

    def analyze_deck_composition(self) -> Dict[str, Any]:
        """
        CALCULABLE: Deck composition analysis

        Logic:
        1. Count cards by type (Asset, Event, Skill, etc.)
        2. Count cards by faction (Guardian, Seeker, etc.)
        3. Calculate average cost from card.cost values
        4. Calculate total XP from card.xp values
        5. Consistency = how focused the deck is (max type count / total cards)

        Example: 30-card deck with 15 Assets, 10 Events, 5 Skills
        - Asset ratio: 15/30 = 50%
        - Consistency: 15/30 = 50% (focused on assets)
        """
        if self._deck_analysis is None:
            card_types = {}
            factions = {}
            costs = []
            xp_costs = []
            traits = {}

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

                # Count traits
                for trait in card.traits:
                    traits[trait] = traits.get(trait, 0) + 1

            # Calculate consistency (how focused the deck is)
            if card_types:
                max_type_count = max(card_types.values())
                consistency_score = max_type_count / len(self.deck)
            else:
                consistency_score = 0.0

            self._deck_analysis = {
                "card_type_distribution": card_types,
                "faction_distribution": factions,
                "trait_distribution": traits,
                "average_cost": sum(costs) / len(costs) if costs else 0,
                "total_xp": sum(xp_costs),
                "deck_size": len(self.deck),
                "consistency_score": consistency_score,
                "most_common_type": (
                    max(card_types.items(), key=lambda x: x[1])[0]
                    if card_types
                    else None
                ),
                "most_common_trait": (
                    max(traits.items(), key=lambda x: x[1])[0] if traits else None
                ),
            }
        return self._deck_analysis

    def calculate_action_economy(self) -> Dict[str, float]:
        """
        CALCULABLE: Action efficiency metrics

        Logic:
        1. Count cards with 'actions' attribute
        2. Count cards with 0 actions (free actions)
        3. Calculate ratios for action efficiency

        Example: 30-card deck with 20 action cards, 5 free actions
        - Action card ratio: 20/30 = 66.7%
        - Free action ratio: 5/20 = 25%
        - Overall efficiency: 5/30 = 16.7%
        """
        action_cards = [card for card in self.deck if hasattr(card, "actions")]
        free_actions = [
            card for card in action_cards if getattr(card, "actions", 0) == 0
        ]

        return {
            "total_action_cards": len(action_cards),
            "free_action_cards": len(free_actions),
            "action_card_ratio": len(action_cards) / len(self.deck) if self.deck else 0,
            "free_action_ratio": (
                len(free_actions) / len(action_cards) if action_cards else 0
            ),
            "overall_efficiency": (
                len(free_actions) / len(self.deck) if self.deck else 0
            ),
        }

    def calculate_resource_economy(self) -> Dict[str, float]:
        """
        CALCULABLE: Resource generation and spending analysis

        Logic:
        1. Count cards that generate resources (economy trait)
        2. Count cards that cost resources (cost > 0)
        3. Calculate resource generation vs spending ratio

        Example: 30-card deck with 5 economy cards, 20 cards with cost > 0
        - Economy ratio: 5/30 = 16.7%
        - Cost ratio: 20/30 = 66.7%
        - Resource balance: 5/20 = 0.25 (generates 25% of what it spends)
        """
        economy_cards = [card for card in self.deck if "economy" in card.traits]
        cost_cards = [
            card
            for card in self.deck
            if hasattr(card, "cost") and card.cost and card.cost > 0
        ]

        return {
            "economy_cards": len(economy_cards),
            "cost_cards": len(cost_cards),
            "economy_ratio": len(economy_cards) / len(self.deck) if self.deck else 0,
            "cost_ratio": len(cost_cards) / len(self.deck) if self.deck else 0,
            "resource_balance": (
                len(economy_cards) / len(cost_cards) if cost_cards else 0
            ),
        }

    # =============================================================================
    # ARCHETYPE ANALYSIS (Based on calculable data)
    # =============================================================================

    def calculate_archetype_scores(self) -> Dict[ArchetypeType, float]:
        """
        CALCULABLE: How well investigator fits different archetypes

        Logic:
        1. Combat: Based on combat stat + combat trait cards
        2. Investigation: Based on intellect stat + investigation trait cards
        3. Support: Based on support trait cards
        4. Economy: Based on economy trait cards
        5. Survival: Based on survival trait cards
        6. Balanced: Inverse of highest specialization

        Example: Roland with 4 combat, 2 intellect, 10 combat cards, 5 investigation cards
        - Combat score: (4/5 * 0.5) + (10/30 * 0.5) = 0.4 + 0.167 = 0.567
        - Investigation score: (2/5 * 0.5) + (5/30 * 0.5) = 0.2 + 0.083 = 0.283
        """
        scores = {}

        # Combat score: 50% stats, 50% cards
        combat_cards = [card for card in self.deck if "combat" in card.traits]
        scores[ArchetypeType.COMBAT] = (
            (self.stats.combat / 5.0) * 0.5  # Normalize stat to 0-1
            + (len(combat_cards) / len(self.deck)) * 0.5
            if self.deck
            else 0
        )

        # Investigation score
        investigation_cards = [
            card for card in self.deck if "investigation" in card.traits
        ]
        scores[ArchetypeType.INVESTIGATION] = (
            (self.stats.intellect / 5.0) * 0.5
            + (len(investigation_cards) / len(self.deck)) * 0.5
            if self.deck
            else 0
        )

        # Support score (cards only)
        support_cards = [card for card in self.deck if "support" in card.traits]
        scores[ArchetypeType.SUPPORT] = (
            len(support_cards) / len(self.deck) if self.deck else 0
        )

        # Economy score (cards only)
        economy_cards = [card for card in self.deck if "economy" in card.traits]
        scores[ArchetypeType.ECONOMY] = (
            len(economy_cards) / len(self.deck) if self.deck else 0
        )

        # Survival score (cards only)
        survival_cards = [card for card in self.deck if "survival" in card.traits]
        scores[ArchetypeType.SURVIVAL] = (
            len(survival_cards) / len(self.deck) if self.deck else 0
        )

        # Balanced score (inverse of highest specialization)
        if scores:
            max_specialization = max(scores.values())
            scores[ArchetypeType.BALANCED] = 1.0 - max_specialization
        else:
            scores[ArchetypeType.BALANCED] = 1.0

        return scores

    def get_primary_archetype(self) -> ArchetypeType:
        """
        CALCULABLE: Get the primary archetype based on highest score

        Logic:
        1. Calculate all archetype scores
        2. Return the archetype with highest score
        3. If tied, return the first one (could be made more sophisticated)
        """
        scores = self.calculate_archetype_scores()
        return max(scores.items(), key=lambda x: x[1])[0]

    # =============================================================================
    # SCENARIO MATCHUP ANALYSIS (Based on calculable data)
    # =============================================================================

    def evaluate_scenario_matchup(self, scenario: Scenario) -> Dict[str, Any]:
        """
        CALCULABLE: How well investigator matches scenario requirements

        Logic:
        1. Get scenario context (time pressure, investigation heavy, combat heavy)
        2. Compare investigator stats to scenario requirements
        3. Calculate matchup scores based on stat alignment
        4. Identify risk factors where investigator is weak

        Example: Roland (3,2,4,2) vs investigation-heavy scenario
        - Intellect matchup: 2/5 = 0.4 (weak)
        - Risk factor: "Low intellect for investigation-heavy scenario"
        """
        context = scenario.get_scenario_context()

        # Calculate individual matchup scores
        time_pressure_score = self._calculate_time_pressure_matchup(context)
        investigation_score = self._calculate_investigation_matchup(context)
        combat_score = self._calculate_combat_matchup(context)

        # Overall matchup is average of individual scores
        overall_matchup = (time_pressure_score + investigation_score + combat_score) / 3

        return {
            "overall_matchup": overall_matchup,
            "time_pressure_matchup": time_pressure_score,
            "investigation_matchup": investigation_score,
            "combat_matchup": combat_score,
            "risk_factors": self._identify_risk_factors(context),
            "strengths": self._identify_strengths(context),
        }

    def _calculate_time_pressure_matchup(self, context: Dict[str, float]) -> float:
        """
        CALCULABLE: Time pressure matchup based on action efficiency

        Logic:
        1. Get scenario time pressure (0-1)
        2. Get investigator action efficiency (0-1)
        3. Closer values = better matchup
        4. Formula: 1 - |time_pressure - action_efficiency|

        Example: Scenario with 0.8 time pressure, investigator with 0.6 action efficiency
        - Matchup: 1 - |0.8 - 0.6| = 1 - 0.2 = 0.8 (good matchup)
        """
        time_pressure = context.get("time_pressure", 0.5)
        action_efficiency = self.calculate_action_economy()["overall_efficiency"]
        return 1.0 - abs(time_pressure - action_efficiency)

    def _calculate_investigation_matchup(self, context: Dict[str, float]) -> float:
        """
        CALCULABLE: Investigation matchup based on intellect stat

        Logic:
        1. Get scenario investigation requirement (0-1)
        2. Get investigator intellect normalized (0-1)
        3. Closer values = better matchup

        Example: Investigation-heavy scenario (0.8), Roland with 2 intellect
        - Intellect score: 2/5 = 0.4
        - Matchup: 1 - |0.8 - 0.4| = 1 - 0.4 = 0.6 (moderate matchup)
        """
        investigation_heavy = context.get("investigation_heavy", 0.5)
        intellect_score = self.stats.intellect / 5.0  # Normalize to 0-1
        return 1.0 - abs(investigation_heavy - intellect_score)

    def _calculate_combat_matchup(self, context: Dict[str, float]) -> float:
        """
        CALCULABLE: Combat matchup based on combat stat

        Logic:
        1. Get scenario combat requirement (0-1)
        2. Get investigator combat normalized (0-1)
        3. Closer values = better matchup

        Example: Combat-heavy scenario (0.8), Roland with 4 combat
        - Combat score: 4/5 = 0.8
        - Matchup: 1 - |0.8 - 0.8| = 1 - 0 = 1.0 (perfect matchup)
        """
        combat_heavy = context.get("combat_heavy", 0.5)
        combat_score = self.stats.combat / 5.0  # Normalize to 0-1
        return 1.0 - abs(combat_heavy - combat_score)

    def _identify_risk_factors(self, context: Dict[str, float]) -> List[str]:
        """
        CALCULABLE: Identify potential risk factors based on stat gaps

        Logic:
        1. Check if scenario requirements exceed investigator capabilities
        2. Use hardcoded thresholds based on game mechanics
        3. Return specific risk descriptions

        Example: Time-pressured scenario with low action efficiency
        - Risk: "Low action efficiency for time-pressured scenario"
        """
        risks = []

        # Time pressure risk
        if (
            context.get("time_pressure", 0.5) > 0.7
            and self.calculate_action_economy()["overall_efficiency"] < 0.2
        ):
            risks.append("Low action efficiency for time-pressured scenario")

        # Investigation risk
        if context.get("investigation_heavy", 0.5) > 0.7 and self.stats.intellect < 3:
            risks.append("Low intellect for investigation-heavy scenario")

        # Combat risk
        if context.get("combat_heavy", 0.5) > 0.7 and self.stats.combat < 3:
            risks.append("Low combat for combat-heavy scenario")

        return risks

    def _identify_strengths(self, context: Dict[str, float]) -> List[str]:
        """
        CALCULABLE: Identify investigator strengths for scenario

        Logic:
        1. Check if investigator stats exceed scenario requirements
        2. Return specific strength descriptions

        Example: High combat investigator in combat-heavy scenario
        - Strength: "High combat for combat-heavy scenario"
        """
        strengths = []

        # Combat strength
        if context.get("combat_heavy", 0.5) > 0.7 and self.stats.combat >= 4:
            strengths.append("High combat for combat-heavy scenario")

        # Investigation strength
        if context.get("investigation_heavy", 0.5) > 0.7 and self.stats.intellect >= 4:
            strengths.append("High intellect for investigation-heavy scenario")

        # Action efficiency strength
        if (
            context.get("time_pressure", 0.5) > 0.7
            and self.calculate_action_economy()["overall_efficiency"] > 0.3
        ):
            strengths.append("High action efficiency for time-pressured scenario")

        return strengths

    # =============================================================================
    # CARD RECOMMENDATION (Based on calculable data)
    # =============================================================================

    def get_recommended_card_types(self) -> List[Tuple[CardType, float]]:
        """
        CALCULABLE: Get recommended card types based on archetype

        Logic:
        1. Determine primary archetype
        2. Assign card type preferences based on archetype
        3. Use fixed scores based on archetype needs

        Example: Combat archetype investigator
        - Assets (weapons): 0.9 priority
        - Events (combat events): 0.7 priority
        - Skills (combat skills): 0.5 priority
        """
        archetype = self.get_primary_archetype()

        if archetype == ArchetypeType.COMBAT:
            return [
                (CardType.ASSET, 0.9),  # Weapons are primary
                (CardType.EVENT, 0.7),  # Combat events are secondary
                (CardType.SKILL, 0.5),  # Combat skills are tertiary
            ]
        elif archetype == ArchetypeType.INVESTIGATION:
            return [
                (CardType.ASSET, 0.8),  # Investigation tools
                (CardType.SKILL, 0.7),  # Investigation skills
                (CardType.EVENT, 0.6),  # Investigation events
            ]
        elif archetype == ArchetypeType.SUPPORT:
            return [
                (CardType.ASSET, 0.7),  # Support assets
                (CardType.EVENT, 0.6),  # Support events
                (CardType.SKILL, 0.5),  # Support skills
            ]
        else:  # Balanced or other
            return [
                (CardType.ASSET, 0.6),
                (CardType.EVENT, 0.6),
                (CardType.SKILL, 0.6),
            ]

    def calculate_deck_synergy_score(self, cards: List[PlayerCard]) -> float:
        """
        CALCULABLE: Calculate how well cards synergize based on shared traits

        Logic:
        1. For each pair of cards, check for shared traits
        2. Count total synergies found
        3. Return ratio of synergies to total possible pairs

        Example: 3 cards with traits [A,B], [B,C], [A,C]
        - Pairs: (1,2) shares B, (1,3) shares A, (2,3) shares C
        - Synergies: 3, Total pairs: 3, Score: 3/3 = 1.0
        """
        if not cards or len(cards) < 2:
            return 0.0

        synergies = 0
        total_pairs = 0

        for i, card1 in enumerate(cards):
            for card2 in cards[i + 1 :]:
                total_pairs += 1
                if self._cards_share_traits(card1, card2):
                    synergies += 1

        return synergies / total_pairs if total_pairs > 0 else 0.0

    def _cards_share_traits(self, card1: PlayerCard, card2: PlayerCard) -> bool:
        """
        CALCULABLE: Check if two cards share any traits

        Logic:
        1. Get traits from both cards
        2. Check for intersection
        3. Return True if any traits are shared

        Example: Card1 has [combat, weapon], Card2 has [weapon, asset]
        - Shared traits: [weapon]
        - Returns: True
        """
        shared_traits = set(card1.traits) & set(card2.traits)
        return len(shared_traits) > 0

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
                "stat_efficiency": self.calculate_stat_efficiency(),
                "stat_breakpoints": self.analyze_stat_breakpoints(),
                "deck_composition": self.analyze_deck_composition(),
                "action_economy": self.calculate_action_economy(),
                "resource_economy": self.calculate_resource_economy(),
                "archetype_scores": {
                    k.value: v for k, v in self.calculate_archetype_scores().items()
                },
                "primary_archetype": self.get_primary_archetype().value,
                "recommended_card_types": [
                    {"type": t.value, "priority": p}
                    for t, p in self.get_recommended_card_types()
                ],
            },
        }

    def __str__(self) -> str:
        return f"Investigator({self.name}, {self.faction.value})"

    def __repr__(self) -> str:
        return (
            f"Investigator(code={self.code}, name={self.name}, faction={self.faction})"
        )

