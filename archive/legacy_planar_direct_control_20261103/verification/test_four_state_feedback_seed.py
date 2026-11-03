"""Run233 finite-horizon full-state feedback seed tests (no invariance claim)."""
import unittest
from pathlib import Path
import check_four_state_feedback_seed as m


class FeedbackSeedTests(unittest.TestCase):
    def test_constants(self):
        self.assertAlmostEqual(m.RADIUS, m.R0 + m.RT * m.THRUST)
        self.assertTrue(m.TMIN <= m.THRUST <= m.TMAX)

    def test_plant_euler(self):
        self.assertEqual(m.step((0, 0, 0, 0), (m.THRUST, 0), 0), (0, 0, 0, 0))
        self.assertAlmostEqual(m.step((0, 0, 0, 0), (m.THRUST, 0), m.RADIUS)[1], m.H * m.RADIUS)

    def test_reject_invalid(self):
        with self.assertRaises(ValueError):
            m.step((0, 0, 0, 0), (20, 0), 0)
        with self.assertRaises(ValueError):
            m.step((0, 0, 0, 0), (m.THRUST, 0), 3)
        with self.assertRaises(ValueError):
            m.episode('positive', ticks=0)

    def test_policy_saturates(self):
        self.assertLessEqual(abs(m.policy((5, 3, .45, 2))[1]), m.TAUMAX)
        self.assertEqual(m.policy((0, 0, 0, 0), False)[1], 0)

    def test_baseline_violates(self):
        self.assertIsNotNone(m.episode('positive', feedback=False)['first_violation_tick'])

    def test_finite_deterministic_trajectories(self):
        d = m.verify()
        self.assertEqual(d['ticks_per_episode'], 1000)
        self.assertTrue(all(v['first_violation_tick'] is None for v in d['deterministic_scenarios'].values()))

    def test_seeded_monte_carlo_reproducible(self):
        a, b = m.verify(), m.verify()
        self.assertEqual(a, b)
        self.assertEqual(a['random_episodes'], 128)
        self.assertEqual(a['random_violations'], 0)
        self.assertEqual(a['gate_A'], 'blocked')

    def test_real_config(self):
        root = Path(__file__).resolve().parents[1]
        if (root / 'configs/planar_baseline.json').exists():
            self.assertEqual(m.verify(root)['random_episodes'], 128)
        else:
            self.skipTest('requires full checkout; CI must verify')


if __name__ == '__main__':
    unittest.main()
