"""
Difficulty Modifier - Handles difficulty-specific adjustments and calculations
Follows SRP by focusing solely on difficulty-related logic
"""

from typing import Dict, List, Tuple, Any

import sys
import os
backend_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
if backend_path not in sys.path:
    sys.path.append(backend_path)

from domain import Difficulty


class DifficultyModifier:
    """Manages difficulty-specific modifications and adjustments"""
    
    def __init__(self, difficulty: Difficulty):
        self.difficulty = difficulty
        self._load_difficulty_settings()
    
    def _load_difficulty_settings(self) -> None:
        """Load difficulty-specific settings and modifiers"""
        self.settings = self._get_difficulty_settings()
        self.chaos_modifiers = self._get_chaos_bag_modifiers()
        self.resource_modifiers = self._get_resource_modifiers()
        self.enemy_modifiers = self._get_enemy_modifiers()
    
    def _get_difficulty_settings(self) -> Dict[str, Any]:
        """Get base difficulty settings"""
        settings_map = {
            Difficulty.EASY: {
                "name": "Easy",
                "description": "Recommended for new players",
                "doom_bonus": 2,
                "resource_bonus": 0.2,
                "damage_reduction": 0.1,
                "horror_reduction": 0.1,
            },
            Difficulty.STANDARD: {
                "name": "Standard", 
                "description": "Balanced experience",
                "doom_bonus": 0,
                "resource_bonus": 0.0,
                "damage_reduction": 0.0,
                "horror_reduction": 0.0,
            },
            Difficulty.HARD: {
                "name": "Hard",
                "description": "For experienced players",
                "doom_bonus": -1,
                "resource_bonus": -0.1,
                "damage_reduction": -0.1,
                "horror_reduction": -0.1,
            },
            Difficulty.EXPERT: {
                "name": "Expert",
                "description": "Maximum challenge",
                "doom_bonus": -2,
                "resource_bonus": -0.2,
                "damage_reduction": -0.2,
                "horror_reduction": -0.2,
            },
        }
        
        return settings_map.get(self.difficulty, settings_map[Difficulty.STANDARD])
    
    def _get_chaos_bag_modifiers(self) -> Dict[str, float]:
        """Get chaos bag difficulty modifiers"""
        modifiers_map = {
            Difficulty.EASY: {
                "positive_token_bonus": 0.15,  # More positive tokens
                "negative_token_reduction": 0.1,  # Fewer/weaker negative tokens
                "auto_fail_reduction": 0.0,  # Same auto-fail chance
                "elder_sign_bonus": 0.1,  # Slightly better elder sign effects
            },
            Difficulty.STANDARD: {
                "positive_token_bonus": 0.0,
                "negative_token_reduction": 0.0,
                "auto_fail_reduction": 0.0,
                "elder_sign_bonus": 0.0,
            },
            Difficulty.HARD: {
                "positive_token_bonus": -0.1,  # Fewer positive tokens
                "negative_token_reduction": -0.15,  # More/stronger negative tokens
                "auto_fail_reduction": 0.0,
                "elder_sign_bonus": -0.1,  # Weaker elder sign effects
            },
            Difficulty.EXPERT: {
                "positive_token_bonus": -0.2,
                "negative_token_reduction": -0.25,
                "auto_fail_reduction": 0.0,
                "elder_sign_bonus": -0.2,
            },
        }
        
        return modifiers_map.get(self.difficulty, modifiers_map[Difficulty.STANDARD])
    
    def _get_resource_modifiers(self) -> Dict[str, float]:
        """Get resource-related difficulty modifiers"""
        modifiers_map = {
            Difficulty.EASY: {
                "starting_resources": 1.2,  # 20% more starting resources
                "card_draw": 1.1,  # Slightly better card draw
                "action_efficiency": 1.0,  # No change to actions
                "mulligan_bonus": 1.0,  # Better mulligan outcomes
            },
            Difficulty.STANDARD: {
                "starting_resources": 1.0,
                "card_draw": 1.0,
                "action_efficiency": 1.0,
                "mulligan_bonus": 0.0,
            },
            Difficulty.HARD: {
                "starting_resources": 0.9,  # 10% fewer starting resources
                "card_draw": 0.95,  # Slightly worse card draw
                "action_efficiency": 0.95,  # Actions slightly less efficient
                "mulligan_bonus": 0.0,
            },
            Difficulty.EXPERT: {
                "starting_resources": 0.8,  # 20% fewer starting resources
                "card_draw": 0.9,
                "action_efficiency": 0.9,
                "mulligan_bonus": -0.1,  # Worse mulligan outcomes
            },
        }
        
        return modifiers_map.get(self.difficulty, modifiers_map[Difficulty.STANDARD])
    
    def _get_enemy_modifiers(self) -> Dict[str, float]:
        """Get enemy-related difficulty modifiers"""
        modifiers_map = {
            Difficulty.EASY: {
                "enemy_health": 0.9,  # 10% less enemy health
                "enemy_damage": 0.9,  # 10% less enemy damage
                "enemy_horror": 0.9,  # 10% less enemy horror
                "spawn_rate": 0.95,  # Slightly fewer enemy spawns
            },
            Difficulty.STANDARD: {
                "enemy_health": 1.0,
                "enemy_damage": 1.0,
                "enemy_horror": 1.0,
                "spawn_rate": 1.0,
            },
            Difficulty.HARD: {
                "enemy_health": 1.1,  # 10% more enemy health
                "enemy_damage": 1.1,  # 10% more enemy damage
                "enemy_horror": 1.1,  # 10% more enemy horror
                "spawn_rate": 1.05,  # Slightly more enemy spawns
            },
            Difficulty.EXPERT: {
                "enemy_health": 1.2,  # 20% more enemy health
                "enemy_damage": 1.2,  # 20% more enemy damage
                "enemy_horror": 1.2,  # 20% more enemy horror
                "spawn_rate": 1.1,  # 10% more enemy spawns
            },
        }
        
        return modifiers_map.get(self.difficulty, modifiers_map[Difficulty.STANDARD])
    
    def apply_doom_modifier(self, base_doom: int) -> int:
        """Apply difficulty modifier to doom threshold"""
        return max(5, base_doom + self.settings["doom_bonus"])
    
    def apply_resource_modifier(self, base_resources: int) -> int:
        """Apply difficulty modifier to starting resources"""
        multiplier = self.resource_modifiers["starting_resources"]
        return max(1, int(base_resources * multiplier))
    
    def apply_damage_modifier(self, base_damage: int) -> int:
        """Apply difficulty modifier to damage values"""
        if base_damage <= 0:
            return base_damage
            
        multiplier = self.enemy_modifiers["enemy_damage"]
        reduction = self.settings["damage_reduction"]
        
        modified_damage = base_damage * multiplier * (1 + reduction)
        return max(1, int(modified_damage))
    
    def apply_horror_modifier(self, base_horror: int) -> int:
        """Apply difficulty modifier to horror values"""
        if base_horror <= 0:
            return base_horror
            
        multiplier = self.enemy_modifiers["enemy_horror"]
        reduction = self.settings["horror_reduction"]
        
        modified_horror = base_horror * multiplier * (1 + reduction)
        return max(1, int(modified_horror))
    
    def get_skill_test_modifier(self) -> float:
        """Get difficulty modifier for skill test calculations"""
        modifiers = {
            Difficulty.EASY: 0.5,  # Easier skill tests
            Difficulty.STANDARD: 0.0,  # No modifier
            Difficulty.HARD: -0.5,  # Harder skill tests
            Difficulty.EXPERT: -1.0,  # Much harder skill tests
        }
        
        return modifiers.get(self.difficulty, 0.0)
    
    def get_context_multipliers(self) -> Dict[str, float]:
        """Get difficulty-based context multipliers for card evaluation"""
        return {
            "time_pressure_multiplier": self._get_time_pressure_multiplier(),
            "resource_scarcity_multiplier": self._get_resource_scarcity_multiplier(),
            "combat_difficulty_multiplier": self._get_combat_difficulty_multiplier(),
            "investigation_difficulty_multiplier": self._get_investigation_difficulty_multiplier(),
        }
    
    def _get_time_pressure_multiplier(self) -> float:
        """Time pressure increases with difficulty"""
        multipliers = {
            Difficulty.EASY: 0.8,
            Difficulty.STANDARD: 1.0,
            Difficulty.HARD: 1.2,
            Difficulty.EXPERT: 1.4,
        }
        return multipliers.get(self.difficulty, 1.0)
    
    def _get_resource_scarcity_multiplier(self) -> float:
        """Resource scarcity increases with difficulty"""
        multipliers = {
            Difficulty.EASY: 0.7,
            Difficulty.STANDARD: 1.0,
            Difficulty.HARD: 1.3,
            Difficulty.EXPERT: 1.6,
        }
        return multipliers.get(self.difficulty, 1.0)
    
    def _get_combat_difficulty_multiplier(self) -> float:
        """Combat difficulty increases with difficulty"""
        multipliers = {
            Difficulty.EASY: 0.8,
            Difficulty.STANDARD: 1.0,
            Difficulty.HARD: 1.3,
            Difficulty.EXPERT: 1.6,
        }
        return multipliers.get(self.difficulty, 1.0)
    
    def _get_investigation_difficulty_multiplier(self) -> float:
        """Investigation difficulty increases with difficulty"""
        multipliers = {
            Difficulty.EASY: 0.9,
            Difficulty.STANDARD: 1.0,
            Difficulty.HARD: 1.2,
            Difficulty.EXPERT: 1.4,
        }
        return multipliers.get(self.difficulty, 1.0)
    
    def get_card_value_modifier(self, card_type: str) -> float:
        """Get difficulty-based card value modifiers"""
        # Different card types become more/less valuable at different difficulties
        modifiers = {
            Difficulty.EASY: {
                "combat": 0.9,  # Combat less critical on easy
                "investigation": 1.0,
                "survival": 0.8,  # Survival less critical
                "economy": 1.1,  # Economy more valuable (more resources)
            },
            Difficulty.STANDARD: {
                "combat": 1.0,
                "investigation": 1.0,
                "survival": 1.0,
                "economy": 1.0,
            },
            Difficulty.HARD: {
                "combat": 1.2,  # Combat more critical
                "investigation": 1.1,
                "survival": 1.3,  # Survival very important
                "economy": 0.9,  # Economy less valuable (fewer resources)
            },
            Difficulty.EXPERT: {
                "combat": 1.4,
                "investigation": 1.2,
                "survival": 1.5,  # Survival extremely important
                "economy": 0.8,
            },
        }
        
        difficulty_mods = modifiers.get(self.difficulty, modifiers[Difficulty.STANDARD])
        return difficulty_mods.get(card_type, 1.0)