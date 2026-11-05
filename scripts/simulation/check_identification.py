import unittest
import numpy as np
from identify_acceleration import schedule
from audit_cz_interface import minimum_acceleration
from analyze_acceleration import rollout, command_moments, replay


class IdentificationChecks(unittest.TestCase):
    def test_replay_distinguishes_empty_posterior_from_noncontainment(self):
        t = np.arange(376)*.004
        p, v = np.zeros((len(t),3)), np.zeros((len(t),3))
        p[:,0], v[:,0] = .5*t*t, t
        b = dict(index=0,start=0.,end=1.5,times=t,p=p,v=v,
                 cmd_times=np.array([0.]),commands=np.zeros((1,3)))
        result = replay([b])[0]['first_failure_by_axis'][0]
        self.assertEqual(result['first_containment_failure'],1)
        self.assertEqual(result['first_empty_posterior'],2)

    def test_lag_rollout_matches_continuous_step_solution(self):
        tau, t, u = .2, 1., .4
        out = rollout(np.full(250,u), .004, tau)
        v = u*(t-tau*(1-np.exp(-t/tau)))
        p = u*(.5*t*t-tau*t+tau*tau*(1-np.exp(-t/tau)))
        np.testing.assert_allclose(out[-1], [p,v], atol=1e-12)
        np.testing.assert_allclose(rollout(np.full(250,u), .004, 0.)[-1], [.2,.4], atol=1e-12)

    def test_switched_input_position_moment_is_not_mean_input(self):
        b = dict(cmd_times=np.array([0.,.5]),commands=np.array([[1.,0.,0.],[-1.,0.,0.]]))
        dp,dv = command_moments(b,0.,1.,0)
        self.assertEqual(dv,0.)
        self.assertEqual(dp,.25)

    def test_excitation_balanced_without_input_clipping(self):
        for split in ['calibration', 'validation']:
            for block in schedule(split):
                p, v = np.zeros(3), np.zeros(3)
                for phase in block['phases']:
                    u, dt = np.array(phase['u']), phase['duration']
                    self.assertLessEqual(np.max(abs(u)), .4)
                    p += v*dt+.5*u*dt**2
                    v += u*dt
                np.testing.assert_allclose(p, 0., atol=1e-15)
                np.testing.assert_allclose(v, 0., atol=1e-15)

    def test_split_separation(self):
        cal, val = schedule('calibration'), schedule('validation')
        self.assertEqual(len(cal), 6)
        self.assertEqual(len(val), 3)
        self.assertEqual({b['axis'] for b in val}, {0,1,2})
        for axis in range(3):
            self.assertEqual({b['sign'] for b in cal if b['axis']==axis}, {-1,1})

    def test_replay_requires_disturbance_for_inconsistent_measurement(self):
        rows = [dict(sim_time=0., input=[0.,0.,0.], arrivals=[(0,[0.,0.,0.])]),
                dict(sim_time=.5, arrivals=[(1,[.1,0.,0.])])]
        self.assertAlmostEqual(minimum_acceleration(rows, 0, [0.,0.], False), .68, places=7)
        self.assertEqual(minimum_acceleration(rows, 1, [0.,0.], False), 0.)

    def test_replay_uses_measurement_timestamp_for_delayed_packet(self):
        rows = [dict(sim_time=0., input=[0.,0.,0.], arrivals=[]),
                dict(sim_time=.5, input=[0.,0.,0.], arrivals=[]),
                dict(sim_time=1., arrivals=[(1,[.1,0.,0.])])]
        self.assertAlmostEqual(minimum_acceleration(rows, 0, [0.,0.], False), .68, places=7)


if __name__ == '__main__':
    unittest.main()
