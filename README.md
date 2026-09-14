# Nigeria Zoonotic Disease Mapping (WAHIS, 2006-2025)

State-level choropleth maps of reported Rabies, HPAI (avian influenza),
and Trypanosomosis outbreaks in Nigeria, built in QGIS from WAHIS
(World Animal Health Information System) surveillance data. Built as a
practical application of QGIS learned alongside the Johns Hopkins
epidemiology course on Coursera, and as a One Health surveillance
case study.

## What this shows

Three static choropleth maps, one per disease:

- `outputs/nigeria_rabies_choropleth_2006-2025.png`
- `outputs/nigeria_hpai_choropleth_2006-2025.png`
- `outputs/nigeria_trypanosomosis_choropleth_2006-2025.png`

Each map shades Nigeria's 36 states + FCT by the number of outbreaks
reported to WAHIS between 2006 and 2025. States with no outbreak
report in that period are shown in grey and labeled explicitly
("No outbreak report identified in WAHIS for 2006-2025") rather than
folded into the lowest color class, since a real zero and an absence
of reporting are not the same thing.

**Important framing:** these maps show *reported outbreaks*, not true
disease incidence. A grey state has no WAHIS record for that
disease in this window - it does not mean the disease is absent
there. This distinction matters most for Trypanosomosis, where 20 of
37 states have no reported outbreaks at all, most likely reflecting
gaps in surveillance and reporting rather than a genuine absence of
the disease.

## Data pipeline

1. **Raw data**: `data/raw/WAHIS_3_DISEASES_Quantitative_data_2026-09-05.csv`
   - Semester-level WAHIS records for Nigeria, 2005-2026, across Rabies,
     HPAI, and Trypanosomosis.
2. **Cleaning and audit**: `data/processed/animal_disease_RESULTS_2006_2025.xlsx`
   - Full audit trail: geography cleaning (state name mismatches, e.g.
     "Nassarawa" -> "Nasarawa"; a handful of LGA-level rows recoded to
     their parent state), study-period correction to 2006-2025 (2026 is
     a partial year), and validation checks.
3. **QGIS-ready dataset**: `data/processed/QGIS_state_dataset.csv`
   - One row per state, with outbreak totals per disease, a `*_status`
     column distinguishing real zeros from no-data, and both a
     nullable and a zero-filled version of each outbreak column.
4. **Boundaries**: `data/boundaries/nga_admin_boundaries_shp.zip`
   - Nigeria admin boundaries (COD-AB), Office for the Surveyor General
     of the Federation of Nigeria (OSGOF) / OCHA HDX. Admin 1 (37
     states) layer used for these maps.
5. **Mapping**: shapefile joined to `QGIS_state_dataset.csv` on
   state name (`adm1_name` <-> `State`) in QGIS, symbolized as a
   graduated choropleth (Natural Breaks / Jenks, 5 classes) with a
   separate manually-defined class for "no data" states.

## Analysis

`analysis/spearman_correlations.py` tests whether states with a high
burden of one disease also tend to have a high burden of another,
using Spearman rank correlation on pairwise-complete state data.

| Pair | n | rho | p |
|---|---|---|---|
| Rabies vs HPAI | 34 | 0.149 | 0.402 |
| Rabies vs Trypanosomosis | 17 | -0.211 | 0.417 |
| HPAI vs Trypanosomosis | 16 | -0.125 | 0.644 |

None of the three pairs are statistically significant. Reported
outbreak counts for these three diseases do not track together across
states - each shows an independent geographic pattern. The
Trypanosomosis comparisons rest on only 16-17 states with data, so
those results are underpowered and best read as inconclusive rather
than as evidence of no relationship.

## Lessons learned building this in QGIS

A few non-obvious things worth noting for anyone repeating this:

- **NULL vs. zero in graduated symbology**: QGIS's graduated renderer
  doesn't have a built-in way to style NULL values separately. The
  workaround used here: classify on an expression
  (`CASE WHEN "field" IS NULL THEN -1 ELSE "field" END`) so missing
  states get a sentinel value, then give that sentinel its own manual
  class, styled grey. Watch for "Link class boundaries" — if it's
  checked, editing one class's boundary can silently pull an adjacent
  class's boundary along with it, causing the sentinel value to
  overlap with a real class.
- **Map item extent**: when placing a Map item in Print Layout, "Set
  to Map Canvas Extent" only works as expected if the main canvas is
  already tightly zoomed to the layer — otherwise it inherits whatever
  the canvas happened to be showing, which can leave the map tiny
  inside its own frame.
- **Distinguish "no data" from "confirmed zero"** at the data-cleaning
  stage, not just visually — this affects the correct classification
  logic as much as the map's legend text.

## Reproducing

1. Load `data/boundaries/nga_admin_boundaries_shp.zip` (Admin 1 layer)
   in QGIS.
2. Load `data/processed/QGIS_state_dataset.csv`.
3. Join on `adm1_name` (shapefile) <-> `State` (CSV).
4. Symbolize as Graduated, using the CASE expression above on each
   disease's `*_outbreaks` column, 5 classes, Natural Breaks (Jenks),
   plus a manual grey class for the no-data sentinel.

## Source

WAHIS (World Animal Health Information System), World Organisation for
Animal Health (WOAH). Nigeria admin boundaries: OCHA HDX (COD-AB),
Office for the Surveyor General of the Federation of Nigeria (OSGOF).
