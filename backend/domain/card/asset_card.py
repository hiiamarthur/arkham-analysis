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

    @staticmethod
    def has_uses(real_text: str, uses_type: str) -> bool:
        """
        Return True if the card's real_text contains a 'Uses (X <uses_type>).' pattern.
        Matches ArkhamDB's logic: realText LIKE '%<uses_type>).%'
        """
        return f"{uses_type}).".lower() in (real_text or "").lower()

    # def __post_init__(self):
    #     super().__post_init__()
    #     # Override card_type for asset cards
    #     if self.card_type != CardType.ASSET:
    #         object.__setattr__(self, 'card_type', CardType.ASSET)

    # Scoring methods moved to scoring model layer
    # The domain should not contain scoring/evaluation logic
