#!/usr/bin/env python3
"""
Test script to demonstrate ScenarioContextService usage
Run with: python test_scenario_context.py
"""

import asyncio
import json
from app.services.scenario_context_service import scenario_context_service


async def test_gathering_context():
    """Test The Gathering scenario context extraction"""
    print("=== Testing The Gathering Scenario Context ===\n")
    
    # Test different difficulty levels
    difficulties = ["Easy", "Standard", "Hard", "Expert"]
    
    for difficulty in difficulties:
        print(f"--- {difficulty} Difficulty ---")
        context = await scenario_context_service.get_scenario_context("01104", difficulty)
        
        # Display key context information
        print(f"Scenario: {context['scenario_name']}")
        print(f"Campaign: {context['campaign']}")
        print(f"Average Enemy Health: {context['avg_enemy_health']}")
        print(f"Average Enemy Fight: {context['avg_enemy_fight']}")
        print(f"Average Enemy Evade: {context['avg_enemy_evade']}")
        print(f"Average Location Shroud: {context['avg_shroud_value']}")
        print(f"Average Clues per Location: {context['avg_clues_per_location']}")
        print(f"Doom Threshold: {context['doom_threshold']}")
        
        # Show chaos bag composition
        print("Chaos Bag:")
        chaos_tokens = context['chaos_tokens']
        for token, count in chaos_tokens.items():
            if count > 0:
                print(f"  {token}: {count}")
        
        # Show special token effects
        if 'special_token_effects' in context:
            print("Special Token Effects:")
            for token, effect in context['special_token_effects'].items():
                print(f"  {token}: {effect['description']}")
        
        print(f"Resource Scarcity: {context['resource_scarcity']}")
        print(f"Action Economy Stress: {context['action_economy_stress']}")
        print(f"Scenario Length: {context['scenario_length']}")
        print(f"Victory Conditions: {context['victory_conditions']}")
        print("-" * 50)


async def test_context_caching():
    """Test context caching performance"""
    print("\n=== Testing Context Caching ===")
    
    import time
    
    # First call (should build context)
    start_time = time.time()
    context1 = await scenario_context_service.get_scenario_context("01104", "Standard")
    first_call_time = time.time() - start_time
    print(f"First call (build): {first_call_time:.4f} seconds")
    
    # Second call (should use cache)
    start_time = time.time()
    context2 = await scenario_context_service.get_scenario_context("01104", "Standard")
    second_call_time = time.time() - start_time
    print(f"Second call (cache): {second_call_time:.4f} seconds")
    
    # Verify they're the same
    print(f"Contexts identical: {context1 == context2}")
    print(f"Performance improvement: {first_call_time / second_call_time:.1f}x faster")


async def demonstrate_card_evaluation_context():
    """Show how scenario context would be used in card evaluation"""
    print("\n=== Card Evaluation Context Usage ===")
    
    # Get scenario context
    context = await scenario_context_service.get_scenario_context("01104", "Standard")
    
    # Example card evaluation considerations based on context
    print("Based on The Gathering context, here's how cards would be evaluated differently:")
    print()
    
    print("🗡️  COMBAT CARDS:")
    print(f"   - Enemy fight values average {context['avg_enemy_fight']}, so cards with +2 combat boost are valuable")
    print(f"   - Average enemy health is {context['avg_enemy_health']}, so 1-damage cards are often sufficient")
    print(f"   - Primary enemy type: {context['primary_enemy_type']} (affects specific counters)")
    print()
    
    print("🔍 INVESTIGATION CARDS:")
    print(f"   - Average shroud value is {context['avg_shroud_value']}, so +2 intellect cards are strong")
    print(f"   - Average clues per location: {context['avg_clues_per_location']}")
    print(f"   - Total clues needed: {context['total_clues_in_scenario']} per investigator")
    print(f"   - Special movement rules: {context['special_movement_rules']}")
    print()
    
    print("🎭 CHAOS BAG CONSIDERATIONS:")
    negative_tokens = sum(count for token, count in context['chaos_tokens'].items() 
                         if token.startswith('-') and count > 0)
    total_tokens = sum(context['chaos_tokens'].values())
    negative_ratio = negative_tokens / total_tokens
    print(f"   - Negative token ratio: {negative_ratio:.2%}")
    print(f"   - Special tokens have additional effects (skull, cultist, tablet)")
    print(f"   - Cards that ignore chaos tokens are more valuable due to special effects")
    print()
    
    print("⏰ TEMPO CONSIDERATIONS:")
    print(f"   - Scenario length: {context['scenario_length']} ({context['tempo']})")
    print(f"   - Doom threshold: {context['doom_threshold']} turns")
    print(f"   - Action economy stress: {context['action_economy_stress']}")
    print(f"   - Early game setup cards are valuable due to slow buildup")
    print()
    
    print("💰 RESOURCE CONSIDERATIONS:")
    print(f"   - Resource scarcity: {context['resource_scarcity']}")
    print(f"   - Card draw availability: {context['card_draw_availability']}")
    print(f"   - Expensive cards are less penalized due to normal resource availability")


async def compare_difficulty_impacts():
    """Show how difficulty affects context and card evaluation"""
    print("\n=== Difficulty Impact Analysis ===")
    
    difficulties = ["Easy", "Standard", "Expert"]
    contexts = {}
    
    for diff in difficulties:
        contexts[diff] = await scenario_context_service.get_scenario_context("01104", diff)
    
    print("Chaos Bag Comparison:")
    print("Token    Easy  Std  Expert")
    print("-" * 25)
    
    # Get all unique tokens
    all_tokens = set()
    for context in contexts.values():
        all_tokens.update(context['chaos_tokens'].keys())
    
    # Sort tokens for better display
    sorted_tokens = sorted(all_tokens, key=lambda x: (
        0 if x.startswith('+') else 1 if x == '0' else 2 if x.startswith('-') else 3,
        x
    ))
    
    for token in sorted_tokens:
        easy_count = contexts["Easy"]['chaos_tokens'].get(token, 0)
        std_count = contexts["Standard"]['chaos_tokens'].get(token, 0)
        expert_count = contexts["Expert"]['chaos_tokens'].get(token, 0)
        print(f"{token:8s} {easy_count:3d}  {std_count:3d}   {expert_count:3d}")
    
    print("\nSpecial Token Effect Changes:")
    for diff in difficulties:
        if 'special_token_effects' in contexts[diff]:
            print(f"\n{diff}:")
            for token, effect in contexts[diff]['special_token_effects'].items():
                print(f"  {token}: {effect['description']}")


async def main():
    """Run all tests"""
    try:
        await test_gathering_context()
        await test_context_caching()
        await demonstrate_card_evaluation_context()
        await compare_difficulty_impacts()
        
        print("\n✅ All tests completed successfully!")
        print("\nNext steps:")
        print("1. Run database migration to create encounter tables")
        print("2. Call /scenarios/populate-encounter-data to fetch real encounter card data") 
        print("3. Integrate scenario context into your BaseEvaluator.evaluate_card_strength()")
        print("4. Add more scenarios beyond The Gathering")
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    asyncio.run(main())