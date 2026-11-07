"""Who Builds AI? Interactive country concentration narrative for a fixed Epoch AI snapshot.

All chart data is derived from the source CSV by running ``python analysis.py``.
Processed row-level weights are read directly from data/processed at runtime.
"""
from pathlib import Path
import hashlib
import pandas as pd
import plotly.express as px
import streamlit as st
from analysis import SOURCE, COUNTRY, load_data, annual_summary

ROOT = Path(__file__).resolve().parent
PROCESSED = ROOT / "data" / "processed"
SNAPSHOT_DATE = "26 October 2026"

st.set_page_config(page_title="Who Builds AI?", page_icon="◈", layout="wide")
st.markdown('''<style>
.stApp {background-color:#f5f7fb;} h1,h2,h3 {color:#102c48;}
[data-testid="stMetric"] {background:white;border:1px solid #dde5ef;border-radius:12px;padding:18px;}
.block-container {padding-top:1.5rem; max-width:1250px;}
</style>''', unsafe_allow_html=True)

@st.cache_data(show_spinner=False)
def load_package():
    """Read the unchanged source data and the versioned processed weights."""
    raw, clean = load_data()
    weights_path = PROCESSED / "model_country_weights.csv"
    if not weights_path.exists():
        st.error("Processed data is missing. Run `python analysis.py` and reload.")
        st.stop()
    weights = pd.read_csv(weights_path)
    return raw, clean, weights


def plot(fig):
    """Apply readable visual settings consistently across the charts."""
    fig.update_layout(template="plotly_white", paper_bgcolor="rgba(0,0,0,0)",
                      font=dict(size=13, color="#102c48"),
                      margin=dict(l=10, r=15, t=28, b=12))
    st.plotly_chart(fig, width="stretch", config={"displaylogo": False})


def download(frame, filename, label):
    st.download_button(label, frame.to_csv(index=False).encode(), filename, "text/csv")


raw, clean, weights = load_package()
fixed_all = weights[weights.year.between(2010, 2025)]
fixed_annual = annual_summary(fixed_all)
fixed_last = fixed_annual[fixed_annual.year == 2025].iloc[0]

st.caption("DATA NARRATIVE STUDIO  /  EPOCH AI SNAPSHOT  /  2010–2025")
st.title("Who Builds AI?")
st.markdown("### Is notable AI model development becoming more concentrated in a few countries?")
st.write("**Audience:** A technology policy analyst examining research capacity and international collaboration.")
st.info(
    f"**Answer for the fixed 2010–2025 dataset:** recent notable-model activity is highly concentrated "
    f"among three country labels. The 2025 share is {fixed_last.top3_share_pct:.1f}% "
    "but concentration did not increase steadily over the full period. "
    "This is a curated sample, not all models worldwide."
)
st.caption(
    f"**Source:** Epoch AI, *Data on AI models* · "
    f"**Last data snapshot:** {SNAPSHOT_DATE} · **Latest included model date:** 31 December 2025 · "
    "Static data; no live refresh"
)

with st.sidebar:
    st.header("Explore the evidence")
    start, end = st.slider("Publication years", 2010, 2025, (2010, 2025))
    single = st.checkbox("Sensitivity: single-country models only", value=False)
    st.caption("Default: one model contributes a total weight of one, divided equally across unique country labels.")
    st.markdown("[Source and data citation: Epoch AI](https://epoch.ai/data/ai-models)")
    st.caption(f"Last snapshot: {SNAPSHOT_DATE}. The dataset does not update automatically.")

# Each processed row is a model/country allocation; filter without recomputing the source.
exp = weights.loc[weights.year.between(start, end)].copy()
if single:
    exp = exp.loc[exp.country_count == 1].copy()
if exp.empty:
    st.warning("No eligible records match this selection. Change the year range or sensitivity option.")
    st.stop()

annual = annual_summary(exp)
window = clean.loc[clean.year.between(start, end)]

a, b, c = st.columns(3)
a.metric("Eligible models · selected years", f"{exp.source_record.nunique():,}")
b.metric("Country labels · selected years", str(exp.country.nunique()))
c.metric(f"Top-three share · {int(annual.iloc[-1].year)}", f"{annual.iloc[-1].top3_share_pct:.1f}%")
st.caption(
    f"Full fixed dataset: {fixed_all.source_record.nunique():,} eligible models, 2010–2025. "
    f"In the selected years, {int((window.country_count == 0).sum())} records with missing country labels were excluded; "
    f"{int((window.country_count > 1).sum())} multi-country records exist before sensitivity filtering."
)
first, last = annual.iloc[0], annual.iloc[-1]
delta = last.top3_share_pct - first.top3_share_pct
st.write(
    f"**For the current filters:** top-three share changes from **{first.top3_share_pct:.1f}%** "
    f"in {int(first.year)} to **{last.top3_share_pct:.1f}%** in {int(last.year)} "
    f"({delta:+.1f} percentage points). This endpoint comparison is not a causal claim."
)

tabs = st.tabs(["01 · Country distribution", "02 · Change over time", "03 · Concentration",
                "Verify a number", "Methods & AI use"])
counts = exp.groupby("country", as_index=False).weight.sum().sort_values("weight", ascending=False)

with tabs[0]:
    st.subheader("Where are notable models attributed?")
    limit = min(20, len(counts))
    if limit == 1:
        topn = 1
        st.caption("Only one country label exists for this selection.")
    else:
        topn = st.slider("Number of countries to display", 1 if limit < 3 else 3,
                         limit, min(10, limit))
    shown = counts.head(topn).sort_values("weight")
    bar = px.bar(shown, x="weight", y="country", orientation="h", text="weight",
                 labels={"weight": "Fractional model count (models)", "country": "Country label"},
                 color_discrete_sequence=["#157f88"])
    bar.update_traces(texttemplate="%{x:.1f}", textposition="outside", cliponaxis=False)
    bar.update_layout(xaxis_range=[0, max(shown.weight) * 1.22])
    plot(bar)
    st.caption("Figure 1 · Comparison: fractional counts by attributed country, selected years. All countries remain in the denominator.")

    st.subheader("How is the country share divided?")
    top_five = counts.head(5).copy()
    remainder = max(0.0, float(counts.weight.sum() - top_five.weight.sum()))
    composition = top_five.rename(columns={"country": "group"}).copy()
    if remainder > 0.000001:
        composition = pd.concat([composition, pd.DataFrame([{"group": "All other country labels", "weight": remainder}])],
                                ignore_index=True)
    tree = px.treemap(composition, path=["group"], values="weight",
                      color="group", color_discrete_sequence=["#0d827b", "#53799d", "#a9bdcc", "#dc987b", "#9b8abb", "#c8c9bc"])
    tree.update_traces(texttemplate="%{label}<br>%{value:.1f} models", textfont_size=13)
    tree.update_layout(showlegend=False)
    plot(tree)
    st.caption("Figure 2 · Part-to-whole: top five country labels and the combined remainder. Areas represent fractional model counts, not geographic area. The totals use all eligible models in the selected period.")
    st.dataframe(counts.rename(columns={"country": "Country label", "weight": "Fractional models"}),
                 hide_index=True, width="stretch")
    download(counts, "country_ranking.csv", "Download country ranking")

with tabs[1]:
    st.subheader("How did attributed model counts change over time?")
    names = st.multiselect("Compare countries", counts.country.tolist(), default=counts.country.head(5).tolist())
    totals = (exp.groupby(["year", "country"]).weight.sum().unstack(fill_value=0)
              .reindex(range(start, end + 1), fill_value=0))
    if names:
        series = totals[names].reset_index().melt(id_vars="year", var_name="country", value_name="weight")
        trend = px.line(series, x="year", y="weight", color="country", markers=True,
                        labels={"year": "Publication year", "weight": "Fractional model count (models)", "country": "Country"})
        trend.update_layout(legend_title_text="Attributed country")
        plot(trend)
        st.caption("Figure 3 · Change over time: selected country labels, fractional model counts. A zero means no qualifying record in this sample, not zero AI research worldwide.")
        st.write("**All plotted values (readable without hovering):**")
        st.dataframe(totals[names].round(2).rename_axis("Publication year"), width="stretch")
    else:
        st.info("No country selected. Choose one or more countries to view a comparison.")

with tabs[2]:
    st.subheader("Does the top-three share rise consistently?")
    trend = px.line(annual, x="year", y="top3_share_pct", markers=True,
                    custom_data=["eligible_models", "top3_countries"],
                    labels={"year": "Publication year", "top3_share_pct": "Top-three share (%)"},
                    color_discrete_sequence=["#157f88"])
    trend.update_yaxes(range=[0, 105])
    # Label the key years directly. The full table below has all annual values.
    important = {int(annual.year.iloc[0]), 2017, 2024, int(annual.year.iloc[-1])}
    labels = [f"{v:.1f}%" if int(y) in important else "" for y, v in
              zip(annual.year, annual.top3_share_pct)]
    trend.update_traces(text=labels, textposition="top center", mode="lines+markers+text")
    plot(trend)
    st.caption("Figure 4 · Change over time: each year the three largest country weights are re-ranked and divided by all eligible records for that year. Percent (%) shown on the y-axis.")

    volume = px.bar(annual, x="year", y="eligible_models", text="eligible_models",
                    labels={"year": "Publication year", "eligible_models": "Eligible model records (models)"},
                    color_discrete_sequence=["#9caec2"])
    volume.update_traces(textposition="outside")
    plot(volume)
    st.caption("Figure 5 · Comparison: annual sample counts. Early years with few models make percentages less reliable.")
    with st.expander("Optional: Herfindahl–Hirschman Index (HHI)"):
        hhi = px.line(annual, x="year", y="hhi", markers=True,
                      labels={"year": "Publication year", "hhi": "HHI (unitless, 0–1)"})
        hhi.update_yaxes(range=[0, 1])
        plot(hhi)
        st.write("HHI uses the full country-share distribution; a value closer to 1 indicates greater concentration.")
    st.write("**Annual values (available without hovering):**")
    st.dataframe(annual.round({"top3_weight": 3, "top3_share_pct": 2, "hhi": 3}),
                 hide_index=True, width="stretch")
    download(annual, "annual_concentration.csv", "Download annual calculation")

with tabs[3]:
    st.subheader("Trace a displayed top-three share back to source records")
    year = st.selectbox("Verification year", annual.year.tolist(), index=len(annual) - 1)
    one = exp[exp.year == year]
    ranked = (one.groupby("country", as_index=False).weight.sum()
              .sort_values(["weight", "country"], ascending=[False, True]))
    numerator = ranked.head(3).weight.sum()
    denominator = one.source_record.nunique()
    st.code(f"{numerator:.6f} / {denominator} × 100 = {numerator / denominator * 100:.6f}%")
    st.write("Step 1 — Country totals: the first three rows make the numerator.")
    st.dataframe(ranked, hide_index=True, width="stretch")
    st.write("Step 2 — Allocations: each model with k unique country labels gives 1/k to each label.")
    cols = ["source_record", "Model", "Publication date", COUNTRY,
            "country", "country_count", "weight"]
    st.dataframe(one[cols], hide_index=True, width="stretch")
    st.write("Step 3 — Original, unchanged source columns linked by source_record.")
    original = raw[raw.source_record.isin(one.source_record)][[
        "source_record", "Model", "Organization", "Publication date", COUNTRY, "Reference"]]
    st.dataframe(original, hide_index=True, width="stretch")
    st.caption("source_record is the 1-based CSV record number (not a physical text-line number).")
    download(one[cols], "verification_weights.csv", "Download verification rows")
    st.download_button("Download original source CSV", SOURCE.read_bytes(),
                       "notable_ai_models.csv", "text/csv")
    st.caption("Source SHA-256: " + hashlib.sha256(SOURCE.read_bytes()).hexdigest())

with tabs[4]:
    st.subheader("Methods, limits, and responsible AI use")
    st.markdown("""
**Source and limits**
- Source: Epoch AI, *Data on AI models*. This project analyses a fixed user-provided CSV snapshot received 26 October 2026, not a live feed.
- The included publication years are **2010–2025**. The year 2026 is incomplete and is excluded. Publication coverage can still be incomplete for prior years.
- Exclude invalid publication dates and missing country fields; remove exact duplicate records. Preserve original country/territory labels.
- Organisation country labels are **not researcher nationality**, model quality, compute ownership, or national economic productivity.
- This is a **curated sample** of notable models. Counts do not represent every AI model worldwide.

**Model weighting and scope**
- Split comma-separated country labels; trim whitespace and deduplicate repeated labels **within each model**.
- Each model counts once in total. A model with k unique countries gives each a weight of 1/k.
- Re-rank countries every year; top-three share is their combined weight divided by eligible models that year.
- The sensitivity toggle restricts analysis to single-country models; it answers a narrower question.

**Why the chart forms fit**
- Ranking: sorted horizontal bars (rather than a map, which can distort comparisons through land area).
- Part-to-whole: labelled treemap of the top five and the remainder.
- Change over time: line charts on the same time axis (rather than separate pie charts with hard-to-compare angles).
- The sample-volume chart warns against over-interpreting years with very few models.

**AI use and verification**
- ChatGPT assisted with research framing, coding, calculations, tests, documentation, and presentation drafting.
- The code includes unit tests of mass conservation, a known synthetic case, and a **separate exact-fraction 2025 recalculation**.
- These are computational checks, not an independent audit of every source record. See `docs/AI_PROVENANCE_MATRIX.csv` and `docs/DATA_AI_DISCLOSURE.md` for detail.
    """)
    st.markdown("[Epoch AI source](https://epoch.ai/data/ai-models). Methodology and AI provenance are also documented in the project README and `docs/` folder.")
