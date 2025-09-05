"""
Card Adapter Registry - Domain-side registry for card conversion
Uses dependency inversion to avoid importing API classes in domain
"""

from abc import ABC, abstractmethod
from typing import Protocol, TypeVar, Dict, Type, Any
from domain.card import EncounterCard, PlayerCard

# Type variables for generic conversion
TSchema = TypeVar('TSchema')
TDomain = TypeVar('TDomain')


class CardAdapter(Protocol[TSchema, TDomain]):
    """Protocol defining card conversion interface"""
    
    @abstractmethod
    def schema_to_domain(self, schema: TSchema) -> TDomain:
        """Convert schema object to domain object"""
        pass


class CardAdapterRegistry:
    """Registry for card adapters - lives in domain layer"""
    
    def __init__(self):
        self._adapters: Dict[str, CardAdapter] = {}
    
    def register_adapter(self, card_type: str, adapter: CardAdapter) -> None:
        """Register an adapter for a specific card type"""
        self._adapters[card_type] = adapter
    
    def convert_to_domain(self, card_type: str, schema_obj: Any) -> Any:
        """Convert schema object to domain object using registered adapter"""
        adapter = self._adapters.get(card_type)
        if not adapter:
            raise ValueError(f"No adapter registered for card type: {card_type}")
        
        return adapter.schema_to_domain(schema_obj)
    
    def is_supported(self, card_type: str) -> bool:
        """Check if a card type has a registered adapter"""
        return card_type in self._adapters
    
    def get_supported_types(self) -> list[str]:
        """Get all supported card types"""
        return list(self._adapters.keys())


# Global registry instance
card_adapter_registry = CardAdapterRegistry()


def register_card_adapter(card_type: str):
    """Decorator for registering card adapters"""
    def decorator(adapter_class):
        card_adapter_registry.register_adapter(card_type, adapter_class())
        return adapter_class
    return decorator