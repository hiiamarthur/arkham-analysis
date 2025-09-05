"""
Card Adapters - Clean conversion between schema and domain objects
"""

from .card_adapter_registry import (
    CardAdapter,
    CardAdapterRegistry,
    card_adapter_registry,
    register_card_adapter
)

__all__ = [
    'CardAdapter',
    'CardAdapterRegistry', 
    'card_adapter_registry',
    'register_card_adapter'
]