import unittest
from fractions import Fraction as Q
from check_recursive_tube import terminal_certificate, candidate, posterior, replay


class RecursiveTubeTests(unittest.TestCase):
    def test_terminal_invariance_and_admissibility(self):
        c=terminal_certificate()
        self.assertEqual(c['image_radii'],[Q(7,20),Q(3,4)])
        self.assertLessEqual(c['state_bound'],2)
        self.assertLessEqual(c['input_bound'],1)

    def test_initial_feasible_candidate(self):
        c=candidate(Q(1,2),(-Q(1),Q(1)),Q(0))
        self.assertTrue(c['feasible'])
        self.assertLessEqual(c['terminal_e'],Q(2,5))
        self.assertLessEqual(c['terminal_d'],Q(4,5))

    def test_conditioning_excludes_inconsistent_error(self):
        self.assertEqual(posterior((-Q(1),Q(1)),Q(0)),(-Q(1,5),Q(1,5)))
        with self.assertRaises(ValueError):posterior((-Q(1),Q(1)),Q(2))

    def test_closed_loop_fallback_replay(self):
        r=replay()
        self.assertEqual(r['steps'],1024)
        self.assertEqual(r['violations'],0)


if __name__=='__main__':unittest.main()
