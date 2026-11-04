# 活动测试

旧单元测试和形式化算术检查已移入 archive/legacy_planar_direct_control_20261103/tests 与 verification，不计入当前外环研究通过项。

运行 `python -m unittest discover -s tests -v` 检查 [startup_gate](test_startup_gate.py) 的CZ支持、退化/空集、非中心信息、因果量词、输入饱和和离散模型边界；运行 `python -m experiments.cz_startup_predecessor --check` 逐字复核登记的数学证书。两条命令均进入CI。当前未建立在线延迟CZ/SMF、Tube MPC或SITL闭环测试。
