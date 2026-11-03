import unittest
from fractions import Fraction as Q
from check_mode_indexed_box_terminal_obstruction import (contract,residual,step,clip,nonzero_causal_torque,corner_witness,five_cycle_proof,torque_relative_degree,run)

class BoxNoGoTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.c=contract()
    def test_frozen_contract(self):
        c=self.c
        self.assertEqual((c['h'],c['j'],c['tmin'],c['tmax'],c['tau_max']),(Q(1,50),Q(1,50),Q(981,200),Q(2943,200),Q(2,25)))
    def test_five_cycle_edges_exist(self):
        self.assertEqual(len(five_cycle_proof(self.c)['cycle']),5)
        self.assertIn((4,0,'success'),self.c['edges'])
    def test_exact_positive_residual(self):
        self.assertEqual(residual(self.c['tmin']),Q(47,25)+Q(243,16000)*Q(981,200))
        self.assertGreater(self.c['h']*residual(self.c['tmin']),0)
    def test_torque_policy_nonzero_and_within_bounds(self):
        x=(Q(1),Q(1,2),Q(0),Q(0));u=nonzero_causal_torque(x,self.c)
        self.assertEqual(u,Q(1,25));self.assertLessEqual(abs(u),self.c['tau_max'])
    def test_corner_fails_with_nonzero_torque_and_zero_disturbance(self):
        w=corner_witness(self.c)
        self.assertEqual(Q(w['next'][0]),Q(101,100))
        self.assertGreater(Q(w['position_excess']),0)
    def test_position_next_independent_of_torque_and_thrust(self):
        x=(Q(1),Q(1,2),Q(0),Q(0))
        positions={step(x,t,u,Q(0),self.c)[0] for t in (self.c['tmin'],self.c['tmax']) for u in (-self.c['tau_max'],Q(0),self.c['tau_max'])}
        self.assertEqual(positions,{Q(101,100)})
    def test_no_go_includes_zero_velocity_radii_case(self):
        d=five_cycle_proof(self.c)
        self.assertGreater(Q(d['forced_positive_velocity_radius']),0)
        self.assertIn('all V_i=0',d['cycle_sum'])
    def test_exact_relative_degree(self):
        d=torque_relative_degree(self.c)
        self.assertEqual(d['first_torque_effect'],{'omega':1,'phi':2,'v':3,'p':4})
    def test_scope_does_not_claim_general_impossibility(self):
        d=run()
        self.assertEqual(d['gate_A'],'blocked')
        self.assertIn('not to translated',d['cycle_proof']['scope'])
        self.assertEqual(d['status'],'PASS')

if __name__=='__main__':unittest.main()
