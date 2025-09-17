from typing import List, Dict, Any, Optional, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime

from ..investigators.investigators_clean import Investigator, ArchetypeType
from ..scenario import Scenario
from ..card.card_type import CardType
from ..difficulty import Difficulty


class AnalysisContext:
    """Context class with only calculable statistics"""

    def __init__(
        self,
        difficulty: Difficulty = Difficulty.STANDARD,
        player_count: int = 3,
    ):
        self.difficulty = difficulty
        self.player_count = player_count
        self.analysis_timestamp = datetime.now()

    # =============================================================================
    # CARD VALUE ANALYSIS (Based on calculable data)
    # =============================================================================

    def calculate_card_value_in_context(
        self,
        card_code: str,
        investigator: Investigator,
        scenario: Optional[Scenario] = None,
    ) -> Dict[str, Any]:
        """
        CALCULABLE: Calculate contextual card value based on investigator and scenario

        Logic:
        1. Base value from card stats (cost, XP, traits)
        2. Investigator synergy based on archetype match
        3. Scenario bonus based on scenario requirements
        4. Total value = base + synergy + scenario bonus

        Example: Machete for Roland in combat-heavy scenario
        - Base value: 2 (cost) + 0 (XP) + 1 (weapon trait) = 3
        - Investigator synergy: +2 (combat archetype)
        - Scenario bonus: +1 (combat-heavy scenario)
        - Total: 6
        """
        base_value = self._get_base_card_value(card_code)
        investigator_bonus = self._calculate_investigator_synergy(
            card_code, investigator
        )
        scenario_bonus = (
            self._calculate_scenario_bonus(card_code, scenario) if scenario else 0.0
        )

        total_value = base_value + investigator_bonus + scenario_bonus

        return {
            "base_value": base_value,
            "investigator_synergy": investigator_bonus,
            "scenario_bonus": scenario_bonus,
            "total_value": total_value,
            "value_breakdown": {
                "base": base_value / total_value if total_value > 0 else 0,
                "investigator": (
                    investigator_bonus / total_value if total_value > 0 else 0
                ),
                "scenario": scenario_bonus / total_value if total_value > 0 else 0,
            },
        }

    def _get_base_card_value(self, card_code: str) -> float:
        """
        CALCULABLE: Get base card value from database

        Logic:
        1. Query card from database
        2. Calculate value based on cost, XP, and traits
        3. Formula: (5 - cost) + (3 - xp) + trait_bonus

        Example: Machete (cost=2, xp=0, traits=[weapon, melee])
        - Cost value: 5 - 2 = 3
        - XP value: 3 - 0 = 3
        - Trait bonus: +1 (weapon trait)
        - Total: 7
        """
        # This would query the database for actual card data
        # For now, return a placeholder based on common patterns
        return 5.0  # Placeholder - would be calculated from DB

    def _calculate_investigator_synergy(
        self, card_code: str, investigator: Investigator
    ) -> float:
        """
        CALCULABLE: Calculate investigator synergy based on archetype match

        Logic:
        1. Get investigator's primary archetype
        2. Check if card traits match archetype needs
        3. Return synergy bonus based on match quality

        Example: Combat card for combat archetype investigator
        - Archetype: Combat
        - Card traits: [combat, weapon]
        - Match: Perfect (2/2 traits match)
        - Bonus: +2
        """
        archetype = investigator.get_primary_archetype()

        # This would check actual card traits from database
        # For now, use archetype-based logic
        if archetype == ArchetypeType.COMBAT:
            return 1.0  # Combat cards get bonus
        elif archetype == ArchetypeType.INVESTIGATION:
            return 1.0  # Investigation cards get bonus
        else:
            return 0.5  # Other cards get small bonus

    def _calculate_scenario_bonus(self, card_code: str, scenario: Scenario) -> float:
        """
        CALCULABLE: Calculate scenario-specific bonus

        Logic:
        1. Get scenario context (time pressure, investigation heavy, etc.)
        2. Check if card traits help with scenario requirements
        3. Return bonus based on how much the card helps

        Example: Fast card in time-pressured scenario
        - Scenario: High time pressure
        - Card: Fast action (0 actions)
        - Bonus: +1 (helps with time pressure)
        """
        context = scenario.get_scenario_context()
        bonus = 0.0

        # Time pressure bonus
        if context.get("time_pressure", 0.5) > 0.7:
            # This would check if card is fast/action-efficient
            bonus += 0.5

        # Investigation bonus
        if context.get("investigation_heavy", 0.5) > 0.7:
            # This would check if card helps with investigation
            bonus += 0.5

        return bonus

    # =============================================================================
    # DECK OPTIMIZATION (Based on calculable data)
    # =============================================================================

    def calculate_deck_power_level(
        self, investigator: Investigator
    ) -> Dict[str, float]:
        """
        CALCULABLE: Calculate overall deck power level

        Logic:
        1. Get deck composition analysis
        2. Get archetype scores
        3. Calculate synergy score
        4. Combine metrics with weighted average

        Example: Roland with focused combat deck
        - Consistency: 0.8 (focused on combat)
        - Archetype match: 0.9 (combat archetype)
        - Synergy: 0.7 (good card interactions)
        - Power: (0.8 * 0.3) + (0.9 * 0.4) + (0.7 * 0.3) = 0.81
        """
        deck_analysis = investigator.analyze_deck_composition()
        archetype_scores = investigator.calculate_archetype_scores()
        synergy_score = investigator.calculate_deck_synergy_score(investigator.deck)

        # Get primary archetype score
        primary_archetype = investigator.get_primary_archetype()
        archetype_match = archetype_scores[primary_archetype]

        # Weighted combination
        power_level = (
            deck_analysis["consistency_score"] * 0.3
            + archetype_match * 0.4
            + synergy_score * 0.3
        )

        return {
            "overall_power": power_level,
            "consistency": deck_analysis["consistency_score"],
            "archetype_match": archetype_match,
            "synergy_score": synergy_score,
            "tier_equivalent": self._power_to_tier(power_level),
        }

    def _power_to_tier(self, power_level: float) -> str:
        """
        CALCULABLE: Convert power level to tier based on distribution

        Logic:
        1. Use quartile-based tier boundaries
        2. S tier: top 5%, A tier: next 15%, B tier: next 30%, C tier: next 30%, D tier: bottom 20%
        3. This would be calibrated based on actual deck data

        Example: Power level 0.85
        - 0.85 >= 0.8: S tier
        """
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

    def analyze_win_conditions(
        self, investigator: Investigator, scenario: Scenario
    ) -> List[Dict[str, Any]]:
        """
        CALCULABLE: Analyze win conditions based on scenario and investigator

        Logic:
        1. Check scenario type (investigation, combat, etc.)
        2. Check investigator strengths
        3. Identify primary and secondary win conditions
        4. Suggest required card types

        Example: Investigation-heavy scenario with Roland
        - Primary: Investigation (Roland is weak here)
        - Secondary: Combat (Roland is strong here)
        - Required: Investigation tools, combat backup
        """
        win_conditions = []

        # Primary win condition based on scenario
        if scenario.is_investigation_heavy():
            win_conditions.append(
                {
                    "type": "investigation",
                    "priority": "high",
                    "description": "Gather clues efficiently",
                    "investigator_strength": investigator.stats.intellect / 5.0,
                    "required_card_types": ["investigation", "clue"],
                }
            )

        if scenario.is_combat_heavy():
            win_conditions.append(
                {
                    "type": "combat",
                    "priority": "high",
                    "description": "Defeat enemies efficiently",
                    "investigator_strength": investigator.stats.combat / 5.0,
                    "required_card_types": ["combat", "weapon"],
                }
            )

        # Secondary win conditions
        win_conditions.append(
            {
                "type": "survival",
                "priority": "medium",
                "description": "Survive until scenario completion",
                "investigator_strength": (
                    investigator.stats.health + investigator.stats.sanity
                )
                / 20.0,
                "required_card_types": ["survival", "healing"],
            }
        )

        return win_conditions

    def evaluate_tech_choices(
        self, investigator: Investigator, scenario: Scenario
    ) -> List[Dict[str, Any]]:
        """
        CALCULABLE: Evaluate tech choices based on scenario requirements

        Logic:
        1. Identify scenario weaknesses for investigator
        2. Suggest card types that address weaknesses
        3. Calculate synergy scores for suggested cards

        Example: Roland in investigation-heavy scenario
        - Weakness: Low intellect
        - Tech choice: Investigation tools
        - Synergy: Medium (not his primary archetype)
        """
        tech_choices = []

        # Check for investigation weakness
        if scenario.is_investigation_heavy() and investigator.stats.intellect < 3:
            tech_choices.append(
                {
                    "card_type": "investigation",
                    "reason": "Low intellect for investigation-heavy scenario",
                    "priority": "high",
                    "synergy_score": 0.5,  # Medium synergy for non-primary archetype
                }
            )

        # Check for combat weakness
        if scenario.is_combat_heavy() and investigator.stats.combat < 3:
            tech_choices.append(
                {
                    "card_type": "combat",
                    "reason": "Low combat for combat-heavy scenario",
                    "priority": "high",
                    "synergy_score": 0.5,
                }
            )

        # Check for action efficiency weakness
        if (
            scenario.get_scenario_context().get("time_pressure", 0.5) > 0.7
            and investigator.calculate_action_economy()["overall_efficiency"] < 0.2
        ):
            tech_choices.append(
                {
                    "card_type": "action_economy",
                    "reason": "Low action efficiency for time-pressured scenario",
                    "priority": "medium",
                    "synergy_score": 0.7,
                }
            )

        return tech_choices

    # =============================================================================
    # SYNERGY ANALYSIS (Based on calculable data)
    # =============================================================================

    def analyze_card_synergies(
        self, card_codes: List[str]
    ) -> Dict[str, List[Dict[str, Any]]]:
        """
        CALCULABLE: Analyze card synergies based on shared traits

        Logic:
        1. For each card pair, check for shared traits
        2. Calculate synergy score based on trait overlap
        3. Identify synergy type based on trait combinations

        Example: Machete + Vicious Blow
        - Machete traits: [weapon, melee]
        - Vicious Blow traits: [combat, skill]
        - Shared traits: None
        - Synergy: Low (different types)
        """
        synergies = {}

        for i, card1 in enumerate(card_codes):
            card_synergies = []
            for j, card2 in enumerate(card_codes[i + 1 :], i + 1):
                synergy_score = self._calculate_card_synergy(card1, card2)
                if synergy_score > 0.3:  # Lower threshold for more results
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
        """
        CALCULABLE: Calculate synergy between two cards

        Logic:
        1. Get traits from both cards (from database)
        2. Calculate trait overlap ratio
        3. Apply bonus for complementary traits

        Example: Two combat cards
        - Card1 traits: [combat, weapon]
        - Card2 traits: [combat, skill]
        - Shared: [combat]
        - Overlap: 1/2 = 0.5
        - Synergy: 0.5
        """
        # This would query the database for actual card traits
        # For now, return a placeholder
        return 0.6  # Placeholder

    def _get_synergy_type(self, card1: str, card2: str) -> str:
        """
        CALCULABLE: Get synergy type based on trait combinations

        Logic:
        1. Analyze shared and complementary traits
        2. Classify synergy type based on trait patterns

        Example: Weapon + Combat skill
        - Type: "combo" (one enables the other)
        """
        # This would analyze actual trait combinations
        return "combo"  # Placeholder

    # =============================================================================
    # UTILITY METHODS
    # =============================================================================

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary for API responses"""
        return {
            "difficulty": self.difficulty.value,
            "player_count": self.player_count,
            "analysis_timestamp": self.analysis_timestamp.isoformat(),
        }

