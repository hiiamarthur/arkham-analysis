from typing import Dict

from typing import Tuple


class BaseEvaluator:
    """
    A basic evaluator that calculates strength based on weighted sum.
    """

    WEIGHTS = {
        "action": 2.0,
        "card": 2.0,
        "damage": 2.5,
        "clue": 2.5,
        "icon": 1.0,
        "horror": 1.5,
        "health": 1.5,
        "use": -1.0,
        "move": 2.0,
        "doom": -9.0,
        "fast": 2.0,
        "reaction": 2.0,
        "exhaust": -0.5,
        "blessed": 1.5,
        "cursed": -1.5,
        "sealed": -2.5,
        "encounter": -3.0,
        "enemy": -3.0,
        "xp": 15.0,
    }

    AXIOMS = {
        "general_constants": {
            "actions_per_turn": 3,
            "resource_per_turn": 1,
            "card_per_turn": 1,
            "starting_hand": 5,
            "starting_resources": 5,
            "average_scenario_rounds": 12,
            "average_deck_size": 30,
        },
        "enemy_axioms": {
            "average_enemy_health": 3,
            "elite_enemy_health": 5,
            "encounter_card_draws_per_turn": 1,
            "encounter_action_cost": 1.5,
        },
        "investigator_roles": {
            "guardian": {"damage": 1.3, "health": 1.2},
            "seeker": {"clues": 1.3, "cards": 1.2},
            "rogue": {"resources": 1.3, "agility": 1.2},
            "mystic": {"willpower": 1.3, "charges": 1.2},
            "survivor": {"recursion": 1.3, "fail_effects": 1.2},
        },
        "card_type_tendencies": {
            "asset": "long_term",
            "event": "single_use",
            "skill": "single_test",
        },
        "resource_weights": {
            "action": 2.0,
            "card": 2.0,
            "damage": 2.5,
            "clue": 2.5,
            "icon": 1.0,
            "horror": 1.5,
            "health": 1.5,
            "use": 2.0,
            "move": 2.0,
            "doom": -9.0,
            "fast": 2.0,
            "reaction": 2.0,
            "exhaust": -0.5,
            "blessed": 1.5,
            "cursed": -1.5,
            "sealed": -2.5,
            "encounter": -3.0,
            "enemy": -3.0,
            "xp": 15.0,
        },
    }

    def evaluate_card(
        self,
        effects: Dict[str, float],
        weights: Dict[str, float],
        trigger_probs: Dict[str, float],
        pass_probs: Dict[str, float],
        investigator_scaling: Dict[str, float],
        synergy_range: Tuple[float, float],
        scenario_weight: float = 1.0,
    ) -> Tuple[float, float]:
        """
        Returns (low_estimate, high_estimate)
        """
        total_base = 0
        for effect, quantity in effects.items():
            weight = float(weights.get(effect, 0))
            trigger_prob = float(trigger_probs.get(effect, 1.0))
            pass_prob = float(pass_probs.get(effect, 1.0))
            scaling = float(investigator_scaling.get(effect, 1.0))

            effect_value = float(quantity) * weight * trigger_prob * pass_prob * scaling
            total_base += effect_value

        low, high = synergy_range
        final_low = total_base * low * scenario_weight
        final_high = total_base * high * scenario_weight

        return final_low, final_high

    # def evaluate(self, card_data):
    #     score = 0.0
    #     for attr, weight in self.WEIGHTS.items():
    #         value = getattr(card_data, attr, None)
    #         if value is not None:
    #             score += value * weight
    #     return round(score, 2)
