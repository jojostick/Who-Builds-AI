# Validation record

Prepared 26 October 2026.

## Passed

- Five unittest checks: country parsing, per-model weight conservation and year bounds, independent 2025 recalculation, single-country sensitivity, and a synthetic allocation case with a known HHI.
- Independent verification used Python csv and exact Fraction arithmetic, separate from the pandas aggregation used by the app. Result: top-three weight 311/3; denominator 107; share 96.88473520249221%.
- Streamlit AppTest: default app execution, expected 867 model records and 96.9% headline, sensitivity toggle, 2024-2025 year range, 2024 verification selection, empty country selection and a single-year range. No application exceptions occurred.
- The source snapshot contains 1,082 rows and 47 original columns. No exact duplicate records or invalid dates were found. The 2010-2025 sample has one missing-country record, which is excluded.
- The four-page Recording_Pack.pdf was rendered for a visual layout check.

## Verification limits

Streamlit AppTest is a headless execution and widget test; no live browser layout inspection was completed. No public deployment, user-machine installation, student review, group approval or actual recording has been completed. Test timing does not establish the length of a spoken recording. The supplied data has not been independently audited against each model's original publication.

## Re-run

From the project directory, with requirements installed:

```bash
python -m unittest -v test_analysis
python test_app.py
python analysis.py
```

Dependency versions are recorded in requirements.txt. The preparation environment used Python 3.12.14. The user's local Mac environment has not been tested.

## Part 2 revision — 7 November 2026

- Existing five `test_analysis.py` unit tests passed again in the preparation environment.
- `python scripts/check_reproducibility.py` passed for **all four processed outputs**. The app has been updated to read `data/processed/model_country_weights.csv`.
- Added labelled comparison bars, a top-five/remainder treemap (part-to-whole), exact-value tables, and an explicit snapshot date.
- Syntax compilation and standalone Plotly chart-construction checks can be performed without Streamlit.
- **Limitation:** Streamlit was not installed in the available offline test runtime and package installation was blocked by network DNS. The updated Part 2 app therefore **has not yet passed a fresh Streamlit AppTest or browser check**. Do not cite the earlier Part 1 AppTest as validation of this revised app. Run `python test_app.py` and perform a browser check after installation on the student's Mac.
