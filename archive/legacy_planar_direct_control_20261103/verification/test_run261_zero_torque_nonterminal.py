import unittest
from fractions import Fraction as F
from check_run261_zero_torque_nonterminal import (
    H, R, T, PULSE, pulse_witness, adversarial_continuation, verify,
)


class TestRun261(unittest.TestCase):
    def test_pulse_ends_at_zero(self):
        states, _ = pulse_witness()
        self.assertEqual(len(states), 5)
        self.assertEqual(states[-1][:2], (F(0), F(0)))

    def test_pulse_residual_is_admissible(self):
        _, phi = pulse_witness()
        self.assertLess(T * phi, R)

    def test_first_bad_is_119(self):
        _, bad = adversarial_continuation()
        self.assertEqual(bad['tick'], 119)

    def test_118_safe(self):
        rows, _ = adversarial_continuation()
        self.assertLess(rows[-2]['v'], F(3))

    def test_119_position_still_safe(self):
        _, bad = adversarial_continuation()
        self.assertLess(bad['p'], F(5))

    def test_119_velocity_unsafe(self):
        _, bad = adversarial_continuation()
        self.assertGreater(bad['v'], F(3))

    def test_closed_form_exact(self):
        rows, _ = adversarial_continuation()
        for n, row in enumerate(rows):
            self.assertEqual(row['v'], n * H * R)
            self.assertEqual(row['p'], H * H * R * n * (n - 1) / 2)

    def test_both_patterns_covered(self):
        result = verify()
        self.assertIn('SMM', result['histories'][1])
        self.assertIn('MMS', result['histories'][1])

    def test_not_generalized(self):
        result = verify()
        self.assertFalse(result['rules_out_other_causal_controllers'])
        self.assertFalse(result['rules_out_terminal_information_rci'])
        self.assertEqual(result['gate_A'], 'blocked')


if __name__ == '__main__':
    unittest.main()
