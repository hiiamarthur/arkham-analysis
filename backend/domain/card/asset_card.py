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

    # Scoring methods moved to scoring model layer
    # The domain should not contain scoring/evaluation logic
