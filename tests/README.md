# 活动测试

旧单元测试和形式化算术检查已移入 archive/legacy_planar_direct_control_20261103/tests 与 verification，不计入当前外环研究通过项。

先安装根目录requirements-research.txt，再使用虚拟环境运行 `python -m unittest discover -s tests -v`。现有17项startup_gate测试加11项[test_finite_memory_tube](test_finite_memory_tube.py)，共28项。分别运行 `python -m experiments.cz_startup_predecessor --check` 和 `python -m experiments.finite_memory_certificate --check` 复核两个数学证书。新增闭环用 `python -m experiments.finite_memory_tube`；没有SITL或物理飞行测试。详见[验证记录](../docs/research/proposal/VALIDATION.md)。

抗扰更新：另增4项[test_robustness](test_robustness.py)，活动测试总计32项；覆盖精确预算边界交叉核验、成对外生刺激、恢复时间定义和失败停止。`python -m experiments.robustness`运行抗扰扫描，`python -m experiments.validate_robustness`重放，`python -m experiments.report_robustness`生成[结果报告](../docs/research/proposal/ROBUSTNESS_RESULTS.md)。

SITL初测另见[Gazebo结果](../docs/simulation/CZ_SITL_RESULTS.md)：4次正式接入均未通过，未计入上述数学测试成功项。WSL专用`scripts/simulation/check_cz_adapter.py`有4项接入检查，运行时不会启动模拟器。
