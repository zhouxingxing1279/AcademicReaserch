"""Exact terminal-tube invariance and causal SMF/MPC regression tests."""
import itertools
import unittest
from fractions import Fraction as Q
from pathlib import Path

import check_attitude_terminal_smf_mpc as m


class AttitudeTerminalSMFMPCTests(unittest.TestCase):
    def test_exact_terminal_and_error_rpi(self):
        c=m.exact_certificate()
        self.assertEqual(c['error_image'],c['error_radii'])
        self.assertEqual(c['terminal_image'][0],c['terminal_radii'][0])
        self.assertLess(c['terminal_image'][1],c['terminal_radii'][1])
        self.assertEqual(c['feedback_noise'],Q(2,625))
        self.assertEqual(c['correction'],Q(8,625))
        self.assertEqual(c['nominal_input_limit'],Q(42,625))
        self.assertEqual(c['terminal_nominal_input_support'],Q(6,125))

    def test_rpi_vertices_under_all_measurement_corners(self):
        for ep,es,np,no in itertools.product((-1,1),repeat=4):
            e=(ep*m.E_PHI,es*m.E_S-4*ep*m.E_PHI)
            n=(np*m.SIGMA[0],no*m.SIGMA[1])
            enext=m.state_step(e,m.feedback(tuple(e[i]+n[i] for i in range(2))))
            self.assertTrue(m.inside_error(enext))
        for zp,zs in itertools.product((-1,1),repeat=2):
            z=(zp*m.ZF_PHI,zs*m.ZF_S-4*zp*m.ZF_PHI)
            zn=m.nominal_step(z,m.feedback(z))
            self.assertTrue(m.inside_terminal(zn))
            self.assertLessEqual(abs(m.feedback(z)),m.exact_certificate()['nominal_input_limit'])

    def test_every_grid_plan_shifts_feasibly(self):
        c=m.exact_certificate()
        for z in ((Q(0),Q(0)),(Q(1,50),Q(-1,10)),(Q(-1,50),Q(1,10))):
            for plan in itertools.product(m.GRID,repeat=m.N):
                if m.feasible(z,plan,c):
                    znext=m.nominal_step(z,plan[0])
                    self.assertTrue(m.feasible(znext,m.tail(z,plan),c))

    def test_midpoint_uses_smf_not_hidden_truth_and_fails_closed(self):
        p=((-m.SIGMA[0],m.SIGMA[0]),(-m.SIGMA[1],m.SIGMA[1]))
        self.assertEqual(m.certified_midpoint(p),(Q(0),Q(0)))
        too_wide=((Q(-1,100),Q(1,100)),(-m.SIGMA[1],m.SIGMA[1]))
        with self.assertRaisesRegex(ValueError,'exceeds'):
            m.certified_midpoint(too_wide)
        with self.assertRaisesRegex(ValueError,'Inconsistent'):
            m.smf_observe(p,(Q(1),Q(0)))

    def test_full_closed_loop_and_real_optimization(self):
        data=m.run()
        self.assertEqual(data['episodes'],32)
        self.assertEqual(data['total_steps'],1536)
        self.assertEqual(data['violations'],0)
        self.assertGreater(data['optimizer_changed_steps'],0)
        self.assertLess(data['mpc_mean_tracking_rmse'],data['terminal_only_mean_tracking_rmse'])
        self.assertLessEqual(data['max_abs_phi'],m.PHI_LIMIT)
        self.assertLessEqual(data['max_abs_omega'],m.OMEGA_LIMIT)
        self.assertLessEqual(data['max_abs_tau'],m.TAU_LIMIT)
        for row in data['rows']:
            self.assertEqual(row['smf_coverage'],row['steps']+1)

    def test_real_repository_contract_when_available(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertTrue(m.config_contract(root))
        else:
            self.skipTest('no complete checkout: config assertion runs in GitHub CI')


if __name__=='__main__':unittest.main()
