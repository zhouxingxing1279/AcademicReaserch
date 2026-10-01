# Run 137：联合 ancillary RCI 前的名义推力预留门槛

日期：2026-10-01。文献准入见 [run137_literature_gate.md](run137_literature_gate.md)，推导见 [第 74 章](../learning/74_nominal_thrust_reserve_gate.md)。仓库起点为本地 Run 136 `6e389c1`；远端 `main` 为 `1c49659`，远端 Run 136 `3c3944f` 与本地 tree SHA `8bc8945f3d67f081bddeb892f69b6a67431c7143` 完全一致。

## 1. 仓库与文献核查

Run 136 的 15-mode zonotope 证书可执行，基线全仓 120/120 测试通过。配置仍只有 actual input bounds `[4.905,14.715] x [-0.08,0.08]`，没有单独 nominal input allocation；`K`、`L_by_mode` 与 terminal certificate 为空。

本轮精读 Lorenzetti--Pavone 的 coupled estimation/control-error RPI 与 state/input tightening，重读 Köhler 等 Assumption 7/Theorem 4 的 estimation/tracking bounds 和 terminal shift，重读 Mulagaleti--Bemporad 的 qLPV configuration-constrained RCI 以及 Wehbeh--Kerrigan 的 state/control-dependent GSIP。联合误差图与 RCI 方法学均被覆盖，创新准入不通过；只准入仓库合同纠正。

## 2. 核心命题与证据等级

对

\[
e_{v_z}^{+}=e_{v_z}+h(\delta T+r_z),\quad
|r_z|\le 2.086+0.10125T,
\]

在实际推力硬约束下，由紧致集合的最大/最小 `e_vz` 点得到 controller-independent 必要条件

\[
\bar T\in[7.48763125,11.13910625]\;{\rm N}.
\]

- **精确证明：**低于左界时存在持续正 residual 造成严格单调上漂；高于右界时存在持续负 residual 造成严格单调下漂。结论覆盖有限 mode-indexed compact family。
- **精确算术核查：**两个端点 witness、两个 correction reserve 与必要区间均使用 `Fraction`。
- **条件边界：**该区间只消除 vertical equilibrium authority obstruction，不证明 RCI 存在；hover `9.81 N` 通过。
- **配置结论：**若 nominal MPC 复用完整 actual thrust interval，则联合 ancillary RCI 问题严格不可行。当前配置未另行声明 nominal bounds，因此不能直接启动 12 维 RCI 求解。

## 3. 实现与验证

按 TDD 新增两项测试。RED 阶段因 `check_nominal_thrust_reserve` 缺失而 2/2 预期失败；GREEN 阶段实现 exact verifier 后 2/2 通过。验证器读取真实配置，输出 exact interval、endpoint witnesses、hover gate、配置缺失标志与证据边界。

归档结果位于 `results/theory_nominal_thrust_reserve_20261001/exact_checks.json`。提交前最终全仓回归为 **122/122 通过，137.868 s**；Python compile 与 `git diff --check` 通过。归档中的源码哈希由最终 verifier、测试、配置和第 74 章重新计算。

## 4. 主线判断

本轮没有继续搜索 K 或构造高维 RCI，因为在 nominal/correction 输入分配未冻结前，求解器 infeasible 只会重复已证明的 endpoint obstruction，solver success 则很可能隐式使用未声明的 input reserve。该纠正把下一步从“直接做 12 维联合集合”收缩为“先冻结 nominal input set，再做强基线”。

离硕士课题级完整方法仍缺：收紧输入下的 mode-indexed augmented-error RCI、horizontal/torque/source-domain closure、nominal terminal/shift、同预算严格优势与四旋翼闭环验证。

## 5. 下一唯一问题

在配置中冻结一个独立 nominal input set：thrust 必须严格落入 `[7.48763125,11.13910625] N`，torque 也要给 correction 留余量；随后以 hover-neighborhood 为第一强基线，构造或反驳消费 Run 136 exact zonotope support 的 mode-indexed augmented `(eta,d=hat x-z)` RCI。若最小基线仍不可行，必须给出 certificate-class 或解析反证，不能继续随机 K 搜索。
