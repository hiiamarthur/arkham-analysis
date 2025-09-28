from typing import Optional, Dict, Any, List
from app.schemas.context_schema import GameContextSchema
from app.schemas.gpt_schema import OpenAIRequest
from app.services.gpt_service import GPTService
from app.services.context_service import ContextService
from app.services.card_service import CardService
from domain.card.context.investigator_context import InvestigatorContext


class AnalysisService:
    """
    Context-aware card analysis service that modifies GPT system prompts
    based on game context, investigator context, and scenario context
    """

    def __init__(
        self,
        gpt_service: GPTService,
        context_service: ContextService,
        card_service: CardService,
    ):
        self.gpt_service = gpt_service
        self.context_service = context_service
        self.card_service = card_service
        self.base_system_prompt = self.gpt_service.system_messages["content"]

    async def analyze_card_strength(
        self,
        card_codes: List[str],
        game_context: Optional[GameContextSchema] = None,
        investigator_code: Optional[str] = None,
        campaign_context: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Analyze card strength with context-aware system prompt
        """
        # Build context-aware system prompt
        contextual_system_prompt = await self._build_contextual_system_prompt(
            game_context, investigator_code, campaign_context
        )
        
        # Analyze each card with the contextual prompt
        card_analyses = {}
        for card_code in card_codes:
            try:
                # Get card info first
                card_info = await self._get_card_info(card_code)
                
                # Create card analysis prompt
                card_prompt = f"Analyze the strength and value of card '{card_code}' ({card_info.get('name', 'Unknown')}) given the current context."
                
                # Run GPT analysis with contextual system prompt
                analysis = await self._run_contextual_gpt_analysis(
                    card_prompt, contextual_system_prompt
                )
                
                card_analyses[card_code] = {
                    "card_info": card_info,
                    "strength_analysis": analysis,
                }
                
            except Exception as e:
                card_analyses[card_code] = {
                    "error": f"Analysis failed: {str(e)}"
                }
        
        return {
            "analysis_type": "contextual_card_strength",
            "context_applied": {
                "has_game_context": game_context is not None,
                "has_investigator_context": investigator_code is not None,
                "has_campaign_context": campaign_context is not None,
            },
            "card_analyses": card_analyses
        }

    async def analyze_card_synergies(
        self,
        card_codes: List[str],
        investigator_code: Optional[str] = None,
        campaign_context: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """
        Analyze card synergies with investigator and campaign context
        """
        contextual_system_prompt = await self._build_contextual_system_prompt(
            None, investigator_code, campaign_context
        )
        
        # Create synergy analysis prompt
        card_list = ", ".join(card_codes)
        synergy_prompt = f"""
        Analyze the synergies between these cards: {card_list}
        
        Consider:
        1. Direct card interactions and combos
        2. Resource efficiency when used together
        3. Action economy improvements
        4. Timing and sequencing strategies
        5. Risk mitigation through redundancy
        """
        
        analysis = await self._run_contextual_gpt_analysis(
            synergy_prompt, contextual_system_prompt
        )
        
        return {
            "analysis_type": "card_synergy_analysis",
            "cards_analyzed": card_codes,
            "synergy_analysis": analysis
        }

    async def analyze_card_timing(
        self,
        card_codes: List[str],
        game_context: Optional[GameContextSchema] = None,
        investigator_code: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Analyze optimal timing for card usage given current game state
        """
        contextual_system_prompt = await self._build_contextual_system_prompt(
            game_context, investigator_code, None
        )
        
        timing_analyses = {}
        for card_code in card_codes:
            card_info = await self._get_card_info(card_code)
            
            timing_prompt = f"""
            Analyze the optimal timing for playing '{card_code}' ({card_info.get('name', 'Unknown')}).
            
            Consider:
            1. Current game state urgency and pressure
            2. Resource availability and opportunity cost
            3. Setup requirements and prerequisites
            4. Maximum impact scenarios
            5. Risk vs reward of waiting
            """
            
            analysis = await self._run_contextual_gpt_analysis(
                timing_prompt, contextual_system_prompt
            )
            
            timing_analyses[card_code] = {
                "card_info": card_info,
                "timing_analysis": analysis
            }
        
        return {
            "analysis_type": "card_timing_analysis",
            "timing_analyses": timing_analyses
        }

    async def _build_contextual_system_prompt(
        self,
        game_context: Optional[GameContextSchema] = None,
        investigator_code: Optional[str] = None,
        campaign_context: Optional[Dict] = None,
    ) -> str:
        """Build context-aware system prompt by filling template with dynamic values"""
        
        # Calculate context-specific axioms
        context_axioms = await self._calculate_context_axioms(
            game_context, investigator_code, campaign_context
        )
        
        # Fill the template with context-adjusted values
        contextual_prompt = self.base_system_prompt.format(**context_axioms)
        
        return contextual_prompt

    async def _calculate_context_axioms(
        self,
        game_context: Optional[GameContextSchema] = None,
        investigator_code: Optional[str] = None,
        campaign_context: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Calculate context-specific axioms to replace hardcoded values"""
        
        # Default axioms (comprehensive game mechanics)
        axioms = {
            # Combat axioms
            "avg_enemy_health": 3,
            "hits_to_kill": 2,
            "elite_health_multiplier": "5-6",
            "enemy_damage_range": "1-2",
            "enemy_horror_range": "1-2",
            
            # Investigation axioms
            "avg_clues_per_location": 2,
            "avg_shroud": 3,
            "investigation_target_number": 6,  # Skill + stat needed for ~75% success
            "skill_icon_value": 0.5,  # Each +1 skill icon worth ~0.5 resources
            
            # Chaos bag and test success axioms
            "base_success_rate": 60,  # Base success rate for balanced skill tests
            "skill_bonus_success_rate": 15,  # Each +1 skill increases success by ~15%
            "chaos_token_mitigation_value": 1.5,  # Ignore/redraw effects
            "auto_success_value": 3.0,  # Auto-success effects are very valuable
            
            # Survivability axioms
            "health_sanity_value": 1.5,  # Each health/sanity point worth
            "horror_heal_value": 2.0,  # Horror healing more valuable (harder to get)
            "damage_heal_value": 1.5,  # Damage healing value
            "trauma_prevention_value": 4.0,  # Preventing trauma is very valuable
            
            # Resource and action axioms
            "action_value": 2.0,
            "card_value": "1-2",
            "resource_acceleration_value": 0.8,  # Extra resources beyond 1-per-action
            "fast_card_value": 2.0,
            
            # Contextual values (adjusted by game state)
            "clue_value": 2.5,
            "damage_value": "2-2.5"
        }
        
        # Game context adjustments
        if game_context:
            # Analyze current enemies to adjust enemy axioms
            if game_context.enemies_in_play:
                total_health = sum(enemy.max_health for enemy in game_context.enemies_in_play)
                avg_health = total_health / len(game_context.enemies_in_play)
                axioms["avg_enemy_health"] = round(avg_health, 1)
                axioms["hits_to_kill"] = max(1, round(avg_health / 2))
            
            # Analyze locations to adjust location axioms
            if game_context.locations_in_play:
                revealed_locations = [loc for loc in game_context.locations_in_play if loc.status.value == "revealed"]
                if revealed_locations:
                    total_clues = sum(loc.current_clues for loc in revealed_locations)
                    investigator_count = len(game_context.investigators)
                    if investigator_count > 0:
                        axioms["avg_clues_per_location"] = round(total_clues / (len(revealed_locations) * investigator_count), 1)
            
            # Analyze locations to adjust investigation axioms
            if game_context.locations_in_play:
                revealed_locations = [loc for loc in game_context.locations_in_play if loc.status.value == "revealed"]
                if revealed_locations:
                    total_shroud = sum(getattr(loc, 'shroud', 3) for loc in revealed_locations)
                    avg_shroud_current = total_shroud / len(revealed_locations)
                    axioms["avg_shroud"] = round(avg_shroud_current, 1)
                    
                    # Adjust investigation target based on current shroud values
                    axioms["investigation_target_number"] = max(4, round(avg_shroud_current + 2))
            
            # Adjust resource values based on threat level
            threat_assessment = self.context_service.calculate_threat_level(game_context)
            threat_level = threat_assessment.get("overall_threat_level", 0)
            
            if threat_level > 0.7:  # Emergency - defensive values more important
                axioms["fast_card_value"] = 2.5
                axioms["damage_value"] = "2.5-3.0"
                axioms["health_sanity_value"] = 2.0  # Survivability more valuable
                axioms["trauma_prevention_value"] = 5.0
                axioms["auto_success_value"] = 4.0  # Reliability critical
            elif threat_level > 0.4:  # Moderate pressure
                axioms["health_sanity_value"] = 1.7
                axioms["chaos_token_mitigation_value"] = 2.0
            elif threat_level < 0.3:  # Stable - setup and efficiency more valuable
                axioms["action_value"] = 2.2  # Actions slightly more valuable for setup
                axioms["resource_acceleration_value"] = 1.0  # Economy building matters
                axioms["skill_icon_value"] = 0.7  # Commits more valuable when stable
        
        # Investigator context adjustments
        if investigator_code:
            try:
                investigator_context = await self._get_investigator_context(investigator_code)
                if investigator_context and investigator_context.primary_role:
                    role = investigator_context.primary_role
                    
                    if role == "seeker":
                        axioms["clue_value"] = 3.0  # Clues more valuable for seekers
                        axioms["card_value"] = "1.5-2.5"  # Better draw engines
                        axioms["skill_icon_value"] = 0.7  # Skill commits more valuable
                        axioms["investigation_target_number"] = 5  # Better at investigation
                        axioms["auto_success_value"] = 3.5  # Reliability matters for clue gathering
                    elif role == "fighter":
                        axioms["damage_value"] = "3.0-3.5"  # Damage more valuable for fighters
                        axioms["enemy_damage_range"] = "1-3"  # Expect tougher enemies
                        axioms["health_sanity_value"] = 2.0  # Need to tank damage
                        axioms["trauma_prevention_value"] = 5.0  # Trauma is devastating for fighters
                        axioms["chaos_token_mitigation_value"] = 2.2  # Combat reliability crucial
                    elif role == "support":
                        axioms["action_value"] = 1.8  # Actions less valuable, more about efficiency
                        axioms["fast_card_value"] = 2.2  # Fast effects help team coordination
                        axioms["resource_acceleration_value"] = 1.2  # Economy building for team
                        axioms["horror_heal_value"] = 2.5  # Support often handles horror
                    elif role == "mystic":
                        axioms["chaos_token_mitigation_value"] = 2.5  # Spells need reliability
                        axioms["auto_success_value"] = 4.0  # Mystics value consistency highly
                        axioms["horror_heal_value"] = 2.2  # Often deal with horror effects
                    elif role == "survivor":
                        axioms["skill_icon_value"] = 1.0  # Survivors rely heavily on commits
                        axioms["resource_acceleration_value"] = 0.5  # Used to resource scarcity
                        axioms["damage_heal_value"] = 2.2  # Good at self-healing
            except Exception:
                pass
        
        # Campaign context adjustments
        if campaign_context:
            campaign = campaign_context.get("campaign", "").lower()
            difficulty = campaign_context.get("difficulty", "standard")
            
            # Difficulty adjustments
            if difficulty == "expert":
                axioms["enemy_damage_range"] = "2-3"
                axioms["enemy_horror_range"] = "1-3"
                axioms["avg_enemy_health"] = axioms["avg_enemy_health"] * 1.2
                axioms["base_success_rate"] = 45  # Harder chaos bag
                axioms["health_sanity_value"] = 2.5  # Survivability critical
                axioms["trauma_prevention_value"] = 6.0  # Trauma devastating on expert
                axioms["auto_success_value"] = 5.0  # Reliability extremely valuable
                axioms["chaos_token_mitigation_value"] = 3.0
            elif difficulty == "hard":
                axioms["base_success_rate"] = 50
                axioms["health_sanity_value"] = 2.0
                axioms["trauma_prevention_value"] = 5.0
                axioms["chaos_token_mitigation_value"] = 2.5
            elif difficulty == "easy":
                axioms["enemy_damage_range"] = "1-2"
                axioms["avg_enemy_health"] = axioms["avg_enemy_health"] * 0.8
                axioms["base_success_rate"] = 75  # Easier chaos bag
                axioms["health_sanity_value"] = 1.0  # Less pressure
                axioms["trauma_prevention_value"] = 3.0
                axioms["skill_icon_value"] = 0.3  # Less need for skill icons
            
            # Campaign-specific adjustments
            if "forgotten_age" in campaign:
                axioms["enemy_damage_range"] = "1-3"  # Poison/hazards
                axioms["avg_shroud"] = 4  # Higher shroud values
                axioms["damage_value"] = "2.5-3.0"  # Damage prevention more valuable
                axioms["damage_heal_value"] = 2.5  # Poison healing crucial
                axioms["trauma_prevention_value"] = 5.5  # Explores/hazards cause trauma
                axioms["investigation_target_number"] = 7  # Harder investigation
            elif "path_to_carcosa" in campaign:
                axioms["enemy_horror_range"] = "2-4"  # Heavy horror focus
                axioms["clue_value"] = 2.8  # Slightly harder to get clues
                axioms["horror_heal_value"] = 3.0  # Horror healing extremely valuable
                axioms["trauma_prevention_value"] = 6.0  # Horror trauma common
                axioms["auto_success_value"] = 4.5  # Treacheries punish failure heavily
            elif "circle_undone" in campaign:
                axioms["chaos_token_mitigation_value"] = 3.0  # Cursed/blessed tokens
                axioms["skill_icon_value"] = 0.8  # Token manipulation important
                axioms["auto_success_value"] = 4.0  # Chaos bag variance high
            elif "dream_eaters" in campaign:
                axioms["horror_heal_value"] = 2.8  # Dream/reality horror effects
                axioms["card_value"] = "2-3"  # Complex card interactions
                axioms["investigation_target_number"] = 6  # Mixed investigation difficulty
            elif "innsmouth_conspiracy" in campaign:
                axioms["skill_icon_value"] = 0.9  # Blessed/cursed token interactions
                axioms["chaos_token_mitigation_value"] = 2.8
                axioms["resource_acceleration_value"] = 1.1  # Key resources important
            elif "night_of_the_zealot" in campaign:
                axioms["avg_shroud"] = 2  # Easier investigation
                axioms["enemy_damage_range"] = "1-2"  # Standard enemies
                axioms["base_success_rate"] = 65  # Beginner-friendly chaos bag
                axioms["trauma_prevention_value"] = 3.5  # Lower stakes
        
        return axioms

    async def _calculate_context_multipliers(
        self,
        game_context: Optional[GameContextSchema] = None,
        investigator_code: Optional[str] = None,
        campaign_context: Optional[Dict] = None,
    ) -> Dict[str, Any]:
        """Calculate mathematical multipliers based on context"""
        
        multipliers = {
            "threat_multiplier": 1.0,
            "defense_multiplier": 1.0,
            "setup_multiplier": 1.0,
            "difficulty_multiplier": 1.0,
            "safety_multiplier": 1.0,
            "role_multipliers": {},
            "campaign_multipliers": {}
        }
        
        # Game context: threat level affects value priorities
        if game_context:
            threat_assessment = self.context_service.calculate_threat_level(game_context)
            threat_level = threat_assessment.get("overall_threat_level", 0)
            
            # Emergency situations: defensive cards more valuable, setup cards less valuable
            if threat_level > 0.7:  # Emergency
                multipliers["defense_multiplier"] = 1.5
                multipliers["setup_multiplier"] = 0.7
                multipliers["damage_prevented_multiplier"] = 1.4
                multipliers["horror_prevented_multiplier"] = 1.4
            elif threat_level > 0.4:  # High pressure
                multipliers["defense_multiplier"] = 1.2
                multipliers["setup_multiplier"] = 0.9
                multipliers["damage_prevented_multiplier"] = 1.2
                multipliers["horror_prevented_multiplier"] = 1.2
            else:  # Stable
                multipliers["defense_multiplier"] = 0.9
                multipliers["setup_multiplier"] = 1.2
                multipliers["action_multiplier"] = 1.1  # Action efficiency more valuable when stable
        
        # Investigator context: role affects what's valuable
        if investigator_code:
            try:
                investigator_context = await self._get_investigator_context(investigator_code)
                if investigator_context and investigator_context.primary_role:
                    role = investigator_context.primary_role
                    
                    if role == "fighter":
                        multipliers["role_multipliers"] = {
                            "combat": 1.3,
                            "clues": 0.8,
                            "resources": 1.0,
                            "card_draw": 0.9
                        }
                        multipliers["damage_dealt_multiplier"] = 1.3
                        multipliers["damage_prevented_multiplier"] = 1.2
                    elif role == "seeker":
                        multipliers["role_multipliers"] = {
                            "combat": 0.7,
                            "clues": 1.4,
                            "resources": 1.0,
                            "card_draw": 1.3
                        }
                        multipliers["clue_multiplier"] = 1.4
                        multipliers["card_draw_multiplier"] = 1.3
                    elif role == "support":
                        multipliers["role_multipliers"] = {
                            "combat": 0.9,
                            "clues": 1.0,
                            "resources": 1.3,
                            "card_draw": 1.1
                        }
                        multipliers["resource_multiplier"] = 1.3
                    elif role == "flex":
                        multipliers["role_multipliers"] = {
                            "combat": 1.1,
                            "clues": 1.1,
                            "resources": 1.1,
                            "card_draw": 1.1
                        }
            except Exception:
                pass
        
        # Campaign context: difficulty and mechanics affect risk tolerance
        if campaign_context:
            difficulty = campaign_context.get("difficulty", "standard")
            campaign = campaign_context.get("campaign", "").lower()
            
            # Difficulty multipliers
            if difficulty == "expert":
                multipliers["difficulty_multiplier"] = 1.0
                multipliers["safety_multiplier"] = 1.4  # Safety much more valuable
            elif difficulty == "hard":
                multipliers["difficulty_multiplier"] = 1.0
                multipliers["safety_multiplier"] = 1.2
            elif difficulty == "easy":
                multipliers["difficulty_multiplier"] = 1.0
                multipliers["safety_multiplier"] = 0.8  # Can take more risks
            
            # Campaign-specific multipliers
            if "forgotten_age" in campaign:
                multipliers["campaign_multipliers"] = {
                    "horror_resist": 1.2,
                    "damage_resist": 1.3,  # Poison/hazards
                    "special": 1.1
                }
                multipliers["damage_prevented_multiplier"] = 1.3
            elif "path_to_carcosa" in campaign:
                multipliers["campaign_multipliers"] = {
                    "horror_resist": 1.4,  # Heavy horror focus
                    "damage_resist": 1.0,
                    "special": 1.2
                }
                multipliers["horror_prevented_multiplier"] = 1.4
            elif "night_of_the_zealot" in campaign:
                multipliers["campaign_multipliers"] = {
                    "horror_resist": 1.0,
                    "damage_resist": 1.0,
                    "special": 0.9  # Simpler mechanics
                }
        
        return multipliers

    async def _run_contextual_gpt_analysis(
        self, user_prompt: str, contextual_system_prompt: str
    ) -> str:
        """Run GPT analysis with contextual system prompt"""
        # Temporarily modify the GPT service's system message
        original_system_message = self.gpt_service.system_messages["content"]
        self.gpt_service.system_messages["content"] = contextual_system_prompt
        
        try:
            # Run the analysis
            gpt_request = OpenAIRequest(content=user_prompt)
            gpt_response = await self.gpt_service.async_request(gpt_request)
            
            # Extract content
            if gpt_response.choices and len(gpt_response.choices) > 0:
                return gpt_response.choices[0].message.content
            return "No response generated"
            
        finally:
            # Restore original system message
            self.gpt_service.system_messages["content"] = original_system_message

    async def _get_card_info(self, card_code: str) -> Dict[str, Any]:
        """Get basic card information"""
        try:
            # Use existing card service to get card info
            # This is a simplified version - you might want to expand this
            return {
                "code": card_code,
                "name": f"Card {card_code}",  # Would fetch actual name
                "type": "unknown",  # Would fetch actual type
            }
        except Exception as e:
            return {
                "code": card_code,
                "name": "Unknown",
                "error": str(e)
            }

    async def _get_investigator_context(self, investigator_code: str) -> Optional[InvestigatorContext]:
        """Get investigator context"""
        try:
            from domain.card.investigator_card import InvestigatorCard
            from domain.card.faction import Faction
            from domain.card.card_type import CardType
            
            investigator = InvestigatorCard(
                code=investigator_code,
                name=f"Investigator {investigator_code}",
                traits=[],
                faction=Faction.NEUTRAL,
                text="",
                card_type=CardType.INVESTIGATOR
            )
            
            return InvestigatorContext.from_investigator_card(investigator)
        except Exception as e:
            print(f"Error creating investigator context: {e}")
            return None