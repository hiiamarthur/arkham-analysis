from typing import List, Dict
from datetime import datetime
from collections import defaultdict, Counter

from ..investigator_card import InvestigatorCard
from ..deck import Deck


class InvestigatorStats:
    """Investigator-focused analysis providing card rankings and performance insights"""

    def __init__(
        self,
        investigator: InvestigatorCard,
        decks: List[Deck],
        trend_period: str = "month",
    ):
        self.investigator_code = investigator.code
        self.investigator_name = self._get_investigator_name(decks)
        self.all_decks = decks  # Store all decks for meta calculations
        self.decks = [
            deck for deck in decks if deck.investigator_code == investigator.code
        ]
        self.trend_period = trend_period

    def _get_investigator_name(self, decks: List[Deck]) -> str:
        """Get investigator name from decks"""
        for deck in decks:
            if deck.investigator_code == self.investigator_code:
                return getattr(deck, "investigator_name", self.investigator_code)
        return self.investigator_code

    def get_stats(self) -> Dict:
        """
        Complete investigator statistics including card rankings and performance analysis
        """
        if not self.decks:
            return {
                "investigator_info": {
                    "code": self.investigator_code,
                    "name": self.investigator_name,
                    "total_decks": 0,
                },
                "error": "No decks found for this investigator",
            }

        return {
            "investigator_info": {
                "code": self.investigator_code,
                "name": self.investigator_name,
                "total_decks": len(self.decks),
                "deck_activity_period": self._get_activity_period(),
            },
            # Core card analysis
            "card_rankings": self._get_card_rankings(),
            "staple_cards": self._get_staple_cards(),
            "rising_cards": self._get_trending_cards(direction="rising"),
            "falling_cards": self._get_trending_cards(direction="falling"),
            # Deck composition insights
            "deck_composition": self._get_deck_composition_stats(),
            "card_synergies": self._get_card_synergies(),
            "deck_archetypes": self._get_deck_archetypes(),
            # Performance indicators
            "optimization_score": self._calculate_optimization_score(),
            "underused_gems": self._find_underused_gems(),
            "overused_cards": self._find_overused_cards(),
            # Meta analysis
            "meta_position": self._get_meta_position(),
            "popularity_trends": self._get_popularity_trends(),
            "deck_diversity": self._calculate_deck_diversity(),
            # Advanced insights
            "card_efficiency_ratings": self._get_card_efficiency_ratings(),
            "build_recommendations": self._generate_build_recommendations(),
        }

    def _get_activity_period(self) -> Dict:
        """Get the time period of deck activity"""
        if not self.decks:
            return {}

        dates = [
            datetime.fromisoformat(deck.date_creation.replace("Z", "+00:00"))
            for deck in self.decks
            if hasattr(deck, "date_creation") and deck.date_creation
        ]

        if not dates:
            return {}

        return {
            "earliest_deck": min(dates).isoformat(),
            "latest_deck": max(dates).isoformat(),
            "active_months": len(set((d.year, d.month) for d in dates)),
        }

    def _get_card_rankings(self) -> List[Dict]:
        """Rank cards by usage frequency and effectiveness for this investigator"""
        card_usage = Counter()
        card_counts = defaultdict(list)  # Track quantities used

        for deck in self.decks:
            for card_code, quantity in deck.slots.items():
                card_usage[card_code] += 1
                card_counts[card_code].append(quantity)

        rankings = []
        total_decks = len(self.decks)

        for card_code, usage_count in card_usage.most_common(50):  # Top 50 cards
            quantities = card_counts[card_code]
            usage_rate = usage_count / total_decks
            avg_quantity = sum(quantities) / len(quantities)

            rankings.append(
                {
                    "card_code": card_code,
                    "usage_count": usage_count,
                    "usage_rate": usage_rate,
                    "average_quantity": round(avg_quantity, 2),
                    "min_quantity": min(quantities),
                    "max_quantity": max(quantities),
                    "consistency_score": self._calculate_consistency_score(quantities),
                }
            )

        return rankings

    def _get_staple_cards(self) -> List[Dict]:
        """Identify cards that are essential/staple for this investigator"""
        rankings = self._get_card_rankings()

        # Cards used in >60% of decks are considered staples
        staples = [card for card in rankings if card["usage_rate"] > 0.6]

        # Add stability metrics
        for staple in staples:
            staple["staple_confidence"] = min(
                staple["usage_rate"] * staple["consistency_score"], 1.0
            )

        return sorted(staples, key=lambda x: x["staple_confidence"], reverse=True)

    def _get_trending_cards(self, direction: str = "rising") -> List[Dict]:
        """Find cards trending up or down in usage"""
        if len(self.decks) < 10:  # Need minimum data for trends
            return []

        # Split decks into recent vs older periods
        sorted_decks = sorted(self.decks, key=lambda d: d.date_creation or "")
        split_point = len(sorted_decks) // 2

        older_decks = sorted_decks[:split_point]
        recent_decks = sorted_decks[split_point:]

        older_usage = self._get_usage_rates(older_decks)
        recent_usage = self._get_usage_rates(recent_decks)

        trending = []
        for card_code in set(older_usage.keys()) | set(recent_usage.keys()):
            old_rate = older_usage.get(card_code, 0)
            new_rate = recent_usage.get(card_code, 0)

            if old_rate > 0:  # Avoid division by zero
                change_rate = (new_rate - old_rate) / old_rate
                if (direction == "rising" and change_rate > 0.2) or (
                    direction == "falling" and change_rate < -0.2
                ):
                    trending.append(
                        {
                            "card_code": card_code,
                            "old_usage_rate": old_rate,
                            "new_usage_rate": new_rate,
                            "change_rate": change_rate,
                            "trend_strength": abs(change_rate),
                        }
                    )

        return sorted(trending, key=lambda x: x["trend_strength"], reverse=True)[:10]

    def _get_usage_rates(self, decks: List[Deck]) -> Dict[str, float]:
        """Calculate usage rates for cards in given deck list"""
        if not decks:
            return {}

        card_usage = Counter()
        for deck in decks:
            for card_code in deck.slots.keys():
                card_usage[card_code] += 1

        return {
            card_code: count / len(decks) for card_code, count in card_usage.items()
        }

    def _get_deck_composition_stats(self) -> Dict:
        """Analyze deck composition patterns"""
        if not self.decks:
            return {}

        total_cards = []

        for deck in self.decks:
            deck_size = sum(deck.slots.values())
            total_cards.append(deck_size)

        return {
            "average_deck_size": round(sum(total_cards) / len(total_cards), 1),
            "deck_size_range": [min(total_cards), max(total_cards)],
            "most_common_size": Counter(total_cards).most_common(1)[0][0],
            "deck_size_consistency": self._calculate_consistency_score(total_cards),
        }

    def _get_card_synergies(self) -> List[Dict]:
        """Find cards that often appear together in decks"""
        card_pairs = defaultdict(int)
        card_usage = defaultdict(int)

        for deck in self.decks:
            cards_in_deck = list(deck.slots.keys())
            for card in cards_in_deck:
                card_usage[card] += 1

            # Count co-occurrences
            for i, card1 in enumerate(cards_in_deck):
                for card2 in cards_in_deck[i + 1 :]:
                    pair = tuple(sorted([card1, card2]))
                    card_pairs[pair] += 1

        synergies = []
        for (card1, card2), co_count in card_pairs.items():
            if co_count >= 3:  # Minimum threshold
                card1_usage = card_usage[card1]
                card2_usage = card_usage[card2]

                # Calculate synergy strength (Jaccard similarity)
                synergy_strength = co_count / (card1_usage + card2_usage - co_count)

                synergies.append(
                    {
                        "card1": card1,
                        "card2": card2,
                        "co_occurrence_count": co_count,
                        "synergy_strength": round(synergy_strength, 3),
                        "card1_usage_rate": card1_usage / len(self.decks),
                        "card2_usage_rate": card2_usage / len(self.decks),
                    }
                )

        return sorted(synergies, key=lambda x: x["synergy_strength"], reverse=True)[:15]

    def _get_deck_archetypes(self) -> List[Dict]:
        """Identify common deck archetypes for this investigator"""
        # This is a simplified approach - could use clustering algorithms
        card_combinations = defaultdict(int)

        for deck in self.decks:
            # Use top 5 most frequent cards as archetype signature
            sorted_cards = sorted(deck.slots.items(), key=lambda x: x[1], reverse=True)
            signature = tuple(sorted([card for card, _ in sorted_cards[:5]]))
            card_combinations[signature] += 1

        archetypes = []
        for signature, count in card_combinations.items():
            if count >= 2:  # Minimum decks to form an archetype
                archetypes.append(
                    {
                        "archetype_signature": list(signature),
                        "deck_count": count,
                        "percentage": (count / len(self.decks)) * 100,
                        "archetype_id": f"archetype_{len(archetypes) + 1}",
                    }
                )

        return sorted(archetypes, key=lambda x: x["deck_count"], reverse=True)

    def _calculate_optimization_score(self) -> float:
        """Calculate how optimized the investigator's decks are on average"""
        if not self.decks:
            return 0.0

        # Simplified optimization score based on:
        # - Consistency of card choices
        # - Usage of staple cards
        # - Deck size consistency

        staples = self._get_staple_cards()
        staple_score = len(staples) / 10.0  # Normalize to 0-1 scale

        composition = self._get_deck_composition_stats()
        consistency_score = composition.get("deck_size_consistency", 0.5)

        return min((staple_score + consistency_score) / 2, 1.0)

    def _find_underused_gems(self) -> List[Dict]:
        """Find cards that might be undervalued/underused for this investigator"""
        # This would require cross-referencing with general card power level
        # For now, find cards with low usage but high consistency when used
        rankings = self._get_card_rankings()

        gems = []
        for card in rankings:
            if card["usage_rate"] < 0.2 and card["consistency_score"] > 0.8:
                gems.append(
                    {
                        "card_code": card["card_code"],
                        "usage_rate": card["usage_rate"],
                        "consistency_score": card["consistency_score"],
                        "gem_potential": card["consistency_score"]
                        / (card["usage_rate"] + 0.1),
                    }
                )

        return sorted(gems, key=lambda x: x["gem_potential"], reverse=True)[:10]

    def _find_overused_cards(self) -> List[Dict]:
        """Find cards that might be overused (high usage, low consistency)"""
        rankings = self._get_card_rankings()

        overused = []
        for card in rankings:
            if card["usage_rate"] > 0.4 and card["consistency_score"] < 0.5:
                overused.append(
                    {
                        "card_code": card["card_code"],
                        "usage_rate": card["usage_rate"],
                        "consistency_score": card["consistency_score"],
                        "overuse_indicator": card["usage_rate"]
                        / (card["consistency_score"] + 0.1),
                    }
                )

        return sorted(overused, key=lambda x: x["overuse_indicator"], reverse=True)[:10]

    def _get_meta_position(self) -> Dict:
        """Analyze investigator's position in the current meta"""
        total_decks_in_meta = len(self.all_decks) if self.all_decks else 1
        meta_share = (len(self.decks) / total_decks_in_meta) if total_decks_in_meta > 0 else 0.0

        return {
            "total_decks": len(self.decks),
            "meta_share": meta_share,
            "total_decks_analyzed": total_decks_in_meta,
            "activity_level": (
                "active"
                if len(self.decks) > 10
                else "moderate" if len(self.decks) > 5 else "low"
            ),
            "deck_innovation_score": self._calculate_innovation_score(),
        }

    def _calculate_innovation_score(self) -> float:
        """Calculate how innovative/diverse the investigator's decks are"""
        if len(self.decks) < 2:
            return 0.0

        unique_cards = set()
        for deck in self.decks:
            unique_cards.update(deck.slots.keys())

        # Innovation = unique cards / (average cards per deck * number of decks)
        avg_deck_size = sum(sum(deck.slots.values()) for deck in self.decks) / len(
            self.decks
        )
        innovation = len(unique_cards) / (avg_deck_size * len(self.decks))

        return min(innovation * 10, 1.0)  # Scale to 0-1

    def _get_popularity_trends(self) -> Dict:
        """Track popularity trends over time"""
        # Group decks by time period
        dated_decks = [
            deck
            for deck in self.decks
            if hasattr(deck, "date_creation") and deck.date_creation
        ]

        if len(dated_decks) < 5:
            return {"insufficient_data": True}

        # Simple trend calculation
        sorted_decks = sorted(dated_decks, key=lambda d: d.date_creation)
        periods = []

        # Split into quarters
        total_decks = len(sorted_decks)
        quarter_size = max(1, total_decks // 4)

        for i in range(0, total_decks, quarter_size):
            period_decks = sorted_decks[i : i + quarter_size]
            periods.append(len(period_decks))

        return {
            "quarterly_deck_counts": periods,
            "trend_direction": (
                "increasing" if periods[-1] > periods[0] else "decreasing"
            ),
            "peak_period": periods.index(max(periods)) + 1,
        }

    def _calculate_deck_diversity(self) -> Dict:
        """Measure diversity in deck building for this investigator"""
        if len(self.decks) < 2:
            return {"diversity_score": 0.0}

        all_cards = []
        unique_decks = set()

        for deck in self.decks:
            deck_signature = tuple(sorted(deck.slots.items()))
            unique_decks.add(deck_signature)
            all_cards.extend(deck.slots.keys())

        diversity_score = len(unique_decks) / len(self.decks)
        card_variety = len(set(all_cards)) / len(all_cards)

        return {
            "diversity_score": round(diversity_score, 3),
            "unique_deck_ratio": round(len(unique_decks) / len(self.decks), 3),
            "card_variety_score": round(card_variety, 3),
            "total_unique_cards": len(set(all_cards)),
        }

    def _get_card_efficiency_ratings(self) -> List[Dict]:
        """Rate card efficiency based on usage patterns"""
        rankings = self._get_card_rankings()[:20]  # Top 20 cards

        efficiency_ratings = []
        for card in rankings:
            # Efficiency = usage_rate * consistency * (1 / average_quantity)
            # Higher usage, more consistent, lower quantities needed = more efficient
            efficiency = (
                card["usage_rate"]
                * card["consistency_score"]
                * (1 / max(card["average_quantity"], 0.1))
            )

            efficiency_ratings.append(
                {
                    "card_code": card["card_code"],
                    "efficiency_score": round(efficiency, 3),
                    "usage_rate": card["usage_rate"],
                    "consistency_score": card["consistency_score"],
                    "average_quantity": card["average_quantity"],
                }
            )

        return sorted(
            efficiency_ratings, key=lambda x: x["efficiency_score"], reverse=True
        )

    def _generate_build_recommendations(self) -> Dict:
        """Generate deck building recommendations for this investigator"""
        staples = self._get_staple_cards()[:10]
        gems = self._find_underused_gems()[:5]
        trending_up = self._get_trending_cards("rising")[:5]

        return {
            "core_recommendations": [card["card_code"] for card in staples],
            "hidden_gems": [card["card_code"] for card in gems],
            "trending_picks": [card["card_code"] for card in trending_up],
            "build_advice": self._generate_build_advice(staples, gems),
            "meta_considerations": {
                "optimization_priority": (
                    "high" if self._calculate_optimization_score() < 0.6 else "low"
                ),
                "innovation_opportunity": (
                    "high" if self._calculate_innovation_score() < 0.3 else "moderate"
                ),
            },
        }

    def _generate_build_advice(
        self, staples: List[Dict], gems: List[Dict]
    ) -> List[str]:
        """Generate textual build advice"""
        advice = []

        if len(staples) < 5:
            advice.append(
                f"Consider building around more consistent core cards - only {len(staples)} staples identified"
            )

        if self._calculate_optimization_score() < 0.5:
            advice.append("Deck optimization could be improved - focus on consistency")

        if gems:
            advice.append(
                f"Explore underused cards like {gems[0]['card_code']} for potential advantages"
            )

        diversity = self._calculate_deck_diversity()
        if diversity["diversity_score"] < 0.3:
            advice.append("Consider experimenting with more diverse builds")

        return advice if advice else ["Current builds show good optimization"]

    def _calculate_consistency_score(self, values: List[int]) -> float:
        """Calculate consistency score for a list of values"""
        if len(values) <= 1:
            return 1.0

        mean_val = sum(values) / len(values)
        if mean_val == 0:
            return 1.0

        # Coefficient of variation (inverted for consistency)
        variance = sum((x - mean_val) ** 2 for x in values) / len(values)
        std_dev = variance**0.5
        cv = std_dev / mean_val

        return max(0.0, 1.0 - cv)
