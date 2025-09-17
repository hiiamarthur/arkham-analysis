from typing import List, Dict, Optional, Union
from datetime import datetime, timedelta
from collections import defaultdict
from ..deck import Deck
from ..player_card import PlayerCard


class CardStats:
    def __init__(
        self, card: PlayerCard, decks: List[Deck], trend_period: str = "month"
    ):
        print("__init__len", len(decks))
        self.decks = decks
        self.card = card
        self.trend_period = trend_period

    def get_deck_stats(self, trend_period: str = "month"):
        return {
            "popularity": self.get_popularity(),
            "trend": self.get_trend(period=trend_period),
        }

    def get_investigator_usage_rate(self):
        return {
            investigator: len(
                [deck for deck in self.decks if deck.investigator_code == investigator]
            )
            / len(self.decks)
            for investigator in set(
                deck.investigator_code
                for deck in self.decks
                if hasattr(deck, "investigator_code")
            )
            if len(
                [deck for deck in self.decks if deck.investigator_code == investigator]
            )
            > 0
        }

    def get_popularity(self):
        included_deck = [
            deck
            for deck in self.decks
            if self.card.code in deck.slots.keys()
            or self.card.code in dict(deck.sideSlots).keys()
        ]
        print("len", len(included_deck), len(self.decks))
        return {
            "overall_usage_rate": (
                len(included_deck) / len(self.decks) if len(self.decks) > 0 else 0.0
            ),
            "investigator_usage_rate": self._calculate_investigator_usage_rates(
                included_deck
            ),
            "investigator_spread": self._calculate_investigator_spread(included_deck),
        }

    def _calculate_investigator_spread(self, included_deck):
        """Calculate what fraction of investigators use this card (safely handle division by zero)"""
        # Get unique investigators that use this card
        investigators_using_card = set(
            [
                deck.investigator_code
                for deck in included_deck
                if hasattr(deck, "investigator_code") and deck.investigator_code
            ]
        )

        # Get total unique investigators in dataset
        total_investigators = set(
            [
                deck.investigator_code
                for deck in self.decks
                if hasattr(deck, "investigator_code") and deck.investigator_code
            ]
        )

        # Safely calculate spread
        if len(total_investigators) == 0:
            return 0.0

        return len(investigators_using_card) / len(total_investigators)

    def _calculate_investigator_usage_rates(self, included_deck):
        """Calculate usage rates per investigator (safely handle division by zero)"""
        usage_rates = {}

        # Get all unique investigators
        all_investigators = set(
            deck.investigator_code
            for deck in self.decks
            if hasattr(deck, "investigator_code") and deck.investigator_code
        )

        for investigator in all_investigators:
            # Decks with this card for this investigator
            investigator_decks_with_card = [
                deck
                for deck in included_deck
                if hasattr(deck, "investigator_code")
                and deck.investigator_code == investigator
            ]

            # Total decks for this investigator
            total_investigator_decks = [
                deck
                for deck in self.decks
                if hasattr(deck, "investigator_code")
                and deck.investigator_code == investigator
            ]

            # Safe division
            if len(total_investigator_decks) > 0:
                usage_rates[investigator] = len(investigator_decks_with_card) / len(
                    total_investigator_decks
                )
            else:
                usage_rates[investigator] = 0.0

        return usage_rates

    def get_trend(self, period: str = "month") -> Dict:
        """
        Calculate card usage trend over time periods
        Args:
            period: 'week', 'month', or 'year'
        Returns:
            Dict with trend data including usage rates over time
        """
        if not self.decks:
            return {"trend_data": {}, "trend_direction": "stable", "change_rate": 0}

        # Filter decks that have date_creation
        dated_decks = [
            deck
            for deck in self.decks
            if hasattr(deck, "date_creation") and deck.date_creation
        ]
        if not dated_decks:
            return {"trend_data": {}, "trend_direction": "no_data", "change_rate": 0}

        # Group decks by time period
        period_groups = defaultdict(list)
        period_usage = {}

        for deck in dated_decks:
            period_key = self._get_period_key(deck.date_creation, period)
            period_groups[period_key].append(deck)

        # Calculate usage rate for each period
        for period_key, period_decks in period_groups.items():
            decks_with_card = [
                deck
                for deck in period_decks
                if self.card.code in deck.slots.keys()
                or self.card.code in dict(deck.sideSlots).keys()
            ]
            usage_rate = len(decks_with_card) / len(period_decks) if period_decks else 0
            period_usage[period_key] = {
                "usage_rate": usage_rate,
                "total_decks": len(period_decks),
                "decks_with_card": len(decks_with_card),
            }

        # Calculate trend direction
        sorted_periods = sorted(period_usage.keys())
        trend_direction = "stable"
        change_rate = 0

        if len(sorted_periods) >= 2:
            recent_usage = period_usage[sorted_periods[-1]]["usage_rate"]
            older_usage = period_usage[sorted_periods[0]]["usage_rate"]

            if older_usage > 0:
                change_rate = ((recent_usage - older_usage) / older_usage) * 100
                if change_rate > 5:
                    trend_direction = "increasing"
                elif change_rate < -5:
                    trend_direction = "decreasing"

        return {
            "trend_data": dict(sorted(period_usage.items())),
            "trend_direction": trend_direction,
            "change_rate": round(change_rate, 2),
            "periods_analyzed": len(sorted_periods),
        }

    def _get_period_key(self, date: Union[datetime, str], period: str) -> str:
        """Generate period key for grouping"""
        if isinstance(date, str):
            # Handle ISO format strings with timezone
            date_str = date.replace("Z", "+00:00") if "Z" in date else date
            try:
                date = datetime.fromisoformat(date_str)
            except ValueError:
                # Fallback for other date formats
                date = datetime.strptime(date_str, "%Y-%m-%d")

        if period == "week":
            # Get Monday of the week
            monday = date - timedelta(days=date.weekday())
            return monday.strftime("%Y-W%U")
        elif period == "month":
            return date.strftime("%Y-%m")
        elif period == "year":
            return date.strftime("%Y")
        else:
            return date.strftime("%Y-%m")  # Default to month
