import unittest
import sys
import os

# Add the project root to Python path
sys.path.append(
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from domain.Token.chaos_bag import ChaosBag
from domain.Token.token import (
    ChaosToken,
    TokenString,
    ElderSignToken,
    AutoFailToken,
    PlusOneToken,
    ZeroToken,
    MinusOneToken,
    MinusTwoToken,
    BlessToken,
    CurseToken,
    SkullToken,
)
from domain.Scenario import (
    NightOfTheZealot,
    TheDunwichLegacy,
    ScenarioType,
    Difficulty,
)


class TestChaosToken(unittest.TestCase):
    """Test individual chaos tokens"""

    def test_elder_sign_token(self):
        token = ElderSignToken()
        self.assertEqual(token.name, TokenString.ELDER_SIGN)
        self.assertEqual(token.value, 0)
        self.assertFalse(token.revealAnotherToken)

    def test_auto_fail_token(self):
        token = AutoFailToken()
        self.assertEqual(token.name, TokenString.AUTO_FAIL)
        self.assertEqual(token.value, -999)
        self.assertFalse(token.revealAnotherToken)

    def test_bless_token(self):
        token = BlessToken()
        self.assertEqual(token.name, TokenString.BLESS)
        self.assertEqual(token.value, 2)
        self.assertTrue(token.revealAnotherToken)

    def test_curse_token(self):
        token = CurseToken()
        self.assertEqual(token.name, TokenString.CURSE)
        self.assertEqual(token.value, -2)
        self.assertTrue(token.revealAnotherToken)

    def test_skull_token(self):
        token = SkullToken("Test effect", -3)
        self.assertEqual(token.name, TokenString.SKULL)
        self.assertEqual(token.value, -3)
        self.assertEqual(token.effect, "Test effect")


class TestChaosBag(unittest.TestCase):
    """Test ChaosBag class functionality"""

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.empty_bag = ChaosBag()
        self.simple_bag = ChaosBag(
            [
                ElderSignToken(),
                AutoFailToken(),
                ZeroToken(),
                MinusOneToken(),
                MinusTwoToken(),
            ]
        )

    def test_empty_bag_initialization(self):
        """Test empty bag initialization"""
        self.assertEqual(len(self.empty_bag.tokens), 0)

    def test_bag_with_tokens_initialization(self):
        """Test bag initialization with tokens"""
        self.assertEqual(len(self.simple_bag.tokens), 5)

    def test_add_token(self):
        """Test adding tokens to bag"""
        initial_count = len(self.empty_bag.tokens)
        self.empty_bag.add_token(PlusOneToken())
        self.assertEqual(len(self.empty_bag.tokens), initial_count + 1)

    def test_draw_token_from_empty_bag(self):
        """Test drawing from empty bag raises error"""
        with self.assertRaises(ValueError):
            self.empty_bag.draw_token()

    def test_draw_token_reduces_bag_size(self):
        """Test drawing token reduces bag size"""
        initial_count = len(self.simple_bag.tokens)
        token = self.simple_bag.draw_token()
        self.assertEqual(len(self.simple_bag.tokens), initial_count - 1)
        self.assertIsInstance(token, ChaosToken)

    def test_probability_calculation_empty_bag(self):
        """Test probability calculation with empty bag"""
        prob = self.empty_bag.calculate_pass_prob(base_stat=3, difficulty=2)
        self.assertEqual(prob, 0.0)

    def test_probability_calculation_guaranteed_success(self):
        """Test probability with guaranteed success (Elder Sign only)"""
        elder_sign_bag = ChaosBag([ElderSignToken()])
        prob = elder_sign_bag.calculate_pass_prob(base_stat=1, difficulty=10)
        self.assertEqual(prob, 1.0)

    def test_probability_calculation_guaranteed_failure(self):
        """Test probability with guaranteed failure (Auto-fail only)"""
        auto_fail_bag = ChaosBag([AutoFailToken()])
        prob = auto_fail_bag.calculate_pass_prob(base_stat=10, difficulty=1)
        self.assertEqual(prob, 0.0)

    def test_probability_calculation_basic_tokens(self):
        """Test probability calculation with basic numerical tokens"""
        # Bag with only +1, 0, -1 tokens
        basic_bag = ChaosBag(
            [
                PlusOneToken(),  # +1: 4+1=5 >= 3 ✓
                ZeroToken(),  # 0:  4+0=4 >= 3 ✓
                MinusOneToken(),  # -1: 4-1=3 >= 3 ✓
            ]
        )
        prob = basic_bag.calculate_pass_prob(base_stat=4, difficulty=3)
        self.assertEqual(prob, 1.0)  # All tokens succeed

        # Test where some tokens fail
        basic_bag2 = ChaosBag(
            [
                PlusOneToken(),  # +1: 2+1=3 >= 4 ✗
                ZeroToken(),  # 0:  2+0=2 >= 4 ✗
                MinusOneToken(),  # -1: 2-1=1 >= 4 ✗
            ]
        )
        prob2 = basic_bag2.calculate_pass_prob(base_stat=2, difficulty=4)
        self.assertEqual(prob2, 0.0)  # All tokens fail

    def test_probability_calculation_with_bless_tokens(self):
        """Test probability calculation with reveal-another-token mechanics"""
        # Bless token (+2) that reveals another token
        bless_bag = ChaosBag(
            [
                BlessToken(),  # +2, reveal another
                ZeroToken(),  # After bless: 3+2+0=5 >= 4 ✓
            ]
        )
        prob = bless_bag.calculate_pass_prob(base_stat=3, difficulty=4)
        self.assertEqual(prob, 0.5)  # 50% chance to draw bless first


class TestScenarios(unittest.TestCase):
    """Test scenario implementations"""

    def test_night_of_zealot_easy(self):
        """Test Night of the Zealot Easy difficulty"""
        scenario = NightOfTheZealot(ScenarioType.THE_GATHERING, Difficulty.EASY)

        # Check bag has correct number of tokens
        # Base: Elder Sign + Auto-fail + 12 other tokens = 14 total for Easy
        self.assertEqual(len(scenario.chaos_bag.tokens), 14)

        # Test probability calculation
        prob = scenario.chaos_bag.calculate_pass_prob(base_stat=4, difficulty=3)
        self.assertGreater(prob, 0.0)
        self.assertLess(prob, 1.0)

    def test_night_of_zealot_expert(self):
        """Test Night of the Zealot Expert difficulty"""
        scenario = NightOfTheZealot(ScenarioType.THE_GATHERING, Difficulty.EXPERT)

        # Expert should have fewer tokens and be harder
        expert_tokens = len(scenario.chaos_bag.tokens)

        easy_scenario = NightOfTheZealot(ScenarioType.THE_GATHERING, Difficulty.EASY)
        easy_tokens = len(easy_scenario.chaos_bag.tokens)

        # Expert has fewer total tokens
        self.assertLess(expert_tokens, easy_tokens)

    def test_dunwich_legacy_standard(self):
        """Test Dunwich Legacy Standard difficulty"""
        scenario = TheDunwichLegacy(
            ScenarioType.EXTRACURRICULAR_ACTIVITIES, Difficulty.STANDARD
        )

        # Check bag is properly initialized
        self.assertGreater(len(scenario.chaos_bag.tokens), 0)

        # Test probability calculation
        prob = scenario.chaos_bag.calculate_pass_prob(base_stat=3, difficulty=2)
        self.assertGreater(prob, 0.0)
        self.assertLessEqual(prob, 1.0)


class TestProbabilityEdgeCases(unittest.TestCase):
    """Test edge cases in probability calculations"""

    def test_mixed_token_bag(self):
        """Test realistic mixed token bag"""
        mixed_bag = ChaosBag(
            [
                ElderSignToken(),  # Always succeeds
                AutoFailToken(),  # Always fails
                PlusOneToken(),  # +1
                ZeroToken(),  # 0
                ZeroToken(),  # 0
                MinusOneToken(),  # -1
                MinusOneToken(),  # -1
                MinusTwoToken(),  # -2
                SkullToken("", -2),  # -2
                SkullToken("", -3),  # -3
            ]
        )

        # Test various skill test scenarios
        prob_easy = mixed_bag.calculate_pass_prob(base_stat=5, difficulty=2)
        prob_hard = mixed_bag.calculate_pass_prob(base_stat=3, difficulty=5)

        # Easy test should have higher success rate
        self.assertGreater(prob_easy, prob_hard)

        # Both should be between 0 and 1
        self.assertGreaterEqual(prob_easy, 0.0)
        self.assertLessEqual(prob_easy, 1.0)
        self.assertGreaterEqual(prob_hard, 0.0)
        self.assertLessEqual(prob_hard, 1.0)


def demonstrate_chaos_bag_usage():
    """Demonstrate practical usage of the chaos bag system"""
    print("=== CHAOS BAG DEMONSTRATION ===\n")

    # Create a Night of the Zealot scenario
    print("1. Creating Night of the Zealot - The Gathering (Standard)")
    scenario = NightOfTheZealot(ScenarioType.THE_GATHERING, Difficulty.STANDARD)
    print(f"   Chaos bag contains {len(scenario.chaos_bag.tokens)} tokens\n")

    # Test different skill scenarios
    test_cases = [
        {"skill": 2, "difficulty": 2, "description": "Low skill vs low difficulty"},
        {"skill": 4, "difficulty": 3, "description": "Good skill vs medium difficulty"},
        {"skill": 3, "difficulty": 5, "description": "Medium skill vs high difficulty"},
        {"skill": 6, "difficulty": 4, "description": "High skill vs medium difficulty"},
    ]

    print("2. Testing skill test probabilities:")
    for i, test in enumerate(test_cases, 1):
        prob = scenario.chaos_bag.calculate_pass_prob(
            base_stat=test["skill"], difficulty=test["difficulty"]
        )
        print(f"   {i}. {test['description']}")
        print(
            f"      Skill {test['skill']} vs Difficulty {test['difficulty']}: {prob:.1%} success rate"
        )

    print("\n3. Comparing difficulties:")
    difficulties = [
        Difficulty.EASY,
        Difficulty.STANDARD,
        Difficulty.HARD,
        Difficulty.EXPERT,
    ]

    for diff in difficulties:
        scenario = NightOfTheZealot(ScenarioType.THE_GATHERING, diff)
        prob = scenario.chaos_bag.calculate_pass_prob(base_stat=4, difficulty=3)
        print(f"   {diff.value.title()}: {prob:.1%} success (skill 4 vs difficulty 3)")

    print("\n4. Testing token draw mechanics:")
    test_bag = ChaosBag(
        [
            ElderSignToken(),
            AutoFailToken(),
            ZeroToken(),
            MinusOneToken(),
            SkullToken("Test skull", -2),
        ]
    )

    print(f"   Created test bag with {len(test_bag.tokens)} tokens")
    for i in range(3):
        if test_bag.tokens:  # Check if tokens remain
            token = test_bag.draw_token()
            print(f"   Draw {i+1}: {token.name.value} (value: {token.value})")
        else:
            print(f"   Draw {i+1}: Bag is empty!")

    print(f"   Tokens remaining: {len(test_bag.tokens)}")


if __name__ == "__main__":
    # Run the demonstration
    demonstrate_chaos_bag_usage()

    print("\n" + "=" * 50)
    print("RUNNING UNIT TESTS")
    print("=" * 50)

    # Run unit tests
    unittest.main(verbosity=2)
