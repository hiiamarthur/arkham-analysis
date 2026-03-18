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


def _next_sunday_midnight_utc() -> datetime:
    """Returns the next Sunday 00:00 UTC datetime (same boundary as the cache TTL)."""
    now = datetime.utcnow()
    days_ahead = (6 - now.weekday()) % 7 or 7
    return (now + timedelta(days=days_ahead)).replace(hour=0, minute=0, second=0, microsecond=0)


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
                return cached_stats

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
            except Exception:
                pass
        adapter = UnifiedCardAdapter()

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
                    pass

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
                "last_updated": datetime.utcnow().isoformat() + "Z",
                "next_update": _next_sunday_midnight_utc().isoformat() + "Z",
            },
        }

        if redis_client.is_connected:
            from app.api.v1.endpoints import seconds_until_next_sunday_midnight
            await redis_client.set(cache_key, result, expire=seconds_until_next_sunday_midnight())

        return result

    async def get_investigator_stats(self, investigator_code: str, days: int = 90):
        """Get stats for an investigator"""
        investigator = await self.card_repo.get_first(
            filters={"filter_by[code][equals]": investigator_code}
        )
        if not investigator or investigator.type_code != CardType.INVESTIGATOR.value:
            raise ValueError(f"Investigator with ID {investigator_code} not found")

        decks = []
        if self.deck_service:
            try:
                # Get actual deck objects (not summary) for analysis
                decks = await self.deck_service.get_decks_last_n_days(days)
            except Exception:
                pass
        adapter = UnifiedCardAdapter()

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
                    pass

        # Extract signature slots from deck_requirements
        # Structure: {"card": {"SLOT_CODE": {"CHOICE_CODE": "CHOICE_CODE", ...}}}
        # Each slot has one or more valid choices (original + replacements)
        signature_slots: dict = {}
        deck_req = investigator.deck_requirements
        if isinstance(deck_req, dict):
            card_req = deck_req.get("card", {})
            if isinstance(card_req, dict):
                for slot_code, choices in card_req.items():
                    if isinstance(choices, dict):
                        signature_slots[slot_code] = list(choices.keys())
                    elif isinstance(choices, str):
                        signature_slots[slot_code] = [choices]
                    else:
                        signature_slots[slot_code] = [slot_code]

        investigator_stats = InvestigatorStats(
            cast(
                InvestigatorCard,
                adapter.schema_to_domain(schema=CardSchema.from_model(investigator)),
            ),
            converted_decks,
            signature_slots=signature_slots,
        )
        stats = investigator_stats.get_stats()

        # Override investigator name from the DB card — deck-derived name falls back to
        # the code string when there are no matching decks (e.g. parallel investigators).
        if "investigator_info" in stats and investigator.name:
            stats["investigator_info"]["name"] = investigator.name

        # Enrich stats with card names
        await self._enrich_stats_with_card_names(stats)

        return stats

    async def get_investigator_card_rankings(
        self,
        investigator_code: str,
        days: int = 90,
        min_xp: Optional[int] = None,
        max_xp: Optional[int] = None,
        query: Optional[str] = None,
        limit: int = 20,
    ) -> dict:
        """Compute only card rankings for an investigator with server-side filtering."""
        RANKINGS_CACHE_KEY = f"investigator:card_rankings:v1:{investigator_code}"
        redis_client = await get_redis_client()

        # Try raw rankings cache first (unfiltered, unenriched)
        raw_rankings = None
        if redis_client.is_connected:
            raw_rankings = await redis_client.get(RANKINGS_CACHE_KEY)

        if raw_rankings is None:
            investigator = await self.card_repo.get_first(
                filters={"filter_by[code][equals]": investigator_code}
            )
            if not investigator or investigator.type_code != CardType.INVESTIGATOR.value:
                raise ValueError(f"Investigator {investigator_code} not found")

            decks = []
            if self.deck_service:
                try:
                    decks = await self.deck_service.get_decks_last_n_days(days)
                except Exception:
                    pass

            adapter = UnifiedCardAdapter()
            converted_decks = []
            for deck in decks:
                if hasattr(deck, "name") and deck.name:
                    try:
                        converted_decks.append(Deck.from_dict({
                            "name": deck.name,
                            "date_creation": getattr(deck, "date_creation", ""),
                            "date_update": getattr(deck, "date_update", ""),
                            "investigator_code": getattr(deck, "investigator_code", ""),
                            "investigator_name": getattr(deck, "investigator_name", ""),
                            "slots": getattr(deck, "slots", {}),
                            "sideSlots": getattr(deck, "sideSlots", {}) if isinstance(getattr(deck, "sideSlots", {}), dict) else {},
                            "ignoreDeckLimitSlots": getattr(deck, "ignoreDeckLimitSlots", None),
                            "xp_spent": getattr(deck, "xp_spent", None),
                            "xp_adjustment": getattr(deck, "xp_adjustment", None),
                            "exile_string": getattr(deck, "exile_string", None),
                            "taboo_id": getattr(deck, "taboo_id", None),
                            "meta": getattr(deck, "meta", ""),
                            "tags": getattr(deck, "tags", ""),
                            "previous_deck": getattr(deck, "previous_deck", None),
                            "next_deck": getattr(deck, "next_deck", None),
                        }))
                    except Exception:
                        pass

            signature_slots: dict = {}
            deck_req = investigator.deck_requirements
            if isinstance(deck_req, dict):
                card_req = deck_req.get("card", {})
                if isinstance(card_req, dict):
                    for slot_code, choices in card_req.items():
                        if isinstance(choices, dict):
                            signature_slots[slot_code] = list(choices.keys())
                        elif isinstance(choices, str):
                            signature_slots[slot_code] = [choices]
                        else:
                            signature_slots[slot_code] = [slot_code]

            investigator_stats = InvestigatorStats(
                cast(InvestigatorCard, adapter.schema_to_domain(schema=CardSchema.from_model(investigator))),
                converted_decks,
                signature_slots=signature_slots,
            )
            raw_rankings = investigator_stats._get_card_rankings()

            # Enrich with card names / xp / subname
            card_codes = [c["card_code"] for c in raw_rankings]
            if card_codes:
                try:
                    cards = await self.card_repo.get_all(
                        filter_by={"filter_by[code][in]": card_codes},
                        items_per_page=len(card_codes) + 10,
                    )
                    name_map = {c.code: c.name for c in cards if c.name}
                    xp_map = {c.code: c.xp for c in cards if c.xp is not None}
                    subname_map = {c.code: c.subname for c in cards if c.subname}
                    for card in raw_rankings:
                        code = card["card_code"]
                        card["card_name"] = name_map.get(code, code)
                        card["card_xp"] = xp_map.get(code)
                        card["card_subname"] = subname_map.get(code)
                except Exception as e:
                    print(f"Warning: Could not enrich card rankings: {e}")

            if redis_client.is_connected:
                from app.api.v1.endpoints import seconds_until_next_sunday_midnight
                await redis_client.set(RANKINGS_CACHE_KEY, raw_rankings, expire=seconds_until_next_sunday_midnight())

        # Apply server-side filters
        results = raw_rankings
        if min_xp is not None:
            results = [c for c in results if (c.get("card_xp") or 0) >= min_xp]
        if max_xp is not None:
            results = [c for c in results if (c.get("card_xp") or 0) <= max_xp]
        if query:
            q = query.lower()
            results = [c for c in results if q in (c.get("card_name") or c["card_code"]).lower()]

        total = len(results)
        return {
            "investigator_code": investigator_code,
            "cards": results[:limit],
            "total": total,
            "filters": {"min_xp": min_xp, "max_xp": max_xp, "query": query, "limit": limit},
        }

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
            for key in ["must_include", "core_recommendations", "hidden_gems", "trending_picks"]:
                for code in rec.get(key, []):
                    card_codes.add(code)
            # From must_include_replacements (dict of slot_code -> [alt_codes])
            for alt_codes in rec.get("must_include_replacements", {}).values():
                for code in alt_codes:
                    card_codes.add(code)

        # Batch fetch all card names in a single query
        card_name_map = {}
        card_xp_map = {}
        card_subname_map = {}
        if card_codes:
            try:
                cards = await self.card_repo.get_all(
                    filter_by={"filter_by[code][in]": list(card_codes)},
                    items_per_page=len(card_codes) + 10,
                )
                card_name_map = {card.code: card.name for card in cards if card.name}
                card_xp_map = {card.code: card.xp for card in cards if card.xp is not None}
                card_subname_map = {card.code: card.subname for card in cards if card.subname}
            except Exception as e:
                print(f"Warning: Could not batch fetch card names: {e}")

        # Add card names to stats
        if "card_rankings" in stats:
            for card in stats["card_rankings"]:
                if "card_code" in card:
                    card["card_name"] = card_name_map.get(card["card_code"], card["card_code"])
                    card["card_xp"] = card_xp_map.get(card["card_code"])
                    card["card_subname"] = card_subname_map.get(card["card_code"])

        if "staple_cards" in stats:
            for card in stats["staple_cards"]:
                if "card_code" in card:
                    card["card_name"] = card_name_map.get(card["card_code"], card["card_code"])
                    card["card_xp"] = card_xp_map.get(card["card_code"])
                    card["card_subname"] = card_subname_map.get(card["card_code"])

        for key in ["rising_cards", "falling_cards"]:
            if key in stats:
                for card in stats[key]:
                    if "card_code" in card:
                        card["card_name"] = card_name_map.get(card["card_code"], card["card_code"])
                        card["card_xp"] = card_xp_map.get(card["card_code"])
                        card["card_subname"] = card_subname_map.get(card["card_code"])

        for key in ["underused_gems", "overused_cards"]:
            if key in stats:
                for card in stats[key]:
                    if "card_code" in card:
                        card["card_name"] = card_name_map.get(card["card_code"], card["card_code"])
                        card["card_xp"] = card_xp_map.get(card["card_code"])
                        card["card_subname"] = card_subname_map.get(card["card_code"])

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
                codes = archetype.get("archetype_signature", [])
                archetype["archetype_signature_names"] = [card_name_map.get(c, c) for c in codes]
                archetype["archetype_signature_xp"] = [card_xp_map.get(c) for c in codes]
                archetype["archetype_signature_subnames"] = [card_subname_map.get(c) for c in codes]

        if "build_recommendations" in stats:
            rec = stats["build_recommendations"]
            for key in ["must_include", "core_recommendations", "hidden_gems", "trending_picks"]:
                codes = rec.get(key, [])
                rec[f"{key}_names"] = [card_name_map.get(c, c) for c in codes]
                rec[f"{key}_xp"] = [card_xp_map.get(c) for c in codes]
                rec[f"{key}_subnames"] = [card_subname_map.get(c) for c in codes]
            # Enrich replacement names/xp/subnames
            replacements = rec.get("must_include_replacements", {})
            rec["must_include_replacements_names"] = {
                slot_code: [card_name_map.get(c, c) for c in alt_codes]
                for slot_code, alt_codes in replacements.items()
            }
            rec["must_include_replacements_xp"] = {
                slot_code: [card_xp_map.get(c) for c in alt_codes]
                for slot_code, alt_codes in replacements.items()
            }
            rec["must_include_replacements_subnames"] = {
                slot_code: [card_subname_map.get(c) for c in alt_codes]
                for slot_code, alt_codes in replacements.items()
            }

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
        from sqlalchemy import select, text
        from app.models.arkham_model import TraitModel
        try:
            # Query traits table directly — much faster than loading all cards
            stmt = select(TraitModel.name).distinct().order_by(TraitModel.name)
            result = await self.db.execute(stmt)
            traits = [row[0] for row in result.all() if row[0]]
            return traits
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
        from sqlalchemy import select
        from app.models.arkham_model import CardModel
        try:
            # Query distinct encounter codes/names directly — much faster than loading all cards
            stmt = (
                select(CardModel.encounter_code, CardModel.encounter_name)
                .where(CardModel.encounter_code.isnot(None))
                .distinct()
                .order_by(CardModel.encounter_name)
            )
            result = await self.db.execute(stmt)
            encounter_sets = [
                {"code": row[0], "name": row[1] or row[0]}
                for row in result.all()
                if row[0]
            ]
            return encounter_sets
        except Exception as e:
            print(f"Error getting encounter sets: {e}")
            return []
