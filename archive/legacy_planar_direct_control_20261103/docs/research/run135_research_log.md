# Run 135：time-uniform estimator-error 多集的构造与证书类否证

日期：2026-09-29。文献准入见 [run135_literature_gate.md](run135_literature_gate.md)，完整推导见 [第 72 章](../learning/72_time_uniform_estimator_multiset.md)。本轮从本地 Run 134 提交 `e666490` 继续；远端 `main` 为 `1c49659`，远端最新研究分支仍为 Run 126 `c00d102`。

## 1. 本轮问题

Run 134 要求先给 15-mode bounded-dropout observer 一个 time-uniform、mode-indexed `E_eta^j`，再进入实际推力相关的 ancillary RCI。本轮先复核第 06--07 章：已经存在逐边 actual-input 误差 inclusion、共同收缩度量和有限时域半径传播；真正未闭合的是无限时域/任意滚动窗口。

## 2. 文献与准入

精读 Athanasopoulos--Smpoukis--Jungers 2017 的 invariant multi-set 定义、逐边等价条件、minimal/maximal multi-set 和有限外逼近；重读 Hassaan--Pati--Shen--Yong 2021 的 finite missing-data language、equalized recovery 和 time-varying estimator tubes。结论是：图不变多集已有直接理论，且 time-uniform invariance 比 intermittent-data MPC 的 finite/periodic tube 更强。因此本轮只准入基线构造和反例，不准入创新声明。

## 3. 核心结果与证据等级

定义 `T(r)_b=max_(a->b)(sqrt(19/20) r_a+sqrt(q_ab))`。该映射在无穷范数下为 contraction，唯一固定点给出 scalar/common-metric 类的最小模式半径；其 15 个椭球逐边不变。

- **条件性解析证明：**对冻结线性 inclusion，固定点存在、唯一且为最小 supersolution；对应模式椭球逐边包含。
- **精确算术核查：**平方根与迭代均用 `10^-12` 有向舍入，17/17 边的上界包含通过；结果文件保存源码 SHA-256。
- **严格反例：**半径下界约为 7.015--7.365；每一模式的速度支持下界均大于 3 m/s，角度支持下界均大于 0.45 rad，故任何中心下的原硬状态 tightening 都为空。
- **未证明：**冻结集合跨出 residual 有效域，不能升级为全局非线性真值包含；未构造 geometry-preserving 无限时域多集、ancillary RCI、terminal 或 recursive feasibility。

## 4. 实现与验证

新增 `check_mode_invariant_radius.py` 和三项测试：手算自环固定点、双模态逐边不变性、无前驱模式拒绝。测试按 red-green 执行；随后在真实 15 模态/17 边上生成 `results/theory_mode_invariant_radius_20260929/exact_checks.json`。

主要命令：

```bash
PYTHONPATH=verification python -m unittest verification/test_mode_invariant_radius.py -v
PYTHONPATH=verification python verification/check_mode_invariant_radius.py --output /tmp/mode_invariant_radius.json
ACADEMIC_RESEARCH_NO_WRITE=1 python -m unittest discover -s verification -p 'test_*.py' -q
git diff --check
```

最终完整回归为 `118/118` 通过，耗时 `82.438 s`；定向 verifier 复算与归档 JSON 逐字一致，`git diff --check` 通过。测试通过只支持实现一致性；一般固定点与不变性证明在第 72 章。

## 5. 失败尝试、止损与主线判断

没有继续调 `P_j`、噪声系数或 horizon 来掩盖失败。C2-R 已显示 geometry-preserving 25-step 集合远小于共同椭球；本轮 time-uniform 固定点又严格说明把全部噪声压成一个 scalar energy 的稳态代价。因此停止 scalar/common-metric 椭球支线。

论文主线尚未达到硕士课题闭环：估计真值包含仍缺无限时域、固定复杂度且 domain-valid 的几何多集；其后还有 joint ancillary RCI、输入分配、terminal/shift、同预算强基线和四旋翼闭环。当前成果是正确的证据链纠偏，不是独立创新。

## 6. 下一唯一问题

在相同 15 模态、actual-input timing 与 residual domain 下，用 forward reachable sums 加 certified tail 构造 geometry-preserving 外不变多集，并判定全部状态坐标支持能否闭合在物理域；失败时给出最早严格阻断方向。通过后才恢复第 71 章联合 ancillary RCI。
