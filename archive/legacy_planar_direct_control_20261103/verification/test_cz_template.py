import unittest
from fractions import Fraction as Q
import numpy as np
from check_constrained_zonotope import eye
from check_cz_template import Template, compress, outward, rollout


class TemplateContracts(unittest.TestCase):
    def test_float_inputs_are_rejected(self):
        with self.assertRaises(TypeError):
            Template([[1.0], [-1.0]], [Q(1), Q(1)])
        p = Template(np.vstack((eye(1), -eye(1))), [Q(1), Q(1)])
        with self.assertRaises(TypeError):
            rollout(p, [[1.0]], [[Q(0)]], 1)

    def test_asymmetric_triangle_rebuild(self):
        h = np.vstack((eye(2), -eye(2), [[Q(1), Q(1)]]))
        p = Template(h, [Q(1), Q(1), Q(0), Q(0), Q(1)])
        c = p.to_cz()
        for point in ([0, 0], [1, 0], [0, 1], [Q(1, 4), Q(1, 2)]):
            latent = p.witness(point)
            self.assertTrue(all(abs(v) <= 1 for v in latent))
            self.assertTrue(np.array_equal(c.c+c.g @ latent, point))
            self.assertTrue(np.array_equal(c.a @ latent, c.b))
        self.assertEqual(c.support_certificate([Q(1), Q(1)])[0], 1)

    def test_zero_width_and_inconsistent_bounds(self):
        p = Template(np.vstack((eye(1), -eye(1), eye(1))), [Q(0)]*3)
        self.assertEqual(list(p.witness([Q(0)])), [0, 0])
        with self.assertRaises(ValueError):
            Template(p.h, [Q(1), Q(0), Q(-1)]).to_cz()

    def test_cap_prevents_constraint_loss_on_fallback(self):
        h = np.vstack((eye(2), -eye(2), [[Q(1), Q(-1)], [Q(-1), Q(1)]]))
        p = Template(h, [Q(1)]*4+[Q(0)]*2)
        loose, _ = compress(p.to_cz(), h, skip_lp=True)
        capped, _ = compress(p.to_cz(), h, cap=p, skip_lp=True)
        self.assertEqual(loose.b[4], 2)
        self.assertEqual(capped.b[4], 0)
        self.assertTrue(np.array_equal(capped.b, p.b))

    def test_rollover_with_deliberately_loose_queries(self):
        h = np.vstack((eye(1), -eye(1)))
        p = Template(h, [Q(1), Q(1)])
        old, _ = rollout(p, eye(1), np.array([[Q(1, 10)]], dtype=object), 3)
        posterior = Template(h, [Q(1, 2), Q(1, 2)])
        new, checks = rollout(posterior, eye(1), np.array([[Q(1, 10)]], dtype=object),
                              3, old=old, skip_lp=True)
        self.assertEqual(checks['shift_rows'], 4)
        for i in range(3):
            self.assertTrue(all(new[i].b <= old[i+1].b))
        self.assertEqual(new[-1].b[0], Q(4, 5))

    def test_outward_rounding_and_recenter(self):
        self.assertGreaterEqual(outward(Q(-1, 3)), Q(-1, 3))
        p = Template(np.vstack((eye(1), -eye(1))), [Q(3, 4), Q(-1, 4)])
        q = p.recenter([Q(1, 2)])
        self.assertEqual(list(q.b), [Q(1, 4), Q(1, 4)])


if __name__ == '__main__':
    unittest.main()
