# Data and AI disclosure statement — Who Builds AI?

## Data and scope
- Source: Epoch AI, *Data on AI models*, https://epoch.ai/data/ai-models.
- Data file: `data/notable_ai_models.csv`, a fixed snapshot supplied for this project on 26 October 2026. It is not a live feed.
- The raw source file is retained; `analysis.py` generates the processed files in `data/processed/`.
- Analysis uses 2010–2025, excluding 2026 as incomplete and excluding records without a usable country label from the relevant denominator.
- Model weights are split equally across unique attributed country/territory labels. These labels do not establish researcher nationality, individual contribution, capability or productivity.
- Attribution and source licence information should be checked against Epoch AI's current data page before submission.

## AI use and authorship
ChatGPT substantially assisted with research framing, code and Streamlit visualisations, data-processing logic, numerical verification, automated checks, documentation, GitHub/deployment guidance, and presentation drafting. The project should **not** be described as entirely independent human-written code or documentation.

The individual project contributor, Junjie Chen, performed the GitHub upload, folder-path correction, commit/push process, and Streamlit deployment using AI-guided instructions. The contributor also reported checking the local dashboards and the deployed app's main interactions and 2025 verification display. These are distinct from AI-generated or assistant-executed tests.

Details of substantive AI uses, tests that could fail, observed outcomes, and follow-up actions appear in `docs/AI_PROVENANCE_MATRIX.csv`. There are no fabricated group-member contributions.

## Verification status as of 7 November 2026
- **Computational tests:** Five data-analysis unit tests passed in the assistant's environment. Four processed output files regenerated exactly from the supplied CSV. An independent Python method recalculated 2025's top-three share as approximately 96.884735%, displayed as 96.9%.
- **Student-performed actions:** Local Streamlit app opened; the student reported that the dashboard pages and verification function were working. The GitHub push and public deployment were evidenced by student screenshots. The student reported the five deployed-app checks were normal.
- **Not yet established:** Independent student audit of selected raw source rows, formally measured cold-load time and interaction latency, formal colour-vision-deficiency check, a complete line-by-line student document audit, and instructor permission to submit a nominally group-based assignment individually.

Automated numerical tests support calculations but do **not** prove that the original source data is fully correct or that every chart meets visual accessibility requirements. Do not change an outstanding item to “passed” without performing and recording the test.

## Personal checklist before final submission
- [ ] Manually trace at least one raw record's source fields to its country allocations and note the record ID.
- [ ] Explain 2025's `103.6667 / 107 × 100 ≈ 96.9%` calculation in your own words.
- [ ] Run and retain local output from `python -m unittest -v test_analysis` and `python scripts/check_reproducibility.py` if not already done.
- [x] Inspect the local and public app views and controls (student-reported 7 November 2026).
- [ ] Measure cold-load and interaction speed; document date and browser conditions.
- [ ] Perform and record a colour-vision/readability check.
- [ ] Confirm the course's AI use policy and obtain teaching-team approval for individual submission.
- [ ] Review and correct every AI-use row and disclosure statement to match your actual work.

**Version control:** The final submission PDF must identify the commit hash corresponding to the deployed, assessed files. Updating these disclosure files changes the commit hash.
