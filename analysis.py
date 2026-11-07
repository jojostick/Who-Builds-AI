"""Reproducible analysis of the supplied Epoch AI snapshot."""
from pathlib import Path
import hashlib
import json
import pandas as pd

ROOT = Path(__file__).resolve().parent
SOURCE = ROOT / 'data/notable_ai_models.csv'
COUNTRY = 'Country (of organization)'


def country_list(value):
    """Deduplicate country labels within a model, preserving source labels."""
    if pd.isna(value):
        return []
    return sorted({s.strip() for s in str(value).split(',') if s.strip()})


def load_data():
    raw = pd.read_csv(SOURCE)
    raw.insert(0, 'source_record', range(1, len(raw) + 1))
    clean = raw.drop_duplicates(subset=list(raw.columns[1:])).copy()
    clean['year'] = pd.to_datetime(clean['Publication date'], errors='coerce').dt.year
    clean['countries'] = clean[COUNTRY].apply(country_list)
    clean['country_count'] = clean['countries'].str.len()
    return raw, clean


def allocate(clean, start=2010, end=2025, single_only=False):
    eligible = clean.loc[clean['year'].between(start, end) & (clean.country_count > 0)].copy()
    if single_only:
        eligible = eligible.loc[eligible.country_count == 1].copy()
    eligible['weight'] = 1.0 / eligible.country_count
    expanded = eligible.explode('countries').rename(columns={'countries': 'country'})
    expanded['year'] = expanded['year'].astype(int)
    return expanded


def annual_summary(expanded):
    rows = []
    for year, group in expanded.groupby('year'):
        counts = group.groupby('country')['weight'].sum().sort_values(ascending=False)
        denominator = group.source_record.nunique()
        top = counts.head(3)
        rows.append({'year': int(year), 'eligible_models': denominator,
                     'represented_countries': len(counts),
                     'top3_countries': '; '.join(top.index),
                     'top3_weight': float(top.sum()),
                     'top3_share_pct': float(top.sum() / denominator * 100),
                     'hhi': float(((counts / denominator) ** 2).sum())})
    return pd.DataFrame(rows)


def export():
    raw, clean = load_data()
    expanded = allocate(clean)
    annual = annual_summary(expanded)
    # Keep generated data with the source samples for reproducible deployment.
    output = ROOT / 'data' / 'processed'
    output.mkdir(parents=True, exist_ok=True)
    annual.to_csv(output / 'annual_concentration.csv', index=False)
    expanded[['source_record', 'Model', 'Organization', 'Publication date', 'year', COUNTRY,
              'country', 'country_count', 'weight', 'Reference']].to_csv(output / 'model_country_weights.csv', index=False)
    expanded.groupby(['year', 'country'], as_index=False)['weight'].sum().to_csv(output / 'country_year.csv', index=False)
    window = clean[clean.year.between(2010, 2025)]
    audit = {'raw_rows': len(raw), 'exact_duplicates_removed': len(raw)-len(clean),
             'invalid_dates': int(clean.year.isna().sum()),
             'missing_country_all_years': int((clean.country_count == 0).sum()),
             'window_rows': len(window), 'window_missing_country': int((window.country_count == 0).sum()),
             'eligible_models_2010_2025': int(expanded.source_record.nunique()),
             'multi_country_models_2010_2025': int(((window.country_count > 1)).sum()),
             'rows_2026_excluded': int((clean.year == 2026).sum()),
             'sha256': hashlib.sha256(SOURCE.read_bytes()).hexdigest()}
    (output / 'data_audit.json').write_text(json.dumps(audit, indent=2))
    print(json.dumps(audit, indent=2))
    print(annual.to_string(index=False))

if __name__ == '__main__':
    export()
