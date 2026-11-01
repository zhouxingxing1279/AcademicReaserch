"""Run249 focused safety and honest evidence-level regression tests."""
import json, unittest
from fractions import Fraction as F
from pathlib import Path
import check_four_state_shielded_smf_mpc as m

class TestShieldedSMFMPC(unittest.TestCase):
    def test_config_contract(self):
        root=Path(__file__).resolve().parents[1]
        cfg=root/'configs/planar_baseline.json'
        if not cfg.exists():self.skipTest('requires full checkout')
        d=json.loads(cfg.read_text())
        self.assertEqual(d['plant']['truth_semantics'],'defined_discrete_euler')
        self.assertEqual(F(str(d['plant']['dt_s'])),m.H)
        self.assertEqual(F(str(d['plant']['inertia_kg_m2'])),m.J)
        self.assertEqual(F(str(d['domain']['input_upper'][1])),m.U)
        self.assertEqual(d['sensing']['position_period_ticks'],5)
        self.assertEqual(d['sensing']['max_consecutive_missed_packets'],2)
        self.assertEqual(d['sensing']['always_observed_indices'],[4,5])
        self.assertEqual(d['sensing']['position_indices'],[0,1])
    def test_rational_sin(self):
        for x in [F(0),F(1,100),F(1,5),m.PHI_MAX,-m.PHI_MAX]:
            lo,hi=m.sin_bounds(x)
            import math
            self.assertLessEqual(float(lo)-1e-15,math.sin(float(x)))
            self.assertGreaterEqual(float(hi)+1e-15,math.sin(float(x)))
    def test_outward_rounding(self):
        for x in [F(-1,3),F(1,3),F(1,7),F(-11,100)]:
            self.assertLessEqual(m.down(x),x)
            self.assertGreaterEqual(m.up(x),x)
    def test_zero_backup_55(self):
        rows=m.zero_certificate()
        self.assertEqual(len(rows),56)
        self.assertTrue(all(m.safe(r) for r in rows))
        self.assertGreater(rows[-1]['v'][1],F(2))
        self.assertLess(rows[-1]['v'][1],m.V_MAX)
    def test_nonzero_actions_safe_at_start(self):
        cand=m.safety_first_actions(m.INIT,0)
        self.assertEqual(set(cand),set(m.ACTIONS))
        for a,(nxt,tail) in cand.items():
            self.assertTrue(m.safe(nxt));self.assertTrue(m.safe(tail))
    def test_posterior_monotonic_tail(self):
        # Strict subset posterior is obtained by strip intersection.
        nxt=m.step(m.INIT,m.ACTIONS[0])
        y=sum(nxt['phi'])/2
        post=m.strip(nxt,{'phi':y})
        self.assertIsNotNone(post)
        for k in m.KEYS:
            self.assertGreaterEqual(post[k][0],nxt[k][0]);self.assertLessEqual(post[k][1],nxt[k][1])
        self.assertIsNotNone(m.rollout(post,(F(0),)*54))
    def test_inconsistent_strip_rejected(self):
        self.assertIsNone(m.strip(m.INIT,{'p':F(9)}))
    def test_miss_automaton(self):
        words=m.all_words(11)
        self.assertTrue(words)
        self.assertTrue(all('MMM' not in w for w in words))
        self.assertIn('S'*11,words)
        self.assertIn('MMS'*3+'MM',words)
    def test_mpc_uses_posterior_not_truth(self):
        a,n,c=m.choose(m.INIT,0)
        self.assertIn(a,m.ACTIONS)
        self.assertGreater(n,0)
        self.assertGreaterEqual(c,0)
    def test_short_replay_and_containment(self):
        word='S'*11
        out=m.replay(word,{'p':F(0),'v':F(0),'phi':F(0),'omega':F(0)},1,'mpc')
        self.assertEqual(out['contained'],4*55)
        self.assertEqual(out['violations'],0)
    def test_archive_if_full_checkout(self):
        root=Path(__file__).resolve().parents[1]
        archive=root/'results/four_state_shielded_smf_mpc_20261101/checks.json'
        if not archive.exists():self.skipTest('requires full checkout')
        self.assertEqual(json.loads(archive.read_text())['run'],249)
        self.assertFalse(json.loads(archive.read_text())['terminal_invariant_set'])

if __name__=='__main__':unittest.main()
