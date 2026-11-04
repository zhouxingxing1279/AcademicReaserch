"""Exact boundary tests for the information-set common command gate."""
from fractions import Fraction as F
from itertools import product
import unittest
try:
    from src.outerloop import startup_gate as g
except ModuleNotFoundError:
    g = None


def diag(values):
    return tuple(tuple(v if i == j else F(0) for j in range(len(values))) for i,v in enumerate(values))


def model(t=F(1), zoh=True):
    a=tuple(tuple(F(i==j)+(t if i<3 and j==i+3 else 0) for j in range(6)) for i in range(6))
    b=tuple(tuple((t*t/2 if i<3 and zoh else t if i>=3 else 0) if j==i%3 else F(0) for j in range(3)) for i in range(6))
    return a,b,b


def box_rows(radii):
    rows=[]; bounds=[]
    for i,r in enumerate(radii):
        for s in (1,-1):
            rows.append(tuple(F(s if j==i else 0) for j in range(len(radii))))
            bounds.append(r)
    return tuple(rows),tuple(bounds)


class StartupGateTests(unittest.TestCase):
    def setUp(self):
        self.assertIsNotNone(g, 'The exact startup gate implementation is missing')

    def box(self,radii,center=None):
        return g.CZ(center or (F(0),)*len(radii),diag(radii))

    def gate(self,info,noise=F(1,10),p=F(1),v=F(2),u=F(1),t=F(1),zoh=True,**kw):
        a,b,d=model(t,zoh)
        h,lim=box_rows((p,)*3+(v,)*3)
        return g.startup_gate(a,b,d,info,self.box((noise,)*3),h,lim,(u,)*3,**kw)

    def test_box_support_and_vertices(self):
        z=self.box((F(1),F(2)),(F(3),F(-1)))
        self.assertEqual(len(z.vertices()),4)
        self.assertEqual(z.support((1,-2)),10)

    def test_scott_equation_10_noncentral_triangle(self):
        z=g.CZ((0,0),((F(3,2),F(-3,2),F(1,2)),(1,F(1,2),-1)),((1,1,1),),(-1,))
        self.assertEqual(set(z.vertices()),{(F(1,2),F(-5,2)),(F(-7,2),F(1,2)),(F(5,2),F(3,2))})
        self.assertEqual(z.support((1,0)),F(5,2))

    def test_nonzero_rhs_center_not_member(self):
        z=g.CZ((0,0),diag((F(1),F(1))),((1,1),),(F(1),))
        self.assertEqual(set(z.vertices()),{(F(0),F(1)),(F(1),F(0))})
        self.assertEqual(z.support((-1,-1)),-1)

    def test_redundant_constraints(self):
        z=g.CZ((0,0),diag((F(1),F(1))),((1,1),(2,2),(0,0)),(0,0,0))
        self.assertEqual(set(z.vertices()),{(F(1),F(-1)),(F(-1),F(1))})

    def test_inconsistent_information_is_not_feasible(self):
        z=g.CZ((0,0),diag((F(1),F(1))),((1,1),),(3,))
        with self.assertRaises(g.EmptyInformation): z.support((1,0))
        z=g.CZ((0,),((1,),),((1,),(1,)),(0,1))
        self.assertEqual(z.vertices(),())

    def test_point_cz_and_zero_generator(self):
        z=g.CZ((F(2),),((),))
        self.assertEqual(z.vertices(),((F(2),),))
        self.assertEqual(z.support((F(-1),)),F(-2))

    def test_budget_exhaustion_is_not_infeasibility(self):
        with self.assertRaises(g.BudgetExceeded):
            self.box((F(1),)*6).vertices(max_bases=1)

    def test_float_and_bad_dimensions_rejected(self):
        with self.assertRaises(TypeError): g.CZ((0.1,),((1,),))
        with self.assertRaises(ValueError): g.CZ((0,0),((1,),))
        with self.assertRaises(ValueError): g.CZ((0,),((1,),),((1,1),),(0,))

    def test_correlations_avoid_false_infeasibility(self):
        eq=tuple(tuple(F(j==i or j==i+3) for j in range(6)) for i in range(3))
        z=g.CZ((0,)*6,diag((F(1),)*6),eq,(0,)*3)
        exact=self.gate(z)
        outer=self.gate(self.box((F(1),)*6))
        self.assertEqual(exact.status,'feasible')
        self.assertEqual(exact.command,(F(0),)*3)
        self.assertEqual(outer.status,'infeasible')
        self.assertEqual(exact.state_supports[0],0)
        self.assertEqual(outer.state_supports[0],2)

    def test_common_command_causality_gap(self):
        z=self.box((F(0),)*3+(F(1),)*3)
        self.assertEqual(self.gate(z,noise=F(1,4),p=F(2),v=F(1)).status,'infeasible')
        for velocity in product((-1,1),repeat=3):
            for noise in product((F(-1,4),F(1,4)),repeat=3):
                # Forbidden statewise policy, included only as a counterexample.
                command=tuple(-q for q in velocity)
                self.assertTrue(all(abs(q+u+w)<=1 for q,u,w in zip(velocity,command,noise)))

    def test_translated_information_requires_common_nonzero_command(self):
        z=self.box((F(0),)*6,(F(0),)*3+(F(1),)*3)
        out=self.gate(z,noise=F(1,4),p=F(2),v=F(1),u=F(1,4))
        self.assertEqual(out.status,'feasible')
        self.assertEqual(out.command,(F(-1,4),)*3)
        self.assertEqual(self.gate(z,noise=F(1,4),p=F(2),v=F(1),u=F(1,5)).status,'infeasible')

    def test_initial_unsafety_is_separate(self):
        z=self.box((F(2),)*3+(F(0),)*3)
        self.assertEqual(self.gate(z).status,'initial_unsafe')

    def test_euler_and_zoh_must_not_be_mixed(self):
        z=self.box((F(0),)*6)
        self.assertEqual(self.gate(z,noise=F(1),p=F(1,4),zoh=False).status,'feasible')
        self.assertEqual(self.gate(z,noise=F(1),p=F(1,4),zoh=True).status,'infeasible')

    def test_input_coupling_and_lower_dimensional_feasible_set(self):
        z=self.box((F(0),)*6,(F(0),)*3+(F(1),)*3)
        out=self.gate(z,noise=F(1,4),p=F(2),v=F(1),u=F(1,4),
            extra_input_rows=((-1,-1,-1),),extra_input_limits=(F(7,10),))
        self.assertEqual(out.status,'infeasible')

    def test_three_axis_regression_entrypoint(self):
        import importlib.util
        spec=importlib.util.find_spec('experiments.cz_startup_predecessor')
        self.assertIsNotNone(spec,'Reproducible experiment entrypoint is missing')
        from experiments.cz_startup_predecessor import run_suite
        records, timings=run_suite(full_grid=False)
        self.assertEqual(len(records),10)
        self.assertEqual(len(timings),len(records))
        intervals={r['id']:r.get('axis_interval') for r in records if r['id'].startswith('pr210')}
        self.assertEqual(intervals,{'pr210_v_1_10':['-2','2'], 'pr210_v_2_5':['-3/2','3/2'], 'pr210_v_1':None})

    def test_cross_axis_state_and_correlated_disturbance(self):
        info=g.CZ((0,)*6,diag((F(1),F(1),F(0),F(0),F(0),F(0))),
                  ((1,1,0,0,0,0),),(0,))
        noise=g.CZ((0,)*3,diag((F(1,10),)*3),((1,1,0),),(0,))
        a,b,d=model()
        rows,limits=box_rows((F(2),)*6)
        rows+=((F(1),F(1),0,0,0,0),(F(-1),F(-1),0,0,0,0))
        limits+=(F(0),F(0))
        out=g.startup_gate(a,b,d,info,noise,rows,limits,(1,)*3)
        self.assertEqual(out.status,'feasible')
        self.assertEqual(out.command,(F(0),)*3)
        independent=self.box((F(1,10),)*3)
        self.assertEqual(g.startup_gate(a,b,d,info,independent,rows,limits,(1,)*3).status,'infeasible')

    def test_command_budget_exhaustion_is_unresolved(self):
        info=g.CZ((0,0,0,1,1,1),((),)*6)
        noise=g.CZ((F(1,4),)*3,((),)*3)
        a,b,d=model()
        rows,limits=box_rows((F(2),)*3+(F(1),)*3)
        with self.assertRaises(g.BudgetExceeded):
            g.startup_gate(a,b,d,info,noise,rows,limits,(1,)*3,max_bases=1)


if __name__=='__main__': unittest.main()
