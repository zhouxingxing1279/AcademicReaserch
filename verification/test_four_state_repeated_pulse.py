"""Run242 repeated-pulse exact rational obstruction regression tests."""
import math
import unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_repeated_pulse as m

class RepeatedPulseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.result=m.verify()

    def test_exact_run241_coefficients(self):
        self.assertEqual(m.coefficients(),(F(8829,62500),F(26487,1250000)))
        self.assertEqual(m.SHAPE,(1,)*3+(-1,)*6+(1,)*3+(0,)*3)

    def test_attitude_reset(self):
        self.assertEqual(len(m.angle_coefficients()),15)
        self.assertEqual(max(m.angle_coefficients()),F(3,25))
        self.assertEqual(sum(m.SHAPE),0)

    def test_area_expansion(self):
        self.assertEqual(self.result['determinant'],str(F(1276487,1250000)))
        self.assertEqual(self.result['determinant_minus_one'],str(F(26487,1250000)))
        for n in m.MODES:
            self.assertEqual(m.det2(m.pulse_jacobian(n)),F(1276487,1250000))

    def test_complex_unstable_eigenvalues(self):
        for n in m.MODES:
            a=m.pulse_jacobian(n)
            self.assertLess(m.trace2(a)**2-4*m.det2(a),0)
            self.assertGreater(m.det2(a),1)

    def test_mode_lengths(self):
        self.assertEqual([x['macrocycle_ticks'] for x in self.result['modes']],[20,25,30])

    def test_independent_nonlinear_euler_jacobian_sanity(self):
        # Numerical finite difference is a sanity check, not the proof.
        h=float(m.H); T=float(m.T); gain=float(m.GAIN)
        def cycle(n,p,v):
            phi=omega=0.
            for _ in range(n):p,v=p+h*v,v
            y=p
            for s in m.SHAPE:
                p,v,phi,omega=(p+h*v,v-h*T*math.sin(phi),
                               phi+h*omega,omega+h/float(m.J)*gain*y*s)
            self.assertAlmostEqual(phi,0.,places=13)
            self.assertAlmostEqual(omega,0.,places=13)
            return p,v
        eps=1e-6
        for n in m.MODES:
            c1=cycle(n,eps,0.)
            c2=cycle(n,0.,eps)
            numerical=((c1[0]/eps,c2[0]/eps),(c1[1]/eps,c2[1]/eps))
            exact=m.pulse_jacobian(n)
            for i in range(2):
                for j in range(2):
                    self.assertAlmostEqual(numerical[i][j],float(exact[i][j]),places=9)

    def test_scope_flags(self):
        self.assertFalse(self.result['recursive_invariance_ruled_out'])
        self.assertFalse(self.result['arbitrary_causal_controller_ruled_out'])
        self.assertFalse(self.result['smf_mpc_closed_loop_certified'])

    def test_invalid_mode(self):
        with self.assertRaises(ValueError):m.pulse_jacobian(7)

    def test_full_config(self):
        root=Path(__file__).resolve().parents[1]
        if (root/'configs/planar_baseline.json').exists():
            self.assertEqual(m.verify(root),self.result)
        else:self.skipTest('requires complete repository checkout')

if __name__=='__main__':unittest.main()
