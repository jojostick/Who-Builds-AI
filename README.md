# Who Builds AI? — Assignment 3 Part 2 Portfolio

## One-sentence research question
**Is notable AI model development becoming more concentrated in a few countries?**

The question is arguable: the 2024–2025 top-three share rises, but the full 2010–2025 trend fluctuates, and country counts alone cannot measure overall AI capability. A different timeframe or indicator can lead to a different defensible answer.

**Target persona:** a technology policy analyst who needs to assess which countries are associated with notable model development and whether the distribution changes over time, to decide which regions and collaborations deserve closer investigation.

**Answer shown on the app's opening screen:** in this fixed Epoch AI snapshot, model development is highly concentrated among three country labels in 2025 (96.9%), but the series is not a steady upward trend. This is not a claim about every AI model globally.

## Three user stories and walkthroughs

1. **As a technology policy analyst, I want to compare attributed model counts across countries, so that I can identify leading model-development locations.** Walkthrough: open **01 · Country distribution**, change **Number of countries to display**, read the ranked bars and the labelled top-five treemap and table.
2. **As a research analyst, I want to compare annual model counts for selected countries, so that I can understand the direction and timing of changes.** Walkthrough: open **02 · Change over time**, change **Compare countries** and the sidebar **Publication years**, inspect the chart and exact-values table.
3. **As a technology policy analyst, I want to track the top-three share and verify its calculation, so that I can assess evidence of concentration before communicating conclusions.** Walkthrough: open **03 · Concentration**, review the concentration and annual volume charts, toggle **Sensitivity: single-country models only**, and go to **Verify a number** to trace 2025 to country weights and original CSV rows.

## Data and methods

- Source: Epoch AI, [Data on AI models](https://epoch.ai/data/ai-models). Supplied file: `data/notable_ai_models.csv`; a **fixed snapshot received 26 October 2026**, not a live or constantly updated feed.
- Reported source licence: **Creative Commons Attribution** (see Epoch AI's data page; preserve this attribution when redistributing).
- Original CSV: **1,082 records**. Eligible 2010–2025 after excluding missing country fields: **867 records**. 2026 is incomplete and excluded. Multi-country records: **160**.
- Every model contributes **one** model unit in total: its weight is divided equally across its distinct country labels. Country/territory labels are kept exactly as listed; this is not a statement about researcher nationality or relative work contribution.
- **Top-three share (%) = (sum of three largest country weights in that year / eligible model count in that year) × 100.** In 2025: (311/3) / 107 × 100 = **96.884735…%**, displayed as **96.9%**.
- The 2025 top-three labels are **United States of America, China, and South Korea**. The 2024 share was **88.8%**; this is not evidence of a monotonic trend since 2010.

See [`docs/METHODOLOGY.md`](docs/METHODOLOGY.md), [`docs/DATA_DICTIONARY.md`](docs/DATA_DICTIONARY.md), and the **Methods & AI use** tab for source, transformations, assumptions, and limitations.

## Visual vocabulary and labels

| Figure | Visual form / purpose | Location |
| --- | --- | --- |
| 1 | Ranked bar chart — **comparison** of fractional model counts | Country distribution |
| 2 | Treemap — **part-to-whole** contribution of top-five vs remaining labels | Country distribution |
| 3 | Multi-series line — **change over time** in model counts | Change over time |
| 4 | Line — **change over time** in top-three share | Concentration |
| 5 | Annual bar — **comparison** of yearly eligible sample sizes | Concentration |
| Optional | HHI line — concentration sensitivity by a different metric | Concentration |

Important values are visible in bar labels, key on-graph annotations, and tables under the charts, without requiring hover. Country names, years, percentage units, and model-count units are written explicitly. Colors are not the only way to distinguish series, but a manual colour-vision check remains necessary.

## Run locally (macOS)

From the project folder in Terminal:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
python analysis.py
python -m unittest -v test_analysis
python test_app.py
python -m streamlit run app.py
```

Visit the local address Streamlit prints (usually `http://localhost:8501`). Files are located relative to `app.py`, not your current shell working directory.

If using Python 3.13, try Python 3.12 if you encounter a package compatibility problem. Never upload `.venv/` or private credentials.

## Reproduce the processed data

`python analysis.py` regenerates **all** files in `data/processed/` from `data/notable_ai_models.csv`:

- `model_country_weights.csv`: source-record ID, year, model, country and fractional allocation; the app loads this processed file to build charts.
- `country_year.csv`: sum of country weights by year.
- `annual_concentration.csv`: yearly eligible count, top-three share and HHI.
- `data_audit.json`: filter counts and source SHA-256.

Use `python scripts/check_reproducibility.py` to regenerate the outputs and verify that the committed processed files have not changed. The app always verifies its number against row-level source allocations in the **Verify a number** tab.

## How to test the application

1. The first screen states the research question, target persona, a fact about the full 2010–2025 dataset, the fixed-snapshot date and limitations.
2. Move the **Publication years** slider; toggle **Sensitivity: single-country models only**. The displayed data should change.
3. In the second tab, clear all countries: a friendly info message appears instead of an exception or blank display.
4. Check all charts at **1366 × 768** and test readability without hover. Confirm only vertical page scrolling is necessary.
5. In **Verify a number**, keep default year range and sensitivity off, select 2025: the calculation must show **96.884735%** (approximately 96.9%). Check the weights and source IDs.
6. On the deployed URL, measure cold-load time (target <5 seconds) and interaction response (target about 1 second). **These browser performance checks have not yet been verified.**

## Publish and submit

1. Create a GitHub repository; upload the contents of **this folder** with `app.py` at the repository root. Commit the snapshot and processed files. Do not fabricate collaborators or checks.
2. Open [Streamlit Community Cloud](https://share.streamlit.io/) → Create app → choose your repository, branch and `app.py` entrypoint. Confirm the public URL from a signed-out browser.
3. Record the exact **Git commit hash or release tag** tested on the deployed site, so assessors can run the same version.
4. Submit **one PDF** containing the **deployed app URL**, **repository URL**, and **commit hash/release tag**. All other evidence lives in the repository at that commit.
5. Complete `docs/AI_PROVENANCE_MATRIX.csv` and `docs/DATA_AI_DISCLOSURE.md` honestly after you perform additional personal checks. No unperformed human review or additional team member is represented.

The supplied brief specifies a **4–5 member group project**, **one PDF per group**, due **20 November 2026, 23:59**. **Individual submission is not automatically authorised**. If you will submit alone, obtain approval from the teaching team; keep an evidence trail of your actual work. See `docs/PART2_CHECKLIST.md` for the 30 marking items and open checks.

## Repository contents

```
app.py                         # interactive Streamlit app
analysis.py                    # reproducible data transforms
requirements.txt               # Python dependencies
data/notable_ai_models.csv     # original Epoch AI sample
data/processed/                # regenerated, versioned files used by the app
scripts/check_reproducibility.py
docs/DATA_DICTIONARY.md
docs/AI_PROVENANCE_MATRIX.csv
docs/DATA_AI_DISCLOSURE.md
docs/PART2_CHECKLIST.md
test_analysis.py               # arithmetic and parsing unit tests
test_app.py                    # headless Streamlit widget checks
```

Earlier Part 1 recording aids remain in `docs/` for reference; they are not Part 2 submission deliverables.
