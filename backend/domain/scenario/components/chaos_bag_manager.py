"""
Chaos Bag Manager - Handles all chaos bag operations and modifications
Follows SRP by focusing solely on chaos bag management
"""

from typing import Dict, List, Any, Optional
import random
import statistics
from collections import Counter

# Import from parent domain structure
import sys
import os

backend_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", ".."
)
if backend_path not in sys.path:
    sys.path.append(backend_path)

from domain import ScenarioType, Difficulty, get_scenario_modifications
from domain.Token.chaos_bag import ChaosBag
from domain.Token.token import (
    ChaosToken,
    SkullToken,
    CultistToken,
    TabletToken,
    ElderThingToken,
)


class ChaosBagManager:
    """Manages chaos bag operations, modifications, and simulations"""

    def __init__(
        self, chaos_bag: ChaosBag, scenario_type: ScenarioType, difficulty: Difficulty
    ):
        self.chaos_bag = chaos_bag
        self.scenario_type = scenario_type
        self.difficulty = difficulty
        self._modifications_applied = False
        self._simulation_cache: Optional[Dict[str, Any]] = None

    def apply_scenario_modifications(self) -> None:
        """Apply scenario-specific token modifications to chaos bag"""
        if self._modifications_applied:
            return

        modifications = get_scenario_modifications(self.scenario_type, self.difficulty)
        if modifications:
            self._modify_special_tokens(modifications)

        self._modifications_applied = True
        self._clear_simulation_cache()

    def _modify_special_tokens(self, modifications: Dict[str, Dict[str, Any]]) -> None:
        """Apply modifications to special tokens"""
        for i, token in enumerate(self.chaos_bag.tokens):
            if isinstance(token, SkullToken) and "skull" in modifications:
                skull_data = modifications["skull"]
                self.chaos_bag.tokens[i] = SkullToken(
                    skull_data.get("effect", ""), skull_data.get("value", token.value)
                )
            elif isinstance(token, CultistToken) and "cultist" in modifications:
                cultist_data = modifications["cultist"]
                self.chaos_bag.tokens[i] = CultistToken(
                    cultist_data.get("effect", ""),
                    cultist_data.get("value", token.value),
                )
            elif isinstance(token, TabletToken) and "tablet" in modifications:
                tablet_data = modifications["tablet"]
                self.chaos_bag.tokens[i] = TabletToken(
                    tablet_data.get("effect", ""), tablet_data.get("value", token.value)
                )
            elif isinstance(token, ElderThingToken) and "elder_thing" in modifications:
                elder_data = modifications["elder_thing"]
                self.chaos_bag.tokens[i] = ElderThingToken(
                    elder_data.get("effect", ""), elder_data.get("value", token.value)
                )

    def simulate_draws(self, num_draws: int = 1000) -> Dict[str, Any]:
        """Simulate chaos bag draws and return statistics"""
        if self._simulation_cache and num_draws == 1000:
            return self._simulation_cache

        values = []
        token_counts = Counter()

        for _ in range(num_draws):
            token = random.choice(self.chaos_bag.tokens)
            token_counts[token.__class__.__name__] += 1

            if hasattr(token, "value") and isinstance(token.value, (int, float)):
                values.append(token.value)
            else:
                # Handle special tokens (auto-fail, elder sign, etc.)
                if hasattr(token, "get_numeric_value"):
                    values.append(token.get_numeric_value())
                else:
                    values.append(0)  # Neutral value for unknown tokens

        simulation_results = {
            "num_draws": num_draws,
            "mean_value": statistics.mean(values) if values else 0,
            "median_value": statistics.median(values) if values else 0,
            "std_dev": statistics.stdev(values) if len(values) > 1 else 0,
            "min_value": min(values) if values else 0,
            "max_value": max(values) if values else 0,
            "token_distribution": dict(token_counts),
            "negative_draws": sum(1 for v in values if v < 0),
            "positive_draws": sum(1 for v in values if v > 0),
            "neutral_draws": sum(1 for v in values if v == 0),
        }

        # Cache results for standard simulation size
        if num_draws == 1000:
            self._simulation_cache = simulation_results

        return simulation_results

    def get_expected_value(self) -> float:
        """Calculate theoretical expected value of chaos bag"""
        total_value = 0
        valid_tokens = 0

        for token in self.chaos_bag.tokens:
            if hasattr(token, "value") and isinstance(token.value, (int, float)):
                total_value += token.value
                valid_tokens += 1

        return total_value / valid_tokens if valid_tokens > 0 else 0.0

    def calculate_success_probability(
        self, target_difficulty: int, skill_value: int = 0
    ) -> float:
        """Calculate probability of success for a skill test"""
        successes = 0
        total_tokens = len(self.chaos_bag.tokens)

        for token in self.chaos_bag.tokens:
            if hasattr(token, "value") and isinstance(token.value, (int, float)):
                final_value = skill_value + token.value
                if final_value >= target_difficulty:
                    successes += 1
            # Handle special tokens (would need more complex logic for real implementation)

        return successes / total_tokens if total_tokens > 0 else 0.0

    def get_hostility_rating(self) -> float:
        """Calculate how hostile the chaos bag is (0.0 to 1.0)"""
        total_tokens = len(self.chaos_bag.tokens)
        negative_impact = 0

        for token in self.chaos_bag.tokens:
            if hasattr(token, "value") and isinstance(token.value, (int, float)):
                if token.value < 0:
                    negative_impact += abs(token.value)

        # Normalize based on typical chaos bag composition
        max_possible_negative = total_tokens * 4  # Rough estimate
        return (
            min(1.0, negative_impact / max_possible_negative)
            if max_possible_negative > 0
            else 0.0
        )

    def get_chaos_bag_composition(self) -> Dict[str, int]:
        """Get count of each token type in chaos bag"""
        composition = Counter()

        for token in self.chaos_bag.tokens:
            token_name = token.__class__.__name__.replace("Token", "")
            composition[token_name] += 1

        return dict(composition)

    def _clear_simulation_cache(self) -> None:
        """Clear cached simulation results"""
        self._simulation_cache = None

    def reset_modifications(self) -> None:
        """Reset chaos bag to original state (useful for testing)"""
        self._modifications_applied = False
        self._clear_simulation_cache()
        # Note: This would require storing original chaos bag state
        # Implementation depends on how ChaosBag class handles resets
