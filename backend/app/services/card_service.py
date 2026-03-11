from typing import Any, Dict, Optional, List, Tuple, cast
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta

from app.models.arkham_model import CardModel
from app.repositories.base_repositories import BaseRepository
from app.services.deck_service import DeckService
from app.adapters.card_adapters import UnifiedCardAdapter
from app.schemas.card_schema import CardSchema
from app.core.redis_client import get_redis_client
from domain.card.investigator_card import InvestigatorCard
from domain.card.context import InvestigatorStats
from domain.card.card_type import CardType
from domain.card import PlayerCard
from domain.card.deck import Deck
from domain.card.context.card_stats import CardStats


class CardService:
    def __init__(
        self,
        db: AsyncSession,
        card_repo: Optional[BaseRepository[CardModel]],
        deck_service: Optional[DeckService] = None,
    ):
        self.db = db
        self.card_repo = card_repo or BaseRepository(CardModel, db)
        self.deck_service = deck_service

    async def get_card_stats(
        self, card_id: str, days: int = 365, trend_period: str = "month"
    ):
        """Get comprehensive card statistics including popularity and trends"""
        # Try to get from cache first
        redis_client = await get_redis_client()
        cache_key = f"card_stats:{card_id}"

        if redis_client.is_connected:
            cached_stats = await redis_client.get(cache_key)
            if cached_stats:
                print(f"Cache hit for card {card_id}")
                return cached_stats

        print(f"Cache miss for card {card_id}, calculating stats...")

        # Get card from database
        card = await self.card_repo.get_first(
            filters={"filter_by[code][equals]": card_id}
        )
        if not card:
            raise ValueError(f"Card with ID {card_id} not found")

        # Get recent deck data if deck_service is available
        decks = []
        if self.deck_service:
            try:
                # Get actual deck objects (not summary) for analysis
                decks = await self.deck_service.get_decks_last_n_days(days)
            except Exception as e:
                print(f"Warning: Could not fetch deck data for card stats: {e}")
        adapter = UnifiedCardAdapter()
        # Create CardStats with the deck data

        # Debug: Check what we actually have
        if decks:
            print("First deck type:", type(decks[0]))
            print("First deck has name:", hasattr(decks[0], "name"))
            if hasattr(decks[0], "name"):
                print("First deck name:", decks[0].name)

        # Convert decks to domain objects
        converted_decks = []
        for deck in decks:
            if hasattr(deck, "name") and deck.name:
                try:
                    converted_deck = Deck.from_dict(
                        {
                            "name": deck.name,
                            "date_creation": getattr(deck, "date_creation", ""),
                            "date_update": getattr(deck, "date_update", ""),
                            "investigator_code": getattr(deck, "investigator_code", ""),
                            "investigator_name": getattr(deck, "investigator_name", ""),
                            "slots": getattr(deck, "slots", {}),
                            "sideSlots": (
                                getattr(deck, "sideSlots", {})
                                if isinstance(getattr(deck, "sideSlots", {}), dict)
                                else {}
                            ),
                            "ignoreDeckLimitSlots": getattr(
                                deck, "ignoreDeckLimitSlots", None
                            ),
                            "xp_spent": getattr(deck, "xp_spent", None),
                            "xp_adjustment": getattr(deck, "xp_adjustment", None),
                            "exile_string": getattr(deck, "exile_string", None),
                            "taboo_id": getattr(deck, "taboo_id", None),
                            "meta": getattr(deck, "meta", ""),
                            "tags": getattr(deck, "tags", ""),
                            "previous_deck": getattr(deck, "previous_deck", None),
                            "next_deck": getattr(deck, "next_deck", None),
                        }
                    )
                    converted_decks.append(converted_deck)
                except Exception as e:
                    print(f"Error converting deck: {e}")

        print("Converted decks:", len(converted_decks))

        card_stats = CardStats(
            cast(
                PlayerCard,
                adapter.schema_to_domain(schema=CardSchema.from_model(card)),
            ),
            converted_decks,
        )

        # Build response with cache metadata
        result = {
            "card_info": {"code": card.code, "name": card.name, "type": card.type_name},
            "deck_stats": card_stats.get_deck_stats(trend_period=trend_period),
            "data_source": {
                "decks_analyzed": len(decks),
                "days_covered": days,
                "trend_period": trend_period,
                "last_updated": datetime.now().isoformat(),
                "next_update": (datetime.now() + timedelta(days=7)).isoformat(),
            },
        }

        # Cache the result (7 days TTL)
        if redis_client.is_connected:
            cache_ttl = 60 * 60 * 24 * 7  # 7 days
            await redis_client.set(cache_key, result, expire=cache_ttl)

        return result

    async def get_investigator_stats(self, investigator_code: str, days: int = 365):
        """Get stats for an investigator"""
        investigator = await self.card_repo.get_first(
            filters={"filter_by[code][equals]": investigator_code}
        )
        print(
            "investigator is",
            investigator.type_code if investigator else "none",
            (investigator.type_code if investigator else "none")
            == CardType.INVESTIGATOR.value,
            investigator_code,
        )
        if not investigator or investigator.type_code != CardType.INVESTIGATOR.value:
            raise ValueError(f"Investigator with ID {investigator_code} not found")

        decks = []
        if self.deck_service:
            try:
                # Get actual deck objects (not summary) for analysis
                decks = await self.deck_service.get_decks_last_n_days(days)
            except Exception as e:
                print(f"Warning: Could not fetch deck data for card stats: {e}")
        adapter = UnifiedCardAdapter()
        # Create CardStats with the deck data

        # Debug: Check what we actually have
        if decks:
            print("First deck type:", type(decks[0]))
            print("First deck has name:", hasattr(decks[0], "name"))
            if hasattr(decks[0], "name"):
                print("First deck name:", decks[0].name)

        # Convert decks to domain objects
        converted_decks = []
        for deck in decks:
            if hasattr(deck, "name") and deck.name:
                try:
                    converted_deck = Deck.from_dict(
                        {
                            "name": deck.name,
                            "date_creation": getattr(deck, "date_creation", ""),
                            "date_update": getattr(deck, "date_update", ""),
                            "investigator_code": getattr(deck, "investigator_code", ""),
                            "investigator_name": getattr(deck, "investigator_name", ""),
                            "slots": getattr(deck, "slots", {}),
                            "sideSlots": (
                                getattr(deck, "sideSlots", {})
                                if isinstance(getattr(deck, "sideSlots", {}), dict)
                                else {}
                            ),
                            "ignoreDeckLimitSlots": getattr(
                                deck, "ignoreDeckLimitSlots", None
                            ),
                            "xp_spent": getattr(deck, "xp_spent", None),
                            "xp_adjustment": getattr(deck, "xp_adjustment", None),
                            "exile_string": getattr(deck, "exile_string", None),
                            "taboo_id": getattr(deck, "taboo_id", None),
                            "meta": getattr(deck, "meta", ""),
                            "tags": getattr(deck, "tags", ""),
                            "previous_deck": getattr(deck, "previous_deck", None),
                            "next_deck": getattr(deck, "next_deck", None),
                        }
                    )
                    converted_decks.append(converted_deck)
                except Exception as e:
                    print(f"Error converting deck: {e}")

        investigator_stats = InvestigatorStats(
            cast(
                InvestigatorCard,
                adapter.schema_to_domain(schema=CardSchema.from_model(investigator)),
            ),
            converted_decks,
        )
        stats = investigator_stats.get_stats()

        # Enrich stats with card names
        await self._enrich_stats_with_card_names(stats)

        return stats

    async def _enrich_stats_with_card_names(self, stats: dict):
        """Add card names to all card_code fields in stats"""
        # Collect all unique card codes
        card_codes = set()

        # From card rankings
        if "card_rankings" in stats:
            for card in stats["card_rankings"]:
                if "card_code" in card:
                    card_codes.add(card["card_code"])

        # From staple cards
        if "staple_cards" in stats:
            for card in stats["staple_cards"]:
                if "card_code" in card:
                    card_codes.add(card["card_code"])

        # From rising/falling cards
        for key in ["rising_cards", "falling_cards"]:
            if key in stats:
                for card in stats[key]:
                    if "card_code" in card:
                        card_codes.add(card["card_code"])

        # From underused gems and overused cards
        for key in ["underused_gems", "overused_cards"]:
            if key in stats:
                for card in stats[key]:
                    if "card_code" in card:
                        card_codes.add(card["card_code"])

        # From card synergies
        if "card_synergies" in stats:
            for synergy in stats["card_synergies"]:
                if "card1" in synergy:
                    card_codes.add(synergy["card1"])
                if "card2" in synergy:
                    card_codes.add(synergy["card2"])

        # From card efficiency ratings
        if "card_efficiency_ratings" in stats:
            for card in stats["card_efficiency_ratings"]:
                if "card_code" in card:
                    card_codes.add(card["card_code"])

        # From deck archetypes
        if "deck_archetypes" in stats:
            for archetype in stats["deck_archetypes"]:
                for code in archetype.get("archetype_signature", []):
                    card_codes.add(code)

        # From build recommendations
        if "build_recommendations" in stats:
            rec = stats["build_recommendations"]
            for key in ["core_recommendations", "hidden_gems", "trending_picks"]:
                for code in rec.get(key, []):
                    card_codes.add(code)

        # Fetch card names
        card_name_map = {}
        for code in card_codes:
            try:
                card = await self.card_repo.get_first(
                    filters={"filter_by[code][equals]": code}
                )
                if card:
                    card_name_map[code] = card.name
            except Exception:
                card_name_map[code] = code  # Fallback to code if lookup fails

        # Add card names to stats
        if "card_rankings" in stats:
            for card in stats["card_rankings"]:
                if "card_code" in card:
                    card["card_name"] = card_name_map.get(card["card_code"], card["card_code"])

        if "staple_cards" in stats:
            for card in stats["staple_cards"]:
                if "card_code" in card:
                    card["card_name"] = card_name_map.get(card["card_code"], card["card_code"])

        for key in ["rising_cards", "falling_cards"]:
            if key in stats:
                for card in stats[key]:
                    if "card_code" in card:
                        card["card_name"] = card_name_map.get(card["card_code"], card["card_code"])

        for key in ["underused_gems", "overused_cards"]:
            if key in stats:
                for card in stats[key]:
                    if "card_code" in card:
                        card["card_name"] = card_name_map.get(card["card_code"], card["card_code"])

        if "card_synergies" in stats:
            for synergy in stats["card_synergies"]:
                if "card1" in synergy:
                    synergy["card1_name"] = card_name_map.get(synergy["card1"], synergy["card1"])
                if "card2" in synergy:
                    synergy["card2_name"] = card_name_map.get(synergy["card2"], synergy["card2"])

        if "card_efficiency_ratings" in stats:
            for card in stats["card_efficiency_ratings"]:
                if "card_code" in card:
                    card["card_name"] = card_name_map.get(card["card_code"], card["card_code"])

        if "deck_archetypes" in stats:
            for archetype in stats["deck_archetypes"]:
                archetype["archetype_signature_names"] = [
                    card_name_map.get(code, code)
                    for code in archetype.get("archetype_signature", [])
                ]

        if "build_recommendations" in stats:
            rec = stats["build_recommendations"]
            for key in ["core_recommendations", "hidden_gems", "trending_picks"]:
                rec[f"{key}_names"] = [
                    card_name_map.get(code, code) for code in rec.get(key, [])
                ]

    async def search_all_cards(
        self,
        query: Optional[str] = None,
        faction: Optional[str] = None,
        card_type: Optional[str] = None,
        min_xp: Optional[int] = None,
        max_xp: Optional[int] = None,
        min_cost: Optional[int] = None,
        max_cost: Optional[int] = None,
        pack_code: Optional[str] = None,
        traits: Optional[str] = None,
        include_investigators: bool = False,
        only_player_cards: bool = True,
    ) -> List[CardSchema]:
        """
        Search for cards with comprehensive filtering.
        Returns ALL matching cards (client will handle pagination/filtering).
        By default, excludes investigator cards (use include_investigators=True to include them).
        """
        filters = {}

        # Text search in name, text, and traits
        # Only apply search filter if query is provided and not empty
        if query and query.strip():
            filters["filter_by[name][contains]"] = query.strip()

        # Faction filter
        if faction:
            filters["filter_by[faction_code][equals]"] = faction

        # Card type filter
        if card_type:
            filters["filter_by[type_code][equals]"] = card_type

        # Pack filter
        if pack_code:
            filters["filter_by[pack_code][equals]"] = pack_code

        # if only_player_cards:
        #     filters["filter_by[type_code][not_in]"] = [
        #         card_type.__str__() for card_type in CardType.encounter_cards()
        #     ]

        # Get all matching cards (no pagination at DB level)
        try:
            cards = await self.card_repo.get_all(
                filter_by=filters,
                # Get a reasonable batch size to avoid timeouts
                items_per_page=500,
            )
        except Exception as e:
            print(f"Error fetching cards from repository: {e}")
            return []

        # Convert to schemas
        card_schemas = [CardSchema.from_model(card) for card in cards]

        # Apply additional filters that might not be supported by DB filtering
        filtered_cards = []
        for card_schema in card_schemas:
            # Exclude investigators by default (unless explicitly requested)
            if not include_investigators:
                card_type_code = getattr(card_schema, "type_code", "")
                if card_type_code == CardType.INVESTIGATOR.value:
                    continue

            # XP filtering
            if min_xp is not None or max_xp is not None:
                card_xp = getattr(card_schema, "xp", None) or 0
                if min_xp is not None and card_xp < min_xp:
                    continue
                if max_xp is not None and card_xp > max_xp:
                    continue

            # Cost filtering
            if min_cost is not None or max_cost is not None:
                card_cost = card_schema.cost
                if card_cost is not None:
                    if min_cost is not None and card_cost < min_cost:
                        continue
                    if max_cost is not None and card_cost > max_cost:
                        continue

            # Traits filtering (if provided)
            if traits:
                card_traits = getattr(card_schema, "traits", "") or ""
                if traits.lower() not in card_traits.lower():
                    continue

            filtered_cards.append(card_schema)

        return len(filtered_cards), filtered_cards

    async def search_cards_paginated(
        self,
        # Text search
        query: Optional[str] = None,
        text_search: Optional[str] = None,
        flavor_search: Optional[str] = None,
        # Card attributes
        faction: Optional[str] = None,
        card_type: Optional[str] = None,
        subtype: Optional[str] = None,
        traits: Optional[str] = None,
        slot: Optional[str] = None,
        pack_code: Optional[str] = None,
        illustrator: Optional[str] = None,
        # Boolean filters
        is_unique: Optional[bool] = None,
        permanent: Optional[bool] = None,
        exceptional: Optional[bool] = None,
        # Numeric filters
        min_xp: Optional[int] = None,
        max_xp: Optional[int] = None,
        min_cost: Optional[int] = None,
        max_cost: Optional[int] = None,
        min_skill_willpower: Optional[int] = None,
        max_skill_willpower: Optional[int] = None,
        min_skill_intellect: Optional[int] = None,
        max_skill_intellect: Optional[int] = None,
        min_skill_combat: Optional[int] = None,
        max_skill_combat: Optional[int] = None,
        min_skill_agility: Optional[int] = None,
        max_skill_agility: Optional[int] = None,
        min_health: Optional[int] = None,
        max_health: Optional[int] = None,
        min_sanity: Optional[int] = None,
        max_sanity: Optional[int] = None,
        # Pagination
        page: int = 1,
        limit: int = 20,
        include_investigators: bool = False,
        only_player_cards: bool = True,
    ) -> tuple[int, List[CardSchema]]:
        """
        Search for cards with server-side pagination.
        Returns (total_count, cards_for_current_page).
        """
        filters = {}

        # Text search in name
        if query and query.strip():
            filters["filter_by[name][contains]"] = query.strip()

        # Faction filter
        if faction:
            filters["filter_by[faction_code][equals]"] = faction

        # Card type filter
        if card_type:
            filters["filter_by[type_code][equals]"] = card_type

        # Subtype filter
        if subtype:
            filters["filter_by[subtype_code][equals]"] = subtype

        # Pack filter
        if pack_code:
            filters["filter_by[pack_code][equals]"] = pack_code

        # Illustrator filter
        if illustrator:
            filters["filter_by[illustrator][contains]"] = illustrator

        # Boolean filters
        if is_unique is not None:
            filters["filter_by[is_unique][equals]"] = is_unique

        if permanent is not None:
            filters["filter_by[permanent][equals]"] = permanent

        if exceptional is not None:
            filters["filter_by[exceptional][equals]"] = exceptional

        # Numeric filters
        if min_cost is not None:
            filters["filter_by[cost][gte]"] = min_cost
        if max_cost is not None:
            filters["filter_by[cost][lte]"] = max_cost

        if min_skill_willpower is not None:
            filters["filter_by[skill_willpower][gte]"] = min_skill_willpower
        if max_skill_willpower is not None:
            filters["filter_by[skill_willpower][lte]"] = max_skill_willpower

        if min_skill_intellect is not None:
            filters["filter_by[skill_intellect][gte]"] = min_skill_intellect
        if max_skill_intellect is not None:
            filters["filter_by[skill_intellect][lte]"] = max_skill_intellect

        if min_skill_combat is not None:
            filters["filter_by[skill_combat][gte]"] = min_skill_combat
        if max_skill_combat is not None:
            filters["filter_by[skill_combat][lte]"] = max_skill_combat

        if min_skill_agility is not None:
            filters["filter_by[skill_agility][gte]"] = min_skill_agility
        if max_skill_agility is not None:
            filters["filter_by[skill_agility][lte]"] = max_skill_agility

        if min_health is not None:
            filters["filter_by[health][gte]"] = min_health
        if max_health is not None:
            filters["filter_by[health][lte]"] = max_health

        if min_sanity is not None:
            filters["filter_by[sanity][gte]"] = min_sanity
        if max_sanity is not None:
            filters["filter_by[sanity][lte]"] = max_sanity

        # Get total count first (without pagination)
        try:
            all_cards = await self.card_repo.get_all(
                filter_by=filters,
                items_per_page=10000,  # Large number to get all matches
            )
        except Exception as e:
            print(f"Error fetching cards from repository: {e}")
            return 0, []

        # Apply additional filters
        filtered_cards = []
        for card in all_cards:
            # Exclude investigators by default
            if not include_investigators:
                if card.type_code == CardType.INVESTIGATOR.value:
                    continue

            # Text search filters
            if text_search:
                card_text = getattr(card, "text", "") or ""
                if text_search.lower() not in card_text.lower():
                    continue

            if flavor_search:
                card_flavor = getattr(card, "flavor", "") or ""
                if flavor_search.lower() not in card_flavor.lower():
                    continue

            # Only apply filters that can't be done at database level
            # Slot filter (complex matching - not supported by database)
            if slot:
                card_slot = getattr(card, "real_slot", "") or ""
                if slot.lower() not in card_slot.lower():
                    continue

            # Apply traits filter
            if traits:
                card_traits_obj = getattr(card, "traits", None)
                if card_traits_obj:
                    # Handle both string and list of TraitModel objects
                    if isinstance(card_traits_obj, str):
                        card_traits_str = card_traits_obj
                    elif isinstance(card_traits_obj, list):
                        # Extract trait names from TraitModel objects
                        trait_names = []
                        for trait_obj in card_traits_obj:
                            if hasattr(trait_obj, "name") and trait_obj.name:
                                trait_names.append(trait_obj.name)
                            elif isinstance(trait_obj, str):
                                trait_names.append(trait_obj)
                        card_traits_str = " ".join(trait_names)
                    else:
                        card_traits_str = str(card_traits_obj)

                    # Check if the search trait is in the card's traits
                    if traits.lower() not in card_traits_str.lower():
                        continue
                else:
                    # Card has no traits, skip it
                    continue

            filtered_cards.append(card)

        # Get total count after filtering
        total_count = len(filtered_cards)

        # Apply pagination
        start_index = (page - 1) * limit
        end_index = start_index + limit
        paginated_cards = filtered_cards[start_index:end_index]

        # Convert to schemas
        card_schemas = [CardSchema.from_model(card) for card in paginated_cards]

        return total_count, card_schemas

    async def get_all_traits(self) -> List[str]:
        """
        Get all unique traits from all cards.
        Returns a sorted list of unique trait strings.
        """
        try:
            # Get all cards
            cards = await self.card_repo.get_all(
                filter_by={},
                items_per_page=10000,
            )

            # Extract and parse traits
            all_traits = set()
            for card in cards:
                if card.traits:
                    # Traits might be a string or a list of TraitModel objects
                    if isinstance(card.traits, str):
                        # Traits are stored as comma-separated values like "Item. Weapon. Firearm."
                        # Split by period and strip whitespace
                        traits_list = [
                            trait.strip()
                            for trait in card.traits.replace(".", ",").split(",")
                            if trait.strip()
                        ]
                        all_traits.update(traits_list)
                    elif isinstance(card.traits, list):
                        # If it's a list of TraitModel objects, extract names
                        for trait_obj in card.traits:
                            if hasattr(trait_obj, "name") and trait_obj.name:
                                all_traits.add(trait_obj.name.strip())
                            elif isinstance(trait_obj, str):
                                all_traits.add(trait_obj.strip())

            # Return sorted list
            return sorted(list(all_traits))
        except Exception as e:
            print(f"Error getting traits: {e}")
            return []

    async def get_all_investigators(self) -> List[Dict[str, str]]:
        """
        Get all investigators with their codes and names.
        Returns a list of dictionaries with code and name.
        """
        try:
            # Get all investigator cards
            cards = await self.card_repo.get_all(
                filter_by={"filter_by[type_code][equals]": "investigator"},
                items_per_page=1000,
            )

            # Extract code and name
            investigators = []
            for card in cards:
                if card.code and card.name:
                    investigators.append({
                        "code": card.code,
                        "name": card.name,
                        "faction_code": card.faction_code if hasattr(card, 'faction_code') else None,
                    })

            # Sort by name
            investigators.sort(key=lambda x: x["name"])
            return investigators
        except Exception as e:
            print(f"Error getting investigators: {e}")
            return []

    async def get_all_encounter_sets(self) -> List[dict]:
        """
        Get all unique encounter sets.
        Returns a list of {code, name} objects.
        """
        try:
            # Get all cards with encounter set info
            cards = await self.card_repo.get_all(
                filter_by={},
                items_per_page=10000,
            )

            # Extract unique encounter sets
            encounter_sets = {}
            for card in cards:
                # Check if card has encounter set code
                encounter_code = getattr(card, "encounter_code", None)
                encounter_name = getattr(card, "encounter_name", None)

                if encounter_code:
                    encounter_sets[encounter_code] = {
                        "code": encounter_code,
                        "name": encounter_name or encounter_code,
                    }

            # Return sorted list by name
            return sorted(list(encounter_sets.values()), key=lambda x: x["name"])
        except Exception as e:
            print(f"Error getting encounter sets: {e}")
            return []
