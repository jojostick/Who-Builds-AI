# Assignment 3 Part 2 — 30-point rubric audit

**Status key:** `Implemented in files` means there is related code or documentation, not that a teaching-team check has passed. `Needs manual check` requires browser/testing evidence. `Missing for submission` cannot be done without the student's accounts or decisions.

## Question, persona and stories (6)
1. README states one-sentence arguable research question — **Implemented in files** (`README.md`).
2. Question appears on app opening screen — **Implemented in files** (`app.py`).
3. The question allows alternative answers from the same data — **Implemented in files** (trend and alternative HHI).
4. README specifies target persona and supported decision — **Implemented in files** (`README.md`).
5. Three as-a/I-want/so-that user stories — **Implemented in files** (`README.md`).
6. Stories can be walked through in app — **User-reported pass** (README walkthroughs and live-app check, 7 Nov 2026).

## Analytical quality (6)
7. Every number from data package — **Implemented in files**, verify via `test_analysis.py`, `analysis.py` and the app trace.
8. App states an answer to the question — **Implemented in files** (app opening screen).
9. App explains what data cannot show — **Implemented in files** (`Methods & AI use`).
10. Units, baselines and time coverage stated — **Implemented in files** (labels/captions; inspect browser).
11. Claims stay within what data shows — **Needs manual review**, particularly geographic interpretation.
12. Every chart has title or caption — **Implemented in files** (five captioned figures).

## Visual form (6)
13. At least four charts — **Implemented in files** (five charts, optional sixth).
14. At least three Visual Vocabulary families — **Implemented in files** (comparison, part-to-whole, change over time), **requires course taxonomy confirmation**.
15. Each visual form matches its task — **Needs manual review**.
16. Axes/legends labelled with units — **Implemented in files**, browser check required.
17. Values readable without hover — **Implemented in files** (chart labels plus data tables), browser check required.
18. Colours survive colour-vision-deficiency test — **User-reported pass** (Chrome colour-vision simulation, 7 Nov 2026; screenshots not retained).

## App works (6)
19. Deployed URL loads under 5 seconds — **Deployed; user-reported pass** (warm-page load under five seconds, 7 Nov 2026; no logged cold-start measurement).
20. App opens on whole-dataset fact — **Implemented in files** (867 models, 2025 result).
21. At least two interactions respond in about 1 second — **User-reported pass** (about one second or faster for filters, 7 Nov 2026; no exact log).
22. Empty filter state gives message — **Implemented in files** (empty country multiselect; no-data guard).
23. Layout at 1366×768 uses vertical scroll only — **User-reported pass** (1366 x 768 browser review, 7 Nov 2026).
24. Sources and last data refresh visible on screen — **Implemented in files** (fixed snapshot date), browser check required.

## Data package and process (6)
25. Source and processed files in `data/` — **Implemented in files**.
26. Dictionary source/URL/licence/columns/units/key/time/latest/transform — **Implemented in files**, accuracy check required.
27. Commit hash/tag resolves; app runs from it — **Implemented; user-reported pass** (public app and a resolving GitHub commit, 7 Nov 2026).
28. Matrix: one row per substantial AI use, every group member and falsifiable verification — **Documented for sole contributor**; **group rule unresolved**, no fabricated team members.
29. Data and AI disclosure present — **Implemented in files**.
30. Processed files regenerate using documented transforms — **Implemented in files** (`python analysis.py`; `scripts/check_reproducibility.py`).

## Submission blockers
- Teacher approval if submitting alone despite the 4–5 member group rule.
- Public URL and GitHub repository exist. The single submission PDF must be regenerated using the final commit SHA *after* any final documentation push.
- Browser, timing, visual and manual trace checks were reported by student on 7 Nov 2026; results documented in `docs/FINAL_VALIDATION_LOG.md` without independently instrumented screenshots or exact timing logs.
