from typing import Optional, Dict, Any
import json
from app.schemas.context_schema import UserContextSchema
from app.services.cache_service import cache_service


class ContextService:
    """Service for managing user context and preferences"""

    def __init__(self):
        self.cache_service = cache_service
        self.cache_prefix = "user_context"

    async def store_user_context(
        self, user_context: UserContextSchema, user_id: Optional[str] = None
    ) -> UserContextSchema:
        """Store user context (in cache for now, could be database later)"""
        cache_key = f"{self.cache_prefix}:{user_id or 'anonymous'}"
        
        # Convert to dict for storage
        context_data = user_context.dict()
        
        # Store in cache with longer TTL (24 hours)
        await self.cache_service.set_with_key(
            "user_contexts", cache_key, context_data, ttl=86400
        )
        
        return user_context

    async def get_user_context(
        self, user_id: Optional[str] = None
    ) -> Optional[UserContextSchema]:
        """Retrieve user context"""
        cache_key = f"{self.cache_prefix}:{user_id or 'anonymous'}"
        
        try:
            context_data = await self.cache_service.get_with_key(
                "user_contexts", cache_key
            )
            
            if context_data:
                return UserContextSchema(**context_data)
            
            # Return default context if none found
            return UserContextSchema()
            
        except Exception as e:
            print(f"Error retrieving user context: {e}")
            return UserContextSchema()

    async def update_user_context(
        self, user_id: Optional[str], user_context: UserContextSchema
    ) -> UserContextSchema:
        """Update existing user context"""
        # For now, this is the same as store_user_context
        # In a real app, you might want to merge with existing context
        return await self.store_user_context(user_context, user_id)

    async def delete_user_context(self, user_id: Optional[str] = None):
        """Delete user context"""
        cache_key = f"{self.cache_prefix}:{user_id or 'anonymous'}"
        
        try:
            await self.cache_service.delete_with_key("user_contexts", cache_key)
        except Exception as e:
            print(f"Error deleting user context: {e}")
            raise

    def apply_user_context_to_analysis(
        self, analysis_result: Dict[str, Any], user_context: UserContextSchema
    ) -> Dict[str, Any]:
        """Apply user context to modify analysis results"""
        
        # Apply weight preferences to scoring
        if "card_rankings" in analysis_result:
            rankings = analysis_result["card_rankings"]
            
            # Adjust rankings based on user preferences
            for category in rankings:
                if "cards" in rankings[category]:
                    for card in rankings[category]["cards"]:
                        self._apply_user_weights(card, user_context)
        
        # Filter by owned packs if specified
        if user_context.owned_packs:
            analysis_result = self._filter_by_owned_packs(
                analysis_result, user_context.owned_packs
            )
        
        # Add user-specific recommendations
        analysis_result["user_recommendations"] = self._generate_user_recommendations(
            analysis_result, user_context
        )
        
        return analysis_result

    def _apply_user_weights(self, card_data: Dict, user_context: UserContextSchema):
        """Apply user preference weights to card scoring"""
        weights = user_context.weight_preferences
        
        # Adjust score based on user weights
        if "score" in card_data and "factors" in card_data:
            factors = card_data["factors"]
            adjusted_score = 0
            
            for factor, value in factors.items():
                weight = weights.get(factor, 1.0)
                adjusted_score += value * weight
            
            card_data["user_adjusted_score"] = adjusted_score

    def _filter_by_owned_packs(
        self, analysis_result: Dict[str, Any], owned_packs: list
    ) -> Dict[str, Any]:
        """Filter recommendations based on owned packs"""
        # This would require pack information in card data
        # For now, just add a note
        analysis_result["pack_filter_applied"] = True
        analysis_result["owned_packs"] = owned_packs
        return analysis_result

    def _generate_user_recommendations(
        self, analysis_result: Dict[str, Any], user_context: UserContextSchema
    ) -> Dict[str, Any]:
        """Generate personalized recommendations based on user context"""
        recommendations = {
            "based_on_play_style": f"Recommendations optimized for {user_context.play_style} play style",
            "difficulty_considerations": f"Analysis adjusted for {user_context.preferred_difficulty} difficulty",
            "group_size_notes": f"Recommendations for {user_context.typical_group_size} games"
        }
        
        if user_context.max_xp_budget:
            recommendations["xp_budget"] = f"Filtered for {user_context.max_xp_budget} XP budget"
        
        if user_context.current_campaign:
            recommendations["campaign_specific"] = f"Optimized for {user_context.current_campaign} campaign"
        
        return recommendations