# Run 134：六状态 ancillary 合同与推力修正必要性

日期：2026-09-29。文献准入见 [run134_literature_gate.md](run134_literature_gate.md)，完整推导见 [第71章](../learning/71_control_dependent_ancillary_contract.md)。本轮从本地 Run 133 提交 `d6f12e6` 继续；远端 `main` 为 `1c49659`，远端最新研究分支仍为 Run 126 `c00d102`。

## 1. 本轮问题与停止条件

Run 133 要求冻结六状态 ancillary/tracking error contract，并选择保持 paired `(A(T),W(T))` 的非轴对齐有限证书。本轮先审计其隐含前提：当 ancillary law 可以修正 thrust 时，实际 `T` 是否仍可作为外生 LPV scheduling parameter。

停止条件为：若 `delta T=0` 导致完整六状态紧致 RPI 不可能，而 `delta T` 非零又使 `T` 成为反馈决策的一部分，则不实现 exogenous-LPV RPI 求解器，先保存正确联合图与剩余输入。

## 2. 文献核查

Mulagaleti--Bemporad 2025 已给出 self-scheduling qLPV 的 configuration-constrained polytopic RCI、vertex controls，并利用候选 RCI 内的 scheduling dependence 减少保守性。故“非轴对齐 polytope + self-scheduling correlation”不是空白。

Wehbeh--Kerrigan 2025 用 planar quadrotor 展示 state/control-dependent uncertainty 应保留其共同图；Wehbeh--Kerrigan--Scaccia 2026 将更一般的 decision-dependent uncertainty 写成 GSIP，以 existence-constrained SIP、adaptive discretization 和 worst-case separation oracle处理。后者的收敛定理要求每个有限子问题全局求解，而数值实验实际使用多起点局部 NLP，所以不能把一次 solver success 当成 robust certificate。

Hanema--Lazar--Tóth 2020 的 LPV tube MPC 假定 scheduling 当前可测但外生，未来可变。它是 arbitrary-future scheduling 的强 baseline，却不直接覆盖由 output-feedback correction 生成的实际 thrust。

## 3. 六状态误差合同

定义 `e=x-z`、`eta=x-hat x`、`T=bar T+delta T`、`tau=bar tau+delta tau`。控制器可用偏差为 `hat x-z=e-eta`。对名义小角度模型与当前全域余项模型逐式相减，得到

\[
\begin{aligned}
e_{p_x}^+&=e_{p_x}+he_{v_x},&
e_{p_z}^+&=e_{p_z}+he_{v_z},\\
e_{v_x}^+&=e_{v_x}-h\bar T e_\phi-h\delta T z_\phi-h\delta T e_\phi+hr_x,&
e_{v_z}^+&=e_{v_z}+h\delta T+hr_z,\\
e_\phi^+&=e_\phi+he_\omega,&
e_\omega^+&=e_\omega+h\delta\tau/J.
\end{aligned}
\]

其中 `|r_x|<=d_x(T)`、`|r_z|<=d_z(T)` 且同一实际 `T` 决定二者。当前配置把额外 process noise 设为零，故角速度式只是冻结 benchmark；未给数值界的物理 torque disturbance 仍是接口缺口。

关键变化是：若 `delta u=kappa_j(e-eta,z,bar u)`，实际 `T` 是 controller-dependent scheduling；横向还有 `delta T*z_phi`。所以 Run 133 写下的 e-space paired endpoint inclusion 只是外生 `T` 情况的必要草图，不是完整 output-feedback contract。

## 4. 精确否定 torque-only ancillary

若固定 `delta T=0`，垂向速度误差满足

\[
e_{v_z}^+=e_{v_z}+hr_z,
\qquad r_z\in[-d_z(T),d_z(T)],\quad d_z(T)>0.
\]

假设存在非空紧致 RPI `E`，取其中 `e_vz` 最大值 `M` 的点，再取合法 `r_z=d_z(T)`，下一步 `e_vz=M+h d_z(T)>M`，与不变性矛盾。因此该不可能性与集合形状、static/dynamic torque law 和数值求解器无关。

结论不是“六状态 ancillary 不存在”，而是：在当前 residual 合同下，它必须分配 thrust correction；一旦这么做，就必须保留实际 thrust 与控制、名义状态、estimator error 和 residual bound 的联合图。

## 5. 正确证书与证据等级

正确的 mode-edge 目标应量化 `e in S_c^j`、`eta in E_eta^j`、admissible `(z,bar u)`，施加 `delta u=kappa_j(e-eta,z,bar u)`、`bar u+delta u in U`、`T=bar T+delta T` 和 `r in W(T)`，再证明后继进入 `S_c^{j+}`。它是 configuration-constrained/decision-dependent RCI 图，而非独立 `A x W` 组合。

- **已证明：**六状态误差代数；`delta T=0` 下不存在非空紧致全状态 tracking-error RPI。
- **文献事实：**qLPV polytopic RCI、vertex control、decision-dependent uncertainty GSIP 和外生 LPV tube 均已有强近邻。
- **条件性规范：**联合图证书必须显式纳入 mode-dependent `E_eta^j` 和 nominal/correction input allocation。
- **未证明：**存在 thrust correction 时是否有非轴对齐 RCI；有限 endpoint/vertex reduction 是否精确；common nominal terminal 是否非空；完整六自由度保证。

## 6. 为什么不实现

本轮不新增求解器或数值结果。解析反证无需 Monte Carlo；缺少 `E_eta^j` 时，任何 augmented RCI 数值问题都没有完整输入。实现 exogenous paired-endpoint LMI/LP 会得到语义错误的结果，不能推进约束满足或递归可行性证据链。

回归命令与原始结果：

```bash
ACADEMIC_RESEARCH_NO_WRITE=1 python -m unittest discover -s verification -p 'test_*.py' -q
# Ran 115 tests in 82.308s
# OK
```

`git diff --check` 同时通过。回归只验证文档更新没有破坏既有可执行证据，不把测试通过升级为本轮理论命题证明。

## 7. 论文级主线与下一唯一问题

本轮继续纠正证明依赖，而不是再做局部法向枚举。当前主线的最早缺口已具体化为 estimator-to-controller interface：先构造/否定 15-mode、time-uniform、可靠的 `E_eta^j`；再联合实际 thrust graph 合成 `S_c^j`；之后才能形成 tightening、common nominal terminal、同预算严格优势和闭环验证。

下一唯一问题：**从 rolling SMF 构造或否定 mode-indexed estimator-error family `E_eta^j`，逐边验证 prediction/intersection/reduction 在 actual-input 时序下保持真值包含。**
