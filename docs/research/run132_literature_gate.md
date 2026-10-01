# Run 132 文献准入卡：间歇数据下的 terminal baseline 是否需要 mode-indexed family

日期：2026-09-29。仓库起点为本地 Run 131 提交 `27d7de1`；远端 `main` 为 `1c49659`，远端最新研究分支仍为 Run 126 `c00d102`。本轮问题是：15-mode bounded-dropout automaton 是否必须先构造 mode-indexed terminal family，才能闭合输出反馈 tube MPC 的递归可行性。

## 1. 最近邻与本轮实际阅读

| 文献 | 本轮阅读层级 | 已解决内容 | 对本轮候选的约束 |
|---|---|---|---|
| Hassaan, Pati, Shen, Yong, *Time-Varying Tube-Based Output Feedback MPC for Constrained Linear Systems with Intermittently Delayed Data*, IFAC-PapersOnLine 54(5):103--108, 2021, DOI [10.1016/j.ifacol.2021.08.482](https://doi.org/10.1016/j.ifacol.2021.08.482) | **全文定向精读** Sections 2.2、3.1--3.2，Assumptions 1--3、Theorems 5--7 | 用周期有限长度语言描述缺测/时延；构造时变 estimator/control tubes；Assumption 2 用一个对全部周期相位有效的 common nominal terminal set 与 gain，Theorem 6 由旧解移位和 terminal action 证明递归可行。 | 直接覆盖“有限丢包语言 + 时变 tube + terminal shift”。mode-indexed terminal family 不是默认必要条件；必须先超过其 common-set baseline。 |
| Rutledge, Yong, Ozay, *Finite horizon constrained control and bounded-error estimation in the presence of missing data*, Nonlinear Analysis: Hybrid Systems 36:100854, 2020, DOI [10.1016/j.nahs.2020.100854](https://doi.org/10.1016/j.nahs.2020.100854) | **全文定向精读** Sections 3--4、Definition 2、equalized-recovery formulation 与 synthesis | missing-data language 可表达连续丢包上界；prefix-based affine feedback 在噪声、状态/输入约束下实现有限时域 equalized recovery。Remark 3 明确允许 zonotope 等 set template。 | bounded-dropout automaton、mode/prefix feedback 与集合界均不是空白；但本文是有限时域，不单独给出本项目所需 receding-horizon terminal proof。 |
| Hassaan, Shen, Yong, *Path-Dependent Controller and Estimator Synthesis with Robustness to Delayed and Missing Data*, HSCC 2021, DOI [10.1145/3447928.3456655](https://doi.org/10.1145/3447928.3456655) | **全文定向精读** Sections 2--5，fixed-length/reduced event language 与 path-dependent synthesis | 对时变 affine system 按观测路径合成 controller/estimator；以 reduced event language 消除相同可观察历史造成的冲突，并用多面体 error bounds 改善 worst-case 设计。 | “按模式/路径索引 controller 与 estimator”本身已有直接近邻；不能把 15 个模式的索引结构当创新。 |
| Wildhagen, Pezzutto, Schenato, Allgöwer, *Self-triggered MPC robust to bounded packet loss via a min-max approach*, CDC 2022 extended version, arXiv:2204.00339 | **全文定向阅读** problem formulation、min-max MPC、terminal law 与 recursive-feasibility argument | 在连续丢包数有界时使用 min-max MPC 和尾端控制律，证明对所有允许丢包 realization 的递归可行、约束满足和收敛。 | bounded packet loss 下 terminal/shift 证明已有另一条强基线；虽非 output-feedback SMF，也否定“bounded loss + terminal proof”作为首次性。 |

## 2. 最强同条件基线与严格差异

最接近本轮问题的基线是 Hassaan--Pati--Shen--Yong 2021。其 terminal 条件不是按数据模式维护一族集合，而是要求存在共同 `K_f,X_f`：`X_f` 对 nominal terminal dynamics 不变，且 `X_f` 位于所有周期相位的 state-tightened sets 的交中，`K_f X_f` 位于所有 phase-dependent input-tightened sets 的交中。该共同集合足以支撑旧 nominal sequence 移位。

因此本项目若直接构造 `X_f^sigma` 并逐边验证

\[
(A_\sigma+B_\sigma K_\sigma)X_f^\sigma\oplus W_\sigma
\subseteq X_f^{\sigma'},
\qquad K_\sigma X_f^\sigma\subseteq U_{\mathrm{tight},\sigma},
\]

只是在已有 path-dependent synthesis 与 switched/packet-loss invariant-family 思路上的实现组合。严格差异只能是：共同集合基线在**同一六状态四旋翼合同、同一 estimator/control tubes 和同一硬约束**下不可行或显著过保守，而 mode-indexed family 可用可检查证书恢复非空 terminal domain，并最终与固定预算 CZ support query 安全衔接。

## 3. 仓库事实与当前证明义务

仓库已有 bounded-loss automaton 是 15 modes、17 edges、最大 15 tick 位置包间隔；mode-dependent quadratic metric 已认证估计误差齐次部分的逐边收缩。但这不是 terminal controller 证书。当前 `configs/planar_baseline.json` 仍明确给出 `K=null`、`terminal_certificate=null`、`L_by_mode=null`。此外，第33章已严格否定旧 hover-DARE 候选在当前 residual/torque 合同下的输入可行性；第34--35章的 30,000 点 static-`K` 搜索失败只是数值观察；第36章又说明一般控制序列在有限时域可以可行，因此不能宣称物理不可行。

这意味着当前连 Hassaan Assumption 2 的 common-set baseline 都尚未实例化。没有合法的 ancillary/terminal gain、局部未来扰动合同和 phase-dependent input tightenings，直接枚举 15 个 terminal sets 不会产生可审查的命题。

必须依次闭合：

1. 在同一 thrust-scheduled 六状态局部合同上确定未来 disturbance/remainder set；不能把当前估计误差当未来扰动。
2. 用证书化方法联合得到 terminal/ancillary gain 与非空 invariant domain，不能再把随机 gain 扫描当证明。
3. 先检查 Hassaan-style common `X_f` 对全部 15 modes/17 edges 的 worst-phase state/input tightenings是否非空。
4. 仅当共同集合被可靠否定或造成有意义的认证可行域损失时，才准入 mode-indexed `X_f^sigma`；随后还需证明 mode switch、measurement arrival/recenter 和旧计划移位的一致性。

## 4. 推翻条件、收益与准入结论

候选 mode-indexed family 会被以下任一结果推翻为论文主创新：共同 `X_f` 已非空且在相同预算下性能差异无实际意义；mode-indexed family 只重现 path-dependent feedback；family 仍因 torque/state tightening 为空；或无法把 terminal phase 与在线 posterior/recenter 时序一致地连接。

**mode-indexed terminal 创新/实现准入：不通过。方向纠正准入：通过。**

本轮不写控制代码。该结论不是“算法失败”，而是最近邻给出了更强、结构更简单且必须先复现的 common-terminal baseline，同时仓库缺少任何合法 terminal gain/certificate。下一轮应先选择与 thrust-scheduled LPV 和局部 residual 相容的 certificate-based joint `K_f/X_f` synthesis 类，实例化或反驳 Hassaan Assumption 2；只有 common baseline 的证据齐备后，mode-indexed family 才有比较意义。
