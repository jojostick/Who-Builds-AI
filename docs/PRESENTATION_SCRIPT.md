# Individual recording script

Draft for rehearsal, approximately four minutes depending on pace and screen actions. Target a final duration below 4:50. Dashboard 3 is a proposed contribution, not a confirmed group allocation. Confirm it with the group before recording. Only describe personal review actions after you have actually completed them.

## 0:00–0:35 | Question and audience

Hello. My proposed contribution asks: is notable AI model development becoming more concentrated in a few countries?

Our target user is a technology policy analyst. This person wants to understand where model development is taking place and whether participation is becoming broader. The evidence comes from the supplied Epoch AI notable models dataset. This measures a selected set of important models, rather than all AI activity.

## 0:35–1:10 | Dashboard contribution

This app has three dashboards. The first compares country totals. The second shows changes in model counts. My proposed focus is the third dashboard, which measures concentration using the share attributed to the top three countries each year.

I use 2010 to 2025. I exclude 2026 because the calendar year is incomplete. The default analysis includes 867 model records with country information.

## 1:10–1:50 | Result and design choice

In 2025, the top-three share is about 96.9 percent. In 2024, it is about 88.8 percent. This suggests a recent increase. However, the whole series fluctuates. The 2010 share is also 100 percent, based on only ten models. Therefore, I would not claim that concentration rises continuously.

The visual task is comparing changes over time. The design uses a line chart on a common percentage scale. Multiple pie charts were rejected because small changes in slice angles are difficult to compare. The model-count chart below gives context about annual sample sizes.

## 1:50–3:15 | Live verification

I will now trace the 2025 value back to the source.

On the verification tab, I select 2025. The denominator is 107 eligible model records. The first three country totals sum to about 103.67. Dividing this by 107 and multiplying by 100 gives 96.8847 percent, rounded to 96.9 on the dashboard.

The totals can be fractional because a model can be associated with more than one country. For a model with two unique countries, each receives half a unit. Repeated labels within the same model are removed before this calculation. Each model still contributes exactly one unit overall.

Here are the row-level weights, and here are the corresponding original model names, dates and country fields. The source record identifier connects the calculation to the original CSV. The download button provides that unchanged CSV for checking.

## 3:15–3:50 | Limitations and sensitivity

There are important limits. This is a curated dataset, not a complete census. Country information describes the developing organisations, not every researcher's nationality. Model counts also do not measure model quality or productivity.

The single-country option lets the audience test a narrower sample by excluding internationally associated models. That changes the population being measured, so it should be interpreted as a sensitivity check.

## 3:50–4:30 | AI disclosure and conclusion

ChatGPT assisted with topic selection, Python code, data analysis, documentation and this script. The package includes automated checks for total model weights and an independent recalculation of the 2025 value. These checks support arithmetic consistency, but they do not prove that every source record is correct.

My conclusion is that this snapshot shows high concentration and a recent increase, but not a steady increase throughout the full period. The dashboard makes that claim inspectable by connecting the chart to the source records.

## Optional personal-check sentence

Add only after completing it: "I also manually checked a source record and its country weights, and reproduced the 2025 calculation." Do not claim to have written the app independently or to have completed checks you have not performed.
