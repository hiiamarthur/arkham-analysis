from fastapi import APIRouter, Depends, Response, HTTPException
from typing import List, Dict, Any, Set
from collections import Counter
from datetime import datetime, timedelta
import asyncio

from sqlalchemy import select

from app.api.deps import get_card_service, get_deck_service
from app.services.card_service import CardService
from app.services.deck_service import DeckService
from app.models.arkham_model import CardModel
from app.core.redis_client import get_redis_client
from . import ARKHAM_HEADERS, seconds_until_next_sunday_midnight

router = APIRouter()

CACHE_KEY = "dashboard:stats:v5"


@router.get("")
async def get_dashboard_stats(
    response: Response,
    days: int = 90,
    card_service: CardService = Depends(get_card_service),
    deck_service: DeckService = Depends(get_deck_service),
) -> Dict[str, Any]:
    """
    Aggregated dashboard stats from ArkhamDB deck data.
    Default window is 90 days for snappy response times.
    Cached for 2 hours.
    """
    redis_client = await get_redis_client()
    cache_key = f"{CACHE_KEY}:{days}"

    if redis_client.is_connected:
        cached = await redis_client.get(cache_key)
        if cached:
            response.headers.update(ARKHAM_HEADERS)
            response.headers["X-Cache"] = "HIT"
            return cached

    try:
        decks, investigators, reprint_map = await asyncio.wait_for(
            asyncio.gather(
                deck_service.get_decks_last_n_days(days),
                card_service.get_all_investigators(),
                _build_reprint_map(card_service),
            ),
            timeout=30.0,
        )
    except asyncio.TimeoutError:
        raise HTTPException(status_code=504, detail="Deck data fetch timed out. Try again — results will be cached.")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load deck data: {e}")

    if not decks:
        return _empty_response(days)

    def _crunch(decks, investigators, reprint_map):
        inv_lookup: Dict[str, Dict] = {
            i["code"]: {"name": i["name"], "faction_code": i.get("faction_code", "neutral")}
            for i in investigators
        }
        now = datetime.utcnow()
        cutoff_recent = now - timedelta(days=45)
        cutoff_prior = now - timedelta(days=90)

        recent_inv_counter: Counter = Counter()
        prior_inv_counter: Counter = Counter()
        all_inv_counter: Counter = Counter()
        card_counter: Counter = Counter()
        faction_counter: Counter = Counter()
        card_faction_spread: Dict[str, Set[str]] = {}
        xp_spent_values: List[int] = []

        for deck in decks:
            inv_code = deck.investigator_code
            all_inv_counter[inv_code] += 1
            faction = inv_lookup.get(inv_code, {}).get("faction_code", "neutral")
            faction_counter[faction] += 1
            if deck.xp_spent is not None:
                xp_spent_values.append(deck.xp_spent)
            try:
                created = datetime.fromisoformat(deck.date_creation.replace("Z", "+00:00"))
                created = created.replace(tzinfo=None)
            except Exception:
                created = None
            if created:
                if created >= cutoff_recent:
                    recent_inv_counter[inv_code] += 1
                elif created >= cutoff_prior:
                    prior_inv_counter[inv_code] += 1
            for card_code in deck.slots:
                if card_code == inv_code:
                    continue
                # Normalize reprints to their original code so counts are merged
                canonical = reprint_map.get(card_code, card_code)
                card_counter[canonical] += 1
                if canonical not in card_faction_spread:
                    card_faction_spread[canonical] = set()
                card_faction_spread[canonical].add(faction)

        return (
            recent_inv_counter, prior_inv_counter, all_inv_counter,
            card_counter, faction_counter, card_faction_spread, xp_spent_values,
            inv_lookup,
        )

    (
        recent_inv_counter, prior_inv_counter, all_inv_counter,
        card_counter, faction_counter, card_faction_spread, xp_spent_values,
        inv_lookup,
    ) = await asyncio.to_thread(_crunch, decks, investigators, reprint_map)

    total_decks = len(decks)
    now = datetime.utcnow()

    # Single bulk DB query for top-40 card metadata (replaces 40 individual queries)
    top_card_codes = [c for c, _ in card_counter.most_common(40)]
    card_meta = await _bulk_card_metadata(top_card_codes, card_service)

    # Bucket cards by type
    assets_counter: Counter = Counter()
    events_counter: Counter = Counter()
    skills_counter: Counter = Counter()
    level0_counter: Counter = Counter()
    upgraded_counter: Counter = Counter()

    for code in top_card_codes:
        count = card_counter[code]
        meta = card_meta.get(code, {})
        if meta.get("subtype_code") == "basicweakness":
            continue
        type_code = meta.get("type_code", "")
        xp = meta.get("xp") or 0

        if type_code == "asset":
            assets_counter[code] = count
        elif type_code == "event":
            events_counter[code] = count
        elif type_code == "skill":
            skills_counter[code] = count

        if xp == 0:
            level0_counter[code] = count
        else:
            upgraded_counter[code] = count

    # Most versatile: included across 3+ faction types
    versatile_cards = []
    for code in top_card_codes:
        spread = card_faction_spread.get(code, set())
        if len(spread) >= 3:
            meta = card_meta.get(code, {})
            if meta.get("subtype_code") == "basicweakness":
                continue
            versatile_cards.append({
                "code": code,
                "name": meta.get("name", code),
                "type_code": meta.get("type_code", ""),
                "factions": sorted(spread),
                "faction_count": len(spread),
                "deck_count": card_counter[code],
                "inclusion_rate": round(card_counter[code] / total_decks, 3),
            })
    versatile_cards.sort(key=lambda x: x["faction_count"], reverse=True)
    versatile_cards = versatile_cards[:6]

    def _card_list(counter: Counter, limit: int) -> List[Dict]:
        result = []
        for code, count in counter.most_common(limit * 2):  # overfetch to allow filtering
            if len(result) >= limit:
                break
            meta = card_meta.get(code, {})
            if meta.get("subtype_code") == "basicweakness":
                continue
            result.append({
                "code": code,
                "name": meta.get("name", code),
                "type_code": meta.get("type_code", ""),
                "faction_code": meta.get("faction_code", ""),
                "xp": meta.get("xp") or 0,
                "deck_count": count,
                "inclusion_rate": round(count / total_decks, 3),
            })
        return result

    # XP distribution
    xp_dist = {"0": 0, "1-5": 0, "6-15": 0, "16+": 0}
    for xp in xp_spent_values:
        if xp == 0:
            xp_dist["0"] += 1
        elif xp <= 5:
            xp_dist["1-5"] += 1
        elif xp <= 15:
            xp_dist["6-15"] += 1
        else:
            xp_dist["16+"] += 1

    avg_xp = round(sum(xp_spent_values) / len(xp_spent_values), 1) if xp_spent_values else 0

    top_investigators = _top_investigators(all_inv_counter, inv_lookup, total_decks, 10)
    faction_meta = {
        faction: round(count / total_decks * 100, 1)
        for faction, count in faction_counter.most_common()
    }

    rising = _trending(recent_inv_counter, prior_inv_counter, inv_lookup, "rising", 5)
    falling = _trending(recent_inv_counter, prior_inv_counter, inv_lookup, "falling", 5)
    top_inv = top_investigators[0] if top_investigators else None

    result = {
        "meta": {
            "decks_analyzed": total_decks,
            "days": days,
            "generated_at": now.isoformat(),
        },
        "top_investigators": top_investigators,
        "most_popular_cards": _card_list(card_counter, 15),
        "card_stats": {
            "top_assets": _card_list(assets_counter, 8),
            "top_events": _card_list(events_counter, 8),
            "top_skills": _card_list(skills_counter, 8),
            "top_level_0": _card_list(level0_counter, 5),
            "top_upgraded": _card_list(upgraded_counter, 5),
            "most_versatile": versatile_cards,
            "avg_xp_per_deck": avg_xp,
            "xp_distribution": xp_dist,
        },
        "faction_meta_share": faction_meta,
        "trending": {"rising": rising, "falling": falling},
        "highlight": _highlight(top_inv, top_investigators, faction_meta, total_decks, avg_xp),
    }

    if redis_client.is_connected:
        await redis_client.set(cache_key, result, expire=seconds_until_next_sunday_midnight())

    response.headers.update(ARKHAM_HEADERS)
    response.headers["X-Cache"] = "MISS"
    return result


async def _build_reprint_map(card_service: CardService) -> Dict[str, str]:
    """
    Returns {reprint_code: original_code} for every card that is a reprint.
    Originals carry duplicated_by=[...]; reprints have no duplicated_by.
    """
    try:
        stmt = select(CardModel.code, CardModel.duplicated_by).where(
            CardModel.duplicated_by.isnot(None)
        )
        result = await card_service.db.execute(stmt)
        mapping: Dict[str, str] = {}
        for original_code, duped_by in result:
            for reprint_code in (duped_by or []):
                mapping[reprint_code] = original_code
        return mapping
    except Exception as e:
        print(f"Reprint map build failed: {e}")
        return {}


async def _bulk_card_metadata(codes: List[str], card_service: CardService) -> Dict[str, Dict]:
    """Single IN query for all card metadata — replaces N individual get_first calls."""
    if not codes:
        return {}
    try:
        stmt = select(CardModel).where(CardModel.code.in_(codes))
        result = await card_service.db.execute(stmt)
        cards = result.scalars().all()
        return {
            card.code: {
                "name": card.name or card.code,
                "type_code": card.type_code or "",
                "faction_code": card.faction_code or "",
                "xp": getattr(card, "xp", None) or 0,
                "subtype_code": getattr(card, "subtype_code", None) or "",
            }
            for card in cards
        }
    except Exception as e:
        print(f"Card metadata bulk fetch failed: {e}")
        return {}


def _top_investigators(counter, inv_lookup, total_decks, limit):
    result = []
    for code, count in counter.most_common(limit):
        info = inv_lookup.get(code, {})
        result.append({
            "code": code,
            "name": info.get("name", code),
            "faction": info.get("faction_code", "neutral"),
            "deck_count": count,
            "meta_share": round(count / total_decks * 100, 1),
        })
    return result


def _trending(recent, prior, inv_lookup, direction, limit):
    all_codes = set(recent.keys()) | set(prior.keys())
    changes = []
    for code in all_codes:
        r, p = recent[code], prior[code]
        change = (r - p) / p if p > 0 else (r if r > 0 else 0)
        changes.append((code, r, p, change))
    changes.sort(key=lambda x: x[3], reverse=(direction == "rising"))

    result = []
    for code, r, p, change in changes:
        if len(result) >= limit:
            break
        if direction == "rising" and change <= 0:
            continue
        if direction == "falling" and change >= 0:
            continue
        info = inv_lookup.get(code, {})
        result.append({
            "code": code,
            "name": info.get("name", code),
            "faction": info.get("faction_code", "neutral"),
            "recent_decks": r,
            "prior_decks": p,
            "change_pct": round(change * 100, 1),
        })
    return result


def _highlight(top_inv, top_investigators, faction_meta, total_decks, avg_xp):
    if not top_inv:
        return {}
    top_faction = max(faction_meta, key=lambda f: faction_meta[f]) if faction_meta else None
    return {
        "most_played_investigator": top_inv,
        "dominant_faction": {"faction": top_faction, "share": faction_meta.get(top_faction, 0)} if top_faction else None,
        "runner_up": top_investigators[1] if len(top_investigators) > 1 else None,
        "total_decks_analyzed": total_decks,
        "avg_xp_per_deck": avg_xp,
    }


def _empty_response(days):
    return {
        "meta": {"decks_analyzed": 0, "days": days, "generated_at": datetime.utcnow().isoformat()},
        "top_investigators": [],
        "most_popular_cards": [],
        "card_stats": {
            "top_assets": [], "top_events": [], "top_skills": [],
            "top_level_0": [], "top_upgraded": [], "most_versatile": [],
            "avg_xp_per_deck": 0, "xp_distribution": {},
        },
        "faction_meta_share": {},
        "trending": {"rising": [], "falling": []},
        "highlight": {},
    }
