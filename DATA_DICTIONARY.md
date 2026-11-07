# Data dictionary — Who Builds AI?

## Provenance, licences and time coverage
- **Primary source and URL:** Epoch AI, *Data on AI models*, https://epoch.ai/data/ai-models . The source CSV was supplied with the project; its current online version may differ.
- **Licence:** Epoch AI publishes data under Creative Commons Attribution, requiring source attribution (https://epoch.ai/data).
- **Snapshot:** user-provided fixed CSV received **26 October 2026**. This is the snapshot date, **not** a claim that each model record was last updated that day.
- **Source SHA-256:** `dcd97028735d9d985b3ffab6bb19e0e711b400c5c513a4c8dc4acf7fe6a728f5`.
- **Original data:** 1,082 records, 47 original columns. Original publication dates cover **1950–2026**; latest source publication date **2026-10-12**.
- **Analysis data:** 867 eligible records from **2010–2025**; latest included publication date **2025-12-31**. Partial 2026 omitted.
- **Primary key:** the original CSV does **not** supply a verified unique ID. The ingestion script creates `source_record` (1-based CSV record ordinal) before filtering. This is a reproducible **file-local surrogate key**, not a global model ID.
- **Interpretation:** an individual original `Model` value is not assumed unique. Model variants may be separate rows. No independent source audit is claimed.

## 1. `data/notable_ai_models.csv` — original source sample

| Original column | Unit / interpretation |
| --- | --- |
| `Model` | text / category / URL (as recorded) |
| `Organization` | text / category / URL (as recorded) |
| `Publication date` | ISO calendar date (YYYY-MM-DD) |
| `Domain` | text / category / URL (as recorded) |
| `Task` | text / category / URL (as recorded) |
| `Parameters` | count (as recorded; original field semantics apply) |
| `Parameters notes` | text / category / URL (as recorded) |
| `Training compute (FLOP)` | FLOP |
| `Training compute notes` | text / category / URL (as recorded) |
| `Training dataset` | text / category / URL (as recorded) |
| `Training dataset size (total)` | source-reported dataset size (unit may vary) |
| `Dataset size notes` | text / category / URL (as recorded) |
| `Confidence` | text / category / URL (as recorded) |
| `Link` | text / category / URL (as recorded) |
| `Reference` | text / category / URL (as recorded) |
| `Citations` | text / category / URL (as recorded) |
| `Authors` | text / category / URL (as recorded) |
| `Abstract` | text / category / URL (as recorded) |
| `Organization categorization` | text / category / URL (as recorded) |
| `Country (of organization)` | category labels |
| `Notability criteria` | text / category / URL (as recorded) |
| `Notability criteria notes` | text / category / URL (as recorded) |
| `Epochs` | count (as recorded; original field semantics apply) |
| `Training time (hours)` | hours |
| `Training time notes` | text / category / URL (as recorded) |
| `Training hardware` | text / category / URL (as recorded) |
| `Hardware quantity` | count (as recorded; original field semantics apply) |
| `Hardware utilization (MFU)` | source-reported utilisation metric (check original scale) |
| `Training compute cost (2023 USD)` | 2023 US dollars |
| `Compute cost notes` | text / category / URL (as recorded) |
| `Training power draw (W)` | watts (W) |
| `Base model` | text / category / URL (as recorded) |
| `Finetune compute (FLOP)` | FLOP |
| `Finetune compute notes` | text / category / URL (as recorded) |
| `Batch size` | count (as recorded; original field semantics apply) |
| `Batch size notes` | text / category / URL (as recorded) |
| `Model accessibility` | text / category / URL (as recorded) |
| `Training code accessibility` | text / category / URL (as recorded) |
| `Inference code accessibility` | text / category / URL (as recorded) |
| `Accessibility notes` | text / category / URL (as recorded) |
| `Numerical format` | text / category / URL (as recorded) |
| `Frontier model` | text / category / URL (as recorded) |
| `Hardware acquisition cost` | source-reported cost (currency not explicit in column name) |
| `Hardware utilization (HFU)` | source-reported utilisation metric (check original scale) |
| `Training compute cost (cloud)` | source-reported cost (currency not explicit in column name) |
| `Training compute cost (upfront)` | source-reported cost (currency not explicit in column name) |
| `Open model weights?` | text / category / URL (as recorded) |

**Transforms:** `analysis.load_data()` adds `source_record`, drops exact full-row duplicates (0 here), parses `Publication date` into `year`, and splits the `Country (of organization)` string into unique, trimmed labels. The original file is not overwritten.

## 2. `data/processed/model_country_weights.csv` — the app’s row-level input
- **Source / URL:** derived from the original Epoch AI file above; same attribution/licence applies.
- **Key:** composite (`source_record`, `country`) within this fixed snapshot.
- **Coverage:** 2010–2025, latest 2025-12-31; one row per model × unique country label.

| Column | Unit / meaning |
| --- | --- |
| `source_record` | 1-based source CSV data-record ordinal |
| `Model` | original model name; text |
| `Organization` | original developer field; text |
| `Publication date` | source date (YYYY-MM-DD) |
| `year` | integer publication year |
| `Country (of organization)` | unchanged raw country labels; text |
| `country` | one unique parsed label |
| `country_count` | number of distinct labels for the model |
| `weight` | fractional model units allocated to this label, 1 / country_count |
| `Reference` | original reference description; text |

**Transform:** filter 2010–2025, exclude missing country labels, deduplicate labels per model, explode labels into rows, and allocate weight 1/k. The app reads this file and applies year/sensitivity filters directly.

## 3. `data/processed/country_year.csv` — derived annual-country totals
- **Source / URL:** same Epoch AI source; derived by `analysis.py`.
- **Key:** (`year`, `country`). **Coverage:** 2010–2025; latest 2025.
- **Columns:** `year` (calendar year), `country` (country/territory label), `weight` (sum of fractional model units).
- **Transform:** group row-level allocations by year and country and sum weights.

## 4. `data/processed/annual_concentration.csv` — yearly concentration
- **Source / URL:** same Epoch AI source; derived by `analysis.py`.
- **Key:** `year`. **Coverage:** 2010–2025; latest 2025.

| Column | Unit / meaning |
| --- | --- |
| `year` | publication calendar year |
| `eligible_models` | distinct eligible source record count (models) |
| `represented_countries` | distinct non-empty country labels (count) |
| `top3_countries` | three largest-weight country labels in that year; semicolon-delimited text |
| `top3_weight` | combined fractional model units for the three labels |
| `top3_share_pct` | percent of eligible models (0–100%) |
| `hhi` | unitless concentration index (sum of squared fractional country shares, 0–1) |

**Transform:** group weighted rows by year, rank countries by total model weight, sum top three, divide by eligible distinct model records, compute HHI.

## 5. `data/processed/data_audit.json` — processing audit
- **Source / URL:** same original Epoch AI data; derived by `analysis.py`.
- **Key:** one snapshot object (identified by `sha256`). **Time coverage:** input 1950–2026, analytical window 2010–2025.
- **Fields:** `raw_rows` (records); `exact_duplicates_removed` (records); `invalid_dates` (records); `missing_country_all_years` (records); `window_rows` (records); `window_missing_country` (records); `eligible_models_2010_2025` (records); `multi_country_models_2010_2025` (records); `rows_2026_excluded` (records); `sha256` (hex digest).
- **Transform:** inspection and counts during reproducible data export; no hidden transformation or external data is used.

## Reproducibility and known limits
Run `python analysis.py` to regenerate all four processed files from the preserved raw CSV. Run `python scripts/check_reproducibility.py` to check byte-level reproduction against existing packaged outputs. Empty and malformed inputs are not a supported input contract for this fixed-snapshot project.
Country names are deliberately not geopolitically standardised. Splitting comma-separated labels is an assumption of this source snapshot. Fractional weights are a counting convention, not a measured share of actual engineering labour or investment.
