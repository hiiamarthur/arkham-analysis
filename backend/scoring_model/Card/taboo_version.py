from typing import Optional


class TabooVersion:
    def __init__(
        self,
        taboo_id: int,
        text: Optional[str] = None,
        cost: Optional[int] = None,
        level: Optional[int] = None,
    ):
        self.taboo_id = taboo_id
        self.text = text
        self.cost = cost
        self.level = level
