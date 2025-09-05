"""
Base Rule Classes - Building blocks for scenario mechanics
"""

import random
from typing import Dict, List, Any, Callable, Optional
from abc import ABC, abstractmethod


class ScenarioRule(ABC):
    """Base class for all scenario rules"""

    @abstractmethod
    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Apply this rule to the scenario context"""
        pass

    def __str__(self) -> str:
        return f"{self.__class__.__name__}"


class RandomEncounterSetRule(ScenarioRule):
    """Randomly choose encounter sets from options"""

    def __init__(
        self, encounter_sets: List[str], count: int = 1, seed: Optional[int] = None
    ):
        self.encounter_sets = encounter_sets
        self.count = count
        self.seed = seed

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if self.seed:
            random.seed(self.seed)

        chosen = random.sample(
            self.encounter_sets, min(self.count, len(self.encounter_sets))
        )
        context.setdefault("active_encounter_sets", []).extend(chosen)
        context.setdefault("removed_encounter_sets", []).extend(
            [s for s in self.encounter_sets if s not in chosen]
        )
        context.setdefault("random_selections", []).append(
            {
                "rule": "encounter_sets",
                "options": self.encounter_sets,
                "chosen": chosen,
            }
        )
        return context


class ConditionalLocationRule(ScenarioRule):
    """Remove/add locations based on conditions"""

    def __init__(
        self, locations: List[str], condition: Callable, action: str = "remove"
    ):
        self.locations = locations
        self.condition = condition
        self.action = action  # "remove" or "add"

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if self.condition(context):
            if self.action == "remove":
                context.setdefault("removed_locations", []).extend(self.locations)
            elif self.action == "add":
                context.setdefault("additional_locations", []).extend(self.locations)
        return context


class DynamicValueRule(ScenarioRule):
    """Calculate values dynamically based on context"""

    def __init__(self, field: str, calculator: Callable[[Dict[str, Any]], Any]):
        self.field = field
        self.calculator = calculator

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context[self.field] = self.calculator(context)
        return context


class PlayerCountScalingRule(ScenarioRule):
    """Scale values based on player count"""

    def __init__(
        self, field: str, base_value: int, per_player: int = 1, min_players: int = 1
    ):
        self.field = field
        self.base_value = base_value
        self.per_player = per_player
        self.min_players = min_players

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        player_count = context.get("player_count", 2)
        scaling = max(0, player_count - self.min_players)
        context[self.field] = self.base_value + (self.per_player * scaling)
        return context


class ChaosTokenModificationRule(ScenarioRule):
    """Modify chaos tokens based on scenario"""

    def __init__(self, token_modifications: Dict[str, Dict[tuple[str, str], Any]]):
        self.token_modifications = token_modifications

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context.setdefault("chaos_modifications", {}).update(self.token_modifications)
        return context


class TimeBasedRule(ScenarioRule):
    """Handle time-based mechanics (round limits, etc.)"""

    def __init__(self, rounds_limit: Optional[int] = None, doom_per_round: float = 1.0):
        self.rounds_limit = rounds_limit
        self.doom_per_round = doom_per_round

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        if self.rounds_limit:
            context["rounds_limit"] = self.rounds_limit
            context["time_pressure"] = True

        if self.doom_per_round != 1.0:
            context["agenda_rate"] = self.doom_per_round

        return context


class LocationSetupRule(ScenarioRule):
    """Handle complex location setup"""

    def __init__(
        self,
        required_locations: List[str],
        optional_locations: List[str] = [],
        selection_count: int = 0,
    ):
        self.required_locations = required_locations
        self.optional_locations = optional_locations or []
        self.selection_count = selection_count

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        context.setdefault("required_locations", []).extend(self.required_locations)

        if self.optional_locations and self.selection_count > 0:
            selected = random.sample(
                self.optional_locations,
                min(self.selection_count, len(self.optional_locations)),
            )
            context.setdefault("selected_locations", []).extend(selected)
            context.setdefault("unused_locations", []).extend(
                [loc for loc in self.optional_locations if loc not in selected]
            )

        return context


class InvestigatorDependentRule(ScenarioRule):
    """Rules that depend on investigator composition"""

    def __init__(self, investigator_effects: Dict[str, Dict[str, Any]]):
        self.investigator_effects = investigator_effects

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        # This would need investigator info passed in context
        investigators = context.get("investigators", [])

        for investigator in investigators:
            if investigator in self.investigator_effects:
                effects = self.investigator_effects[investigator]
                context.setdefault("investigator_effects", {}).update(effects)

        return context


class ProgressiveRule(ScenarioRule):
    """Rules that change based on scenario progress"""

    def __init__(self, progression_stages: Dict[str, Dict[str, Any]]):
        self.progression_stages = progression_stages

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        current_stage = context.get("progression_stage", "initial")

        if current_stage in self.progression_stages:
            stage_effects = self.progression_stages[current_stage]
            context.update(stage_effects)

        return context


class ResolutionDependentRule(ScenarioRule):
    """Rules that depend on previous scenario resolutions"""

    def __init__(self, resolution_effects: Dict[str, Dict[str, Any]]):
        self.resolution_effects = resolution_effects

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        previous_resolutions = context.get("previous_resolutions", [])

        for resolution in previous_resolutions:
            if resolution in self.resolution_effects:
                effects = self.resolution_effects[resolution]
                context.update(effects)

        return context


class WeaknessRule(ScenarioRule):
    """Handle basic weakness interactions"""

    def __init__(self, weakness_count: int = 1):
        self.weakness_count = weakness_count

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        player_count = context.get("player_count", 2)
        total_weaknesses = self.weakness_count * player_count
        context["expected_weaknesses"] = total_weaknesses
        return context


class DifficultyScalingRule(ScenarioRule):
    """Scale scenario elements based on difficulty"""

    def __init__(self, scaling_factors: Dict[str, Dict[str, float]]):
        self.scaling_factors = scaling_factors

    def apply(self, context: Dict[str, Any]) -> Dict[str, Any]:
        difficulty = context.get("difficulty")
        if not difficulty:
            return context

        difficulty_key = (
            difficulty.value if hasattr(difficulty, "value") else str(difficulty)
        )

        if difficulty_key in self.scaling_factors:
            factors = self.scaling_factors[difficulty_key]
            for field, multiplier in factors.items():
                if field in context and isinstance(context[field], (int, float)):
                    context[field] = int(context[field] * multiplier)

        return context
