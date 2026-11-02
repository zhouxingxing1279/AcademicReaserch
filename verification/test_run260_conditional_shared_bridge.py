import unittest
from fractions import Fraction as F

from check_run255_posterior_bridge import T, safe, LIMIT
from check_run259_rolling_anchor import roll
from check_run260_conditional_shared_bridge import (
    posterior_at_45, unconditional_bridge, verify,
)


class TestRun260ConditionalSharedBridge(unittest.TestCase):
    def test_only_frozen_patterns(self):
        for pat in ('SSS', 'MMM', 'SM'):
            with self.assertRaises(ValueError):
                posterior_at_45(pat)

    def test_matches_run259_smm(self):
        s = posterior_at_45('SMM')
        self.assertEqual(s['v'], tuple(F(v) for v in roll('SMM')[0]['45']['velocity']))

    def test_matches_run259_mms(self):
        s = posterior_at_45('MMS')
        self.assertEqual(s['v'], tuple(F(v) for v in roll('MMS')[0]['45']['velocity']))

    def test_shared_bridge_smm(self):
        self.assertTrue(all(safe(x) for x in unconditional_bridge(posterior_at_45('SMM'))))

    def test_shared_bridge_mms(self):
        self.assertTrue(all(safe(x) for x in unconditional_bridge(posterior_at_45('MMS'))))

    def test_all_hard_margins_strict(self):
        for pat in ('SMM', 'MMS'):
            for state in unconditional_bridge(posterior_at_45(pat)):
                for key, (lo, hi) in state.items():
                    self.assertLess(max(abs(lo), abs(hi)), LIMIT[key])

    def test_exact_tick60_endpoints(self):
        result = verify()
        self.assertEqual(result['branches']['SMM']['tick60_outer']['v'],
                         ['-7841778593/5000000000', '15679162373/10000000000'])
        self.assertEqual(result['branches']['MMS']['tick60_outer']['v'],
                         ['-2187058727/2000000000', '5466914349/5000000000'])

    def test_scope_and_actuation(self):
        result = verify()
        self.assertEqual(result['shared_control_ticks_45_to_59']['actual_thrust_N'], str(T))
        self.assertEqual(result['shared_control_ticks_45_to_59']['torque_Nm'], '0')
        self.assertFalse(result['complete_information_state_terminal_rcis'])
        self.assertFalse(result['infinite_horizon_recursive_feasibility'])
        self.assertFalse(result['general_arbitrary_history_safety'])
        self.assertEqual(result['gate_A'], 'blocked')

    def test_frozen_horizon_only(self):
        with self.assertRaises(ValueError):
            unconditional_bridge(posterior_at_45('SMM'), 16)


if __name__ == '__main__':
    unittest.main()
