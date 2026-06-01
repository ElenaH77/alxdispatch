# alxdispatch.org — What Dispatch Heard, Alexandria VA

Cumulative map of pedestrian, cyclist, and scooter strikes — plus active-advocacy corridor crashes — captured from Alexandria's public dispatch audio.

Live at **https://alxdispatch.org/** (custom domain, GitHub Pages-hosted from this repo).

## Files

- `index.html` — the map page. Self-contained except for Leaflet + PapaParse via CDN.
- `incidents.csv` — the dataset. One row per incident. Columns documented in the handoff spec ([corridor-tracker-handoff.md](../new_upgrade/corridor-tracker-handoff.md) in the dev tree).
- `CNAME` — tells GitHub Pages to serve this repo at the custom domain.

The map fetches `incidents.csv` at load time. To update the map, edit the CSV — no code changes needed.

## Monthly workflow (when adding new incidents)

1. **Add cards to the relevant month-page repo** as usual (e.g., `alx-may-dispatch` → `index.html`, add `<article id="incident-NN">` block and audio under `audio/incident_NN/`).
2. **Append rows to `incidents.csv`** in this repo, one per new card. Match the existing column structure. For `card_url`, use the exact anchor format from the live page (May uses zero-padded two-digit IDs: `#incident-01`; April uses unpadded: `#incident-9`).
3. **Coordinates:** Elena captures these at review time in `batch_reviewer.py` by right-clicking the intersection in Google Maps and pasting the result into the **Coordinates** field on the verdict form. The exported verdicts CSV includes them, so adding a row to `incidents.csv` is a paste, not a separate geocoding step.
4. **Commit + push both repos.** GitHub Pages picks up the new data on its next build (usually within a minute).
5. **Spot-check a couple of new dots** open their cards correctly in the live map.

## Data conventions (don't break these)

- **`vru_strike`** drives the dot color. `Y` = navy (pedestrian/cyclist/scooter/motorcycle struck); blank/N = rust (vehicle-only / other).
- **`child_victim`** = `Y` if the victim was a child (under 18). Renders the dot at radius 9 (between adult VRU at 7 and fatality at 10) plus a `child victim` badge in the popup.
- **`corridor`** = `Braddock` / `Mount Vernon` / blank. Drives corridor filtering and badges.
- **`phase`** = `1` (east, Braddock Phase 1 / original Better Braddock) / `2` (west, Phase 2 / Minnie Howard area). Braddock corridor only.
- **`drca_borders`** = `Y` if within DRCA boundaries (Glebe N, Russell E, Braddock S, Rt 1 + CSX W).
- **`incident_type`** stays separate from `mode`. A two-car crash must never be coded as a VRU strike.
- **`lat`/`lng`** are hand-verified intersection-level coords (Google Maps right-click); `geo_precision` documents the resolution.

## Coverage caveat

April was published as a citywide VRU project. April VRU strikes (including corridor strikes) are complete. April vehicle-only corridor crashes are NOT systematically captured — only one is in the dataset (`apr-101`). Systematic vehicle-crash tracking on the corridors begins May 2026.

## Architecture note

This is a one-time prototype-to-production lift from a chat-built map. The longer-term plan documented in the handoff spec is to *generate* `incidents.csv` from the per-card config in the month-page repos, so a card and its tracker row can never diverge. For now, `incidents.csv` is hand-maintained alongside the cards.
