from abc import abstractmethod
from typing import List, Optional
from scoring_model.Card import ActivationType, CardType
from scoring_model.Card.base_card import BaseCard
from scoring_model.evaluators.base_evalutor import BaseEvaluator


class PlayerCard(BaseCard):
    def __init__(
        self,
        code: str,
        name: str,
        card_type: CardType,
        traits: List[str],
        text: str,
        cost: int,
        level: int = 0,
        skill_willpower: int = 0,
        skill_intellect: int = 0,
        skill_combat: int = 0,
        skill_agility: int = 0,
        skill_wild: int = 0,
        play_action_cost: int = 1,
        is_unique: bool = False,
        is_permanent: bool = False,
        is_exceptional: bool = False,
        activation_type: ActivationType = ActivationType.ACTION,
    ):
        super().__init__(
            code,
            name,
            card_type,
            traits,
            text,
            cost,
            skill_willpower,
            skill_intellect,
            skill_combat,
            skill_agility,
            play_action_cost,
            is_unique,
            is_permanent,
        )
        self.level = level
        self.activation_type = activation_type
        self.skill_wild = skill_wild
        if is_exceptional:
            self.level *= 2

    @abstractmethod
    def calculate_cost(self) -> float:
        """Calculate the cost of the card"""
        return (
            self.play_action_cost * BaseEvaluator.WEIGHTS["action"]
            + self.cost
            + self.level * BaseEvaluator.WEIGHTS["xp"]
        )

    @abstractmethod
    def calculate_gain(self) -> float:
        """Calculate the gain of the card"""
        return (
            self.skill_agility
            + self.skill_combat
            + self.skill_intellect
            + self.skill_willpower
            + self.skill_wild
        ) * BaseEvaluator.WEIGHTS["icon"]

    def apply_taboo(self) -> "BaseCard":
        base_card = super().apply_taboo()
        """Apply taboo modifications to player cards"""
        if self.taboo:
            if self.taboo.text:
                self.text += f"\n\n{self.taboo.text}"
            if self.taboo.xp is not None:
                self.level += self.taboo.xp
        return self
