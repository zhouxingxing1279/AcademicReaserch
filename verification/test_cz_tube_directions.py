import unittest
from fractions import Fraction as Q
from check_cz_tube_directions import run


class TubeDirectionsTests(unittest.TestCase):
    def test_joint_noise_cancellation(self):
        r=run()
        self.assertEqual(r['first_state_joint'],Q(11,10))
        self.assertEqual(r['first_state_separated'],Q(13,10))

    def test_measurement_conditioning(self):
        r=run()
        self.assertEqual(r['conditioned_e_radius'],Q(1,5))
        self.assertEqual(r['conditioned_d_radius'],0)
        # Independently replay feasible endpoints through plant and observer.
        for t in (Q(-1,5),Q(0),Q(1,5)):
            e,w,nu=t,Q(0),-t
            x_next=e+w
            innovation=x_next+nu
            hat_next=innovation/2
            self.assertEqual(hat_next,0)
            self.assertEqual(x_next-hat_next,t)

    def test_only_current_directions_are_insufficient(self):
        r=run()
        self.assertGreater(r['next_state_current_only'],r['next_state_exact'])

    def test_horizon_directions_survive_compression(self):
        r=run()
        self.assertEqual(r['protected_equalities'],14)
        self.assertTrue(all(v['protected']==v['exact'] for v in r['horizon']))


if __name__=='__main__':unittest.main()
