# Final validation log — Who Builds AI?

**Date:** 7 November 2026 (Australia/Sydney)  
**Contributor:** Junjie Chen  
**Context:** Assignment 3 Part 2, individual work on a nominally 4–5 person group assignment.

## Evidence categories

`Assistant-run check` = executed or prepared in the assistant's container; not represented as student's own execution.  
`Student-reported check` = student reported the result in this conversation after performing a local/browser test; not a third-party benchmark.

| Rubric area | Check and falsifiable outcome | Reported result | Evidence type and limit |
|---|---|---|---|
| Source trace | Open **Verify a number** for 2025; locate Eagle 2, source record 191; deduplicate country labels and require each of the three unique labels to have weight `1/3` and total `1` | Pass reported; USA, China, Hong Kong each 1/3 | Student-reported manual trace; not an audit of all rows |
| Numerator / denominator | 2025 top-three weighted sum `103.6667`, eligible rows `107`; `(103.6667/107)*100` must round to `96.9%` | 96.8847%, displays 96.9% | Student-reported explanation; separate assistant-run computational calculation independently matched 96.884735% |
| Local and deployed app | Three dashboard tabs and Verify a number display without exceptions; interactions change data | Pass reported | Student-reported browser checks |
| Browser layout | 1366 x 768 viewport; readable figures and only vertical page scrolling | Pass reported | Student-reported; no retained screenshot at that precise viewport |
| Public site load | Warm-page load under five seconds (rubric target) | Under five seconds | Student-reported category, no numeric stopwatch log, cold-start not checked |
| Interaction response | Year and country/sensitivity filters update output in about one second (rubric target) | About one second or faster | Student-reported category, no exact latency samples |
| Colour vision | Use Chrome colour-vision simulation and verify charts remain understandable | Pass reported | Student-reported Chrome simulation, no saved screenshots or certified accessibility audit |
| Arithmetic tests | Five analysis unit tests and four reproducibility comparisons must pass | Five tests and four outputs passed | Assistant-run local checks in preparation environment |

## Artifacts and method

- Public app: https://who-builds-ai-jojostick.streamlit.app/
- Repository: https://github.com/jojostick/Who-Builds-AI
- Derived files: `data/processed/`
- Reproduce: `python -m unittest -v test_analysis` and `python scripts/check_reproducibility.py`
- AI use matrix: `docs/AI_PROVENANCE_MATRIX.csv`

## Outstanding issues (do not mark as passed without evidence)

1. Obtain written teaching-team permission for individual submission of a group assignment.
2. Confirm that disclosed AI assistance complies with the course's academic-integrity policy.
3. Perform an independent editorial pass over chart labels, claims, data dictionary, and the full AI matrix.
4. A warm-page pass does **not** establish that every initial visit after cloud hibernation will load under five seconds; no saved timing trace is included.
5. This record is a truthful self-reported validation log, not proof that a teaching team will award all 30 marks.

**Version control:** Once the final documentation is pushed, capture the new `git rev-parse HEAD` value. The submission PDF must match that exact commit.
