from typing import Dict

from typing import Tuple

from scoring_model.Card import CardEffect


class BaseEvaluator:
    """
    A basic evaluator that calculates strength based on weighted sum.
    """

    WEIGHTS = {
        CardEffect.RESOURCE: 1.0,
        CardEffect.ACTION: 2.0,
        CardEffect.CARD: 2.0,
        CardEffect.DAMAGE: 2.5,
        CardEffect.CLUE: 2.5,
        CardEffect.ICON: 1.0,
        CardEffect.HORROR: 1.5,
        CardEffect.HEALTH: 1.5,
        CardEffect.USE: -1.0,
        CardEffect.MOVE: 2.0,
        CardEffect.DOOM: -9.0,
        CardEffect.FAST: 2.0,
        CardEffect.REACTION: 2.0,
        CardEffect.EXHAUST: -0.5,
        CardEffect.BLESSED: 1.5,
        CardEffect.CURSED: -1.5,
        CardEffect.SEALED: -2.5,
        CardEffect.ENCOUNTER: -3.0,
        CardEffect.ENEMY: -3.0,
        CardEffect.XP: 15.0,
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
        "average_combat_test_difficulty": 3,  # enemy combat etc
        "average_agility_test_difficulty": 3,  # enemy agility etc
        "average_intellect_test_difficulty": 3,  # shread etc
        "average_willpower_test_difficulty": 3,  # treachary etc
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

    def calculate_cost(self, card_data):
        pass

    def evaluate_card_strength(
        self,
        effects: Dict[CardEffect, int],
        trigger_probs,
        pass_probs,
        investigator_scaling,
        synergy_range,
        scenario_weight,
        action_cost,
        resource_cost,
        icons,
        icon_weights,
        icon_need_probs,
    ):
        # Calculate gains
        total_gain = 0
        for effect, quantity in effects.items():
            weight = self.WEIGHTS.get(effect) or 0
            trig_prob = trigger_probs.get(effect, 1.0)
            pass_prob = pass_probs.get(effect, 1.0)
            inv_scale = investigator_scaling.get(effect, 1.0)
            total_gain += quantity * weight * trig_prob * pass_prob * inv_scale

        # Apply synergy and scenario
        low_synergy, high_synergy = synergy_range
        gain_low = total_gain * low_synergy * scenario_weight
        gain_high = total_gain * high_synergy * scenario_weight

        # Calculate costs
        opportunity_cost = sum(
            icons.get(icon, 0)
            * icon_weights.get(icon, 1.0)
            * icon_need_probs.get(icon, 0.5)
            for icon in icons
        )
        total_cost = (action_cost * 2) + resource_cost + opportunity_cost

        # Final values
        final_low = gain_low - total_cost
        final_high = gain_high - total_cost

        return final_low, final_high

    # def evaluate(self, card_data):
    #     score = 0.0
    #     for attr, weight in self.WEIGHTS.items():
    #         value = getattr(card_data, attr, None)
    #         if value is not None:
    #             score += value * weight
    #     return round(score, 2)
