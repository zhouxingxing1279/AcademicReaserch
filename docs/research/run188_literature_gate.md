# Run188 文献准入卡：六 facet meta 坐标自由度门槛

日期：2026-10-27。远端基线为 Run187 `d33c985`（tree `c4bbf0f2`），远端
`main=1c49659`。

| 最近邻 | 本轮实际阅读 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Houska, *Intrinsic Separation Principles*, Automatica 183 (2026), 112661；arXiv:2307.04146 | **重读 §6.1--6.5、式(25)--(27)、Definition 7、Theorem 3及证明** | `Z`的选择决定polytopic ensemble离散化；`H/Omega`固定参数多面体的configuration与极点，极端信息集逐个配置控制。 | 换一组线性meta坐标本身不是新方法；必须证明表示域、闭包与极点预算。 |
| Villanueva--Müller--Houska, *Configuration-Constrained Tube MPC*, Automatica 163 (2024), 111494；arXiv:2208.12554 | **重读 §3.4--3.5、Definition 6、Lemma 1、Theorem 1及vertex-domain构造** | 固定facet参数`y`的configuration domain是多面锥，锥内存在固定线性vertex maps。 | Run186的六offsets是完整六维参数；任何降维坐标必须证明不丢失configuration内合法集合。 |
| Raghuraman--Koeln, *Set operations and order reductions for constrained zonotopes*, Automatica 139 (2022), 110204；arXiv:2009.06039 | **精读 §2、§3开头、式(1)--(3)、Theorem 4相关表示讨论** | 普通zonotope中心对称；CZ用等式约束打破对称性，可表示任意凸多面体，并对generalized intersection闭合。 | “中心＋半径”丢失非中心对称后验是已知表示限制，不构成创新；CZ是后续强基线。 |
| Robbins--Glunt--Thompson--Pangborn, *Online Constraint Tightening for MPC using Constrained Zonotope Reachability Analysis and Zonotope Over-Approximations* (2026) | **仍仅取得正式摘要** | 摘要层面覆盖CZ reachability驱动在线收紧。 | 不据摘要判断定理或首次性，本轮不作CZ tightening声明。 |

## 候选、证伪条件与最强基线

对offset顺序`(+p,+v,-q,-p,-v,+q)`，比较：

1. **direct offsets**：保留六维`y`，完整覆盖Run186 configuration cone；
2. **五参数center/radius**：`(c_p,c_v,r_p,r_v,r_q)`并强制斜向中心
   `c_q=c_p-kappa*c_v`；
3. **六参数center/radius/skew**：另保留`c_q`或
   `delta=c_q-c_p+kappa*c_v`。

若一次合法位置measurement intersection能从`delta=0`产生`delta!=0`且结果仍在同一
configuration cone，则候选2不闭合。若候选3到direct offsets存在可逆线性映射，则对同一个
参数多面体，其`H`与所有`Omega`仅作坐标变换，极点数不变，不能仅凭坐标声称预算优势。

最强同条件基线是Houska的任意`Z/H/Omega` polytopic ensemble；CZ则是允许非中心对称交集的
替代表示。只有某个受约束的meta多面体在相同覆盖与硬约束下减少极端信息集，才可谈预算优势。

## 准入判断

**通过“meta坐标自由度与测量闭包的精确方向纠正证书”；不通过“center/radius降低预算是创新”
或“已构造exact `H/Omega`”。** 本轮允许写最小有理数checker，固定五参数反例、六参数可逆性和
同一参数多面体极点数不变性；不进入15-mode/17-edge LP。
