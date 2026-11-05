"""WSL-only interface checks; no simulator or vehicle is started."""
import json
from types import SimpleNamespace
import unittest
import numpy as np
from cz_sitl import Trial, GazeboReference, Odometry
from src.outerloop.finite_memory import Contract, FiniteMemoryEstimator
from gz.msgs10.pose_v_pb2 import Pose_V


class AdapterTests(unittest.TestCase):
    def test_scene_pose_uses_only_x500_model(self):
        reference = GazeboReference()
        for sec, x in [(1, 0.), (2, 2.)]:
            poses = Pose_V()
            poses.header.stamp.sec = sec
            irrelevant = poses.pose.add()
            irrelevant.name = 'rotor_0'
            irrelevant.position.x = 999.
            model = poses.pose.add()
            model.name = 'x500_0'
            model.position.x = x
            reference.update_scene(poses)
        np.testing.assert_allclose(reference.get()[1], [0., 2., 0.])
        np.testing.assert_allclose(reference.get()[2], [0., 2., 0.])

    def test_world_position_difference_transforms_enu_to_ned(self):
        ref = GazeboReference()
        for ns, xyz in [(0, (2., 3., 4.)), (20_000_000, (2.1, 3.2, 4.1))]:
            msg = Odometry()
            msg.header.stamp.sec = 1
            msg.header.stamp.nsec = ns
            msg.pose.position.x, msg.pose.position.y, msg.pose.position.z = xyz
            ref.update(msg)
        t, p, v, dt = ref.get()
        np.testing.assert_allclose(p, [3.2, 2.1, -4.1])
        np.testing.assert_allclose(v, [10., 5., -5.])
        self.assertAlmostEqual(dt, .02)

    def test_acceleration_only_mask_and_values(self):
        trial = object.__new__(Trial)
        sent = []
        trial.link = SimpleNamespace(mav=SimpleNamespace(set_position_target_local_ned_send=lambda *args: sent.append(args)))
        trial.latest_boot_ms = 100
        trial.position_sp = None
        trial.acceleration_sp = np.array([.2, -.3, .4])
        trial.setpoint()
        self.assertEqual(sent[0][4], 2111)
        self.assertEqual(sent[0][4] & 512, 0)  # acceleration, not FORCE mode
        np.testing.assert_allclose(sent[0][11:14], [.2, -.3, .4])
        trial.acceleration_sp, trial.position_sp = None, np.array([1., 2., -3.])
        trial.setpoint()
        self.assertEqual(sent[1][4], 2552)
        np.testing.assert_allclose(sent[1][5:8], [1., 2., -3.])

    def test_containment_log_is_native_json_boolean(self):
        post = FiniteMemoryEstimator(Contract(), [0., 0.]).observe([])
        contained = bool(post.contains(np.array([0., 0.])))
        self.assertIs(type(contained), bool)
        self.assertEqual(json.loads(json.dumps({'contained': [contained]})), {'contained': [True]})


if __name__ == '__main__':
    unittest.main()
