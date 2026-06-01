# alxdispatch.org — What Dispatch Heard, Alexandria VA

Cumulative map of pedestrian, cyclist, and scooter strikes — plus active-advocacy corridor crashes — captured from Alexandria's public dispatch audio.

Live at **https://alxdispatch.org/** (custom domain, GitHub Pages-hosted from this repo).

## Site structure

This is a **multi-page site** built from a small static generator. The interactive
map is the homepage; methodology, recommendations, data, and the monthly archive
are their own pages, all sharing one header/footer.

```
/                    home — the interactive map + intro + "how to read this map" key
/methodology/        how the data is gathered (evergreen; copied from the April piece)
/recommendations/    the policy / advocacy asks (evergreen; copied from the April piece)
/data/               the dataset: incidents.csv, column dictionary, reuse terms, scope caveat
/about/              what this is, who runs it, the NVFSS handoff plan, contact
/archive/            monthly write-ups, newest first
/archive/2026-05/    the May running log (copied in; the canonical home for May)
                     April lives at its original standalone URL and is linked, not moved.
```

### Source files vs. generated files

- **`build.py`** — the generator. Run `python3 build.py` to regenerate every page.
- **`partials/`** — `base.html` (page skeleton), `footer.html` (shared footer). The nav
  is built in `build.py` so it's defined once.
- **`src/`** — the body content for each page (`home.html`, `methodology.html`, …). **Edit these.**
- **`assets/site.css`** — shared styles (palette, Lora + Work Sans, nav, footer, prose).
- **`incidents.csv`** — the dataset. One row per incident. Full column dictionary on `/data/`.
- `index.html`, `*/index.html` — **generated output. Do not hand-edit** — run `build.py`.
- `CNAME` — tells GitHub Pages to serve this repo at the custom domain.

The map fetches `incidents.csv` at load time. To update the map's *data*, edit the CSV —
no rebuild needed. To change page *content or layout*, edit `src/` or `partials/` and re-run `build.py`.

## Monthly workflow (when adding new incidents)

1. **Build the month's cards** as usual (the per-card config → `build_site.py` in the dev tree).
2. **Bring the month into the archive.** Copy the published month page into
   `archive/<YYYY-MM>/` (its `index.html` + `audio/` + `og.png`). Add the month to
   `ARCHIVE_MONTHS` in `build.py` and to `src/archive.html`, then run `python3 build.py`
   — it injects the shared nav bar into the month page. (April is the grandfathered
   exception: it stays at its original standalone URL and is only *linked* from the archive.)
3. **Append rows to `incidents.csv`**, one per new card. Match the existing columns.
   For `card_url`, point at the in-site archive path: `/archive/<YYYY-MM>/#incident-NN`
   (May uses zero-padded two-digit IDs: `#incident-01`).
4. **Coordinates:** captured at review time in `batch_reviewer.py` (right-click the
   intersection in Google Maps → paste into the **Coordinates** field). The exported
   verdicts CSV includes them, so adding a row is a paste, not a separate geocoding step.
5. **Commit + push.** GitHub Pages rebuilds within a minute. Spot-check that a few new
   dots open their cards and that the audio plays.

## Data conventions (don't break these)

- **`vru_strike`** drives the dot color **and shape**. `Y` = navy **circle** (pedestrian/cyclist/scooter/motorcycle struck); blank/N = rust **diamond** (vehicle-only / other). Color + shape together so the map never relies on color alone (colorblind-safe).
- **`child_victim`** = `Y` if the victim was a child (under 18). Renders the dot at radius 9 (between adult VRU at 7 and fatality at 10) plus a `child victim` badge in the popup.
- **`corridor`** = `Braddock` / `Mount Vernon` / blank. Drives corridor filtering and badges.
- **`phase`** = `1` (east, Braddock Phase 1 / original Better Braddock) / `2` (west, Phase 2 / Minnie Howard area). Braddock corridor only.
- **`drca_borders`** = `Y` if within DRCA boundaries (Glebe N, Russell E, Braddock S, Rt 1 + CSX W).
- **`incident_type`** stays separate from `mode`. A two-car crash must never be coded as a VRU strike.
- **`lat`/`lng`** are hand-verified intersection-level coords (Google Maps right-click); `geo_precision` documents the resolution.

## Coverage caveat

April was published as a citywide VRU project. April VRU strikes (including corridor strikes) are complete. April vehicle-only corridor crashes are NOT systematically captured — only one is in the dataset (`apr-101`). Systematic vehicle-crash tracking on the corridors begins May 2026.

## Architecture note

The site is static (GitHub Pages) and is assembled by `build.py` from `src/` + `partials/`.
`incidents.csv` is still hand-maintained alongside the cards; the longer-term plan documented
in the handoff spec is to *generate* it from the per-card config so a card and its tracker row
can never diverge.
