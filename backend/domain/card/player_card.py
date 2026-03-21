from abc import abstractmethod
from dataclasses import dataclass, field
from typing import Dict, List, Optional
from .faction import Faction
from ..models import TabooData
from .activation_type import ActivationType
from .card_cost_factor import CardCostFactor
from .card_type import CardType
from .base_card import BaseCard
import re


@dataclass
class PlayerCard(BaseCard):
    real_text: Optional[str] = None
    cost: int = 0
    level: int = 0
    skill_willpower: int = 0
    skill_intellect: int = 0
    skill_combat: int = 0
    skill_agility: int = 0
    skill_wild: int = 0
    play_action_cost: int = 1
    is_unique: bool = False
    is_permanent: bool = False
    is_exceptional: bool = False
    activation_type: ActivationType = ActivationType.ACTION
    cost_factors: Dict[CardCostFactor, float] = field(
        default_factory=lambda: {
            CardCostFactor.ACTION: 1,
            CardCostFactor.RESOURCE: 1,
            CardCostFactor.ICON: 1,
            CardCostFactor.XP: 1,
        }
    )
    taboo: Optional[TabooData] = None

    def __post_init__(self):
        # apply exceptional XP doubling
        if self.is_exceptional:
            self.level *= 2

    # def __init__(
    #     self,
    #     code: str,
    #     name: str,
    #     card_type: CardType,
    #     traits: List[str],
    #     faction: Faction,
    #     text: str,
    #     cost: int,
    #     level: int = 0,
    #     skill_willpower: int = 0,
    #     skill_intellect: int = 0,
    #     skill_combat: int = 0,
    #     skill_agility: int = 0,
    #     skill_wild: int = 0,
    #     play_action_cost: int = 1,
    #     is_unique: bool = False,
    #     is_permanent: bool = False,
    #     is_exceptional: bool = False,
    #     activation_type: ActivationType = ActivationType.ACTION,
    #     cost_factors: Dict[CardCostFactor, float] = {
    #         CardCostFactor.ACTION: 1,
    #         CardCostFactor.RESOURCE: 1,
    #         CardCostFactor.ICON: 1,
    #         CardCostFactor.XP: 1,
    #     },
    #     taboo: Optional[TabooData] = None,
    # ):
    #     super().__init__(
    #         code,
    #         name,
    #         card_type,
    #         traits,
    #         faction,
    #         text,
    #         "",
    #         # cost,
    #         # skill_willpower,
    #         # skill_intellect,
    #         # skill_combat,
    #         # skill_agility,
    #         # play_action_cost,
    #         # is_unique,
    #         # is_permanent,
    #     )
    #     self.cost = cost
    #     self.skill_willpower = skill_willpower
    #     self.skill_intellect = skill_intellect
    #     self.skill_combat = skill_combat
    #     self.skill_agility = skill_agility
    #     self.play_action_cost = play_action_cost
    #     self.is_unique = is_unique
    #     self.is_permanent = is_permanent

    #     self.taboo = taboo
    #     self.level = level
    #     self.activation_type = activation_type
    #     self.skill_wild = skill_wild
    #     self.cost_factors = cost_factors
    #     if is_exceptional:
    #         self.level *= 2

    # Scoring methods moved to scoring model layer
    # The domain should not contain scoring/evaluation logic

    def apply_taboo(self) -> "BaseCard":
        base_card = super().apply_taboo()
        """Apply taboo modifications to player cards"""
        if self.taboo:
            if self.taboo.text:
                self.text += f"\n\n{self.taboo.text}"
            if self.taboo.xp is not None:
                self.level += self.taboo.xp
        return self

    def analyze_effect_text(self, text: str) -> Dict:
        text = text.lower()

        result = {
            "requires_test": False,
            "requires_pass": False,
            "fail_to_win": False,
            "test_type": None,  # e.g., "combat", "willpower"
            "parser_pass_condition": "",
            "parser_trigger_condition": "",
        }

        # Identify skill test requirement
        if any(
            keyword in text for keyword in ["fight.", "evade.", "investigate.", "test "]
        ):
            result["requires_test"] = True

        # Identify if effect is conditional on success
        if re.search(
            r"\bif you succeed\b|\bif successful\b|\bwhen you succeed\b", text
        ):
            result["requires_pass"] = True
            result["parser_pass_condition"] = "must pass skill test"

        # Fail-to-win detection
        if re.search(r"\bif you fail\b|\bafter you fail\b", text):
            result["requires_test"] = True
            result["requires_pass"] = True  # but we treat as 1 - P(pass)
            result["fail_to_win"] = True
            result["parser_pass_condition"] = "must fail skill test"

        # Detect test type
        if "fight." in text or "test [combat]" in text:
            result["test_type"] = "combat"
        elif "evade." in text or "test [agility]" in text:
            result["test_type"] = "agility"
        elif "investigate." in text or "test [intellect]" in text:
            result["test_type"] = "intellect"
        elif "use [willpower]" in text or "test [willpower]" in text:
            result["test_type"] = "willpower"

        # Trigger window hints (optional extension)
        if "[reaction]" in text:
            result["parser_trigger_condition"] = "reaction window"
        elif "fast." in text:
            result["parser_trigger_condition"] = "fast action"
        elif "after you" in text or "when you" in text or "play when":
            result["parser_trigger_condition"] = "timing trigger"
        elif "forced" in text:
            result["parser_trigger_condition"] = "forced"
        elif "bonded." in text:
            result["parser_trigger_condition"] = "bonded"
        return result
