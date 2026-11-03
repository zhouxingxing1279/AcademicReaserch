import unittest
from fractions import Fraction as F
from check_four_state_conditional_smf import (
    load, radius, dyn, box_predict, box_observe, contains, cz_initial,
    cz_predict, cz_observe, cz_witness, cz_support_numeric, pair_floor,
    velocity_floor, certified_return_velocity_bound, run_case, run,
)


class FourStateConditionalSMFTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.c=load()

    def test_frozen_contract(self):
        c=self.c
        self.assertEqual(c['h'],F(1,50))
        self.assertEqual(c['tmin'],F(981,200))
        self.assertEqual(c['tmax'],F(2943,200))
        self.assertEqual(c['widths'],(F(1,50),F(1,10),F(1,200),F(1,100)))

    def test_cz_strip_exact_witness_nonzero_measurement(self):
        c=self.c
        cz=cz_initial(c)
        eps=[F(1,2),-F(1,2),F(1,2),-F(1,2)]
        x=tuple(c['center'][i]+c['widths'][i]*eps[i] for i in range(4))
        for i,nu in ((0,F(1,2)),(2,F(-1,2)),(3,F(1))):
            y=x[i]+c['noise'][i]*nu
            cz=cz_observe(cz,i,y,c['noise'][i]);eps.append(nu)
            self.assertTrue(cz_witness(cz,eps,x))

    def test_propagation_and_conditioning_nonzero_truth(self):
        c=self.c;t=c['tmax'];cz=cz_initial(c)
        eps=[F(1,2),-F(1,2),F(1,2),-F(1,2)]
        x=tuple(c['center'][i]+c['widths'][i]*eps[i] for i in range(4))
        box=(c['center'],c['widths'])
        for i in (0,2,3):
            y=x[i]+c['noise'][i]/2
            cz=cz_observe(cz,i,y,c['noise'][i]);eps.append(F(1,2))
            box=box_observe(box,i,y,c['noise'][i])
        for k in range(5):
            x=dyn(x,t,F(0),c['h'],c['j'])
            x=(x[0],x[1]+c['h']*radius(t)/2,x[2],x[3])
            cz=cz_predict(cz,t,F(0),c);eps.append(F(1,2))
            box=box_predict(box,t,F(0),c)
            for i in (2,3):
                nu=F(1,2) if (k+i)%2 else -F(1,2)
                y=x[i]+c['noise'][i]*nu
                cz=cz_observe(cz,i,y,c['noise'][i]);eps.append(nu)
                box=box_observe(box,i,y,c['noise'][i])
            self.assertTrue(cz_witness(cz,eps,x))
            self.assertTrue(contains(box,x))
        y=x[0]-c['noise'][0]/2
        cz=cz_observe(cz,0,y,c['noise'][0]);eps.append(-F(1,2))
        self.assertTrue(cz_witness(cz,eps,x))

    def test_exact_pair_floor_and_return_bound(self):
        c=self.c;t=c['tmin']
        self.assertEqual(pair_floor(15,t,c),F(211342043,1600000000))
        self.assertEqual(velocity_floor(15,t,c),F(1,10)+15*c['h']*radius(t))
        self.assertGreater(certified_return_velocity_bound(15,t,c),F(0))

    def test_all_six_cases_and_numeric_lp_consistency(self):
        c=self.c
        for n in (5,10,15):
            for t in (c['tmin'],c['tmax']):
                r=run_case(c,t,n)
                self.assertGreaterEqual(F(r['certified_box_position_outer_halfwidth']),pair_floor(n,t,c))
                self.assertGreaterEqual(F(r['certified_box_velocity_outer_halfwidth']),velocity_floor(n,t,c))
                self.assertLessEqual(F(r['certified_post_return_velocity_outer_halfwidth']),F(r['post_return_box_velocity_halfwidth']))
                self.assertLessEqual(r['post_return_numeric_CZ_velocity_upper'],float(F(r['certified_post_return_velocity_outer_halfwidth']))+1e-7)
                self.assertLessEqual(F(r['post_return_box_position_halfwidth']),c['noise'][0])

    def test_information_bottleneck_and_post_return_gain(self):
        c=self.c
        for t in (c['tmin'],c['tmax']):
            r=run_case(c,t,15)
            self.assertGreater(velocity_floor(15,t,c),F(1,4))
            self.assertGreater(F(r['certified_velocity_reduction_fraction']),F(1,3))
            self.assertLess(F(r['certified_box_position_outer_halfwidth']),F(1,2))

    def test_report_scope(self):
        d=run()
        self.assertEqual(d['status'],'PASS')
        self.assertEqual(d['gate_A'],'blocked')
        self.assertEqual(len(d['rows']),6)
        self.assertIn('NUMERIC_LP',d['evidence'])


if __name__=='__main__':unittest.main()
