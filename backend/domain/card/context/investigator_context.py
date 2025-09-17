from typing import Dict, List, Optional
from dataclasses import dataclass
from ..investigator_card import InvestigatorCard
from ...difficulty import Difficulty


@dataclass
class InvestigatorContext:
    """
    Investigator-specific context that affects card analysis and recommendations.
    This complements InvestigatorStats by providing investigator-specific modifiers.
    """
    
    # Core investigator data
    investigator: InvestigatorCard
    
    # Starting deck constraints
    faction_access: List[str]  # Primary and secondary factions
    deck_size_requirements: Dict[str, int]  # min/max deck size
    starting_stats: Dict[str, int]  # willpower, intellect, combat, agility
    starting_health: int
    starting_sanity: int
    
    # Deck building rules
    forbidden_cards: List[str] = None  # Cards this investigator cannot take
    required_cards: List[str] = None   # Cards this investigator must include
    deck_building_options: Dict = None  # Special deck building rules
    
    # Signature cards
    signature_cards: List[str] = None
    signature_weakness: str = None
    
    # Special abilities context
    special_abilities: List[Dict] = None  # Investigator abilities that affect card value
    action_economy_modifiers: Dict = None  # Fast actions, extra actions, etc.
    resource_generation: Dict = None  # Extra resources, discounts, etc.
    
    # Role and archetype
    primary_role: str = None  # "seeker", "fighter", "support", "flex"
    secondary_roles: List[str] = None
    recommended_team_size: List[int] = None  # [1, 2, 3, 4] for solo/team viability
    
    # Scenario synergies
    scenario_strengths: List[str] = None  # Scenario types where this investigator excels
    scenario_weaknesses: List[str] = None  # Scenario types where this investigator struggles
    
    # Upgrade paths
    common_upgrade_paths: List[Dict] = None  # Common XP spending patterns
    priority_upgrades: List[str] = None     # Cards to prioritize upgrading
    
    @classmethod
    def from_investigator_card(cls, investigator: InvestigatorCard) -> "InvestigatorContext":
        """Create investigator context from investigator card"""
        
        # This would typically load from a configuration file or database
        # For now, we'll create basic context based on the investigator
        
        context = cls(
            investigator=investigator,
            faction_access=cls._determine_faction_access(investigator),
            deck_size_requirements={"min": 30, "max": 30},  # Standard Arkham deck size
            starting_stats=cls._extract_starting_stats(investigator),
            starting_health=getattr(investigator, 'health', 0),
            starting_sanity=getattr(investigator, 'sanity', 0),
        )
        
        # Load investigator-specific rules (this would come from config/database)
        context._load_investigator_specific_rules()
        
        return context
    
    @staticmethod
    def _determine_faction_access(investigator: InvestigatorCard) -> List[str]:
        """Determine which factions this investigator can access"""
        primary_faction = investigator.faction.value if investigator.faction else "neutral"
        
        # This would be loaded from investigator-specific configuration
        # For now, return primary faction
        return [primary_faction]
    
    @staticmethod
    def _extract_starting_stats(investigator: InvestigatorCard) -> Dict[str, int]:
        """Extract starting stats from investigator card"""
        return {
            "willpower": getattr(investigator, 'skill_willpower', 0),
            "intellect": getattr(investigator, 'skill_intellect', 0),
            "combat": getattr(investigator, 'skill_combat', 0),
            "agility": getattr(investigator, 'skill_agility', 0),
        }
    
    def _load_investigator_specific_rules(self):
        """Load investigator-specific deck building and ability rules"""
        # This would load from a configuration system
        # For now, we'll set some defaults based on investigator code
        
        investigator_rules = self._get_investigator_rules_config()
        
        if investigator_rules:
            self.forbidden_cards = investigator_rules.get("forbidden_cards", [])
            self.required_cards = investigator_rules.get("required_cards", [])
            self.deck_building_options = investigator_rules.get("deck_building_options", {})
            self.signature_cards = investigator_rules.get("signature_cards", [])
            self.signature_weakness = investigator_rules.get("signature_weakness")
            self.special_abilities = investigator_rules.get("special_abilities", [])
            self.primary_role = investigator_rules.get("primary_role")
            self.secondary_roles = investigator_rules.get("secondary_roles", [])
    
    def _get_investigator_rules_config(self) -> Optional[Dict]:
        """Get investigator-specific rules from configuration"""
        # This would load from a JSON file or database
        # For now, return some basic rules for common investigators
        
        investigator_configs = {
            "01001": {  # Roland Banks
                "signature_cards": ["01006", "01007"],
                "signature_weakness": "01007",
                "primary_role": "fighter",
                "secondary_roles": ["seeker"],
                "special_abilities": [
                    {
                        "name": "combat_bonus_after_enemy_defeat",
                        "description": "Roland gets +1 to his next investigate after defeating an enemy"
                    }
                ],
                "scenario_strengths": ["high_enemy_count", "combat_heavy"],
                "common_upgrade_paths": [
                    {"priority": 1, "cards": ["01024", "01026"]},  # Common Roland upgrades
                ]
            },
            "01002": {  # Daisy Walker  
                "signature_cards": ["01008", "01009"],
                "signature_weakness": "01009",
                "primary_role": "seeker",
                "secondary_roles": ["support"],
                "special_abilities": [
                    {
                        "name": "tome_action_bonus",
                        "description": "Daisy can trigger tome abilities without spending actions"
                    }
                ],
                "scenario_strengths": ["high_clue_count", "research_heavy"],
            },
            # Add more investigators as needed
        }
        
        return investigator_configs.get(self.investigator.code)
    
    def get_card_value_modifiers(self, card_code: str) -> Dict[str, float]:
        """Get investigator-specific modifiers for card value"""
        modifiers = {}
        
        # Faction synergy bonuses
        if self._card_matches_faction(card_code):
            modifiers["faction_synergy"] = 1.2
        
        # Special ability synergies
        if self._card_synergizes_with_abilities(card_code):
            modifiers["ability_synergy"] = 1.3
        
        # Role-based bonuses
        if self._card_matches_role(card_code):
            modifiers["role_match"] = 1.1
        
        return modifiers
    
    def _card_matches_faction(self, card_code: str) -> bool:
        """Check if card matches investigator's accessible factions"""
        # This would check the card's faction against faction_access
        return True  # Placeholder
    
    def _card_synergizes_with_abilities(self, card_code: str) -> bool:
        """Check if card synergizes with investigator's special abilities"""
        # This would check card text/type against special_abilities
        return False  # Placeholder
    
    def _card_matches_role(self, card_code: str) -> bool:
        """Check if card matches investigator's primary role"""
        # This would check card type/function against primary_role
        return False  # Placeholder
    
    def get_upgrade_recommendations(self, current_xp: int) -> List[Dict]:
        """Get XP upgrade recommendations based on investigator context"""
        if not self.common_upgrade_paths:
            return []
        
        recommendations = []
        for path in self.common_upgrade_paths:
            if current_xp >= path.get("min_xp", 0):
                recommendations.append(path)
        
        return recommendations[:5]  # Top 5 recommendations