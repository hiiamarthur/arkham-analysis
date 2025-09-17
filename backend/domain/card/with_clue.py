from dataclasses import dataclass


@dataclass
class WithClue:
    clues: int = 0
    clues_fixed: bool = False
    # def __init__(self, clues: int = 0, clues_fixed: bool = False):
    #     self.clues = clues
    #     self.clues_fixed = clues_fixed
