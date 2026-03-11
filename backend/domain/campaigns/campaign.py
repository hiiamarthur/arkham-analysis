from abc import ABC, abstractmethod
from .campaign_type import CampaignType
from ..difficulty import Difficulty
from typing import Dict, List, Type

from ..Token import (
    ChaosToken,
    CultistToken,
    ElderSignToken,
    AutoFailToken,
    SkullToken,
    TabletToken,
    ElderThingToken,
)


class Campaign(ABC):
    def __init__(
        self,
        campaign_type: CampaignType,
        difficulty: Difficulty,
        base_tokens_config: Dict[Type[ChaosToken], int],
    ):
        self.campaign_type = campaign_type
        self.difficulty = difficulty
        self.base_tokens = []
        # Initialize base tokens from config
        for token_class, count in base_tokens_config.items():
            if token_class == SkullToken:
                self.base_tokens.extend([SkullToken("", 0) for _ in range(count)])
            elif token_class == CultistToken:
                self.base_tokens.extend([CultistToken("", 0) for _ in range(count)])
            elif token_class == TabletToken:
                self.base_tokens.extend([TabletToken("", 0) for _ in range(count)])
            elif token_class == ElderThingToken:
                self.base_tokens.extend([ElderThingToken("", 0) for _ in range(count)])
            elif token_class == ElderSignToken:
                self.base_tokens.extend([ElderSignToken("", 0) for _ in range(count)])
            elif token_class == AutoFailToken:
                self.base_tokens.extend([AutoFailToken() for _ in range(count)])
            else:
                raise ValueError(f"Unexpected token class: {token_class}")

    def get_init_tokens(self, difficulty: Difficulty) -> List[ChaosToken]:
        """Create the chaos bag tokens for this campaign at the given difficulty."""
        # Start with base tokens (already initialized in parent constructor)
        all_tokens = self.base_tokens.copy()

        # Add difficulty-specific tokens using child class configuration
        config = self.get_token_config().get(difficulty, {})
        for token_class, count in config.items():
            if isinstance(token_class, tuple):
                cls, *args = token_class
                all_tokens.extend([cls(*args) for _ in range(count)])
            else:
                # All numbered tokens should work with no parameters
                all_tokens.extend([token_class() for _ in range(count)])

        return all_tokens

    @abstractmethod
    def get_token_config(self) -> Dict[Difficulty, Dict[Type[ChaosToken], int]]:
        """Return the token configuration for this campaign."""
        pass
