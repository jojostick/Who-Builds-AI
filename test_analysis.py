"""Run with python -m unittest -v; no external test runner required."""
import csv
import unittest
from collections import defaultdict
from fractions import Fraction
import pandas as pd
from analysis import SOURCE, COUNTRY, country_list, load_data, allocate, annual_summary

class AnalysisTests(unittest.TestCase):
    def test_country_parsing(self):
        self.assertEqual(country_list('US, US, Canada'), ['Canada', 'US'])
        self.assertEqual(country_list(None), [])

    def test_mass_conservation_and_year_bounds(self):
        _, clean = load_data()
        e = allocate(clean)
        self.assertTrue((e.groupby('source_record').weight.sum().sub(1).abs() < 1e-12).all())
        self.assertTrue(e.year.between(2010,2025).all())
        a = annual_summary(e)
        self.assertTrue(a.top3_share_pct.between(0,100.0000001).all())
        self.assertTrue(a.hhi.between(0,1).all())

    def test_independent_2025_recalculation(self):
        # Independently use csv and exact fractions, not pandas aggregation.
        counts = defaultdict(Fraction)
        n = 0
        with SOURCE.open(newline='') as f:
            for row in csv.DictReader(f):
                if not row['Publication date'].startswith('2025-'):
                    continue
                countries = set(s.strip() for s in row[COUNTRY].split(',') if s.strip())
                if not countries:
                    continue
                n += 1
                for country in countries:
                    counts[country] += Fraction(1,len(countries))
        top = sum(sorted(counts.values(), reverse=True)[:3])
        _, clean = load_data()
        result = annual_summary(allocate(clean,2025,2025)).iloc[0]
        self.assertEqual(n,107)
        self.assertEqual(top,Fraction(311,3))
        self.assertAlmostEqual(result.top3_share_pct,float(top/n*100),places=10)

    def test_single_country_sensitivity(self):
        _, clean = load_data()
        e = allocate(clean,single_only=True)
        self.assertTrue((e.country_count == 1).all())
        self.assertTrue((e.weight == 1).all())

    def test_synthetic_case(self):
        d = pd.DataFrame({'year':[2020,2020,2020], 'source_record':[1,2,3],
                          'countries':[['A','B'],['A'],[]], 'country_count':[2,1,0]})
        e = allocate(d,2020,2020)
        self.assertEqual(e.weight.sum(),2)
        self.assertEqual(e.groupby('country').weight.sum().to_dict(),{'A':1.5,'B':0.5})
        self.assertAlmostEqual(annual_summary(e).iloc[0].hhi,0.625)

if __name__ == '__main__':
    unittest.main()
