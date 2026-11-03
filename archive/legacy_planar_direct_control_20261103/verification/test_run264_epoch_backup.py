import unittest
from fractions import Fraction as F
from check_run264_epoch_backup import H,J,T,R,START,LIMIT,sin_bounds,step,safe,certificate

class TestRun264(unittest.TestCase):
    def test_frozen_constants(self):
        self.assertEqual((H,J,T,R),(F(1,50),F(1,50),F(981,100),F(3246383,1600000)))
    def test_taylor_outward(self):
        self.assertEqual(sin_bounds(F(0)),(F(0),F(0)))
        self.assertEqual(sin_bounds(-F(1,125))[0],-sin_bounds(F(1,125))[1])
    def test_modes(self):
        self.assertEqual(set(START),{'SMM','MMS'})
    def test_one_step_euler(self):
        s={k:tuple(F(x) for x in v) for k,v in START['SMM'].items()}
        nxt=step(s)
        self.assertLessEqual(nxt['p'][0],s['p'][0]+H*s['v'][0])
        self.assertGreaterEqual(nxt['p'][1],s['p'][1]+H*s['v'][1])
        self.assertEqual(nxt['omega'],s['omega'])
    def test_safe_all_rows(self):
        for mode in START:
            s={k:tuple(F(x) for x in v) for k,v in START[mode].items()}
            for _ in range(16):
                self.assertTrue(safe(s))
                s=step(s)
    def test_certificate_branches(self):
        c=certificate()
        self.assertEqual((c['start_tick'],c['last_certified_tick']),(60,75))
        self.assertEqual(set(c['branches']),{'SMM','MMS'})
    def test_positive_margins(self):
        for b in certificate()['branches'].values():
            self.assertTrue(all(F(x)>0 for x in b['min_hard_constraint_margin_60_to_75'].values()))
    def test_conservative_not_terminal(self):
        c=certificate()
        self.assertEqual(c['gate_A'],'blocked')
        self.assertIn('terminal information-state RCI',c['not_certified'])
    def test_monotone_interval_growth(self):
        for mode in START:
            s={k:tuple(F(x) for x in v) for k,v in START[mode].items()}
            for _ in range(15):
                n=step(s)
                self.assertGreaterEqual(n['v'][1]-n['v'][0],s['v'][1]-s['v'][0])
                s=n

if __name__=='__main__':unittest.main()
