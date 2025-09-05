from typing import List, Optional
from . import Faction
from . import ActivationType, CardType
from .player_card import PlayerCard
from .with_health_sanity import WithHealthSanity


class AssetCard(PlayerCard, WithHealthSanity):
    def __init__(
        self,
        code: str,
        name: str,
        traits: List[str],
        text: str,
        faction: Faction,
        cost: int,
        level: int = 0,
        skill_willpower: int = 0,
        skill_intellect: int = 0,
        skill_combat: int = 0,
        skill_agility: int = 0,
        skill_wild: int = 0,
        play_action_cost: int = 0,
        slots: Optional[List[str]] = None,
        use: Optional[str] = None,
        health: int = 0,
        sanity: int = 0,
        is_unique: bool = False,
        is_permanent: bool = False,
        is_exceptional: bool = False,
        activation_type: ActivationType = ActivationType.ACTION,
    ):
        PlayerCard.__init__(
            self,
            code,
            name,
            CardType.ASSET,
            traits,
            faction,
            text,
            cost,
            level,
            skill_willpower,
            skill_intellect,
            skill_combat,
            skill_agility,
            skill_wild,
            play_action_cost,
            is_unique,
            is_permanent,
            is_exceptional,
            activation_type,
        )
        WithHealthSanity.__init__(self, health, sanity)
        self.slots = slots or []
        self.use = use

    # Scoring methods moved to scoring model layer
    # The domain should not contain scoring/evaluation logic
