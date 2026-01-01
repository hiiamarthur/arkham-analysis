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
    FrostToken,
)
from typing import Dict, List, Type


class EdgeOfTheEarth(Campaign):

    def __init__(self, difficulty: Difficulty):
        self.base_tokens_config = {
            ElderSignToken: 1,
            AutoFailToken: 1,
            SkullToken: 2,
            CultistToken: 1,
            TabletToken: 1,
        }
        super().__init__(
            CampaignType.THE_EDGE_OF_THE_EARTH, difficulty, self.base_tokens_config
        )

        self.token_configs = {
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
                MinusTwoToken: 2,
                MinusThreeToken: 2,
                MinusFourToken: 2,
                FrostToken: 1,
            },
            Difficulty.HARD: {
                ZeroToken: 2,
                MinusOneToken: 2,
                MinusTwoToken: 3,
                MinusThreeToken: 1,
                MinusFourToken: 2,
                MinusFiveToken: 1,
                FrostToken: 2,
            },
            Difficulty.EXPERT: {
                ZeroToken: 1,
                MinusOneToken: 1,
                MinusTwoToken: 2,
                MinusThreeToken: 1,
                MinusFourToken: 2,
                MinusFiveToken: 1,
                MinusSevenToken: 1,
                FrostToken: 3,
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
