"""
Simple test script to verify the scoring service works
"""

import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), "."))

from scoring_model.services import (
    BaseCardScoringService,
    ConservativeScoringService,
    AggressiveScoringService,
    TempoScoringService,
    ControlScoringService,
    ComboScoringService,
)
from domain.Card.asset_card import AssetCard
from domain.Card.event_card import EventCard
from domain.Card.skill_card import SkillCard
from domain import Faction, CardType, ActivationType, CardCostFactor


def test_scoring_service():
    """Test the scoring service with sample cards"""

    # Create sample cards
    asset_card = AssetCard(
        code="01001",
        name="Test Asset",
        traits=["Item", "Weapon"],
        text="A test asset card",
        faction=Faction.GUARDIAN,
        cost=3,
        level=0,
        skill_willpower=0,
        skill_intellect=0,
        skill_combat=2,
        skill_agility=0,
        skill_wild=0,
        play_action_cost=1,
        health=2,
        sanity=0,
        activation_type=ActivationType.ACTION,
    )

    event_card = EventCard(
        code="01002",
        name="Test Event",
        traits=["Spell"],
        faction=Faction.MYSTIC,
        text="A test event card",
        cost=2,
        level=0,
        skill_willpower=2,
        skill_intellect=0,
        skill_combat=0,
        skill_agility=0,
        skill_wild=1,
        play_action_cost=1,
        activation_type=ActivationType.PLAY,
    )

    skill_card = SkillCard(
        code="01003",
        name="Test Skill",
        traits=["Innate"],
        faction=Faction.SURVIVOR,
        text="A test skill card",
        level=0,
        skill_willpower=0,
        skill_intellect=0,
        skill_combat=0,
        skill_agility=2,
        skill_wild=1,
    )

    # Test different scoring strategies
    base_scorer = BaseCardScoringService()
    conservative_scorer = ConservativeScoringService()
    aggressive_scorer = AggressiveScoringService()
    tempo_scorer = TempoScoringService()
    control_scorer = ControlScoringService()
    combo_scorer = ComboScoringService()

    print("=== Card Scoring Test ===")
    print()

    for card_name, card in [
        ("Asset", asset_card),
        ("Event", event_card),
        ("Skill", skill_card),
    ]:
        print(f"--- {card_name} Card: {card.name} ---")

        # Base scoring
        base_cost = base_scorer.calculate_cost(card)
        base_gain = base_scorer.calculate_gain(card)
        base_net = base_scorer.calculate_net_value(card)

        # Conservative scoring
        cons_cost = conservative_scorer.calculate_cost(card)
        cons_gain = conservative_scorer.calculate_gain(card)
        cons_net = conservative_scorer.calculate_net_value(card)

        # Aggressive scoring
        agg_cost = aggressive_scorer.calculate_cost(card)
        agg_gain = aggressive_scorer.calculate_gain(card)
        agg_net = aggressive_scorer.calculate_net_value(card)

        # Tempo scoring
        tempo_cost = tempo_scorer.calculate_cost(card)
        tempo_gain = tempo_scorer.calculate_gain(card)
        tempo_net = tempo_scorer.calculate_net_value(card)

        # Control scoring
        control_cost = control_scorer.calculate_cost(card)
        control_gain = control_scorer.calculate_gain(card)
        control_net = control_scorer.calculate_net_value(card)

        # Combo scoring
        combo_cost = combo_scorer.calculate_cost(card)
        combo_gain = combo_scorer.calculate_gain(card)
        combo_net = combo_scorer.calculate_net_value(card)

        print(
            f"Base Strategy:      Cost={base_cost:.2f}, Gain={base_gain:.2f}, Net={base_net:.2f}"
        )
        print(
            f"Conservative:       Cost={cons_cost:.2f}, Gain={cons_gain:.2f}, Net={cons_net:.2f}"
        )
        print(
            f"Aggressive:         Cost={agg_cost:.2f}, Gain={agg_gain:.2f}, Net={agg_net:.2f}"
        )
        print(
            f"Tempo:             Cost={tempo_cost:.2f}, Gain={tempo_gain:.2f}, Net={tempo_net:.2f}"
        )
        print(
            f"Control:           Cost={control_cost:.2f}, Gain={control_gain:.2f}, Net={control_net:.2f}"
        )
        print(
            f"Combo:             Cost={combo_cost:.2f}, Gain={combo_gain:.2f}, Net={combo_net:.2f}"
        )
        print()


if __name__ == "__main__":
    test_scoring_service()
