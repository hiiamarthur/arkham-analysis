# Changelog

All notable changes to Arkham Analysis are documented here.

---

## [2.1.0] - 2026-06-10

### Overview
Feature release focused on data accuracy (removing mocked stats), improved discoverability via shareable URLs and cycle filters, and UI polish across the dashboard and card analysis pages.

### New Features

#### Pool Playground
- **Shareable URLs** — investigator selection and all active filters are encoded into query params; sharing the URL restores the exact view for anyone who opens it
- **Session persistence** — state is saved to `sessionStorage` and restored on page refresh until the browser is closed
- **Cycle filter** — replaced the 55-item pack dropdown with compact cycle chips (Core, Dunwich, Carcosa, Forgotten Age, Circle Undone, Dream-Eaters, Innsmouth, and more); chips auto-dim when a cycle has no cards in the current pool
- **Copy link button** — one-click copy of the shareable URL, shown when 2+ investigators are loaded

#### Card Analysis
- **Customizable cards** — cards with upgrade options (Hunter's Armor, Runic Axe, Raven Quill, etc.) now show a formatted customization section with XP pip indicators per upgrade
- **Alternate versions bar** — investigator cards with parallel versions now show a linked bar to navigate between them
- **Encounter filter** — toggle to show/hide encounter cards; spoiler blur mode hides encounter card details except the name

#### Dashboard
- Investigator trend chart lines now use **faction colors** (Guardian blue, Seeker orange, Survivor red, etc.)
- **"Meta Share" renamed to "Deck Rate"** throughout — clearer label for the metric (% of published decks using this investigator/faction)

#### Investigators Page
- Deck Rate stat label updated to match dashboard

### Fixes
- Removed dead card-detail modal containing all mocked/random stats (usage rate, win rate, economy/impact/consistency/versatility scores, fake synergy cards, fake campaign performance) — none of it was visible to users but it has been cleaned up
- Card tooltip added to card listings
- Field suggestions on search
- Investigator image resize logic
- Timeout increased for ArkhamDB sync requests
- Responsive layout fixes

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

[2.1.0]: https://github.com/arthurlau/arkham-analysis/compare/v2.0.1...v2.1.0
[2.0.0]: https://github.com/arthurlau/arkham-analysis/compare/v1.0.0...v2.0.0
[1.0.0]: https://github.com/arthurlau/arkham-analysis/releases/tag/v1.0.0
