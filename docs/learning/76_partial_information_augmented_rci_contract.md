# 76. 增广 ancillary 不变集必须是 partial-information 合同

日期：2026-10-02。承接第 73 章的 15-mode estimator-error zonotope 与第 75 章的输入预算探针。

**结论：当前仓库尚未定义一个可执行的 15-mode augmented RCI 问题。`(eta,d)` 中只有 `d=hat x-z` 可用于反馈，`eta=x-hat x` 是隐藏真值误差；若按普通 full-state RCI 令控制依赖 `(eta,d)`，会得到不可实现的证书。Run 138 只冻结输入盒，不能唯一决定量词、策略类、名义域、mode 时序和共享扰动图。因而本轮不运行高维求解器，而先加入可执行合同门槛。**

## 1. 三个不能混用的问题

记 `q=(eta,d)`，其中

```math
eta=x-\hat x,\qquad d=\hat x-z,\qquad e=x-z=eta+d.
```

### 1.1 固定输出反馈下的 RPI

先冻结可实现策略

```math
delta u=kappa_j(d,z,\bar u),
```

再对闭环图检查

```math
\forall q\in Q_j,\ \forall (j,j^+)\in E,\ \forall \xi:
F_j(q,kappa_j,\xi)\in Q_{j^+}.
```

Lorenzetti--Pavone 的 coupled-error RPI 属于这一类；线性特例是 `delta u=K d`。固定 `K` 失败只能否定该 `K` 或该 certificate class。

### 1.2 普通 full-state RCI

标准 state-feedback RCI 常写成

```math
\forall (eta,d)\in Q_j\ \exists\delta u(eta,d)\ \forall\xi:
F_j(eta,d,\delta u,\xi)\in Q_{j^+}.
```

这允许控制器读取 `eta`。对当前 output-feedback 问题，该量词给出的 policy 通常不可实现；其可行性不能证明真实控制器存在。

### 1.3 正确的 partial-information controlled RCI

对固定当前模式和可见量 `o=(d,j,z,bar u)`，同一控制必须覆盖所有不可区分的隐藏误差。令 fiber

```math
Q_j(d)=\{eta:(eta,d)\in Q_j\}.
```

所需量词至少是

```math
\forall(j,d,z,\bar u)\ \exists\delta u=kappa_j(d,z,\bar u)\
\forall eta\in Q_j(d)\ \forall(j,j^+)\in E(j)\ \forall\xi:\
F_{j\to j^+}(eta,d,z,\bar u,\delta u,\xi)\in Q_{j^+}.
\tag{76.1}
```

`delta u` 必须在未知的下一 packet outcome、真实 residual 和 measurement noise 实现之前选定。把 `exists delta u` 放到这些量词之后会产生非因果假阳性。

## 2. actual-thrust 与共享 primitive

当前模型有

```math
T=\bar T+\delta T,
```

同一 `T` 同时进入横向动力学、`delta T z_phi` 和 residual 半宽。joint graph 应使用一组共享 primitive，例如

```math
r_x=d_x(T)s_x,\quad r_z=d_z(T)s_z,\quad |s_x|,|s_z|\le1,
```

并把同一个 `s_x,s_z` 映射到 `eta^+` 与 `d^+`；这样相加后 `e^+=eta^++d^+` 才与真实 tracking-error 递推一致。把两部分各自换成独立 residual boxes 会增加不存在的自由度；把 `A(T)` 与 `W(T)` 独立取端点笛卡尔积则会增加不存在的最坏组合。两者都不能解释为原问题证书。

Run 136 的 `S_j` 是 estimator-error outer invariant family，可以作为 joint set 的投影约束；但它本身没有定义 `d` policy，也没有补出上述共享 primitive 图。

## 3. 当前缺失的六项合同

对 `configs/planar_baseline.json` 的只读核查得到：

1. 未选择 fixed-feedback RPI 或 partial-information controlled RCI；
2. 未冻结 `kappa_j` 的输入信息和参数化；
3. 未给 `z_phi` 等 nominal variables 单独的 admissible domain；
4. 未把 15 modes、17 edges 与“input 先于下一 packet outcome”写入控制合同；
5. 未给 actual-thrust dependent shared-primitive maps；
6. 未要求候选包含可达初始化 slice，例如 `S_0 x {d=0}`。

因此任何当前 solver 都必须自行补假设。不同补法回答不同问题，局部 `feasible` 或 `infeasible` 均不能升级为本课题结论。

## 4. 可执行门槛

新增 `verification/check_augmented_rci_contract.py`。它只验证问题是否实例化，不验证 RCI 存在。当前配置应稳定返回：

```text
status = blocked
solver_admissible = false
missing_obligations = 6 items
```

测试 fixture 还检查：隐藏 `eta` 或已实现 residual 不得进入 policy observation；控制量词不得放在下一 edge 之后；`eta,d` 必须共享 residual primitive；初始化 artifact 必须是通过 15-mode/17-edge 核查的 Run 136 结果。

## 5. 证据等级与下一问题

- **已核查仓库事实：**当前六项合同缺失，`K/L_by_mode/terminal_certificate` 仍为空。
- **理论合同纠正：**式 (76.1) 给出 output-feedback controlled invariance 的必要因果量词；普通 full-state RCI 不足以证明可实现性。
- **可执行回归门槛：**当前配置被阻止进入 solver；完整受控 fixture 通过。
- **未证明：**任何 augmented RCI 的存在或不存在、可用 nominal torque 内点、terminal/shift 与递归可行性。

下一唯一问题：冻结最小 hover-neighborhood partial-information contract，逐式给出 `(eta,d)` 在 17 条 edge 上的共享 primitive 更新和一个明确的 causal policy class；只有该 gate 变为 `ready` 后才启动 RCI synthesis。

