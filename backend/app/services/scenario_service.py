import asyncio
from typing import Dict, List, Optional, Any, cast
from datetime import datetime
import json
from fastapi import HTTPException
import httpx
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.encounter_model import (
    EncounterCardModel,
    EncounterScenarioSetModel,
    ScenarioModel,
)
from app.models.arkham_model import CardModel, EncounterSetModel
from app.repositories.base_repositories import BaseRepository


from app.adapters.card_adapters import UnifiedCardAdapter
from domain.card import EncounterCard
from domain.scenario.rules import (
    get_encounter_set,
    get_encounter_sets_for_scenario,
    get_encounter_set_by_name,
)
from domain.Token.chaos_bag import ChaosBag
from domain.difficulty import Difficulty
from app.schemas.card_schema import CardSchema, ScenarioContext
from domain.scenarios import ScenarioType, get_scenario_campaign
from domain.scenario.factories import ScenarioFactory


class ScenarioService:
    def __init__(
        self,
        db: AsyncSession,
        card_repo: Optional[BaseRepository[CardModel]],
        encounter_set_repo: Optional[BaseRepository[EncounterSetModel]],
    ):
        self.arkhamdb_base_url = "https://arkhamdb.com/api/public"
        self.scenario_cache = {}
        self.db = db
        self.card_repo = card_repo or BaseRepository(CardModel, db)
        self.encounter_set_repo = encounter_set_repo or BaseRepository(
            EncounterSetModel, db
        )

    async def yield_scenario_context(
        self,
        scenario_code: ScenarioType,
        difficulty: Difficulty,
        no_of_investigators: int,
    ) -> Any:
        """Get complete scenario context with caching"""
        cache_key = f"{scenario_code}_{difficulty.__str__()}"

        if cache_key in self.scenario_cache:
            return self.scenario_cache[cache_key]
        encounter_set_of_scenario = get_encounter_set_by_name(scenario_code.__str__())
        print(
            "encounter_set_of_scenario is",
            encounter_set_of_scenario,
            scenario_code.name,
        )
        encounter_set_used_for_scenario = get_encounter_sets_for_scenario(scenario_code)
        encounter_set_of_scenario_record = await self.encounter_set_repo.get_first(
            filters={"filter_by[name][equals]": encounter_set_of_scenario["name"]}
        )
        print("encounter_set_used_for_scenario", encounter_set_used_for_scenario)
        encounter_cards = await self.card_repo.get_all(
            filter_by={"filter_by[encounter_code][in]": encounter_set_used_for_scenario}
        )
        print(
            "encounter_set_of_scenario",
            scenario_code.__str__(),
            encounter_set_of_scenario,
            encounter_set_of_scenario_record,
        )
        scenarioCard = await self.card_repo.get_first(
            filters={
                "filter_by[type_code][equals]": "scenario",
                "filter_by[encounter_code][equals]": (
                    encounter_set_of_scenario_record.code
                    if encounter_set_of_scenario_record
                    else None
                ),
            },
            # include=["traits", "linked_card", "bonded_cards.bonded_card"],
        )
        print("encounter_cards", encounter_cards)
        if not scenarioCard:
            raise HTTPException(status_code=404, detail="Scenario not found")
        return ScenarioFactory.create_scenario(
            campaign_chaos_bag=ChaosBag(),
            player_count=no_of_investigators,
            campaign_type=get_scenario_campaign(scenario_code),
            scenario_type=scenario_code,
            difficulty=difficulty,
            encounter_cards=[
                cast(
                    EncounterCard,
                    UnifiedCardAdapter().schema_to_domain(
                        schema=CardSchema.from_model(card)
                    ),
                )
                for card in encounter_cards
            ],
        ).to_dict()
        # return ScenarioContext(
        #     scenario_code=scenarioCard.code,
        #     scenario_name=scenarioCard.name,
        #     campaign=get_scenario_campaign(scenario_code),
        #     pack=scenarioCard.pack_code,
        #     difficulty=difficulty,
        # )
        # if scenario and scenario.context_cache:
        #     context = scenario.context_cache
        #     context = self._adjust_for_difficulty(context, difficulty)
        #     self.scenario_cache[cache_key] = context
        #     return context

        # # Build context from scratch
        # context = await self._build_scenario_context(scenario_code)

        # # Cache in database
        # if scenario:
        #     scenario.context_cache = context
        #     scenario.context_updated_at = datetime.utcnow().isoformat()
        # else:
        #     new_scenario = ScenarioModel(
        #         code=scenario_code,
        #         context_cache=context,
        #         context_updated_at=datetime.utcnow().isoformat(),
        #     )
        #     db.add(new_scenario)
        # db.commit()

        # # Adjust for difficulty and cache
        # context = self._adjust_for_difficulty(context, difficulty)
        # self.scenario_cache[cache_key] = context
        # return context

    async def _build_scenario_context(self, scenario_code: str) -> Dict[str, Any]:
        """Build scenario context from ArkhamDB data and hardcoded knowledge"""
        if scenario_code == "01104":  # The Gathering
            return await self._build_gathering_context()
        elif scenario_code == "01120":  # The Midnight Masks
            return await self._build_midnight_masks_context()
        elif scenario_code == "01141":  # The Devourer Below
            return await self._build_devourer_below_context()
        else:
            # Generic scenario context
            return await self._build_generic_context(scenario_code)

    async def _build_gathering_context(self) -> Dict[str, Any]:
        """Build The Gathering scenario context with all the data we discussed"""

        # Get encounter card data from database
        db = next(get_db())
        gathering_enemies = await self._get_gathering_enemy_stats(db)
        gathering_locations = await self._get_gathering_location_stats(db)

        return {
            # Basic Info
            "scenario_code": "01104",
            "scenario_name": "The Gathering",
            "campaign": "Night of the Zealot",
            "pack": "Core Set",
            "difficulty_available": ["Easy", "Standard", "Hard", "Expert"],
            # Enemy Stats (calculated from actual data or hardcoded)
            "avg_enemy_health": 1.75,
            "avg_enemy_fight": 2.25,
            "avg_enemy_evade": 2.5,
            "elite_enemy_count": 0,
            "enemy_damage_range": [1, 1],
            "enemy_horror_range": [0, 1],
            "primary_enemy_type": "Ghoul",
            # Location Stats
            "location_count": 6,
            "avg_clues_per_location": 1.33,
            "avg_shroud_value": 1.83,
            "locked_doors": True,
            "special_movement_rules": False,
            "total_clues_in_scenario": 8,  # Per investigator
            # Chaos Bag (Standard difficulty - will be adjusted)
            "chaos_tokens": {
                "+1": 2,
                "0": 3,
                "-1": 4,
                "-2": 2,
                "-3": 1,
                "-4": 1,
                "skull": 2,
                "cultist": 1,
                "tablet": 1,
                "elder_thing": 1,
                "auto_fail": 1,
                "elder_sign": 1,
            },
            # Special token effects
            "special_token_effects": {
                "skull": {
                    "effect": "neg_ghoul_count",
                    "description": "-X where X = number of Ghoul enemies at your location",
                },
                "cultist": {
                    "effect": "horror_on_fail",
                    "description": "-1. If you fail, take 1 horror",
                },
                "tablet": {
                    "effect": "damage_if_ghoul",
                    "description": "-2. If there is a Ghoul enemy at your location, take 1 damage",
                },
            },
            # Scenario Mechanics
            "doom_threshold": 7,
            "agenda_count": 1,
            "act_count": 1,
            "special_rules": ["Ghouls multiply", "Locked doors", "Ghoul-based tokens"],
            "victory_conditions": "clue_gathering",
            # Encounter Composition
            "encounter_sets": [
                "torch",
                "rats",
                "ghouls",
                "striking_fear",
                "ancient_evils",
            ],
            "treachery_count": 8,
            "enemy_spawn_rate": "medium",
            # Resource Economy Context
            "scenario_length": "short",  # 30-45 min
            "resource_scarcity": "normal",
            "card_draw_availability": "low",
            "action_economy_stress": "low",
            "tempo": "slow_buildup",  # Starts easy, ramps up
            # Difficulty scaling factors
            "difficulty_modifiers": {
                "Easy": {"enemy_health": 0.9, "chaos_modifier": 1.2},
                "Standard": {"enemy_health": 1.0, "chaos_modifier": 1.0},
                "Hard": {"enemy_health": 1.1, "chaos_modifier": 0.8},
                "Expert": {"enemy_health": 1.2, "chaos_modifier": 0.6},
            },
        }

    async def _get_gathering_enemy_stats(self, db: Session) -> Dict[str, Any]:
        """Get enemy statistics from database or return hardcoded values"""

        # Try to get from database first
        enemy_cards = (
            db.query(EncounterCardModel)
            .filter(
                EncounterCardModel.encounter_code.in_(["torch", "rats", "ghouls"]),
                EncounterCardModel.type_code == "enemy",
            )
            .all()
        )

        if enemy_cards:
            total_enemies = len(enemy_cards)
            avg_health = sum(card.health or 0 for card in enemy_cards) / total_enemies
            avg_fight = sum(card.fight or 0 for card in enemy_cards) / total_enemies
            avg_evade = sum(card.evade or 0 for card in enemy_cards) / total_enemies

            return {
                "avg_enemy_health": avg_health,
                "avg_enemy_fight": avg_fight,
                "avg_enemy_evade": avg_evade,
                "enemy_count": total_enemies,
            }
        else:
            # Hardcoded fallback data (The Gathering enemies)
            gathering_enemies = [
                {
                    "name": "Ghoul Minion",
                    "health": 1,
                    "fight": 2,
                    "evade": 3,
                    "damage": 1,
                    "horror": 1,
                },
                {
                    "name": "Swarm of Rats",
                    "health": 1,
                    "fight": 1,
                    "evade": 3,
                    "damage": 1,
                    "horror": 0,
                },
                {
                    "name": "Icy Ghoul",
                    "health": 3,
                    "fight": 4,
                    "evade": 2,
                    "damage": 1,
                    "horror": 1,
                },
                {
                    "name": "Flesh-Eater",
                    "health": 2,
                    "fight": 2,
                    "evade": 2,
                    "damage": 1,
                    "horror": 0,
                },
            ]

            total_enemies = len(gathering_enemies)
            avg_health = (
                sum(e["health"] for e in gathering_enemies) / total_enemies
            )  # 1.75
            avg_fight = (
                sum(e["fight"] for e in gathering_enemies) / total_enemies
            )  # 2.25
            avg_evade = (
                sum(e["evade"] for e in gathering_enemies) / total_enemies
            )  # 2.5

            return {
                "avg_enemy_health": avg_health,
                "avg_enemy_fight": avg_fight,
                "avg_enemy_evade": avg_evade,
                "enemy_count": total_enemies,
            }

    async def _get_gathering_location_stats(self, db: Session) -> Dict[str, Any]:
        """Get location statistics from database or return hardcoded values"""

        # Try to get from database
        location_cards = (
            db.query(EncounterCardModel)
            .filter(
                EncounterCardModel.encounter_code == "torch",
                EncounterCardModel.type_code == "location",
            )
            .all()
        )

        if location_cards:
            total_locations = len(location_cards)
            avg_shroud = (
                sum(card.shroud or 0 for card in location_cards) / total_locations
            )
            avg_clues = (
                sum(card.clues_per_investigator or 0 for card in location_cards)
                / total_locations
            )

            return {
                "location_count": total_locations,
                "avg_shroud_value": avg_shroud,
                "avg_clues_per_location": avg_clues,
            }
        else:
            # Hardcoded The Gathering locations
            gathering_locations = [
                {"name": "Study", "shroud": 2, "clues_per_investigator": 2},
                {"name": "Hallway", "shroud": 1, "clues_per_investigator": 1},
                {"name": "Attic", "shroud": 1, "clues_per_investigator": 1},
                {"name": "Cellar", "shroud": 4, "clues_per_investigator": 2},
                {"name": "Parlor", "shroud": 1, "clues_per_investigator": 1},
                {"name": "Bathroom", "shroud": 2, "clues_per_investigator": 1},
            ]

            avg_shroud = sum(loc["shroud"] for loc in gathering_locations) / len(
                gathering_locations
            )  # 1.83
            avg_clues = sum(
                loc["clues_per_investigator"] for loc in gathering_locations
            ) / len(
                gathering_locations
            )  # 1.33

            return {
                "location_count": len(gathering_locations),
                "avg_shroud_value": avg_shroud,
                "avg_clues_per_location": avg_clues,
            }

    def _adjust_for_difficulty(
        self, context: Dict[str, Any], difficulty: str
    ) -> Dict[str, Any]:
        """Adjust scenario context based on difficulty level"""
        adjusted_context = context.copy()

        # Adjust chaos bag
        if difficulty == "Easy":
            adjusted_context["chaos_tokens"] = {
                "+1": 3,
                "0": 4,
                "-1": 3,
                "-2": 1,
                "-3": 0,
                "-4": 0,
                "skull": 2,
                "cultist": 1,
                "tablet": 1,
                "elder_thing": 1,
                "auto_fail": 1,
                "elder_sign": 1,
            }
        elif difficulty == "Hard":
            adjusted_context["chaos_tokens"] = {
                "+1": 1,
                "0": 2,
                "-1": 4,
                "-2": 3,
                "-3": 2,
                "-4": 1,
                "-5": 1,
                "skull": 2,
                "cultist": 1,
                "tablet": 1,
                "elder_thing": 1,
                "auto_fail": 1,
                "elder_sign": 1,
            }
        elif difficulty == "Expert":
            adjusted_context["chaos_tokens"] = {
                "+1": 0,
                "0": 1,
                "-1": 3,
                "-2": 3,
                "-3": 2,
                "-4": 2,
                "-5": 1,
                "-6": 1,
                "skull": 2,
                "cultist": 1,
                "tablet": 1,
                "elder_thing": 1,
                "auto_fail": 1,
                "elder_sign": 1,
            }

        # Adjust special token effects for difficulty
        if difficulty in ["Hard", "Expert"]:
            if "special_token_effects" in adjusted_context:
                if difficulty == "Hard":
                    adjusted_context["special_token_effects"]["cultist"][
                        "description"
                    ] = "-2. If you fail, take 1 horror"
                    adjusted_context["special_token_effects"]["tablet"][
                        "description"
                    ] = "-3. If there is a Ghoul enemy at your location, take 1 damage"
                elif difficulty == "Expert":
                    adjusted_context["special_token_effects"]["skull"][
                        "description"
                    ] = "-2. If you fail, after this skill test, search the encounter deck and discard pile for a Ghoul enemy, and draw it"
                    adjusted_context["special_token_effects"]["cultist"][
                        "description"
                    ] = "Reveal another token. If you fail, take 2 horror"
                    adjusted_context["special_token_effects"]["tablet"][
                        "description"
                    ] = "-4. If there is a Ghoul enemy at your location, take 1 damage and 1 horror"

        return adjusted_context

    async def _build_midnight_masks_context(self) -> Dict[str, Any]:
        """Placeholder for Midnight Masks scenario context"""
        return {
            "scenario_code": "01120",
            "scenario_name": "The Midnight Masks",
            "campaign": "Night of the Zealot",
            # Add more context here
        }

    async def _build_devourer_below_context(self) -> Dict[str, Any]:
        """Placeholder for Devourer Below scenario context"""
        return {
            "scenario_code": "01141",
            "scenario_name": "The Devourer Below",
            "campaign": "Night of the Zealot",
            # Add more context here
        }

    async def _build_generic_context(self, scenario_code: str) -> Dict[str, Any]:
        """Generic scenario context for unknown scenarios"""
        return {
            "scenario_code": scenario_code,
            "scenario_name": "Unknown Scenario",
            "avg_enemy_health": 3.0,
            "avg_enemy_fight": 3.0,
            "avg_enemy_evade": 3.0,
            "avg_shroud_value": 3.0,
            "chaos_tokens": {
                "+1": 2,
                "0": 3,
                "-1": 4,
                "-2": 2,
                "-3": 1,
                "-4": 1,
                "skull": 2,
                "cultist": 1,
                "tablet": 1,
                "elder_thing": 1,
                "auto_fail": 1,
                "elder_sign": 1,
            },
        }

    async def populate_encounter_cards_from_arkhamdb(self):
        """Fetch and populate encounter cards from ArkhamDB API"""
        db = next(get_db())

        async with httpx.AsyncClient() as client:
            # Get all cards from ArkhamDB
            response = await client.get(f"{self.arkhamdb_base_url}/cards/")
            response.raise_for_status()
            cards_data = response.json()

            encounter_cards = []
            encounter_sets = set()

            for card in cards_data:
                # Only process encounter cards (non-player cards)
                if card.get("type_code") in [
                    "enemy",
                    "treachery",
                    "location",
                ] and card.get("encounter_code"):
                    encounter_sets.add(card.get("encounter_code"))

                    encounter_card = EncounterCardModel(
                        code=card["code"],
                        name=card.get("name"),
                        encounter_code=card.get("encounter_code"),
                        type_code=card.get("type_code"),
                        subtype_code=card.get("subtype_code"),
                        text=card.get("text"),
                        pack_code=card.get("pack_code"),
                        quantity=card.get("quantity", 1),
                        # Enemy stats
                        health=card.get("health"),
                        health_per_investigator=card.get("health_per_investigator"),
                        fight=card.get("enemy_fight"),
                        evade=card.get("enemy_evade"),
                        damage=card.get("enemy_damage"),
                        horror=card.get("enemy_horror"),
                        # Location stats
                        shroud=card.get("shroud"),
                        clues=card.get("clues"),
                        clues_per_investigator=card.get("clues_per_investigator"),
                        # Additional properties
                        traits=(
                            card.get("traits", "").split(". ")
                            if card.get("traits")
                            else []
                        ),
                        victory=card.get("victory"),
                        vengeance=card.get("vengeance"),
                        doom=card.get("doom"),
                    )
                    encounter_cards.append(encounter_card)

            # Create encounter sets
            for set_code in encounter_sets:
                existing_set = (
                    db.query(EncounterScenarioSetModel)
                    .filter(EncounterScenarioSetModel.code == set_code)
                    .first()
                )
                if not existing_set:
                    encounter_set = EncounterScenarioSetModel(
                        code=set_code, name=set_code.title()
                    )
                    db.add(encounter_set)

            # Add all encounter cards
            for card in encounter_cards:
                existing_card = (
                    db.query(EncounterCardModel)
                    .filter(EncounterCardModel.code == card.code)
                    .first()
                )
                if not existing_card:
                    db.add(card)

            db.commit()
            print(
                f"Populated {len(encounter_cards)} encounter cards and {len(encounter_sets)} encounter sets"
            )

    async def refresh_scenario_cache(self, scenario_code: str = None):
        """Refresh scenario context cache"""
        db = next(get_db())

        if scenario_code:
            # Refresh specific scenario
            scenario = (
                db.query(ScenarioModel)
                .filter(ScenarioModel.code == scenario_code)
                .first()
            )
            if scenario:
                context = await self._build_scenario_context(scenario_code)
                scenario.context_cache = context
                scenario.context_updated_at = datetime.utcnow().isoformat()
                db.commit()
                # Clear memory cache
                keys_to_remove = [
                    key
                    for key in self.scenario_cache.keys()
                    if key.startswith(scenario_code)
                ]
                for key in keys_to_remove:
                    del self.scenario_cache[key]
        else:
            # Refresh all scenarios
            scenarios = db.query(ScenarioModel).all()
            for scenario in scenarios:
                context = await self._build_scenario_context(scenario.code)
                scenario.context_cache = context
                scenario.context_updated_at = datetime.utcnow().isoformat()
            db.commit()
            self.scenario_cache.clear()
