"""Focused Run254 exact witness and interval SMF regression."""
import json
import unittest
from fractions import Fraction as F
from pathlib import Path
from check_forced_success_velocity_alias import (
    R, PATTERN, SUCCESS, MISSED, truth_path, outer_history, verify)


class ForcedSuccessAliasTests(unittest.TestCase):
    def test_legal_word(self):
        self.assertEqual(SUCCESS, (5, 10, 15, 30))
        self.assertEqual(MISSED, (20, 25))

    def test_residual_bounds(self):
        self.assertEqual(len(PATTERN), 15)
        self.assertTrue(all(abs(x) <= 1 for x in PATTERN))

    def test_zero_terminal_position(self):
        self.assertEqual(truth_path(1)[30]['p'], 0)
        self.assertEqual(truth_path(-1)[30]['p'], 0)

    def test_velocity_separation(self):
        self.assertEqual(truth_path(1)[30]['v'] - truth_path(-1)[30]['v'], R/4)

    def test_identical_measurements(self):
        plus, minus = truth_path(1), truth_path(-1)
        for k in SUCCESS:
            self.assertEqual(plus[k]['p'], minus[k]['p'])
            self.assertEqual(plus[k]['p'], 0)

    def test_interval_outer(self):
        rows = outer_history()
        self.assertEqual(rows[30]['v'], (-F(269364701, 200000000),
                                         F(269364701, 200000000)))

    def test_all_truth_contained_and_safe(self):
        out = verify()
        self.assertTrue(out['all_truth_ticks_contained_in_run249_smf'])
        self.assertTrue(out['all_truth_ticks_safe'])
        self.assertFalse(out['recursive_feasibility_proved'])

    def test_exact_certificate_roundtrip(self):
        p = Path(__file__).resolve().parents[1] / 'results/forced_success_velocity_alias_20261101/checks.json'
        if not p.exists():
            self.skipTest('full repository certificate not present in isolated copy')
        self.assertEqual(json.loads(p.read_text()), verify())

    def test_real_config(self):
        root = Path(__file__).resolve().parents[1]
        if not (root/'configs/planar_baseline.json').exists():
            self.skipTest('full repository config not present in isolated copy')
        self.assertEqual(verify(root)['gate_A'], 'blocked')


if __name__ == '__main__':
    unittest.main()
