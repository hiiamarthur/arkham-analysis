# Changelog

All notable changes to Arkham Analysis are documented here.

---

## [2.0.1] - 2026-03-21

### Bug Fixes
- Dashboard investigator names now resolve correctly for parallel/reprint investigator codes — parallel decks were previously showing raw codes instead of names
- Investigator-by-faction meta share now correctly normalises parallel investigator codes to their canonical faction before counting
- Meta share window changed from 90 days to 365 days for a more representative picture
- Most versatile cards expanded to show top 10 (was 6)
- XP distribution percentages now calculated against decks with XP data only, so buckets correctly sum to 100%
- Investigator count in dashboard header now reflects deduplicated pool (99 unique investigators)
- Faction colours applied as left-border accents on investigator rank and trending rows

---

## [2.0.0] - 2026-03-21

### Overview
Major feature release focused on card data accuracy through reprint handling, deeper investigator analytics, and improved navigation across all pages.

### New Features

#### Pool Playground (new page)
- Brand new tool to compare card pools across multiple investigators side by side
- Instantly see which cards are shared, exclusive, or overlapping between any combination of investigators
- Each card displays faction, type, XP, cost, and slot at a glance
- Card name links directly to `/analysis/:code` for instant detail lookup
- Supports search, sorting, and column filtering across the combined pool

#### Reprint Deduplication (Global)
- Card statistics now combine counts across all printings of the same card — no more split numbers between original and reprint codes
- Card analysis page shows a **Reprints** section with clickable chips linking to each family member
- Dashboard top-card rankings normalised so reprints count toward the original
- Investigator list filters out parallel/reprint investigators, showing only canonical versions

#### Card Analysis
- Modal navigation: added a **back button** when browsing between related or bonded cards, tooltip shows the previous card's name
- Close button now has a tooltip
- Card page shows a graceful fallback when statistics are unavailable
- Add Card pool Session

#### Investigators Page
- URL updates to `/investigators/:code` on selection — supports direct linking and browser back/forward
- **Card Pool** section: lists every card legally playable by the investigator with XP, faction, type, slot and pack columns
- Card pool shows reprint chips in the name column linking to `/analysis/:code`
- Card pool restrictions (trait-based exclusions) shown as a human-readable summary
- Card rankings, staple cards, and trend lists deduplicate reprints and merge their usage numbers

#### Backend & Infrastructure
- SEO: sitemap and robots.txt; unique meta title and description per route
- Redis cache keys bumped across all endpoints

---

## [1.0.0] - 2026-03-16

### Overview
Initial public release of Arkham Analysis — an open analytics platform for Arkham Horror: The Card Game, powered by ArkhamDB deck data.

### Features

#### Dashboard
- Meta share breakdown by investigator and faction
- Top cards by usage rate with rising/falling trends

#### Card Analysis (`/analysis`)
- Full card browser with filters: faction, type, XP, cost, traits, pack
- Card detail modal: deck inclusion rate, investigator usage, trend chart, bonded cards, taboo status
- XP dot indicator and subname display in card listings

#### Threat Assessment (`/threat-assessment`)
- Chaos bag builder per campaign and scenario
- Token modifier inputs and skill test probability output

#### Investigators (`/investigators`)
- Investigator table with WP/INT/COM/AGI/HP/SAN columns, sortable and filterable
- Per-investigator panel: meta share, top cards, staple cards, synergies, trending picks, deck archetypes, underused gems, build recommendations

#### Backend
- FastAPI + async SQLAlchemy (PostgreSQL) with Redis caching (weekly TTL)
- ArkhamDB data sync pipeline
- Domain-driven card and investigator stats models
- Faction icon SVG system and Arkham custom font integration
- Deployed on Railway

---

[2.0.1]: https://github.com/arthurlau/arkham-analysis/compare/v2.0.0...v2.0.1
[2.0.0]: https://github.com/arthurlau/arkham-analysis/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/arthurlau/arkham-analysis/releases/tag/v1.0.0
