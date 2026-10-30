import unittest
from fractions import Fraction as F
from check_lateral_dropout_support_floor import (
    contract, floor, full_prior_position_radius, pair_witness, radius, run, step,
)


class LateralDropoutSupportTests(unittest.TestCase):
    def setUp(self):
        self.c = contract()

    def test_config_contract(self):
        c = self.c
        self.assertEqual(c['h'], F(1, 50))
        self.assertEqual(c['j'], F(1, 50))
        self.assertEqual((c['tmin'], c['tmax']), (F(981, 200), F(2943, 200)))
        self.assertEqual((c['p0'], c['v0']), (F(1, 50), F(1, 10)))
        self.assertEqual((c['period'], c['misses']), (5, 2))

    def test_tick_zero_common_position_measurement_is_consistent(self):
        c = self.c
        # Both p=+/-0.02 can generate y_px=0 with bounded +/-0.02 noise.
        self.assertEqual(c['p0'], F(1, 50))
        self.assertEqual(c['p0'] + (-F(1, 50)), 0)
        self.assertEqual(-c['p0'] + F(1, 50), 0)

    def test_one_tick_residual_cannot_move_position(self):
        c = self.c
        self.assertEqual(floor([c['tmax']], c), c['p0']+c['h']*c['v0'])
        self.assertEqual(step((F(0),)*4, c['tmax'], F(0), radius(c['tmax']), c['h'], c['j'])[0], 0)

    def test_indistinguishable_pair_for_all_three_return_lengths(self):
        c = self.c
        for n in (5, 10, 15):
            for t in (c['tmin'], c['tmax']):
                seq = [t]*n
                plus, minus = pair_witness(seq, c)
                self.assertEqual(plus[2:], minus[2:])
                self.assertEqual((plus[0]-minus[0])/2, floor(seq, c))

    def test_alternating_schedule_exact_independent_witness(self):
        c = self.c
        seq = [c['tmin'] if i%2 == 0 else c['tmax'] for i in range(15)]
        plus, minus = pair_witness(seq, c)
        self.assertEqual(plus[0], -minus[0])
        self.assertEqual(plus[0], floor(seq, c))
        self.assertLess(floor([c['tmin']]*15, c), plus[0])
        self.assertLess(plus[0], floor([c['tmax']]*15, c))

    def test_zonotope_support_upper_and_attitude_coupling(self):
        c = self.c
        for n in (5, 10, 15):
            seq = [c['tmax']]*n
            self.assertGreater(full_prior_position_radius(seq, c), floor(seq, c))

    def test_archived_audit_shape(self):
        d = run()
        self.assertEqual(d['status'], 'PASS')
        self.assertEqual(len(d['results']), 9)
        self.assertEqual(d['gate_A'], 'blocked')
        self.assertTrue(all(r['does_not_by_itself_violate_global_position_bound'] for r in d['results']))


if __name__ == '__main__':
    unittest.main()
