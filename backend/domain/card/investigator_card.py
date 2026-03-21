from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple
import re

from .faction import Faction
from .card_type import CardType
from .base_card import BaseCard
from .with_health_sanity import WithHealthSanity

# Keys that are deckbuilding count constraints, not pool membership criteria
_NOISE_KEYS = {"limit", "error", "atleast", "deck_size_select", "ignore_match",
               "size", "name", "id", "base_level"}
# Keys that act as positive card selectors
_SELECTOR_KEYS = {"faction", "trait", "type", "uses", "tag", "text"}


@dataclass
class InvestigatorCard(BaseCard, WithHealthSanity):
    deck_limit: Dict[str, Any] = field(default_factory=dict)
    card_type: CardType = CardType.INVESTIGATOR
    play_action_cost: int = 0
    is_unique: bool = True
    is_permanent: bool = True
    deck_options: Optional[List[Dict[str, Any]]] = field(default_factory=list)

    def expand_pool_rules(self) -> Tuple[List[Dict], List[Dict]]:
        """
        Normalize deck_options into flat (inclusion_rules, exclusion_rules) for card pool filtering.

        Handles:
          - faction / trait / type / uses / tag / text  — pass through as-is
          - faction_select                              — fan out to one rule per selectable faction
          - option_select                               — flatten all branches (union for display)
          - bare level-only rule (Dunwich pattern)      — any card at that XP range
          - deck_size_select                            — drop (informational only)

        Strips deckbuilding noise (limit, error, atleast, etc.) from every rule —
        those are count constraints, irrelevant for pool membership.
        """
        inclusion: List[Dict] = []
        exclusion: List[Dict] = []

        for opt in (self.deck_options or []):
            # Strip noise keys — they're deckbuilding constraints, not selectors
            rule = {k: v for k, v in opt.items() if k not in _NOISE_KEYS}
            if not rule:
                continue

            # Exclusion rule
            if rule.get("not"):
                exclusion.append(rule)
                continue

            # faction_select: player picks one faction at deck-build time
            # For pool purposes show the union of all selectable factions
            if "faction_select" in rule:
                base = {k: v for k, v in rule.items() if k != "faction_select"}
                for faction in rule["faction_select"]:
                    inclusion.append({**base, "faction": [faction]})
                continue

            # option_select: player picks one branch — union all for pool display
            if "option_select" in rule:
                for branch in rule["option_select"]:
                    clean = {k: v for k, v in branch.items() if k not in _NOISE_KEYS}
                    if clean:
                        inclusion.append(clean)
                continue

            # deck_size_select: purely informational
            if "deck_size_select" in rule:
                continue

            # Has at least one positive selector — standard rule
            if any(k in rule for k in _SELECTOR_KEYS):
                inclusion.append(rule)
                continue

            # Bare level-only rule (Dunwich pattern): no selector at all
            # Means any player card at this XP range qualifies
            if "level" in rule:
                inclusion.append({"_open_level": True, "level": rule["level"]})

        return inclusion, exclusion

    # def __init__(
    #     self,
    #     code: str,
    #     name: str,
    #     traits: List[str],
    #     text: str,
    #     skill_willpower: int,
    #     skill_intellect: int,
    #     skill_combat: int,
    #     skill_agility: int,
    #     faction: Faction,
    #     health: int,
    #     sanity: int,
    # ):
    #     super().__init__(
    #         code,
    #         name,
    #         CardType.INVESTIGATOR,
    #         traits,
    #         faction,
    #         text,
    #         "",
    #     )
    #     self.skill_willpower = skill_willpower
    #     self.skill_intellect = skill_intellect
    #     self.skill_combat = skill_combat
    #     self.skill_agility = skill_agility
    #     self.play_action_cost = 0
    #     self.is_unique = True
    #     self.is_permanent = True

    #     WithHealthSanity.__init__(self, health, sanity)
