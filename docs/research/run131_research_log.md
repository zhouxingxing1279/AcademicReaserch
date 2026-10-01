# Run 131：两层 tube 架构排重与论文主线纠偏

日期：2026-09-29。文献准入见 [run131_literature_gate.md](run131_literature_gate.md)。本轮从未推送的 Run 130 提交 `ee12daf` 继续；远端 `main` 为 `1c49659`，远端最新研究分支仍为 Run 126 `c00d102`。

## 1. 本轮问题

Run 127--130 已关闭“先对高维 posterior 事后降阶，再要求它进入固定 terminal mRPI”的主线。本轮审计替代架构：由精确/CZ posterior 只负责有限时域控制方向收紧，另用 independent backup/adaptive terminal tube 承担 dropout、recenter 和 shift 的递归可行性。

准入前判退条件是：若近邻已经同时给出 two-tube 分层、在线 estimator bounds、terminal/shift proof 或 estimation-update acceptance/fallback，则不得把架构组合称作创新，也不得先实现再寻找差异。

## 2. 文献核查结果

### 2.1 two-tube 并非新架构

Dey--Dhar--Bhasin 2022 已明确构造 `homothetic and invariant` two-tube：内层 homothetic tube 包含 estimated-state trajectory，固定 state-estimation-error RPI set 与其 Minkowski 相加形成 true-state outer tube；Assumption 4 的 terminal set 与 IV-F 的 shifted candidate 保证递归可行性。

Dey--Bhasin 2025 进一步使用随时间变化的 state-estimation-error sets，并仍以 terminal set、terminal feedback 和 tube shift 证明 recursive feasibility/robust exponential stability。论文摘要直接使用 `two-tier tube architecture` 表述。故“online posterior/estimation information + independent terminal tube”这个宽泛结构至少在 2022--2025 年已有明确先例。

### 2.2 online bounds 与固定 terminal envelope 已闭合

Köhler--Müller--Allgöwer 2021 不只把当前误差界用于约束收紧；其预测还传播 future estimation bounds 和 observer/nominal mismatch。Assumption 7 在 augmented `(x,e,s)` 空间给出 terminal ingredients，Theorem 4 用单调 bound propagation 和 terminal condition 封闭移位证明。该结构已经非常接近“精细在线信息只改善 finite horizon，保守 envelope 保住尾端”。

### 2.3 acceptance/backup 也已有强近邻

Ping 2015 先刷新 zonotopic estimation-error set，再解辅助 feasibility problem 决定是否更新 controller parameters；若失败就继承上一时刻参数。其 Algorithm 8 还包含 zonotope order limit。因此“SMF posterior 更新后先做 feasibility gate，失败则 fallback”也不是空白。

Dey--Bhasin 2026 的覆盖更强：tube geometry、tightening 和 terminal ingredients 随 estimates/sets 更新；Criterion 1 检查 consecutive terminal compatibility，失败时可保持 point estimate/回退集合；Algorithm 1 与 Theorem 2/Appendix IV 用 backup setup 和 old-solution shift 建立 recursive feasibility。

## 3. 准入与证据等级

- **文献事实：**上述五篇的相关正文、假设、算法和证明已定向核查；Ping 2022 仅摘要，不用于定理级判断。
- **排重结论：**广义“两层 tube + online tightening + terminal/backup + fallback”已被多个近邻分别乃至直接覆盖，创新准入失败。
- **条件性方向判断：**当前可能剩余的是 `bounded measurement-loss automaton + CZ support-query budget + mode-indexed backup terminal family + actuator-hard constraints` 的联合接口，但它尚未形成定理，也未确认首次性。
- **未证明：**不存在其他覆盖该联合接口的工作；15-mode terminal family 非空；query-based stage plan 可安全 handoff；相同预算下严格优于强基线；完整六自由度四旋翼保证。

本轮不新增代码。原因不是实现困难，而是文献门槛已经否决宽泛方法；继续写 controller 只会复现已有结构并掩盖真正缺口。

## 4. 与仓库已有间歇测量结果的接口

仓库既有 [05_intermittent_error_interface.md](../learning/05_intermittent_error_interface.md) 已给出 bounded-loss automaton，并说明单一 quadratic metric 在 dropout step 上不能逐步收缩，而 mode-dependent metric 可获得 edge-wise contraction。[06_mode_dependent_nestedness.md](../learning/06_mode_dependent_nestedness.md) 已验证 reachable-mode envelope 的 shift inclusion，但也明确指出 uniform Young recursion 过保守、terminal/control ingredients 未实例化。

这些事实把下一缺口定位在 terminal/backup，而不是继续改 posterior 几何：需要对每条允许模式边验证形如

\[
(A_\sigma+B K_\sigma)X_f^\sigma\oplus W_\sigma
\subseteq X_f^{\sigma'},
\qquad K_\sigma X_f^\sigma\subseteq U_{\mathrm{tight},\sigma}
\]

的条件，并保证 measurement-arrival/recenter 时的 handoff。这里的 `W_sigma` 必须是未来外部扰动与模型余项合同，不能把当前状态估计误差直接当作未来扰动。

## 5. 定期总审视

当前仍未形成完整硕士课题方法，但完成了重要纠偏：Run 127--130 的 post-hoc reduction 是局部表示支线，本轮又排除了把“two-layer”重新包装成主创新。剩余主线只有在 mode-indexed backup terminal family、support-query acceptance 和同预算严格优势三者同时闭合时，才可能达到论文级完整性。

## 6. 验证与下一唯一问题

文档修改前基线回归命令：

```bash
ACADEMIC_RESEARCH_NO_WRITE=1 python -m unittest discover -s verification -p 'test_*.py' -q
```

文档修改前基线与修改后最终回归均为 115 项全部通过；最终回归耗时 80.628 s，`git diff --check` 通过。本日志不把测试通过误写成新理论证明。

下一轮唯一问题：**文献先行核查 switched/packet-loss robust terminal-set 最近邻，然后在仓库 15-mode bounded-dropout automaton 与同一四旋翼外环/执行器合同下，构造或反驳 mode-indexed backup terminal family；逐边检查 robust invariance 与 input tightening。** 若找不到非空 family，给出 certificate-class 明确的反例并停止 support-query handoff 主张；在该骨架闭合前不实现 posterior stage-tightening controller。
