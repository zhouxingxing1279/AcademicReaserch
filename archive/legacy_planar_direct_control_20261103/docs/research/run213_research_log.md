# Run213：历史一致速度收紧恢复第192拍因果 Backup 准入（2026-10-31）

**基线 main：** `36618465d45b5c386520c284eebdf410556bdd58`（Run212）。**唯一问题：** Run212 排除了第192拍的虚假速度下端，但这一严格收紧是否足以在**同一信息、同一控制准入算法**下恢复合法力矩？并且恢复后能继续运行几拍？

## 1. 可计算控制链路与因果性

冻结四状态 Euler 模型、硬约束、15-mode位置返包时序、当前可见推力与Run210原反馈不变。精确重放 `positive_high` 的前191拍。只用150/165/180三个已到达的位置包与150..190已到达的姿态观测，按Run212的 `measurement_support` 构造速度严格外包 `I_hist`，在第192拍控制**之前**执行：

```python
B_refined = (B[0], intersect(B[1], I_hist), B[2], B[3])
u192 = project(proposed(B_refined) - omega_mid(B_refined)/5,
               Run208_two_stage(B_refined, T_visible) ∩ Run210_guard(B_refined, 8))
```

由于完整历史一致真实状态属于 `B` 且满足 `I_hist`，故 `B_refined` 仍为可靠的当前外包；其后运行原Run208/210认证器无需修改。**仅保留一维速度收紧，尚未构造联合CZ或完整历史可行集。**

## 2. 精确结果：严格恢复局部控制准入

| 192拍控制前 | 原独立区间盒 | 历史一致速度交集 |
|---|---:|---:|
| 速度下界 (m/s) | -2.4931037251954926 | **-2.419767402278826** |
| 速度上界 (m/s) | -0.5718721710288258 | -0.5718721710288258 |
| 8拍姿态必要guard | [-0.08,0.08] N·m | [-0.08,0.08] N·m |
| 两层因果backup | **空** | **[-0.08,0.08] N·m** |
| 综合控制准入 | 拒绝 | **准入** |

速度下界严格改善 `7040287/96000000 m/s`。同一控制反馈选出 `u192≈-0.0020447389406053726 N·m`，位于经精确分数审计的准入区间。对首拍力矩端点 `{-0.08,0,0.08}` 与下一拍推力 `{Tmin,(Tmin+Tmax)/2,Tmax}` 的9种组合，独立四拍backup审计均可行且允许零力矩。对连续未来推力区间的覆盖仍依赖原Run208多仿射端点论证，不把9点抽样当成完整证明。

**结论级别：** 给定这一真实可达、测量一致的后验外包，原Run208两层因果策略的有限时域证书恢复非空。不是终端不变性、无限时域安全或递归可行性。

## 3. 同策略滚动闭环与负面结果

以完全相同的前191拍轨迹、后续推力/扰动/测量序列和控制公式做反事实对照。只在第192拍前插入历史速度区间交集，其后仍采用原区间SMF传播、返包速度收紧和原Run210控制器。

| 220拍预算 | 不插入历史界 | 第192拍插入历史界 |
|---|---:|---:|
| 成功准入拍数 | 191 | **192** |
| 首次拒绝 | 第192拍 | **第193拍** |
| 已执行状态包含检查 | 通过 | 通过 |
| 已执行状态硬约束违约 | 0 | 0 |

因此，估计相关性改善**确实转化为一次实际控制准入**，但第193拍再次拒绝；只在一个时刻做一维收紧不足以解决长期安全问题。数值轨迹是指定合法历史，不是所有可能噪声/扰动历史的统计结论。拒绝是控制器fail-closed，不表示真实状态必然不可生存。

## 4. 复现与测试

- 源码：`verification/check_history_tightened_backup.py`；测试：`verification/test_history_tightened_backup.py`；结果：`results/history_tightened_backup_20261031/checks.json`。
- Python 3.13.5，Linux 6.18.57 x86_64；`fractions.Fraction` 用于动力学、后验交集与安全判定，`perf_counter` 只用于耗时。
- 运行指令：`PYTHONPATH=verification python -m unittest -v verification.test_history_tightened_backup`、`python -m py_compile verification/check_history_tightened_backup.py verification/test_history_tightened_backup.py`、`PYTHONPATH=verification python verification/check_history_tightened_backup.py --output /tmp/run213_checks.json`。
- **5/5测试通过**：精确收紧、旧拒绝/新准入、真值包含与当前硬约束、9个独立后继backup检查、同策略第193拍拒绝。
- 本地使用与远端Run206/208/210/211/212关键函数逐式对照的轻量镜像（不是完整仓库checkout）。新增两份Python源码的Git Blob SHA与本地实测文件相同；**未运行完整仓库回归或GitHub CI**。本地一次准入审计约0.013s，仅为该机器和该样例墙钟耗时，不是最坏运行时间保证。
- 所有负面结果和局限保留，未将有限步现象表述为递归可行证明。

## 5. 文献复核（去重87篇不变）

1. Scott、Raimondo、Marseglia、Braatz（2016），*Constrained zonotopes: A new tool for set-based estimation and fault detection*，*Automatica* 69:126–136，DOI https://doi.org/10.1016/j.automatica.2016.02.036；本轮核对原文摘要和已有Run212 Definition 3、Proposition 1、Section 5阅读笔记。其精确集合交运算说明下一步保留历史相关性在理论上可行，但Run213并非CZ实现。
2. Köhler、Müller、Allgöwer（2021），*Robust output feedback model predictive control using online estimation bounds*，arXiv:2105.03427，https://arxiv.org/abs/2105.03427；本轮核对arXiv摘要和已有Run211 Assumption 7、Theorem 4笔记。其鲁棒输出反馈MPC的递归可行性还需要终端条件，本轮并未满足。

没有把摘要核验冒充全文重读，也没有新增去重文献。

## 6. 课题收敛与下一轮唯一优先任务

**Gate A=blocked。** 可行性：历史一致SMF收紧对控制准入的价值已有精确单点见证。创新性：三包消元与集合交本身不是新理论；可能的硕士贡献是**因果历史一致SMF—鲁棒有限时域安全过滤器**的控制相关保守性与复杂度分析。难度：从一次恢复到长期可行需要持续更新相关集合并寻找有效终端策略；六状态四旋翼与完整Tube MPC仍缺失。

**下一轮唯一优先任务：** 解释第193拍再次拒绝的具体约束/假角点，设计一个不泄露未来测量的**滚动历史相关性保持**估计（优先小窗口CZ或等价线性历史约束），在同一控制器和计算预算下检验是否能持续扩大准入域；不能仅重复第192拍的一次性修补。
