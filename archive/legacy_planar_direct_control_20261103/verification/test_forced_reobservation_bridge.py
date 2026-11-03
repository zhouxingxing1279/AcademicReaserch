import unittest
from fractions import Fraction as F
from pathlib import Path
from check_forced_reobservation_bridge import (H, R, U, NOISE_P, BRIDGE,
    D15, LIMITS, envelope, gaps, verify)

class ForcedReobservationBridgeTests(unittest.TestCase):
    def test_shared_nonzero_balanced_torque(self):
        self.assertTrue(any(t != 0 for t in BRIDGE))
        self.assertEqual(sum(BRIDGE), 0)
        self.assertTrue(all(abs(t) <= U for t in BRIDGE))
    def test_tick25_matches_prior_certificate(self):
        self.assertEqual(envelope(10)['p'], F(181187993, 2000000000))
        self.assertEqual(envelope(10)['v'], F(113157903, 160000000))
    def test_uniform_safety_all_ticks(self):
        for j in range(16):
            self.assertTrue(all(v < LIMITS[k] for k,v in envelope(j).items()))
    def test_tick30_safety_margin(self):
        self.assertEqual(envelope(15)['omega'], F(6,5))
        self.assertEqual(envelope(15)['phi'], F(21,125))
    def test_exact_velocity_gap(self):
        self.assertEqual(gaps()[1], D15 + 20*H*R)
    def test_exact_position_gap_lower(self):
        self.assertEqual(gaps()[2], F(236985959,800000000))
    def test_disjoint_success_noise_strips(self):
        self.assertGreater(gaps()[2] - 2*NOISE_P, 0)
    def test_certificate_no_recursive_claim(self):
        c = verify()
        self.assertFalse(c['recursive_feasibility_proved'])
        self.assertFalse(c['terminal_invariant_set_proved'])
        self.assertEqual(c['gate_A'], 'blocked')
    def test_repo_crosscheck_when_available(self):
        root=Path(__file__).resolve().parents[1]
        if not (root/'configs/planar_baseline.json').exists():
            self.skipTest('isolated working directory: repository config absent')
        verify(root)

if __name__ == '__main__': unittest.main()
