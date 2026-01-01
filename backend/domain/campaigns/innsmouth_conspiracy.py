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
from typing import Dict, List, Type


class InnsmouthConspiracy(Campaign):

    def __init__(self, difficulty: Difficulty):
        self.base_tokens_config = {
            ElderSignToken: 1,
            AutoFailToken: 1,
            SkullToken: 2,
            CultistToken: 2,
            TabletToken: 2,
            ElderThingToken: 2,
        }
        super().__init__(
            CampaignType.THE_INNSMOUTH_CONSPIRACY, difficulty, self.base_tokens_config
        )

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
                ZeroToken: 2,
                MinusOneToken: 3,
                MinusTwoToken: 2,
                MinusThreeToken: 2,
                MinusFourToken: 1,
            },
            Difficulty.HARD: {
                ZeroToken: 1,
                MinusOneToken: 2,
                MinusTwoToken: 3,
                MinusThreeToken: 2,
                MinusFourToken: 2,
            },
            Difficulty.EXPERT: {
                MinusOneToken: 1,
                MinusTwoToken: 2,
                MinusThreeToken: 3,
                MinusFourToken: 2,
                MinusFiveToken: 1,
                MinusSixToken: 1,
            },
        }

    def get_init_tokens(self, difficulty: Difficulty) -> List[ChaosToken]:
        # Base tokens that all difficulties have

        config = self.token_configs.get(difficulty, {})

        for token_type, count in config.items():
            self.base_tokens.extend([token_type() for _ in range(count)])

        return self.base_tokens

    def get_token_config(self) -> Dict[Difficulty, Dict[Type[ChaosToken], int]]:
        return self.token_configs
