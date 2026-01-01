import random
from typing import Counter, Dict, List, Union, Optional
from .token import ChaosToken, TokenString


class ChaosBag:
    def __init__(self, tokens: Optional[List[ChaosToken]] = None):
        self.tokens: List[ChaosToken] = tokens or []

    def add_token(self, token: ChaosToken) -> None:
        self.tokens.append(token)
        self.shuffle_tokens()

    def remove_token(self, token: ChaosToken) -> None:
        if token in self.tokens:
            self.tokens.remove(token)
        else:
            raise ValueError(f"Token {token} not found in bag")

    def draw_token(self) -> ChaosToken:
        if not self.tokens:
            raise ValueError("No tokens in bag")
        self.shuffle_tokens()
        return self.tokens.pop()

    def calculate_pass_prob(self, base_stat: int, difficulty: int) -> float:
        """
        Main method: compute exact pass probability considering all token draw paths.
        """
        if not self.tokens:
            return 0.0

        token_counts: Dict[str, int] = Counter(
            [token.name.value for token in self.tokens]
        )
        total_tokens = sum(token_counts.values())

        # Create a mapping of token_name -> ChaosToken instance (just one per type, used for value/effect)
        token_templates: Dict[str, ChaosToken] = {
            token.name.value: token for token in self.tokens
        }

        def recurse(mod_total: int, prob: float, token_pool: List[ChaosToken]) -> float:
            total = len(token_pool)
            if total == 0:
                return 0.0

            result = 0.0

            for i, token in enumerate(token_pool):
                token_prob = 1 / total
                next_pool = token_pool[:i] + token_pool[i + 1 :]  # Remove drawn token

                if (
                    token.name == TokenString.FROST
                    and [
                        token for token in token_pool if token.name == TokenString.FROST
                    ].__len__()
                    > 0
                ):
                    continue  # always fail

                if token.name == TokenString.AUTO_FAIL:
                    continue  # always fail

                if token.name == TokenString.ELDER_SIGN:
                    # Elder Sign always succeeds
                    result += prob * token_prob
                    continue

                if token.revealAnotherToken:
                    # Draw again (pool now smaller)
                    result += recurse(
                        mod_total + token.value, prob * token_prob, next_pool
                    )
                else:
                    total_value = base_stat + mod_total + token.value
                    if total_value >= difficulty:
                        result += prob * token_prob

            return result

        return recurse(mod_total=0, prob=1.0, token_pool=self.tokens.copy())

    def shuffle_tokens(self) -> None:
        random.shuffle(self.tokens)
