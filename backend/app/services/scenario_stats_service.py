"""
Scenario Statistics Service - Pre-computed and dynamic game state analysis
"""
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from app.repositories.base_repositories import BaseRepository
from app.models.arkham_model import CardModel


@dataclass
class ScenarioStats:
    """Pre-computed scenario statistics"""
    total_enemies: int
    enemies_with_retaliate: int
    enemies_with_hunter: int
    total_treacheries: int
    treacheries_with_surge: int
    total_locations: int
    average_shroud: float
    total_doom_threshold: int
    victory_points_available: int
    
    # Threat analysis
    high_damage_enemies: int  # 3+ damage
    high_horror_enemies: int  # 3+ horror
    elusive_enemies: int      # Hard to fight
    
    # Resource analysis
    clue_locations: int
    total_clues_available: int
    
    def to_gpt_context_prompt(self) -> str:
        """Generate scenario-specific context for card analysis prompts"""
        # Calculate adjusted resource values based on scenario difficulty
        damage_value = 2.5 + (self.enemies_with_retaliate * 0.5)  # Higher if retaliate enemies
        clue_value = max(2.0, 2.5 - (self.average_shroud - 2) * 0.3)  # Lower if high shroud
        action_value = 2.0 + (self.treacheries_with_surge * 0.2)  # Higher if surge treacheries
        
        return f"""
SCENARIO CONTEXT FOR CARD ANALYSIS:
Threat Assessment: {self.total_enemies} enemies (avg health ~{self.total_enemies * 2.8:.0f}), {self.enemies_with_retaliate} with retaliate, {self.enemies_with_hunter} hunters
Investigation Requirements: {self.clue_locations} locations, {self.total_clues_available} total clues, average shroud {self.average_shroud:.1f}
Doom Pressure: {self.total_doom_threshold} doom threshold, {self.treacheries_with_surge} surge treacheries
Elite Threats: {self.high_damage_enemies} high-damage enemies, {self.elusive_enemies} elusive enemies

ADJUSTED RESOURCE VALUES:
- Damage prevention/healing: {damage_value:.1f} resources per point
- Clue gathering: {clue_value:.1f} resources per clue
- Action efficiency: {action_value:.1f} resources per action saved
- Fast effects: {action_value:.1f} resources (action savings crucial)
        """.strip()
    
    def get_card_analysis_modifiers(self) -> dict:
        """Get scenario-specific modifiers for card analysis"""
        return {
            "damage_value_multiplier": 1.0 + (self.enemies_with_retaliate * 0.2),
            "clue_value_multiplier": max(0.7, 1.0 - (self.average_shroud - 2) * 0.1),
            "action_value_multiplier": 1.0 + (self.treacheries_with_surge * 0.1),
            "movement_value_multiplier": 1.0 + (self.total_locations / 10.0),
            "combat_focus_weight": min(2.0, self.total_enemies / 5.0),
            "investigation_focus_weight": min(2.0, self.clue_locations / 3.0)
        }


class ScenarioStatsService:
    def __init__(self, card_repo: BaseRepository[CardModel]):
        self.card_repo = card_repo
        self._stats_cache: Dict[str, ScenarioStats] = {}
    
    async def get_scenario_stats(self, encounter_sets: List[str]) -> ScenarioStats:
        """Get pre-computed stats for a scenario"""
        cache_key = "_".join(sorted(encounter_sets))
        
        if cache_key in self._stats_cache:
            return self._stats_cache[cache_key]
        
        # Get all cards for the scenario
        cards = await self.card_repo.get_all(
            filter_by={"filter_by[encounter_code][in]": encounter_sets},
            items_per_page=-1
        )
        
        stats = self._compute_stats(cards)
        self._stats_cache[cache_key] = stats
        return stats
    
    def _compute_stats(self, cards: List[CardModel]) -> ScenarioStats:
        """Compute statistics from card list"""
        enemies = [c for c in cards if c.type_code == "enemy"]
        treacheries = [c for c in cards if c.type_code == "treachery"]
        locations = [c for c in cards if c.type_code == "location"]
        
        return ScenarioStats(
            total_enemies=len(enemies),
            enemies_with_retaliate=len([e for e in enemies if "retaliate" in (e.text or "").lower()]),
            enemies_with_hunter=len([e for e in enemies if "hunter" in (e.text or "").lower()]),
            total_treacheries=len(treacheries),
            treacheries_with_surge=len([t for t in treacheries if "surge" in (t.text or "").lower()]),
            total_locations=len(locations),
            average_shroud=sum(l.shroud or 0 for l in locations) / max(len(locations), 1),
            total_doom_threshold=self._calculate_doom_threshold(cards),
            victory_points_available=sum(c.victory or 0 for c in cards if c.victory),
            high_damage_enemies=len([e for e in enemies if (e.enemy_damage or 0) >= 3]),
            high_horror_enemies=len([e for e in enemies if (e.enemy_horror or 0) >= 3]),
            elusive_enemies=len([e for e in enemies if "elusive" in (e.text or "").lower()]),
            clue_locations=len([l for l in locations if (l.clues or 0) > 0]),
            total_clues_available=sum(l.clues or 0 for l in locations),
        )
    
    def _calculate_doom_threshold(self, cards: List[CardModel]) -> int:
        """Calculate doom threshold from agenda cards"""
        agendas = [c for c in cards if c.type_code == "agenda"]
        return sum(c.doom or 0 for c in agendas)
    
    async def query_dynamic_stat(self, encounter_sets: List[str], query: str) -> Dict[str, Any]:
        """Handle dynamic queries like 'enemies with spawn' """
        cards = await self.card_repo.get_all(
            filter_by={"filter_by[encounter_code][in]": encounter_sets},
            items_per_page=-1
        )
        
        query_lower = query.lower()
        
        if "retaliate" in query_lower:
            enemies = [c for c in cards if c.type_code == "enemy" and "retaliate" in (c.text or "").lower()]
            return {
                "count": len(enemies),
                "cards": [{"name": e.name, "damage": e.enemy_damage} for e in enemies],
                "summary": f"Found {len(enemies)} enemies with Retaliate"
            }
        
        elif "hunter" in query_lower:
            enemies = [c for c in cards if c.type_code == "enemy" and "hunter" in (c.text or "").lower()]
            return {
                "count": len(enemies),
                "cards": [{"name": e.name, "fight": e.enemy_fight} for e in enemies],
                "summary": f"Found {len(enemies)} enemies with Hunter"
            }
        
        elif "surge" in query_lower:
            treacheries = [c for c in cards if c.type_code == "treachery" and "surge" in (c.text or "").lower()]
            return {
                "count": len(treacheries),
                "cards": [{"name": t.name} for t in treacheries],
                "summary": f"Found {len(treacheries)} treacheries with Surge"
            }
        
        return {"error": "Query not recognized"}