# 113. `Gamma` 必须作用于 information-family 图，而非单个 posterior

## 1. 本轮发现的类型错误

Run178 把下一步写成选择 fixed-complexity `Gamma`。若把 `Gamma` 理解为普通 CZ/SPZ order
reduction，输入和输出都是一个物理状态集合。这不足以处理当前输出反馈终端对象，因为控制器
在时刻 `k` 已知连续可见量

```math
d=D(s)=e-eta,
```

并允许使用 `u=kappa_q(d,z,bar u)`；同一个 `d` fiber 内的隐藏状态必须共享该输入，而不同
`d` 可以选择不同输入。故每个离散标签 `q` 的对象实际是集合值映射

```math
d \longmapsto K_q(d),
```

或等价的 lifted graph

```math
G_q=\{(d,s):Ds=d,\ s\in K_q(d)\}.
```

把所有 `d` 的 posterior 先并成一个 CZ 再选单一输入，会错误削弱控制权限；为每个连续 `d`
单独维护一个 CZ，则没有固定存储复杂度。两者都不是第88章所需的有限抽象。

## 2. Rego 方法能解决与不能解决的部分

Rego 等给定已知输入 `u_{k-1}` 和已经实现的测量 `y_k`，用 mean-value 或 first-order Taylor
extension 可靠外包单个 CZ 的非线性预测，并用 generalized intersection 精确表示线性有界误差
测量更新。其 Theorems 2--3 解决

```math
X \mapsto outer(f(X,u,W)),\qquad
X^- \mapsto X^-\cap_C(y-D_vV).
```

Remark 10 和 §4.5 再用外包 order reduction 将生成元/约束数降回给定上限。这个递推可作为
**一条已实现 history** 的可靠估计器基线，但没有给出连续 observation fibers 上的统一策略图，
也没有证明 reduction 后新增 fibers 对同一控制策略逐边闭合。

因此“固定阶 CZ + Rego prediction/update”不能直接充当 `Gamma`。它只能成为 family oracle
内部的单-fiber传播原语。

## 3. 可准入的最小表示合同

下一候选必须显式参数化 fiber。一个最小可审查版本是固定法向、分片仿射 graph：

```math
G_q^i=\{(d,s):F_q^i[d;s]\le g_q^i,\ d\in D_q^i\},
```

其中每个标签的 cell 数、法向数和 `kappa_q^i(d)=K_q^id+k_q^i` 维数预先固定。可靠 oracle
必须对每个 source cell、每条 packet 边及每个 target normal 证明

```math
sup\{a^T[d^+;s^+]:
 (d,s)\in G_q^i,\ xi\in Xi_ell,
 s^+=F_ell(s,kappa_q^i(d),xi),
 d^+=D(s^+)\}\le g_{q'}^j,
```

并同时证明 target cell 覆盖、输入盒、状态盒和非线性余项 source domain。success 边的测量值
是 successor 可见量，不能让它影响当前输入；miss 边也不能省略 always-observed update。

这只是待实例化的类型正确合同。固定法向/分片仿射表示、鲁棒输出反馈 fiber 控制和非线性
Taylor/CZ 外包均已有近邻，不能作为创新。只有在同预算下产生严格更大可行域或更小认证收紧，
并闭合终端与移位证明，才可能形成论文贡献。

## 4. 本轮停止点

本轮不实现单-CZ reduction 或单-fiber checker，因为它们即使通过，也不能验证 family graph。
下一步必须先为一条 miss 边冻结一个 source cell、仿射 fiber policy 和 target fixed normals，
再构造可复算的 nonlinear support oracle。若连该最小 lifted-cell 也无法在硬约束内闭合，应停止
固定复杂度 terminal-family 支线，而不是增加 CZ 阶数掩盖类型错误。

证据等级：`information_family_type_obstruction_from_source_and_primary_full_text`。这不是该
lifted graph 的可行性、RCI、递归可行性或创新证明。
