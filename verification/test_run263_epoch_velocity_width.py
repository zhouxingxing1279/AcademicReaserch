import unittest
from fractions import Fraction as F
from check_run263_epoch_velocity_width import (
    H, T, R, E_P, E_PHI, acceleration_width_per_tick,
    success_cap, legal_futures, final_width, certificate,
)

class TestRun263(unittest.TestCase):
    def test_constants(self):
        self.assertEqual((H,T,R,E_P,E_PHI), (F(1,50),F(981,100),F(3246383,1600000),F(1,50),F(1,200)))
    def test_acceleration_lipschitz_width(self):
        self.assertEqual(acceleration_width_per_tick(), F(3324863,40000000))
    def test_success_caps(self):
        self.assertEqual(success_cap(5), F(41974589,40000000))
        self.assertEqual(success_cap(10), F(68573493,80000000))
        self.assertEqual(success_cap(15), F(13974589,15000000))
    def test_invalid_gap(self):
        with self.assertRaises(ValueError): success_cap(20)
    def test_legal_patterns(self):
        self.assertEqual(set(legal_futures('SMM')), {'SSS','SSM','SMS','SMM'})
        self.assertEqual(len(list(legal_futures('MMS'))), 7)
    def test_forced_success(self):
        for mode in ('SMM','MMS'):
            for pat in legal_futures(mode):
                w, rows = final_width(mode,pat)
                self.assertIsNotNone(w)
                self.assertEqual(rows[-1]['tick'],60)
    def test_mode_caps(self):
        cert = certificate()
        self.assertEqual(F(cert['tick60_mode_max_velocity_width_caps']['SMM']),F(13974589,15000000)+10*F(3324863,40000000))
        self.assertEqual(F(cert['tick60_mode_max_velocity_width_caps']['MMS']),F(75223219,40000000))
    def test_all_branches_bounded(self):
        cert = certificate()
        bound = F(cert['tick60_uniform_velocity_width_cap'])
        self.assertEqual(sum(len(v) for v in cert['branches'].values()), 11)
        self.assertTrue(all(F(item['tick60_velocity_width_cap'])<=bound for mode in cert['branches'].values() for item in mode.values()))
    def test_not_terminal(self):
        cert = certificate()
        self.assertEqual(cert['gate_A'],'blocked')
        self.assertIn('terminal information-state RCI',cert['not_certified'])

if __name__ == '__main__': unittest.main()
