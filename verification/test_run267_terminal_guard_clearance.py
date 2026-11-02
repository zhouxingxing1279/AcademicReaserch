"""Run267 guard screening; assertions are necessary-only, not viability tests."""
import unittest
from fractions import Fraction as F
from check_run267_terminal_guard_clearance import BOXES, DELTA, certificate, sin_bounds, uniform_guard


class TestRun267(unittest.TestCase):
    def test_taylor_encloses_known_sine_zero(self):
        assert sin_bounds(F(0)) == (F(0), F(0))

    def test_taylor_odd_symmetry(self):
        for x in (F(1, 100), F(1, 10), F(9, 20)):
            lo, hi = sin_bounds(x)
            nlo, nhi = sin_bounds(-x)
            self.assertEqual((nlo, nhi), (-hi, -lo))

    def test_delta(self):
        self.assertEqual(DELTA, F(1, 625))

    def test_all_four_box_clearances(self):
        for tick, branches in BOXES.items():
            for mode, box in branches.items():
                with self.subTest(tick=tick, mode=mode):
                    self.assertTrue(all(x > 0 for x in uniform_guard(box)))

    def test_wider_velocity_box_at_75(self):
        for mode in ('SMM', 'MMS'):
            v60 = list(map(F, BOXES[60][mode]['v']))
            v75 = list(map(F, BOXES[75][mode]['v']))
            self.assertLess(v75[0], v60[0])
            self.assertGreater(v75[1], v60[1])

    def test_certificate_not_overclaiming(self):
        c = certificate()
        self.assertEqual(c['gate_A'], 'blocked')
        self.assertIn('information-state RCI', c['not_proved'])
        self.assertIn('not sufficient', c['meaning'])


if __name__ == '__main__':
    unittest.main()
