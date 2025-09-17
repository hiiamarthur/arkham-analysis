from .campaign import Campaign, CampaignType
from ..difficulty import Difficulty
from ..Token.token import (
    ChaosToken,
    ElderSignToken,
    AutoFailToken,
    MinusEightToken,
    PlusOneToken,
    ZeroToken,
    MinusOneToken,
    MinusTwoToken,
    MinusThreeToken,
    MinusFourToken,
    MinusFiveToken,
)
from typing import List


class DunwichLegacy(Campaign):

    base_tokens = [
        ElderSignToken(),
        AutoFailToken(),
    ]

    token_configs = {
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

    def __init__(self, difficulty: Difficulty):
        super().__init__(CampaignType.THE_DUNWICH_LEGACY, difficulty)

    def get_init_tokens(self, difficulty: Difficulty) -> List[ChaosToken]:

        config = self.token_configs.get(difficulty, {})
        for token_type, count in config.items():
            self.base_tokens.extend([token_type() for _ in range(count)])

        return self.base_tokens
