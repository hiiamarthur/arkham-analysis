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
    MinusSevenToken,
    SkullToken,
    CultistToken,
    TabletToken,
    ElderThingToken,
)
from typing import List


class ForgottenAge(Campaign):

    def __init__(self, difficulty: Difficulty):
        super().__init__(CampaignType.THE_FORGOTTEN_AGE, difficulty)

    def get_init_tokens(self, difficulty: Difficulty) -> List[ChaosToken]:
        # Base tokens that all difficulties have
        base_tokens = [
            ElderSignToken(),
            AutoFailToken(),
            SkullToken("", 0),  # 2 skulls in Forgotten Age
            SkullToken("", 0),
            CultistToken("", 0),
            TabletToken("", 0),
            ElderThingToken("", 0),
        ]

        token_configs = {
            Difficulty.EASY: {
                ZeroToken: 3,
                MinusOneToken: 3,
                MinusTwoToken: 2,
                MinusThreeToken: 2,
                MinusFourToken: 1,
            },
            Difficulty.STANDARD: {
                ZeroToken: 2,
                MinusOneToken: 3,
                MinusTwoToken: 3,
                MinusThreeToken: 2,
                MinusFourToken: 1,
            },
            Difficulty.HARD: {
                ZeroToken: 2,
                MinusOneToken: 2,
                MinusTwoToken: 3,
                MinusThreeToken: 2,
                MinusFourToken: 2,
            },
            Difficulty.EXPERT: {
                ZeroToken: 1,
                MinusOneToken: 2,
                MinusTwoToken: 2,
                MinusThreeToken: 3,
                MinusFourToken: 2,
                MinusFiveToken: 1,
                MinusSevenToken: 1,
            },
        }

        config = token_configs.get(difficulty, {})
        for token_type, count in config.items():
            base_tokens.extend([token_type() for _ in range(count)])

        return base_tokens