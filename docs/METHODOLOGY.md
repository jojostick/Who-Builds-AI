# Methodology and findings

## Source and provenance

Epoch AI, Data on AI models, https://epoch.ai/data/ai-models. Source CSV: https://epoch.ai/data/notable_ai_models.csv. Official documentation: https://epoch.ai/data/ai-models (Documentation section). Accessed 26 October 2026.

The analysis uses the user-supplied CSV, not a freshly downloaded version. It contains 1,082 records and 47 original columns. Its SHA-256 is `dcd97028735d9d985b3ffab6bb19e0e711b400c5c513a4c8dc4acf7fe6a728f5`. This hash identifies the file; it does not establish the accuracy of its contents.

## Operational definition

We study the distribution of country labels associated with developing organisations for notable model records. We do not measure researcher nationality or the physical location of model training. Labels are preserved as provided, including territory labels; no geopolitical recoding is applied.

1. Preserve the original CSV and assign a one-based source record ordinal before any filtering.
2. Remove exact duplicates across all original columns. None were found in this snapshot. Different variants of a named model remain separate source records.
3. Parse publication dates. No invalid dates were found.
4. Select 2010–2025 inclusive. This declared window focuses on recent AI development and avoids the incomplete 2026 calendar year. Complete calendar years do not guarantee complete source coverage.
5. Exclude records with missing country information: one in the selected window, 19 across all years.
6. Split country values on commas, trim spaces and deduplicate repeated country labels within each model.
7. Give each model a total weight of one. With k unique countries, assign 1/k to each country. This avoids giving internationally associated models extra total weight. It does not claim equal actual effort.
8. Sum weights by country and year. Rank countries anew each year. Top-three share = sum of the three largest country weights / eligible model records * 100.
9. HHI = sum of squared country shares on a 0–1 scale. It captures the full distribution and may behave differently from top-three share.
10. The optional single-country sensitivity mode removes multi-country records entirely and recalculates both numerator and denominator.

## Verified 2025 example

The default 2025 denominator is 107 eligible model records. The top-three country weights total 311/3 = 103.6666667. Therefore 100 * (311/3) / 107 = 96.8847352%, displayed as 96.9%. Use the verification tab to see country totals, per-model allocations and original source fields. The calculation was independently checked using Python's csv module and exact Fraction arithmetic.

## Interpretation

The top-three share falls from 100% in 2010 to 73.94% in 2017, then fluctuates and reaches 96.88% in 2025. The 2010 value has a denominator of only ten models and three countries. In 2024 the share is 88.78%, so the 2024–2025 increase is about 8.1 percentage points. These facts do not support an uninterrupted long-term rise.

High top-three share and changing dominance among those countries are different questions. The HHI provides complementary evidence rather than a redundant version of the same measure. Neither indicator proves why concentration changes or that concentration is good or bad.

## Limits

- Epoch AI describes the dataset as curated and non-exhaustive. Inclusion, public visibility and recognition delays can affect year comparisons.
- Fractional allocation is a transparent convention. It does not quantify each organisation's effort.
- Small early-year samples make endpoint comparisons unstable.
- A model count gives every record equal importance, regardless of quality, training compute, users or economic effect.
- Country labels cannot reveal all international labour, supply chains or deployment locations.
- Results describe this uploaded snapshot. A later release may change historical totals.

## Design

Dashboard 1 uses sorted horizontal bars for country ranking and readable long names; a geographic map was rejected because land area is unrelated to model counts and small countries can be hard to inspect. Dashboard 2 uses lines to compare yearly counts. Dashboard 3 uses a common-scale line chart for concentration, with annual sample volumes underneath. Repeated pie charts were rejected because slice angles make precise changes harder to compare. All concentration calculations retain the full eligible denominator; selecting comparison countries in Dashboard 2 cannot alter it.
