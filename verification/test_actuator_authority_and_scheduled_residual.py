import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from check_actuator_authority_and_scheduled_residual import (
    T_LOW,
    T_HIGH,
    TAU_LIMIT,
    residual_halfwidth,
    solve_peak_torque,
)


class ActuatorAuthorityTests(unittest.TestCase):
    def test_residual_conditioning_is_strict_at_low_thrust(self):
        self.assertLess(residual_halfwidth(T_LOW), residual_halfwidth(T_HIGH))

    def test_global_boundary_pair(self):
        d = residual_halfwidth(T_HIGH)
        self.assertGreater(
            solve_peak_torque(T_LOW, 380, d)["peak_torque_optimum"], TAU_LIMIT
        )
        self.assertLessEqual(
            solve_peak_torque(T_LOW, 381, d)["peak_torque_optimum"], TAU_LIMIT
        )

    def test_scheduled_boundary_pair(self):
        d = residual_halfwidth(T_LOW)
        self.assertGreater(
            solve_peak_torque(T_LOW, 159, d)["peak_torque_optimum"], TAU_LIMIT
        )
        self.assertLessEqual(
            solve_peak_torque(T_LOW, 160, d)["peak_torque_optimum"], TAU_LIMIT
        )


if __name__ == "__main__":
    unittest.main()
