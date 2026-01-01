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
    SkullToken,
    CultistToken,
    TabletToken,
)
from typing import Dict, List, Type


class DunwichLegacy(Campaign):

    def __init__(self, difficulty: Difficulty):
        self.base_tokens_config = {
            ElderSignToken: 1,
            AutoFailToken: 1,
            SkullToken: 2,
            CultistToken: 1,
        }
        super().__init__(
            CampaignType.THE_DUNWICH_LEGACY, difficulty, self.base_tokens_config
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

    def get_init_tokens(self, difficulty: Difficulty) -> List[ChaosToken]:

        config = self.token_configs.get(difficulty, {})
        for token_type, count in config.items():
            self.base_tokens.extend([token_type() for _ in range(count)])

        return self.base_tokens

    def get_token_config(self) -> Dict[Difficulty, Dict[Type[ChaosToken], int]]:
        return self.token_configs
