import unittest
from dataclasses import replace
from itertools import product
import numpy as np
from scipy.optimize import linprog
from src.outerloop.finite_memory import (Contract, ContractError, FloatCZ,
    FiniteMemoryEstimator, pair_window, full_history, arrival_graph)
from src.outerloop.tube_mpc import TubeDesign, NominalMPC


class FiniteMemoryTests(unittest.TestCase):
    def test_full_delivery_graph(self):
        for M in range(4):
            for L in range(4):
                g = arrival_graph(M, L)
                self.assertGreater(g['edges'], 0)
                for d, h in g['pairs']:
                    self.assertLessEqual(d+h, g['span'])
                    self.assertLessEqual(h, M+L)

    def test_pair_against_explicit_disturbance_vertices(self):
        c = Contract()
        A, B = c.matrices()
        for d in range(1, 4):
            for h in range(min(c.age, c.span-d)+1):
                n = d+h
                u = {k: (-1)**k*.13 for k in range(n)}
                for signs in product([-1, 1], repeat=n+2):
                    state = np.array([.3, -.17])
                    x = [state.copy()]
                    for k in range(n):
                        state = A@state+B*(u[k]+signs[k]*c.acceleration)
                        x.append(state.copy())
                    data = {0: x[0][0]+signs[-2]*c.noise,
                            d: x[d][0]+signs[-1]*c.noise}
                    z = pair_window(c, n, data, u)
                    self.assertTrue(z.contains(x[n]))
                    np.testing.assert_allclose(np.abs(z.generators).sum(axis=1),
                                               c.pair_radius(d, h), atol=1e-12)

    def test_full_history_is_inside_forgotten_window(self):
        c, initial = Contract(), [.2, -.1]
        A, B = c.matrices()
        x, commands, packets = np.array(initial), {}, {}
        for k in range(9):
            packets[k] = x[0]+c.noise*np.sin(k)
            if k >= 2:
                batch = full_history(c, k, packets, commands, initial)
                window = pair_window(c, k, {s: y for s, y in packets.items() if s >= k-c.span}, commands)
                bl, bh = batch.bounds()
                wl, wh = window.bounds()
                self.assertTrue(np.all(wl <= bl+1e-7) and np.all(bh <= wh+1e-7))
                self.assertTrue(window.contains(x))
            commands[k] = .03*np.cos(k)
            x = A@x+B*(commands[k]+c.acceleration*np.sin(k))

    def test_conflicting_duplicate_and_timestamp_errors(self):
        f = FiniteMemoryEstimator(Contract(), [0, 0])
        f.observe([(0, 0.), (0, 0.)])
        for packet in [[(0, 1.)], [(1, 0.)], [(-1, 0.)]]:
            with self.assertRaises(ContractError):
                f.observe(packet)

    def test_empty_posterior_and_nonfeasible_center(self):
        z = FloatCZ(np.zeros(1), np.ones((1, 1)), np.ones((1, 1)), np.array([.8]))
        np.testing.assert_allclose(z.representative(), [.8])
        self.assertFalse(z.contains([0.]))
        c = Contract()
        bad = pair_window(c, 2, {0: 0., 1: 100., 2: 0.}, {0: 0., 1: 0.})
        with self.assertRaises(ContractError):
            bad.representative()

    def test_no_second_timestamp_deadline(self):
        f = FiniteMemoryEstimator(Contract(), [0, 0])
        for k in range(f.contract.span):
            f.observe([(0, 0.)] if k == 0 else [])
            f.advance(0.)
        with self.assertRaises(ContractError):
            f.observe([])

    def test_zero_noise_and_zero_disturbance(self):
        c = replace(Contract(), noise=0., acceleration=0.)
        z = pair_window(c, 3, {0: 1., 1: 1.1, 3: 1.3}, {0: 0., 1: 0., 2: 0.})
        np.testing.assert_allclose(z.representative(), [1.3, .2], atol=1e-10)

    def test_causality_same_received_history(self):
        a, b = FiniteMemoryEstimator(Contract(), [0, 0]), FiniteMemoryEstimator(Contract(), [0, 0])
        # Neither API can accept a hidden state or future schedule.
        for k in range(8):
            za, zb = a.observe([(k, 0.)]), b.observe([(k, 0.)])
            np.testing.assert_array_equal(za.representative(), zb.representative())
            a.advance(0.)
            b.advance(0.)
            self.assertLessEqual(len(a.commands), a.contract.span)
            self.assertLessEqual(len(a.packets), a.contract.span+1)


class TubeTests(unittest.TestCase):
    def test_rpi_all_vertices_and_terminal_support(self):
        d = TubeDesign(Contract())
        for signs in product([-1, 1], repeat=3):
            e = d.S@np.array(signs[:2])
            self.assertTrue(d.in_tube(d.F@e+d.B*d.delta*signs[2]))
        for row, bound in zip(d.Hf, d.hf):
            result = linprog(-(row@d.F), A_ub=d.Hf, b_ub=d.hf,
                             bounds=[(None, None)]*2, method='highs')
            self.assertTrue(result.success)
            self.assertLessEqual(-result.fun, bound+1e-9)
        stage = d.Q+d.R*np.outer(d.K, d.K)
        np.testing.assert_allclose(d.F.T@d.P@d.F-d.P, -stage, atol=1e-12)

    def test_shift_feasibility_and_cost_descent(self):
        d, z = TubeDesign(Contract()), np.array([2.5, -.2])
        m = NominalMPC(d)
        for _ in range(20):
            u = m.solve(z)
            nxt = d.A@z+d.B*u[0]
            shift = m.shifted(z, u)
            self.assertLessEqual(m.violation(nxt, shift), 2e-6)
            drop = m.cost(nxt, shift)-m.cost(z, u)+z@d.Q@z+d.R*u[0]**2
            self.assertLessEqual(drop, 1e-7)
            z = nxt

    def test_nominal_reset_and_too_tight_input(self):
        d = TubeDesign(Contract())
        z = np.array([d.z_limit[0], 0.])
        error = np.array([.1, 0.])
        self.assertTrue(d.in_tube(error))
        self.assertLess(z[0]+error[0], d.state_limits[0])
        self.assertGreater(z[0]+error[0], d.z_limit[0])
        with self.assertRaises(ValueError):
            TubeDesign(Contract(), input_limit=2.)


if __name__ == '__main__':
    unittest.main()
