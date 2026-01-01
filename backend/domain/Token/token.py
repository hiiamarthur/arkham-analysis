from enum import Enum


class TokenString(Enum):
    ELDER_SIGN = "elder_sign"
    ZERO = "zero"
    PLUS_ONE = "plus_one"
    MINUS_ONE = "minus_one"
    MINUS_TWO = "minus_two"
    MINUS_THREE = "minus_three"
    MINUS_FOUR = "minus_four"
    MINUS_FIVE = "minus_five"
    MINUS_SIX = "minus_six"
    MINUS_SEVEN = "minus_seven"
    MINUS_EIGHT = "minus_eight"
    AUTO_FAIL = "auto_fail"
    BLESS = "bless"
    CURSE = "curse"
    SKULL = "skull"
    CULTIST = "cultist"
    TABLET = "tablet"
    ELDER_THING = "elder_thing"
    FROST = "frost"

    @staticmethod
    def from_str(str: str) -> "TokenString":
        return TokenString(str)


class ChaosToken:
    def __init__(
        self,
        name: TokenString,
        effect: str = "",
        value: int = 0,
        revealAnotherToken: bool = False,
    ):
        self.name = name
        self.effect = effect
        self.value = value
        self.revealAnotherToken = revealAnotherToken

    # def __name__(self) -> TokenString:
    #     return self.name


class ElderSignToken(ChaosToken):
    def __init__(
        self, effect: str = "", value: int = 0, revealAnotherToken: bool = False
    ):
        super().__init__(TokenString.ELDER_SIGN, effect, value, revealAnotherToken)


class ZeroToken(ChaosToken):
    def __init__(self):
        super().__init__(TokenString.ZERO, "", 0, False)


class PlusOneToken(ChaosToken):
    def __init__(self):
        super().__init__(TokenString.PLUS_ONE, "", 1, False)


class MinusOneToken(ChaosToken):
    def __init__(self):
        super().__init__(TokenString.MINUS_ONE, "", -1, False)


class MinusTwoToken(ChaosToken):
    def __init__(self):
        super().__init__(TokenString.MINUS_TWO, "", -2, False)


class MinusThreeToken(ChaosToken):
    def __init__(self):
        super().__init__(TokenString.MINUS_THREE, "", -3, False)


class MinusFourToken(ChaosToken):
    def __init__(self):
        super().__init__(TokenString.MINUS_FOUR, "", -4, False)


class MinusFiveToken(ChaosToken):
    def __init__(self):
        super().__init__(TokenString.MINUS_FIVE, "", -5, False)


class MinusSixToken(ChaosToken):
    def __init__(self):
        super().__init__(TokenString.MINUS_SIX, "", -6, False)


class MinusSevenToken(ChaosToken):
    def __init__(self):
        super().__init__(TokenString.MINUS_SEVEN, "", -7, False)


class MinusEightToken(ChaosToken):
    def __init__(self):
        super().__init__(TokenString.MINUS_EIGHT, "", -8, False)


class AutoFailToken(ChaosToken):
    def __init__(self):
        super().__init__(TokenString.AUTO_FAIL, "", -999, False)


class BlessToken(ChaosToken):
    def __init__(self):
        super().__init__(TokenString.BLESS, "", 2, True)


class CurseToken(ChaosToken):
    def __init__(self):
        super().__init__(TokenString.CURSE, "", -2, True)


class SkullToken(ChaosToken):
    def __init__(self, effect, value, revealAnotherToken: bool = False):
        super().__init__(TokenString.SKULL, effect, value, revealAnotherToken)


class CultistToken(ChaosToken):
    def __init__(self, effect, value, revealAnotherToken: bool = False):
        super().__init__(TokenString.CULTIST, effect, value, revealAnotherToken)


class TabletToken(ChaosToken):
    def __init__(self, effect, value, revealAnotherToken: bool = False):
        super().__init__(TokenString.TABLET, effect, value, revealAnotherToken)


class ElderThingToken(ChaosToken):
    def __init__(self, effect, value, revealAnotherToken: bool = False):
        super().__init__(TokenString.ELDER_THING, effect, value, revealAnotherToken)


class FrostToken(ChaosToken):
    def __init__(self, effect):
        super().__init__(TokenString.FROST, effect, -1, True)
