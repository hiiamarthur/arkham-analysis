from typing import Dict

from ..Token.chaos_bag import ChaosBag

from .campaign import Campaign, CampaignType
from ..difficulty import Difficulty
from ..Token import (
    ChaosToken,
    CultistToken,
    ElderSignToken,
    AutoFailToken,
    PlusOneToken,
    SkullToken,
    TabletToken,
    ZeroToken,
    MinusOneToken,
    MinusTwoToken,
    MinusThreeToken,
    MinusFourToken,
    MinusFiveToken,
    MinusEightToken,
)
from typing import Type


class NightOfTheZealot(Campaign):

    def __init__(self, difficulty: Difficulty):
        self.base_token_config: Dict[Type[ChaosToken], int] = {
            ElderSignToken: 1,
            AutoFailToken: 1,
            SkullToken: 2,
            CultistToken: 1,
            TabletToken: 1,
        }
        super().__init__(
            CampaignType.NIGHT_OF_THE_ZEALOT, difficulty, self.base_token_config
        )
        self.token_configs = {
            Difficulty.EASY: {
                PlusOneToken: 2,
                ZeroToken: 3,
                MinusOneToken: 3,
                MinusTwoToken: 2,
            },
            Difficulty.STANDARD: {
                PlusOneToken: 1,
                ZeroToken: 2,
                MinusOneToken: 3,
                MinusTwoToken: 2,
                MinusThreeToken: 1,
                MinusFourToken: 1,
            },
            Difficulty.HARD: {
                ZeroToken: 3,
                MinusOneToken: 2,
                MinusTwoToken: 2,
                MinusThreeToken: 2,
                MinusFourToken: 1,
            },
            Difficulty.EXPERT: {
                ZeroToken: 1,
                MinusOneToken: 2,
                MinusTwoToken: 2,
                MinusThreeToken: 3,
                MinusFourToken: 4,
                MinusFiveToken: 1,
                MinusEightToken: 1,
            },
        }
        self.chaos_bag = ChaosBag(self.get_init_tokens(difficulty))

    def get_token_config(self) -> Dict[Difficulty, Dict[Type[ChaosToken], int]]:
        """Return the token configuration for Night of the Zealot."""
        return self.token_configs
