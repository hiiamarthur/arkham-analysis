from typing import Optional, Dict, Any, List, TYPE_CHECKING
from app.schemas.context_schema import GameContextSchema
from app.schemas.gpt_schema import OpenAIRequest
from app.services.gpt_service import GPTService
from app.services.context_service import ContextService
from app.services.card_service import CardService
from domain.card.context.investigator_context import InvestigatorContext
from domain.scenarios import ScenarioType
from domain.difficulty import Difficulty

if TYPE_CHECKING:
    from app.services.scenario_service import ScenarioService


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
        scenario_service: Optional["ScenarioService"] = None,
    ):
        self.gpt_service = gpt_service
        self.context_service = context_service
        self.card_service = card_service
        self.scenario_service = scenario_service
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
                print(f"Starting analysis for card: {card_code}")
                
                # Get card info first
                card_info = await self._get_card_info(card_code)
                print(f"Got card info for {card_code}: {card_info}")

                # Ensure card_info is a dictionary and has required fields
                if not isinstance(card_info, dict):
                    card_info = {"code": card_code, "name": f"Card {card_code}"}

                card_name = card_info.get("name", f"Card {card_code}")
                print(f"Card name extracted: {card_name}")

                # Create card analysis prompt
                card_prompt = f"Analyze the strength and value of card '{card_code}' ({card_name}) given the current context."
                print(f"Card prompt created successfully")

                # Run GPT analysis with contextual system prompt
                print(f"Starting GPT analysis for {card_code}")
                analysis = await self._run_contextual_gpt_analysis(
                    card_prompt, contextual_system_prompt
                )
                print(f"GPT analysis completed for {card_code}")
                
                # Add delay between API calls to respect rate limits
                import asyncio
                await asyncio.sleep(1)  # 1 second delay between calls

                card_analyses[card_code] = {
                    "card_info": card_info,
                    "strength_analysis": analysis,
                }

            except Exception as e:
                print(f"Error analyzing card {card_code}: {e}")
                print(f"Error type: {type(e)}")
                import traceback
                traceback.print_exc()
                card_analyses[card_code] = {"error": f"Analysis failed: {str(e)}"}

        return {
            "analysis_type": "contextual_card_strength",
            "context_applied": {
                "has_game_context": game_context is not None,
                "has_investigator_context": investigator_code is not None,
                "has_campaign_context": campaign_context is not None,
            },
            "card_analyses": card_analyses,
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
            "synergy_analysis": analysis,
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
                "timing_analysis": analysis,
            }

        return {
            "analysis_type": "card_timing_analysis",
            "timing_analyses": timing_analyses,
        }

    async def _build_contextual_system_prompt(
        self,
        game_context: Optional[GameContextSchema] = None,
        investigator_code: Optional[str] = None,
        campaign_context: Optional[Dict] = None,
    ) -> str:
        """Build context-aware system prompt by filling template with dynamic values"""

        try:
            # Calculate context-specific axioms
            context_axioms = await self._calculate_context_axioms(
                game_context, investigator_code, campaign_context
            )
            print(f"Context axioms calculated: {len(context_axioms)} items")

            # Fill the template with context-adjusted values
            contextual_prompt = self.base_system_prompt.format(**context_axioms)
            print(f"Template filled successfully, length: {len(contextual_prompt)}")

            return contextual_prompt
        except Exception as e:
            print(f"Error in _build_contextual_system_prompt: {e}")
            print(f"Error type: {type(e)}")
            import traceback
            traceback.print_exc()
            raise

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
            "damage_value": "2-2.5",
        }

        # Game context adjustments
        if game_context:
            # Analyze current enemies to adjust enemy axioms
            if game_context.enemies_in_play:
                total_health = sum(
                    enemy.max_health for enemy in game_context.enemies_in_play
                )
                avg_health = total_health / len(game_context.enemies_in_play)
                axioms["avg_enemy_health"] = round(avg_health, 1)
                axioms["hits_to_kill"] = max(1, round(avg_health / 2))

            # Analyze locations to adjust location axioms
            if game_context.locations_in_play:
                revealed_locations = [
                    loc
                    for loc in game_context.locations_in_play
                    if loc.status.value == "revealed"
                ]
                if revealed_locations:
                    total_clues = sum(loc.current_clues for loc in revealed_locations)
                    investigator_count = len(game_context.investigators)
                    if investigator_count > 0:
                        axioms["avg_clues_per_location"] = round(
                            total_clues
                            / (len(revealed_locations) * investigator_count),
                            1,
                        )

            # Analyze locations to adjust investigation axioms
            if game_context.locations_in_play:
                revealed_locations = [
                    loc
                    for loc in game_context.locations_in_play
                    if loc.status.value == "revealed"
                ]
                if revealed_locations:
                    total_shroud = sum(
                        getattr(loc, "shroud", 3) for loc in revealed_locations
                    )
                    avg_shroud_current = total_shroud / len(revealed_locations)
                    axioms["avg_shroud"] = round(avg_shroud_current, 1)

                    # Adjust investigation target based on current shroud values
                    axioms["investigation_target_number"] = max(
                        4, round(avg_shroud_current + 2)
                    )

            # Adjust resource values based on threat level
            threat_assessment = self.context_service.calculate_threat_level(
                game_context
            )
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

        # Investigator context adjustments using existing InvestigatorContext
        if investigator_code:
            try:
                investigator_context = await self._get_investigator_context(
                    investigator_code
                )
                if investigator_context:
                    # Use precomputed investigator context values
                    role = investigator_context.primary_role
                    starting_stats = investigator_context.starting_stats

                    # Adjust axioms based on investigator's actual stats and abilities
                    if role == "seeker":
                        axioms["clue_value"] = 3.0  # Clues more valuable for seekers
                        axioms["card_value"] = "1.5-2.5"  # Better draw engines
                        axioms["skill_icon_value"] = 0.7  # Skill commits more valuable
                        axioms["investigation_target_number"] = max(
                            4, 6 - starting_stats.get("intellect", 0)
                        )  # Adjust based on intellect
                        axioms["auto_success_value"] = (
                            3.5  # Reliability matters for clue gathering
                        )
                    elif role == "fighter":
                        axioms["damage_value"] = (
                            "3.0-3.5"  # Damage more valuable for fighters
                        )
                        axioms["enemy_damage_range"] = "1-3"  # Expect tougher enemies
                        axioms["health_sanity_value"] = 2.0  # Need to tank damage
                        axioms["trauma_prevention_value"] = (
                            5.0  # Trauma is devastating for fighters
                        )
                        axioms["chaos_token_mitigation_value"] = (
                            2.2  # Combat reliability crucial
                        )
                        # Adjust based on combat stat
                        if starting_stats.get("combat", 0) >= 4:
                            axioms["auto_success_value"] = (
                                3.2  # High combat investigators need less auto-success
                            )
                    elif role == "support":
                        axioms["action_value"] = (
                            1.8  # Actions less valuable, more about efficiency
                        )
                        axioms["fast_card_value"] = (
                            2.2  # Fast effects help team coordination
                        )
                        axioms["resource_acceleration_value"] = (
                            1.2  # Economy building for team
                        )
                        axioms["horror_heal_value"] = (
                            2.5  # Support often handles horror
                        )
                    elif role == "mystic":
                        axioms["chaos_token_mitigation_value"] = (
                            2.5  # Spells need reliability
                        )
                        axioms["auto_success_value"] = (
                            4.0  # Mystics value consistency highly
                        )
                        axioms["horror_heal_value"] = (
                            2.2  # Often deal with horror effects
                        )
                        # Adjust based on willpower stat
                        if starting_stats.get("willpower", 0) >= 4:
                            axioms["trauma_prevention_value"] = (
                                3.5  # High willpower investigators handle horror better
                            )
                    elif role == "survivor":
                        axioms["skill_icon_value"] = (
                            1.0  # Survivors rely heavily on commits
                        )
                        axioms["resource_acceleration_value"] = (
                            0.5  # Used to resource scarcity
                        )
                        axioms["damage_heal_value"] = 2.2  # Good at self-healing

                    # Use investigator's special abilities to further adjust values
                    if investigator_context.special_abilities:
                        for ability in investigator_context.special_abilities:
                            ability_name = ability.get("name", "")
                            if "tome" in ability_name.lower():
                                axioms["card_value"] = (
                                    "2-3"  # Tome investigators value card draw more
                                )
                            elif "resource" in ability_name.lower():
                                axioms["resource_acceleration_value"] = 1.5
                            elif "fast" in ability_name.lower():
                                axioms["fast_card_value"] = 3.0
            except Exception as e:
                print(f"Error getting investigator context: {e}")
                pass

        # Campaign context adjustments using existing scenario service when available
        if campaign_context:
            campaign = campaign_context.get("campaign", "").lower()
            difficulty = campaign_context.get("difficulty", "standard")
            scenario_code = campaign_context.get("scenario_code")

            # If scenario service is available and we have a scenario code, get precomputed context
            if self.scenario_service and scenario_code:
                try:
                    # Parse scenario and difficulty from your domain types
                    from domain.scenarios import ScenarioType
                    from domain.difficulty import Difficulty as DifficultyType

                    scenario_enum = (
                        ScenarioType[scenario_code.upper()]
                        if hasattr(ScenarioType, scenario_code.upper())
                        else None
                    )
                    difficulty_enum = getattr(
                        DifficultyType, difficulty.upper(), DifficultyType.STANDARD
                    )

                    if scenario_enum:
                        # Get precomputed scenario context with actual game mechanics
                        scenario_context = (
                            await self.scenario_service.yield_scenario_context(
                                scenario_enum,
                                difficulty_enum,
                                campaign_context.get("investigator_count", 1),
                            )
                        )

                        # Use scenario context to set axioms based on actual game data
                        if hasattr(scenario_context, "chaos_bag"):
                            # Calculate actual success rates from chaos bag
                            axioms["base_success_rate"] = (
                                self._calculate_chaos_bag_success_rate(
                                    scenario_context.chaos_bag, difficulty_enum
                                )
                            )

                        if hasattr(scenario_context, "encounter_cards"):
                            # Calculate actual enemy stats from encounter deck
                            enemy_stats = self._analyze_encounter_deck(
                                scenario_context.encounter_cards
                            )
                            if enemy_stats:
                                axioms["avg_enemy_health"] = enemy_stats.get(
                                    "avg_health", axioms["avg_enemy_health"]
                                )
                                axioms["enemy_damage_range"] = enemy_stats.get(
                                    "damage_range", axioms["enemy_damage_range"]
                                )
                                axioms["enemy_horror_range"] = enemy_stats.get(
                                    "horror_range", axioms["enemy_horror_range"]
                                )

                        print(f"Using precomputed scenario context for {scenario_code}")
                except Exception as e:
                    print(
                        f"Error loading scenario context: {e}, falling back to campaign rules"
                    )
                    # Fall back to campaign-based rules below

            # Difficulty adjustments
            if difficulty == "expert":
                axioms["enemy_damage_range"] = "2-3"
                axioms["enemy_horror_range"] = "1-3"
                axioms["avg_enemy_health"] = round(axioms["avg_enemy_health"] * 1.2, 1)
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
                axioms["avg_enemy_health"] = round(axioms["avg_enemy_health"] * 0.8, 1)
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
                axioms["investigation_target_number"] = (
                    6  # Mixed investigation difficulty
                )
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
            "campaign_multipliers": {},
        }

        # Game context: threat level affects value priorities
        if game_context:
            threat_assessment = self.context_service.calculate_threat_level(
                game_context
            )
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
                multipliers["action_multiplier"] = (
                    1.1  # Action efficiency more valuable when stable
                )

        # Investigator context: role affects what's valuable
        if investigator_code:
            try:
                investigator_context = await self._get_investigator_context(
                    investigator_code
                )
                if investigator_context and investigator_context.primary_role:
                    role = investigator_context.primary_role

                    if role == "fighter":
                        multipliers["role_multipliers"] = {
                            "combat": 1.3,
                            "clues": 0.8,
                            "resources": 1.0,
                            "card_draw": 0.9,
                        }
                        multipliers["damage_dealt_multiplier"] = 1.3
                        multipliers["damage_prevented_multiplier"] = 1.2
                    elif role == "seeker":
                        multipliers["role_multipliers"] = {
                            "combat": 0.7,
                            "clues": 1.4,
                            "resources": 1.0,
                            "card_draw": 1.3,
                        }
                        multipliers["clue_multiplier"] = 1.4
                        multipliers["card_draw_multiplier"] = 1.3
                    elif role == "support":
                        multipliers["role_multipliers"] = {
                            "combat": 0.9,
                            "clues": 1.0,
                            "resources": 1.3,
                            "card_draw": 1.1,
                        }
                        multipliers["resource_multiplier"] = 1.3
                    elif role == "flex":
                        multipliers["role_multipliers"] = {
                            "combat": 1.1,
                            "clues": 1.1,
                            "resources": 1.1,
                            "card_draw": 1.1,
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
                    "special": 1.1,
                }
                multipliers["damage_prevented_multiplier"] = 1.3
            elif "path_to_carcosa" in campaign:
                multipliers["campaign_multipliers"] = {
                    "horror_resist": 1.4,  # Heavy horror focus
                    "damage_resist": 1.0,
                    "special": 1.2,
                }
                multipliers["horror_prevented_multiplier"] = 1.4
            elif "night_of_the_zealot" in campaign:
                multipliers["campaign_multipliers"] = {
                    "horror_resist": 1.0,
                    "damage_resist": 1.0,
                    "special": 0.9,  # Simpler mechanics
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
        """Get basic card information using card service repository"""
        try:
            # Use card service's repository to get actual card data
            if hasattr(self.card_service, "card_repo") and self.card_service.card_repo:
                card = await self.card_service.card_repo.get_first(
                    filters={"filter_by[code][equals]": card_code}
                )

                if card:
                    return {
                        "code": card_code,
                        "name": getattr(card, "name", f"Card {card_code}"),
                        "type": getattr(card, "type_code", "unknown"),
                        "faction": getattr(card, "faction_code", "neutral"),
                        "cost": getattr(card, "cost", None),
                        "xp": getattr(card, "xp", 0),
                    }

            # Fallback if card not found in database
            return {
                "code": card_code,
                "name": f"Card {card_code}",
                "type": "unknown",
                "faction": "neutral",
                "cost": None,
                "xp": 0,
            }
        except Exception as e:
            print(f"Error getting card info for {card_code}: {e}")
            return {
                "code": card_code,
                "name": f"Card {card_code}",
                "type": "unknown",
                "faction": "neutral",
                "cost": None,
                "xp": 0,
                "error": str(e),
            }

    async def _get_investigator_context(
        self, investigator_code: str
    ) -> Optional[InvestigatorContext]:
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
                card_type=CardType.INVESTIGATOR,
            )

            return InvestigatorContext.from_investigator_card(investigator)
        except Exception as e:
            print(f"Error creating investigator context: {e}")
            return None

    def _calculate_chaos_bag_success_rate(self, chaos_bag, difficulty) -> int:
        """Calculate base success rate from actual chaos bag composition"""
        try:
            # This would analyze the chaos bag tokens and calculate success probability
            # For now, return difficulty-based estimates
            if hasattr(difficulty, "name"):
                difficulty_name = difficulty.name.lower()
                if difficulty_name == "expert":
                    return 45
                elif difficulty_name == "hard":
                    return 50
                elif difficulty_name == "easy":
                    return 75
                else:
                    return 60
            return 60
        except Exception as e:
            print(f"Error calculating chaos bag success rate: {e}")
            return 60

    def _analyze_encounter_deck(self, encounter_cards) -> Optional[Dict[str, Any]]:
        """Analyze encounter deck to extract enemy statistics"""
        try:
            if not encounter_cards:
                return None

            enemy_cards = [
                card
                for card in encounter_cards
                if hasattr(card, "type_code") and card.type_code == "enemy"
            ]

            if not enemy_cards:
                return None

            total_health = sum(
                getattr(card, "health", 0)
                for card in enemy_cards
                if hasattr(card, "health")
            )
            total_damage = sum(
                getattr(card, "enemy_damage", 0)
                for card in enemy_cards
                if hasattr(card, "enemy_damage")
            )
            total_horror = sum(
                getattr(card, "enemy_horror", 0)
                for card in enemy_cards
                if hasattr(card, "enemy_horror")
            )

            if len(enemy_cards) > 0:
                avg_health = round(total_health / len(enemy_cards), 1)
                avg_damage = round(total_damage / len(enemy_cards), 1)
                avg_horror = round(total_horror / len(enemy_cards), 1)

                return {
                    "avg_health": avg_health,
                    "damage_range": f"1-{max(2, int(avg_damage + 1))}",
                    "horror_range": f"1-{max(2, int(avg_horror + 1))}",
                }

            return None
        except Exception as e:
            print(f"Error analyzing encounter deck: {e}")
            return None
