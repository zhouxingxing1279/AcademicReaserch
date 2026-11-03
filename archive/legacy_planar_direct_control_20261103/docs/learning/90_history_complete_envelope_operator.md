# 90. 历史完备共同外包算子与量词顺序

## 1. 历史语言和精确信息族

令扩展离散状态

```math
q=(j,r),\qquad j\in\{0,\ldots,14\},\quad
r\in\{\mathrm{init},5,10,15\},
```

并令 `alpha(h)=q` 表示可见历史 `h` 按第89章自动机到达 `q`。对每个历史，联合信息集

```math
I(h)\subseteq\mathbb R^4,
\qquad s=(\eta_{p_z},\eta_{v_z},e_{p_z},e_{v_z}),
```

保留共享 residual/noise primitive；可见量为线性映射

```math
D(s)=e-\eta=d.
```

精确 history-indexed ensemble 是

```math
\mathfrak I_q=\operatorname{cl}\{I(h):h\text{ admissible},\ \alpha(h)=q\}.
```

若压成单一共同外包 `K_q`，正确要求不是某三个 seed 被包含，而是

```math
\bigcup_{I\in\mathfrak I_q}I\subseteq K_q.\tag{90.1}
```

同一 `(q,d,z,\bar u)` observation fiber 上的全部隐藏 `eta` 必须共享一个当前 correction。

## 2. 固定策略下的单调算子

冻结 global residual envelope，并预先固定一张因果策略

```math
\delta u=\kappa_q(d,z,\bar u).
```

令 `F_ell(s,delta u,xi)` 是仓库 `split_successor` 合同对应的 miss/success 联合边映射，其中
同一个 `xi` 同时进入物理、observer、`eta` 和 `e` 更新。对集合族
`K=(K_q)_{q in Q}` 定义

```math
[\mathcal T_\kappa(K)]_{q'}=
I^0_{q'}\ \cup\
\operatorname{cl}\!\bigcup_{q\xrightarrow{\ell}q'}
\{F_\ell(s,\kappa_q(D(s),z,\bar u),\xi):
s\in K_q,\ \xi\in\Xi_\ell\}.\tag{90.2}
```

`I^0` 仅在 `(0,init)` 放入真实初始联合集。固定 `kappa` 时，集合包含
`K subset L` 蕴含 `T_kappa(K) subset T_kappa(L)`；因此

```math
K^{0}=\varnothing,\qquad K^{n+1}=\mathcal T_\kappa(K^n)
```

的并集闭包是该策略下包含初始化的最小前向历史包络。它是 reachable envelope，不自动是
terminal RCI；只有极限存在、满足 `T_kappa(K) subset K` 且全部硬约束成立时才能称闭合。

## 3. 为什么不能把 `exists kappa` 塞进迭代

若第 `n` 层和第 `n+1` 层分别选择不同策略，逐层可行并不产生一张运行时可执行策略。形式上，

```math
\bigcup_\kappa\mathcal T_\kappa(K)
```

表达的是所有策略后继的并集，而不是“存在一张策略控制整个 history family”。不同策略下的
闭合集的交集也未必被任何一张策略保持。因此当前不存在无需指定 policy class/selector 的
规范“最小受控共同外包”。正确的综合量词是先找一张可实现 `kappa`，再要求

```math
\exists\kappa\quad
\mathcal T_\kappa(K)\subseteq K,
```

其中每个 observation fiber 内、未知后继边之间共享同一当前输入。

## 4. 凸化与固定复杂度压缩义务

令 `Gamma` 为 convex hull、CZ reduction 或模板外包。迭代

```math
K^{n+1}=\Gamma(\mathcal T_\kappa(K^n))
```

仍可保持包含性，但 `Gamma` 会生成原历史中未出现的新点，尤其会生成新的 `d=D(s)` fibers。
所以仅证明 `Gamma(A) superset A` 不够；还必须证明：

1. `kappa_q` 在每个新增 fiber 上有定义且不读取隐藏 `eta`；
2. `bar u+kappa_q` 对该 fiber 满足执行器盒；
3. 从整个压缩集合出发的 shared-primitive 后继再次被下一集合包含。

Run148 三 seed 的一次凸包满足 seed 包含，但尚未满足以上三项，因此不能作为循环闭合证书。

## 5. 初始化层与终端层必须分开

`r=init` 的 15 个状态只在首次 success 前可达；success 后进入 45 个 recurrent states，且不再
返回 `init`。因此 terminal family 可以只定义在 `r in {5,10,15}` 上，但完整闭环证明还需：

- 从 `(0,init)` 的真实初始集出发，瞬态层全程满足硬约束；
- 每一种首次 return image 被相应 recurrent terminal family 覆盖；
- recurrent family 在全部 51 条循环边上自映射（42 条 miss、9 条 success）。

不能要求 `init` 层本身成为 recurrent terminal fixed point，也不能用三个首次 return seed
替换瞬态安全证明。

## 6. 证据等级

本章是 **project-specific fixed-policy monotone envelope contract**。单调性是集合像与并集的
直接推论；terminal/init 分层来自第89章可达图。它不是新算法、RCI 存在证明或 MPC 递归
可行性证明。下一步只有在明确 policy class、`Gamma` 和硬约束量词后，才允许实现一次迭代。
