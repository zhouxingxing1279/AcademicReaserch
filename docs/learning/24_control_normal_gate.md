# 24 从几何反例到控制反例：真实 MPC 法向门与一次否证

2026-09-23。接续 [23 滚动 CZ Recenter LP](23_rolling_cz_recenter_lp.md)。本轮专门检查第 23 章最危险的逻辑跳跃：**随机 mixed directions 上出现 recenter support 增长，是否已经说明 Tube MPC 的 shifted candidate 会失效？**

结论是否定的。把随机方向替换为仓库目前已经严格认证的控制相关法向后，26 次滚动测量更新中没有出现一次方向预算违反。因此第 23 章的 mixed-direction 结果目前只能作为几何压力测试，不能作为 MPC 递归可行性失败证据。

## 1. 当前真正有资格称为 control normals 的方向

仓库现有完整六状态控制器尚未合成：`configs/planar_baseline.json` 中 `mpc.K=null`、`terminal_certificate=null`。因此不能人为选择一个平移增益，再把其法向当成“已证明的 MPC 法向”。

目前可从已证明材料中抽取的只有：

1. 六状态 domain/state-box 的 12 个 signed coordinate normals；
2. `docs/theory/05_finite_terminal_polytope.md` 的姿态终端多面体
   \[
   H_a=\begin{bmatrix}1&0\\-1&0\\4&1\\-4&-1\end{bmatrix};
   \]
3. 同一文档已认证反馈
   \[
   K_a=[8/25,\;4/25]
   \]
   诱导的 torque tightening directions \(\pm K_a\)。

把姿态方向嵌入六状态 `(px,pz,vx,vz,phi,omega)` 后，共得到 18 个当前可辩护的方向。

## 2. 实验：复用第 23 章 rolling posterior

新增 `verification/check_control_normals_recenter.py`，完全复用第 23 章的六状态 affine outer model、初始 truth、测量时序与非零 truth-consistent measurement rule，只把 50 个随机 mixed directions 替换为上述 18 个实际已认证法向。

实际运行结果：

| 指标 | 结果 |
|---|---:|
| measurement updates | 26 |
| protected directions | 18 |
| 至少一个方向增长的 ticks | 0 |
| direction-update violations | 0 |
| 最大数值 growth | `3.33e-16` |

该结果不证明 coordinate midpoint 一般安全；第 23 章已经给出一般 mixed-direction 反例。它只说明：**在仓库目前真正拥有证明依据的这些控制法向上，尚未观察到那个失败机制。**

因此本轮否定以下过强说法：

> “第 23 章已经证明 unrestricted recenter 会破坏本项目 Tube MPC 的 recursive feasibility。”

正确表述应为：

> “第 23 章证明一般高维 CZ 的 coordinate midpoint 不能保护任意 mixed direction；是否影响本项目 MPC，取决于真实 state/input/terminal normals。当前已认证的姿态法向没有触发该问题。”

## 3. 为什么姿态法向没有触发并不奇怪

当前姿态 `phi, omega` 每 tick 都直接测量，且已认证终端/输入方向只依赖这两个坐标。第 23 章最明显的 violations 来自高维相关 CZ 的任意斜向投影；而当前可用姿态法向结构非常特殊。

真正可能产生关键 mixed normals 的位置是平移 feedback 对输入约束的映射。例如若将来完整 ancillary feedback 为 \(u=\bar u+K e\)，输入面 \(q_u^T u\le b_u\) 的误差 tightening 方向是

\[
p_u=K^T q_u.
\]

只要 \(K\) 混合位置、速度、姿态误差，\(p_u\) 就不再是坐标方向。但当前仓库没有一个通过完整约束/终端证书的六状态 \(K\)，所以现在构造这种方向会把“候选增益”冒充成“已证明控制器”。

## 4. 与文献的关系：recursive-feasibility gate 不是新概念

Ping (2015), *Dynamic Output Feedback Robust MPC via Zonotopic Set-Membership Estimation for Constrained Quasi-LPV Systems* 已明确讨论：刷新 estimation-error set 后，主 MPC 的下一时刻递归可行性可能丢失，因此通过辅助可行性条件决定是否采用新集合/新控制器参数；失败时继承旧 controller parameters。

Köhler et al. 的 robust adaptive MPC framework 也把 set-membership update 的 monotonic/non-increasing property 与 tube/set update 的递归可行性条件作为核心接口。2026 年 Dey & Bhasin 的 adaptive-tube output-feedback MPC 又进一步允许估计、tightening、terminal ingredients 和 tube geometry 联动更新并证明 recursive feasibility。

因此，“更新估计集合前先过 recursive-feasibility gate”本身不是创新。当前可能的差异只剩更窄的计算结构：**能否用有限 control-normal support certificates + posterior-member center LP，以比完整 tube/auxiliary feasibility recomputation 更低的成本完成这个 gate。** 这仍需严格排重和总成本实验。

## 5. 候选创新的重新排序

### A. control-normal certified update gate — 保留，但降级为待验证候选

形式：对真实 MPC 约束所需的有限方向 \(P_c\)，只在这些方向上认证 posterior tightening 与 recenter budget；证书不足时拒绝更新或继续查询。

必须证明：这些有限方向确实足以覆盖 shifted candidate 的 state/input/terminal inequalities。否则只是集合几何优化。

### B. coordinate-midpoint unsafe therefore MPC fails — 否定

一般几何 unsafe 成立，但本轮真实已认证法向 0/26 失败。不能再把随机方向结果当控制反例。

### C. 先合成一个“方便产生反例”的 K — 否定

研究顺序不能为了证明创新而选增益。下一步应先独立完成满足现有六状态约束/终端条件的 feedback/terminal certificate，再让由该控制器自然产生的 normals 检验 recenter gate。

## 6. 下一步：先闭合控制器，再判断 recenter 候选生死

下一轮最优先任务从“继续增加 recenter 实验”改为：

1. 从现有 04/05/08/09 理论文档提取六状态有限时域与姿态终端构件；
2. 检查能否构造一个不依赖学习、满足输入硬约束的六状态 ancillary feedback + terminal family；
3. 只有该控制器通过约束/不变性 gate 后，计算其真实 \(K^Tq_u\)、state normals、terminal normals；
4. 重跑本轮实验并寻找 shifted-candidate 失效见证；
5. 若真实 normals 仍不触发 recenter 问题，则应主动放弃“center budget 是主要创新”的方向，而把精力转向 CZ 压缩/外包对真实 tightening 保守性的可证明改进。

这一步是研究纪律上的必要 gate：**先证明控制问题真实存在，再设计解决它的方法。**
