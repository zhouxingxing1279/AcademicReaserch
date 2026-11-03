# Run 138：冻结 boundary-tight ancillary allocation existence probe

日期：2026-10-02。文献准入见 [run138_literature_gate.md](run138_literature_gate.md)，推导见 [第 75 章](../learning/75_ancillary_input_allocation_probe.md)。仓库起点为本地 Run 137 `e3ae26d`；`git fetch` 后远端最新成果为 Run 137 `310a2a0`，两者 tree SHA 均为 `ee0fd078bb3555312fb7c10e20e9586a772dc00e`；远端 `main` 仍为 `1c49659`。

## 仓库与文献复核

启动时只读 `current_checkpoint.md`、Run 137、配置、第 71/73/74 章和对应验证器。Run 136 estimator zonotope 与 Run 137 necessary thrust interval 均有可执行 exact checker；配置确实没有独立 nominal/correction bounds，`K`、`L_by_mode`、terminal certificate 仍为空。

本轮重读 Lorenzetti--Pavone 的 nominal/control law、coupled error、input tightening 与 robust constraint proof；并从 arXiv 源码重读 Köhler等的 homothetic tube、simplified tightening、terminal assumptions 与 shift proofs。两者均把 input tightening 绑定到反馈和误差管，不支持把任意静态切分作为最终方法。

## 精确预算结果

对 actual thrust `[4.905,14.715]` 和 `d_z(T)=2.086+0.10125T`，取 correction radius `d_z(14.715)=3.57589375`。在 hover 对称、固定对称 correction 且使用完整 actual box 的证书类中，最大 nominal thrust interval 为 `[8.48089375,11.13910625]`。其与 correction interval 的 Minkowski 和精确恢复 actual thrust interval。

两侧 vertical boundary balance 方程均有精确解；上侧 correction 必须达到 `3.57589375`，因此 authority margin 为零。力矩因缺少已认证 correction support，首个最有利 existence probe 取 nominal `{0}`、correction `[-0.08,0.08]`。这让 ancillary 获得全部力矩，但 nominal 域无内点，不能作为机动 MPC 或 terminal controller 的最终输入域。

证据等级：Minkowski input contract 与边界等式为精确有理数结果；“最大”只对已声明的对称固定预算类成立；因果反馈、增广 RCI、状态/余项域闭合、terminal 与递归可行性仍未证明。

## TDD 与停止理由

未修改基线为 122/122 通过。RED 阶段新增三项测试并更新 Run 137 配置断言，4 项因 checker/fields 缺失按预期失败；GREEN 阶段加入配置和 exact verifier 后定向 5/5 通过。

第一次完整回归为 **125/125 通过**，unittest 报告耗时 `80.640 s`（shell wall time `81.077 s`）。归档 Run 137 nominal-reserve JSON 已按新配置重算；Run 138 exact JSON 保存输入盒、边界平衡、零余量结论和最终源码哈希。

本轮不启动 augmented RCI solver：准入卡的反例条件已表明该静态 split 不是最终 nominal allocation。此时先把 existence probe 固定并显式标注，比在未知 input semantics 下报告 solver success/infeasible 更可审查。下一轮 RCI 若存在，必须输出真实 correction support 以恢复严格内点 nominal input set；若不存在，才讨论 residual/actuator/model 合同。

## 下一唯一问题

在本轮最有利预算下，保留 Run 136 共享 residual/measurement 生成元以及 `T=bar T+delta T` 对 dynamics/residual 的共同依赖，构造或严格否定 15-mode augmented `(eta,d=hat x-z)` RCI。禁止把 `eta` 独立 boxing，禁止把局部 solver infeasible 当作非存在证明。
