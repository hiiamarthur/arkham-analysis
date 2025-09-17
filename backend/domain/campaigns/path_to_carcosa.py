from .campaign import Campaign, CampaignType
from ..difficulty import Difficulty
from ..Token.token import (
    ChaosToken,
    ElderSignToken,
    AutoFailToken,
    PlusOneToken,
    ZeroToken,
    MinusOneToken,
    MinusTwoToken,
    MinusThreeToken,
    MinusFourToken,
    MinusFiveToken,
    MinusSixToken,
    SkullToken,
    CultistToken,
    TabletToken,
    ElderThingToken,
)
from typing import List


class PathToCarcosa(Campaign):

    def __init__(self, difficulty: Difficulty):
        super().__init__(CampaignType.THE_PATH_TO_CARCOSA, difficulty)

        self.base_tokens = [
            ElderSignToken(),
            AutoFailToken(),
        ]

        self.token_configs = {
            Difficulty.EASY: {
                PlusOneToken: 1,
                ZeroToken: 2,
                MinusOneToken: 3,
                MinusTwoToken: 2,
                MinusThreeToken: 1,
                MinusFourToken: 1,
            },
            Difficulty.STANDARD: {
                ZeroToken: 1,
                MinusOneToken: 3,
                MinusTwoToken: 2,
                MinusThreeToken: 2,
                MinusFourToken: 1,
            },
            Difficulty.HARD: {
                MinusOneToken: 2,
                MinusTwoToken: 3,
                MinusThreeToken: 2,
                MinusFourToken: 2,
            },
            Difficulty.EXPERT: {
                MinusOneToken: 1,
                MinusTwoToken: 2,
                MinusThreeToken: 2,
                MinusFourToken: 2,
                MinusFiveToken: 1,
                MinusSixToken: 1,
            },
        }

    def get_init_tokens(self, difficulty: Difficulty) -> List[ChaosToken]:

        config = self.token_configs.get(difficulty, {})
        for token_type, count in config.items():
            self.base_tokens.extend([token_type() for _ in range(count)])

        return self.base_tokens
