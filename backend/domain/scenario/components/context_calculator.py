"""
Context Calculator - Calculates scenario context values for card evaluation
Follows SRP by focusing solely on context calculation logic
"""

from typing import Dict, List, Optional, Any, cast, Union
from typing import TYPE_CHECKING


from ...card import EncounterCard, LocationCard, EnemyCard

if TYPE_CHECKING:
    from ..scenario import Scenario
from ...card import CardType
from ...Token.chaos_bag import ChaosBag

import sys
import os

backend_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."
)
if backend_path not in sys.path:
    sys.path.append(backend_path)

from domain.scenario.rules.scenario_definitions import get_scenario_rules
from domain import ScenarioType, Difficulty


class ContextCalculator:
    """Calculates various scenario context values for informed card evaluation"""

    def __init__(self, scenario: "Scenario"):
        self.scenario = scenario
        self.scenario_type = scenario.scenario_type
        self.difficulty = scenario.difficulty
        self.player_count = scenario.player_count

        # Context calculation parameters (can be tuned)
        self.time_pressure_weights = {
            "doom_ratio": 0.4,
            "scenario_speed": 0.3,
            "difficulty": 0.3,
        }

        self.resource_weights = {
            "clue_availability": 0.5,
            "difficulty": 0.3,
            "scenario_complexity": 0.2,
        }

        # Initialize context with player_count for rule application
        self.context = {
            "player_count": scenario.player_count,
            "difficulty": scenario.difficulty.value,
            "scenario_type": scenario.scenario_type.value,
        }

        # Load and apply scenario rules
        self.rules = get_scenario_rules(scenario.scenario_type)
        for rule in self.rules:
            self.context = rule.apply(self.context)

    def get_scenario_values(self) -> Dict[str, Any]:
        """Get calculated scenario values from rules"""
        return self.context.copy()

    def calculate_time_pressure(
        self, doom_threshold: int, agenda_rate: float, player_count: int = 2
    ) -> float:
        """
        Calculate time pressure context (0.0 to 1.0)
        Higher values indicate more time pressure
        """
        base_pressure = 0.5  # Neutral starting point

        # Factor 1: Doom threshold vs typical game length
        typical_game_rounds = 8
        doom_ratio = doom_threshold / (agenda_rate * typical_game_rounds)

        if doom_ratio < 0.6:  # Very tight time limit
            doom_pressure = 0.8
        elif doom_ratio < 0.8:  # Tight time limit
            doom_pressure = 0.6
        elif doom_ratio > 1.4:  # Generous time limit
            doom_pressure = 0.2
        else:  # Standard time limit
            doom_pressure = 0.4

        # Factor 2: Scenario-specific speed modifiers
        scenario_speed = self._get_scenario_speed_modifier()

        # Factor 3: Difficulty impact on time pressure
        difficulty_pressure = self._get_difficulty_time_modifier()

        # Weighted combination
        final_pressure = (
            doom_pressure * self.time_pressure_weights["doom_ratio"]
            + scenario_speed * self.time_pressure_weights["scenario_speed"]
            + difficulty_pressure * self.time_pressure_weights["difficulty"]
        )

        return max(0.0, min(1.0, final_pressure))

    def get_encounter_traits_count(
        self, cards: List[Union[EncounterCard, EnemyCard]]
    ) -> Dict[str, int]:
        """Count all traits across encounter cards and return as dictionary"""
        trait_counts = {}

        for card in cards:
            # Get traits from the card (handle different possible attribute names)
            traits = getattr(card, "traits", None) or []

            # Handle different trait formats
            if isinstance(traits, str):
                # If traits is a single string, split by common separators
                trait_list = [
                    t.strip() for t in traits.replace(".", ",").split(",") if t.strip()
                ]
            elif hasattr(traits, "__iter__"):
                # If traits is a list/iterable, convert to strings
                trait_list = [str(trait) for trait in traits if str(trait).strip()]
            else:
                trait_list = []

            # Count each trait, multiplied by card quantity
            card_quantity = getattr(card, "quantity", 1)
            for trait in trait_list:
                trait = trait.strip().title()  # Normalize trait names
                if trait:  # Skip empty traits
                    trait_counts[trait] = trait_counts.get(trait, 0) + card_quantity

        return trait_counts

    def calculate_encounter_wide_stats(self) -> Dict[str, Any]:
        """Calculate statistics for shared fields across all encounter card types"""

        if not self.scenario.encounter_cards:
            return {
                "total_encounter_cards": 0,
                "victory_points_available": 0,
                "cards_with_victory": 0,
                "average_victory_per_card": 0,
                "max_victory_single_card": 0,
                "doom_cards": 0,
                "total_doom_on_cards": 0,
                "cards_by_type": {},
                "overall_trait_distribution": {},
            }

        # Initialize counters
        victory_values = []
        doom_values = []
        cards_by_type = {}
        total_cards = 0

        for card in self.scenario.encounter_cards:
            card_quantity = getattr(card, "quantity", 1)
            card_type = getattr(card, "card_type", "unknown")
            total_cards += card_quantity

            # Count cards by type
            cards_by_type[card_type] = cards_by_type.get(card_type, 0) + card_quantity

            # Handle victory points (shared across enemies, locations, etc.)
            victory = getattr(card, "victory", 0) or 0
            if victory > 0:
                victory_values.extend([victory] * card_quantity)

            # Handle doom (can be on locations, enemies, etc.)
            doom = getattr(card, "doom", 0) or 0
            if doom > 0:
                doom_values.extend([doom] * card_quantity)

        # Calculate victory statistics
        total_victory = sum(victory_values)
        cards_with_victory = len(victory_values)
        max_victory = max(victory_values) if victory_values else 0
        avg_victory = total_victory / cards_with_victory if cards_with_victory else 0

        # Calculate doom statistics
        total_doom = sum(doom_values)
        cards_with_doom = len(doom_values)

        # Get overall trait distribution across ALL encounter cards
        overall_traits = self.get_encounter_traits_count(self.scenario.encounter_cards)

        return {
            "total_encounter_cards": total_cards,
            "victory_points_available": total_victory,
            "cards_with_victory": cards_with_victory,
            "average_victory_per_card": avg_victory,
            "max_victory_single_card": max_victory,
            "doom_cards": cards_with_doom,
            "total_doom_on_cards": total_doom,
            "cards_by_type": cards_by_type,  # {"enemy": 12, "treachery": 8, "location": 6}
            "overall_trait_distribution": overall_traits,
            # Additional useful stats
            "encounter_card_density": {
                "enemy_percentage": (
                    cards_by_type.get("enemy", 0) / total_cards * 100
                    if total_cards
                    else 0
                ),
                "treachery_percentage": (
                    cards_by_type.get("treachery", 0) / total_cards * 100
                    if total_cards
                    else 0
                ),
                "location_percentage": (
                    cards_by_type.get("location", 0) / total_cards * 100
                    if total_cards
                    else 0
                ),
            },
        }

    def calculate_treachery_stats(self) -> Dict[str, Any]:
        """Calculate treachery card statistics including test patterns"""
        import re

        treachery_cards = [
            card
            for card in self.scenario.encounter_cards
            if getattr(card, "card_type", None) == "treachery"
        ]

        if not treachery_cards:
            return {
                "trait_count": {},
                "treachery_count": 0,
                "no_of_combat_test": 0,
                "no_of_intellect_test": 0,
                "no_of_willpower_test": 0,
                "no_of_agility_test": 0,
                "average_combat_test_value": 0,
                "average_intellect_test_value": 0,
                "average_willpower_test_value": 0,
                "average_agility_test_value": 0,
                "no_of_card_with_surge": 0,
                "no_of_card_with_peril": 0,
                "no_of_card_with_attach": 0,
            }

        # Get trait counts for treachery cards
        trait_counts = self.get_encounter_traits_count(treachery_cards)

        # Test pattern: Test [willpower] (3) or Test {willpower} (3)
        test_pattern = (
            r"test\s+[\[\{]?(willpower|intellect|combat|agility)[\]\}]?\s*\((\d+)\)"
        )

        # Keyword patterns
        surge_pattern = r"\bsurge\b"
        peril_pattern = r"\bperil\b"
        attach_pattern = r"\battach\b"

        # Initialize counters
        test_counts = {"combat": 0, "intellect": 0, "willpower": 0, "agility": 0}
        test_values = {"combat": [], "intellect": [], "willpower": [], "agility": []}
        surge_count = 0
        peril_count = 0
        attach_count = 0

        total_treachery_count = sum(
            getattr(card, "quantity", 1) for card in treachery_cards
        )

        for card in treachery_cards:
            card_text = getattr(card, "text", "") or ""
            card_quantity = getattr(card, "quantity", 1)

            # Find all test patterns in the card text (case insensitive)
            test_matches = re.findall(test_pattern, card_text.lower(), re.IGNORECASE)

            for skill_type, difficulty in test_matches:
                test_counts[skill_type] += card_quantity
                test_values[skill_type].append(int(difficulty))

            # Check for keywords (case insensitive)
            if re.search(surge_pattern, card_text.lower(), re.IGNORECASE):
                surge_count += card_quantity

            if re.search(peril_pattern, card_text.lower(), re.IGNORECASE):
                peril_count += card_quantity

            if re.search(attach_pattern, card_text.lower(), re.IGNORECASE):
                attach_count += card_quantity

        # Calculate average test values
        def safe_average(values_list):
            return sum(values_list) / len(values_list) if values_list else 0

        return {
            "trait_count": trait_counts,
            "treachery_count": total_treachery_count,
            "no_of_combat_test": test_counts["combat"],
            "no_of_intellect_test": test_counts["intellect"],
            "no_of_willpower_test": test_counts["willpower"],
            "no_of_agility_test": test_counts["agility"],
            "average_combat_test_value": safe_average(test_values["combat"]),
            "average_intellect_test_value": safe_average(test_values["intellect"]),
            "average_willpower_test_value": safe_average(test_values["willpower"]),
            "average_agility_test_value": safe_average(test_values["agility"]),
            "no_of_card_with_surge": surge_count,
            "no_of_card_with_peril": peril_count,
            "no_of_card_with_attach": attach_count,
        }

    def calculate_location_stats(self) -> Dict[str, Any]:
        """Calculate location card statistics including clues and shroud values"""

        location_cards = [
            card
            for card in self.scenario.encounter_cards
            if getattr(card, "card_type", None) == "location"
        ]

        if not location_cards:
            return {
                "trait_count": {},
                "no_of_location": 0,
                "average_clue": 0,
                "average_shroud": 0,
                "highest_clue": 0,
                "lowest_clue": 0,
                "highest_shroud": 0,
                "lowest_shroud": 0,
            }

        # Get trait counts for location cards
        trait_counts = self.get_encounter_traits_count(location_cards)

        # Calculate clue values accounting for clue_fixed flag and player count
        def calculate_clue_value(location_card: LocationCard) -> int:
            base_clues = getattr(location_card, "clues", 0) or 0
            clue_fixed = location_card.clues_fixed  # Default to fixed if not specified

            if clue_fixed:
                # Fixed clues don't scale with player count
                return base_clues
            else:
                # Per-investigator clues scale with player count
                return base_clues * self.player_count

        # Extract shroud values (these don't scale with player count)
        shroud_values = []
        clue_values = []

        for location in location_cards:
            # Get shroud value
            shroud = getattr(location, "shroud", 0) or 0
            shroud_values.append(shroud)

            # Get clue value with proper scaling
            clue_value = calculate_clue_value(cast(LocationCard, location))
            clue_values.append(clue_value)

        # Filter out zero values for min/max calculations to avoid misleading results
        non_zero_clues = [c for c in clue_values if c > 0] or [0]
        non_zero_shrouds = [s for s in shroud_values if s > 0] or [0]

        total_locations = len(location_cards)

        return {
            "trait_count": trait_counts,
            "no_of_location": total_locations,
            "average_clue_per_location": sum(clue_values) / total_locations,
            "average_shroud_per_location": sum(shroud_values) / total_locations,
            "highest_clue": max(clue_values),
            "lowest_clue": min(non_zero_clues),  # Lowest non-zero clue
            "highest_shroud": max(shroud_values),
            "lowest_shroud": min(non_zero_shrouds),  # Lowest non-zero shroud
            "total_clues_available": sum(clue_values),  # Bonus: total clues in scenario
            "locations_with_clues": len(
                [c for c in clue_values if c > 0]
            ),  # Bonus: clue-bearing locations
            "locations_without_clues": len(
                [c for c in clue_values if c == 0]
            ),  # Bonus: non-clue locations
        }

    def calcualte_enemy_stats(self) -> Dict[str, Any]:
        """Calculate enemy stats"""
        enemy_cards = cast(
            List[EnemyCard],
            [
                card
                for card in self.scenario.encounter_cards
                if getattr(card, "card_type", None) == "enemy"
            ],
        )

        no_of_enemy_cards = sum([card.quantity for card in enemy_cards])

        if not enemy_cards or no_of_enemy_cards == 0:
            return {}

        def resolve_health(enemy_card: EnemyCard) -> int:
            if not enemy_card.defeatable:
                return 0
            return (
                self.player_count if enemy_card.health_per_investigator else 1
            ) * enemy_card.health

        fixed_fights = [e.fight for e in enemy_cards if not e.is_X_fight]
        fixed_evades = [e.evade for e in enemy_cards if not e.is_X_evade]
        fixed_healths = [resolve_health(e) for e in enemy_cards if not e.is_X_health]

        return {
            "trait_count": self.get_encounter_traits_count(enemy_cards),
            "enemy_count": no_of_enemy_cards,
            "max_enemy_health": max(fixed_healths),
            "max_enemy_fight": max(fixed_fights),
            "max_enemy_evade": max(fixed_evades),
            "max_enemy_horror": max(enemy.horror for enemy in enemy_cards),
            "max_enemy_damage": max(enemy.damage for enemy in enemy_cards),
            "min_enemy_health": min(fixed_healths),
            "min_enemy_fight": min(fixed_fights),
            "min_enemy_evade": min(fixed_evades),
            "min_enemy_horror": min(enemy.horror for enemy in enemy_cards),
            "min_enemy_damage": min(enemy.damage for enemy in enemy_cards),
            "average_enemy_health": sum(fixed_healths) / no_of_enemy_cards,
            "average_enemy_fight": sum(fixed_fights) / no_of_enemy_cards,
            "average_enemy_evade": sum(fixed_evades) / no_of_enemy_cards,
            "average_enemy_horror": sum(enemy.horror for enemy in enemy_cards)
            / no_of_enemy_cards,
            "average_enemy_damage": sum(enemy.damage for enemy in enemy_cards)
            / no_of_enemy_cards,
            "enemies_with_dynamic_fight": sum(1 for e in enemy_cards if e.is_X_fight),
            "enemies_with_dynamic_evade": sum(1 for e in enemy_cards if e.is_X_evade),
            "enemies_without_fight": sum(1 for e in enemy_cards if not e.fightable),
            "enemies_without_evade": sum(1 for e in enemy_cards if not e.evadeable),
            "enemies_without_health": sum(1 for e in enemy_cards if not e.defeatable),
        }

    def calculate_chaos_bag_stats(
        self, chaos_bag: ChaosBag, investigator_card=None
    ) -> Dict[str, Any]:
        """Calculate detailed chaos bag statistics and success probability analysis

        Args:
            chaos_bag: The chaos bag containing tokens
            investigator_card: Optional investigator card for resolving Elder Sign effects
        """
        print("chaos_bag", chaos_bag.tokens)
        if not chaos_bag or not chaos_bag.tokens:
            return {
                "total_tokens": 0,
                "token_distribution": {},
                "numeric_tokens": {},
                "special_tokens": {},
                "success_probabilities": {},
                "modifier_suggestions": {},
                "special_token_effects": [],
                "calculable_tokens": 0,
                "excluded_tokens": {"elder_sign_count": 0, "auto_fail_count": 0},
            }

        # Initialize counters
        token_distribution = {}
        numeric_tokens = []  # Only tokens that can be used in base statistics
        all_numeric_tokens = []  # All tokens for complete analysis
        special_tokens = {}
        special_token_effects = []
        elder_sign_count = 0
        auto_fail_count = 0

        total_tokens = len(chaos_bag.tokens)

        for token in chaos_bag.tokens:
            token_name = token.__class__.__name__.lower().replace("token", "")
            token_distribution[token_name] = token_distribution.get(token_name, 0) + 1

            # Handle ElderSignToken specially
            if token_name == "eldersign":
                elder_sign_count += 1
                # Only include in calculations if investigator context is available
                if investigator_card and hasattr(
                    investigator_card, "elder_sign_effect"
                ):
                    elder_sign_value = investigator_card.elder_sign_effect
                    numeric_tokens.append(elder_sign_value)
                    all_numeric_tokens.append(elder_sign_value)
                else:
                    # Skip from base statistics but track in all_numeric for distribution
                    all_numeric_tokens.append(
                        0
                    )  # Placeholder for distribution analysis
                special_token_effects.append(
                    {
                        "token_type": token_name,
                        "effect": (
                            "Varies by investigator"
                            if not investigator_card
                            else getattr(
                                investigator_card, "elder_sign_text", "Special ability"
                            )
                        ),
                        "value": (
                            "Variable"
                            if not investigator_card
                            else getattr(investigator_card, "elder_sign_effect", 0)
                        ),
                        "count": token_distribution[token_name],
                    }
                )
                continue

            # Handle AutoFailToken specially
            if token_name == "autofail":
                auto_fail_count += 1
                # Never include auto-fail in numeric calculations as it always fails
                all_numeric_tokens.append(-999)  # For distribution analysis only
                special_token_effects.append(
                    {
                        "token_type": token_name,
                        "effect": "Automatic failure regardless of skill value",
                        "value": "Auto-fail",
                        "count": token_distribution[token_name],
                    }
                )
                continue

            # Handle standard numeric tokens
            if hasattr(token, "value") and isinstance(token.value, (int, float)):
                numeric_tokens.append(token.value)
                all_numeric_tokens.append(token.value)

            # Handle special tokens with effects
            if hasattr(token, "effect") and token.effect:
                special_token_effects.append(
                    {
                        "token_type": token_name,
                        "effect": token.effect,
                        "value": getattr(token, "value", "Variable"),
                        "count": token_distribution[token_name],
                    }
                )

            # Count special tokens
            if token_name in [
                "skull",
                "cultist",
                "tablet",
                "elderthing",
                "autofail",
                "eldersign",
            ]:
                special_tokens[token_name] = special_tokens.get(token_name, 0) + 1

        # Calculate success probabilities for different skill test difficulties
        success_probabilities = {}
        modifier_suggestions = {}

        # Common skill test targets (skill value + modifier needed for 50%, 60%, 70% success)
        target_success_rates = [0.5, 0.6, 0.7, 0.8]

        for target_rate in target_success_rates:
            success_probabilities[f"{int(target_rate*100)}%_success"] = {}
            modifier_suggestions[f"{int(target_rate*100)}%_success"] = {}

            # Calculate for different base skill values (2-6 are common)
            for skill_value in range(2, 7):
                # Find what test difficulty would give target success rate
                required_successes = int(total_tokens * target_rate)

                # Sort tokens to find the threshold
                sorted_tokens = sorted(numeric_tokens, reverse=True)

                if len(sorted_tokens) >= required_successes:
                    threshold_value = sorted_tokens[required_successes - 1]
                    needed_test_value = skill_value + threshold_value

                    success_probabilities[f"{int(target_rate*100)}%_success"][
                        f"skill_{skill_value}"
                    ] = {
                        "test_difficulty": max(0, -threshold_value + skill_value),
                        "actual_success_rate": self._calculate_exact_success_rate(
                            numeric_tokens,
                            skill_value,
                            max(0, -threshold_value + skill_value),
                        ),
                    }

                    # Suggest modifier needed for this success rate at different test difficulties
                    for test_difficulty in [2, 3, 4, 5]:
                        needed_modifier = self._calculate_needed_modifier(
                            numeric_tokens, skill_value, test_difficulty, target_rate
                        )
                        if needed_modifier is not None:
                            modifier_suggestions[f"{int(target_rate*100)}%_success"][
                                f"skill_{skill_value}_test_{test_difficulty}"
                            ] = needed_modifier

        # Calculate basic statistics
        avg_modifier = (
            sum(numeric_tokens) / len(numeric_tokens) if numeric_tokens else 0
        )
        positive_tokens = len([t for t in numeric_tokens if t > 0])
        negative_tokens = len([t for t in numeric_tokens if t < 0])
        zero_tokens = len([t for t in numeric_tokens if t == 0])

        return {
            "total_tokens": total_tokens,
            "calculable_tokens": len(
                numeric_tokens
            ),  # Only tokens used in base statistics
            "excluded_tokens": {
                "elder_sign_count": elder_sign_count,
                "auto_fail_count": auto_fail_count,
                "note": "Elder Sign excluded unless investigator context provided; Auto Fail always excluded from calculations",
            },
            "token_distribution": token_distribution,
            "numeric_summary": {
                "average_modifier": round(avg_modifier, 2),
                "positive_tokens": positive_tokens,
                "zero_tokens": zero_tokens,
                "negative_tokens": negative_tokens,
                "most_common_value": (
                    max(set(numeric_tokens), key=numeric_tokens.count)
                    if numeric_tokens
                    else 0
                ),
                "worst_token": min(numeric_tokens) if numeric_tokens else 0,
                "best_token": max(numeric_tokens) if numeric_tokens else 0,
                "calculation_note": f"Based on {len(numeric_tokens)} calculable tokens out of {total_tokens} total tokens",
            },
            "special_tokens": special_tokens,
            "success_probabilities": success_probabilities,
            "modifier_suggestions": modifier_suggestions,
            "special_token_effects": special_token_effects,
            "chaos_hostility": self._calculate_hostility_score(
                numeric_tokens, special_tokens
            ),
        }

    def _calculate_exact_success_rate(
        self,
        numeric_tokens: List[Union[int, float]],
        skill_value: int,
        test_difficulty: int,
    ) -> float:
        """Calculate exact success rate for a given skill test"""
        if not numeric_tokens:
            return 0.0

        successful_tokens = 0
        total_tokens = len(numeric_tokens)

        for token_value in numeric_tokens:
            if skill_value + token_value >= test_difficulty:
                successful_tokens += 1

        return round(successful_tokens / total_tokens, 3)

    def _calculate_needed_modifier(
        self,
        numeric_tokens: List[Union[int, float]],
        skill_value: int,
        test_difficulty: int,
        target_success_rate: float,
    ) -> Optional[int]:
        """Calculate what modifier is needed to achieve target success rate"""
        if not numeric_tokens:
            return None

        total_tokens = len(numeric_tokens)
        target_successes = int(total_tokens * target_success_rate)

        # Try different modifiers from -3 to +6
        for modifier in range(-3, 7):
            successful_tokens = 0
            effective_skill = skill_value + modifier

            for token_value in numeric_tokens:
                if effective_skill + token_value >= test_difficulty:
                    successful_tokens += 1

            if successful_tokens >= target_successes:
                return modifier

        return None  # No reasonable modifier can achieve this success rate

    def _calculate_hostility_score(
        self, numeric_tokens: List[Union[int, float]], special_tokens: Dict[str, int]
    ) -> float:
        """Calculate a hostility score from 0.0 (friendly) to 1.0 (very hostile)"""
        if not numeric_tokens:
            return 0.5

        # Base hostility from numeric tokens
        avg_modifier = sum(numeric_tokens) / len(numeric_tokens)
        worst_token = min(numeric_tokens)

        # Normalize average (typically ranges from -3 to +1)
        avg_hostility = max(0.0, min(1.0, (-avg_modifier + 1) / 4))

        # Worst token impact
        worst_hostility = max(0.0, min(0.3, (-worst_token - 1) / 10))

        # Special token penalties
        special_hostility = 0.0
        special_hostility += (
            special_tokens.get("autofail", 0) * 0.15
        )  # Auto-fail is very bad
        special_hostility += special_tokens.get("skull", 0) * 0.05
        special_hostility += special_tokens.get("cultist", 0) * 0.05
        special_hostility += special_tokens.get("tablet", 0) * 0.05
        special_hostility += special_tokens.get("elderthing", 0) * 0.05

        return min(1.0, avg_hostility + worst_hostility + special_hostility)

    def calculate_resource_scarcity(
        self, starting_clues: int, player_count: int = 2
    ) -> float:
        """
        Calculate resource scarcity context (0.0 to 1.0)
        Higher values indicate more resource constraints
        """
        base_scarcity = 0.4  # Slightly resource constrained baseline

        # Factor 1: Clues per player ratio
        clues_per_player = starting_clues / player_count
        if clues_per_player < 2:
            clue_scarcity = 0.8
        elif clues_per_player < 3:
            clue_scarcity = 0.6
        elif clues_per_player > 4:
            clue_scarcity = 0.2
        else:
            clue_scarcity = 0.4

        # Factor 2: Difficulty impact on resources
        difficulty_scarcity = self._get_difficulty_resource_modifier()

        # Factor 3: Scenario complexity (more complex = more resource intensive)
        complexity_scarcity = self._get_scenario_complexity_modifier()

        # Weighted combination
        final_scarcity = (
            clue_scarcity * self.resource_weights["clue_availability"]
            + difficulty_scarcity * self.resource_weights["difficulty"]
            + complexity_scarcity * self.resource_weights["scenario_complexity"]
        )

        return max(0.0, min(1.0, final_scarcity))

    def calculate_chaos_hostility(self, chaos_bag: ChaosBag) -> float:
        """
        Calculate chaos bag hostility (0.0 to 1.0)
        Higher values indicate more hostile chaos bag
        """
        total_tokens = len(chaos_bag.tokens)
        if total_tokens == 0:
            return 0.0

        negative_impact = 0
        auto_fail_count = 0
        special_token_penalty = 0

        for token in chaos_bag.tokens:
            # Handle numeric tokens
            if hasattr(token, "value") and isinstance(token.value, (int, float)):
                if token.value < 0:
                    negative_impact += abs(token.value)

            # Handle special tokens
            token_name = token.__class__.__name__.lower()
            if "autofail" in token_name:
                auto_fail_count += 1
            elif any(
                special in token_name
                for special in ["skull", "cultist", "tablet", "elderthing"]
            ):
                special_token_penalty += 2  # Special tokens add uncertainty

        # Calculate hostility components
        numeric_hostility = min(1.0, negative_impact / (total_tokens * 3))  # Normalize
        auto_fail_hostility = min(0.3, auto_fail_count * 0.15)  # Auto-fail cap
        special_hostility = min(
            0.4, special_token_penalty / total_tokens
        )  # Special token impact

        return min(1.0, numeric_hostility + auto_fail_hostility + special_hostility)

    def calculate_encounter_difficulty(self) -> float:
        """
        Calculate overall encounter difficulty (0.0 to 1.0)
        Based on scenario and difficulty combination
        """
        # Base difficulty from difficulty setting
        difficulty_base = {
            Difficulty.EASY: 0.2,
            Difficulty.STANDARD: 0.4,
            Difficulty.HARD: 0.7,
            Difficulty.EXPERT: 0.9,
        }.get(self.difficulty, 0.4)

        # Scenario-specific difficulty modifiers
        scenario_modifier = self._get_scenario_difficulty_modifier()

        return max(0.0, min(1.0, difficulty_base + scenario_modifier))

    def calculate_full_context(
        self,
        doom_threshold: int,
        starting_clues: int,
        agenda_rate: float,
        chaos_bag: ChaosBag,
        player_count,
        investigator_card=None,
    ) -> Dict[str, Any]:
        """Calculate comprehensive scenario context

        Args:
            doom_threshold: Maximum doom before defeat
            starting_clues: Initial clues in scenario
            agenda_rate: Rate of doom accumulation
            chaos_bag: The chaos bag containing tokens
            player_count: Number of players
            investigator_card: Optional investigator card for resolving Elder Sign effects
        """
        return {
            "time_pressure": self.calculate_time_pressure(
                doom_threshold, agenda_rate, player_count
            ),
            # "resource_scarcity": self.calculate_resource_scarcity(
            #     starting_clues, player_count
            # ),
            "encounter_wide_stats": self.calculate_encounter_wide_stats(),  # Shared fields like victory, doom
            "enemy_stats": self.calcualte_enemy_stats(),
            "treachery_stats": self.calculate_treachery_stats(),
            "location_stats": self.calculate_location_stats(),
            # "encounter_traits": self.get_encounter_traits_count(),  # Now in encounter_wide_stats
            "chaos_bag_stats": self.calculate_chaos_bag_stats(
                chaos_bag, investigator_card
            ),  # Detailed chaos bag analysis with investigator context
            "encounter_difficulty": self.calculate_encounter_difficulty(),
            "doom_threshold": float(doom_threshold),
            "starting_clues": float(starting_clues),
            "agenda_rate": agenda_rate,
            "player_count": float(player_count),
        }

    def _get_scenario_speed_modifier(self) -> float:
        """Get scenario-specific speed pressure modifier"""
        # Fast-paced scenarios with time pressure
        fast_scenarios = {
            ScenarioType.THE_MIDNIGHT_MASKS,  # Time pressure mechanics
            ScenarioType.THE_DEVOURER_BELOW,  # Accelerated doom
            ScenarioType.THE_ESSEX_COUNTRY_EXPRESS,  # Moving train
        }

        # Slow-paced scenarios with more time
        slow_scenarios = {
            ScenarioType.THE_GATHERING,  # Tutorial scenario
            ScenarioType.THE_MISKATONIC_MUSEUM,  # Investigation focused
        }

        if self.scenario_type in fast_scenarios:
            return 0.7
        elif self.scenario_type in slow_scenarios:
            return 0.2
        else:
            return 0.4  # Standard pace

    def _get_difficulty_time_modifier(self) -> float:
        """Get difficulty-based time pressure modifier"""
        return {
            Difficulty.EASY: 0.2,
            Difficulty.STANDARD: 0.4,
            Difficulty.HARD: 0.6,
            Difficulty.EXPERT: 0.8,
        }.get(self.difficulty, 0.4)

    def _get_difficulty_resource_modifier(self) -> float:
        """Get difficulty-based resource scarcity modifier"""
        return {
            Difficulty.EASY: 0.1,
            Difficulty.STANDARD: 0.3,
            Difficulty.HARD: 0.6,
            Difficulty.EXPERT: 0.8,
        }.get(self.difficulty, 0.3)

    def _get_scenario_complexity_modifier(self) -> float:
        """Get scenario complexity modifier for resource requirements"""
        # Complex scenarios require more resources/actions
        complex_scenarios = {
            ScenarioType.THE_PALLID_MASK,  # Multiple locations, complex mechanics
            ScenarioType.DIM_CARCOSA,  # Final scenario complexity
            ScenarioType.SHATTERED_AEONS,  # Time manipulation mechanics
        }

        # Simple scenarios are more straightforward
        simple_scenarios = {
            ScenarioType.THE_GATHERING,  # Tutorial
            ScenarioType.THE_DEVOURER_BELOW,  # Direct boss fight
        }

        if self.scenario_type in complex_scenarios:
            return 0.7
        elif self.scenario_type in simple_scenarios:
            return 0.2
        else:
            return 0.4

    def _get_scenario_difficulty_modifier(self) -> float:
        """Get scenario-specific difficulty modifier"""
        # Inherently harder scenarios regardless of difficulty setting
        hard_scenarios = {
            ScenarioType.DIM_CARCOSA,
            ScenarioType.BEFORE_THE_BLACK_THRONE,
            ScenarioType.SHATTERED_AEONS,
        }

        # Easier scenarios
        easy_scenarios = {
            ScenarioType.THE_GATHERING,
            ScenarioType.EXTRACURRICULAR_ACTIVITY,
        }

        if self.scenario_type in hard_scenarios:
            return 0.2
        elif self.scenario_type in easy_scenarios:
            return -0.2
        else:
            return 0.0
