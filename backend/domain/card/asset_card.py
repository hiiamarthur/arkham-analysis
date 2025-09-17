from dataclasses import dataclass, field
from typing import List, Optional
from .faction import Faction
from .activation_type import ActivationType
from .card_type import CardType
from .player_card import PlayerCard
from .with_health_sanity import WithHealthSanity


@dataclass
class AssetCard(PlayerCard, WithHealthSanity):
    card_type: CardType = CardType.ASSET
    slots: List[str] = field(default_factory=list)
    use: Optional[str] = None

    # def __post_init__(self):
    #     super().__post_init__()
    #     # Override card_type for asset cards
    #     if self.card_type != CardType.ASSET:
    #         object.__setattr__(self, 'card_type', CardType.ASSET)

    # Scoring methods moved to scoring model layer
    # The domain should not contain scoring/evaluation logic
