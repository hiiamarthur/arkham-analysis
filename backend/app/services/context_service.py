from typing import Optional, Dict, Any
from app.schemas.context_schema import GameContextSchema
from app.services.cache_service import cache_service


class ContextService:
    """Service for managing game context for GPT analysis"""

    def __init__(self):
        self.cache_service = cache_service
        self.cache_prefix = "game_context"

    async def store_game_context(
        self, game_context: GameContextSchema, session_id: Optional[str] = None
    ) -> GameContextSchema:
        """Store game context for analysis"""
        cache_key = f"{self.cache_prefix}:{session_id or 'default'}"
        
        # Convert to dict for storage
        context_data = game_context.dict()
        
        # Store in cache with shorter TTL (2 hours) since game state changes frequently
        await self.cache_service.set_with_key(
            "game_contexts", cache_key, context_data, ttl=7200
        )
        
        return game_context

    async def get_game_context(
        self, session_id: Optional[str] = None
    ) -> Optional[GameContextSchema]:
        """Retrieve game context"""
        cache_key = f"{self.cache_prefix}:{session_id or 'default'}"
        
        try:
            context_data = await self.cache_service.get_with_key(
                "game_contexts", cache_key
            )
            
            if context_data:
                return GameContextSchema(**context_data)
            
            return None
            
        except Exception as e:
            print(f"Error retrieving game context: {e}")
            return None

    async def update_game_context(
        self, session_id: Optional[str], game_context: GameContextSchema
    ) -> GameContextSchema:
        """Update existing game context"""
        return await self.store_game_context(game_context, session_id)

    async def delete_game_context(self, session_id: Optional[str] = None):
        """Delete game context"""
        cache_key = f"{self.cache_prefix}:{session_id or 'default'}"
        
        try:
            await self.cache_service.delete_with_key("game_contexts", cache_key)
        except Exception as e:
            print(f"Error deleting game context: {e}")
            raise

    def format_for_gpt_analysis(self, game_context: GameContextSchema) -> str:
        """Format game context as a structured prompt for GPT analysis"""
        
        prompt = f"""
# Current Game State Analysis

## Scenario Information
- **Scenario**: {game_context.current_scenario}
- **Act**: {game_context.current_act} | **Agenda**: {game_context.current_agenda}
- **Difficulty**: {game_context.scenario_difficulty}
- **Phase**: {game_context.current_phase}
- **Turn**: {game_context.turn_number}

## Doom Pressure
- **Doom on Agenda**: {game_context.doom_on_agenda}/{game_context.doom_threshold}
- **Total Doom in Play**: {game_context.total_doom_in_play}
- **Turns until Agenda Advances**: {game_context.doom_threshold - game_context.doom_on_agenda}

## Investigators
"""
        
        for inv in game_context.investigators:
            is_active = "🎯 " if inv.investigator_code == game_context.active_investigator else ""
            prompt += f"""
{is_active}**{inv.investigator_code}**:
- Health: {inv.current_health}/{inv.max_health}
- Sanity: {inv.current_sanity}/{inv.max_sanity}
- Resources: {inv.current_resources}
- Actions: {inv.current_actions}
- Location: {inv.location_code}
- Engaged: {inv.is_engaged}
"""

        if game_context.enemies_in_play:
            prompt += "\n## Enemies in Play\n"
            for enemy in game_context.enemies_in_play:
                prompt += f"""
- **{enemy.enemy_code}**: {enemy.current_health}/{enemy.max_health} HP
  - Location: {enemy.location_code}
  - Engaged with: {enemy.engaged_with}
  - Status: {'Exhausted' if enemy.is_exhausted else 'Ready'}
"""

        if game_context.locations_in_play:
            prompt += "\n## Locations\n"
            for location in game_context.locations_in_play:
                prompt += f"""
- **{location.location_code}** ({location.status}): {location.current_clues} clues
  - Investigators: {', '.join(location.investigators_here)}
  - Enemies: {', '.join(location.enemies_here)}
"""

        if game_context.treacheries_in_play:
            prompt += "\n## Active Treacheries\n"
            for treachery in game_context.treacheries_in_play:
                prompt += f"- **{treachery.treachery_code}** (attached to {treachery.attached_to})\n"

        if game_context.special_rules_active:
            prompt += f"\n## Special Rules Active\n"
            for rule in game_context.special_rules_active:
                prompt += f"- {rule}\n"

        prompt += f"""
## Analysis Question
{game_context.analysis_question}

## Available Actions
{', '.join(game_context.available_actions) if game_context.available_actions else 'Standard investigator actions'}

Please analyze this game state and provide strategic recommendations for the active investigator.
"""
        
        return prompt

    def calculate_threat_level(self, game_context: GameContextSchema) -> Dict[str, Any]:
        """Calculate current threat level based on game state"""
        
        threat_factors = {
            "doom_pressure": 0,
            "enemy_pressure": 0,
            "health_pressure": 0,
            "sanity_pressure": 0,
            "resource_pressure": 0
        }
        
        # Doom pressure (0-1 scale)
        doom_ratio = game_context.doom_on_agenda / game_context.doom_threshold
        threat_factors["doom_pressure"] = min(doom_ratio, 1.0)
        
        # Enemy pressure
        engaged_enemies = sum(1 for enemy in game_context.enemies_in_play if enemy.engaged_with)
        threat_factors["enemy_pressure"] = min(engaged_enemies / len(game_context.investigators), 1.0)
        
        # Health/Sanity pressure
        total_health_ratio = 0
        total_sanity_ratio = 0
        for inv in game_context.investigators:
            total_health_ratio += inv.current_health / inv.max_health
            total_sanity_ratio += inv.current_sanity / inv.max_sanity
        
        threat_factors["health_pressure"] = 1 - (total_health_ratio / len(game_context.investigators))
        threat_factors["sanity_pressure"] = 1 - (total_sanity_ratio / len(game_context.investigators))
        
        # Resource pressure
        avg_resources = sum(inv.current_resources for inv in game_context.investigators) / len(game_context.investigators)
        threat_factors["resource_pressure"] = max(0, (3 - avg_resources) / 3)  # Assuming 3 is comfortable
        
        # Overall threat level
        overall_threat = sum(threat_factors.values()) / len(threat_factors)
        
        return {
            "overall_threat_level": overall_threat,
            "threat_factors": threat_factors,
            "threat_description": self._get_threat_description(overall_threat)
        }
    
    def _get_threat_description(self, threat_level: float) -> str:
        """Get human-readable threat description"""
        if threat_level < 0.2:
            return "Low - Situation is under control"
        elif threat_level < 0.4:
            return "Moderate - Some pressure building"
        elif threat_level < 0.6:
            return "High - Dangerous situation"
        elif threat_level < 0.8:
            return "Critical - Immediate action needed"
        else:
            return "Extreme - Emergency measures required"