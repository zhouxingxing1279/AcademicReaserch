# 124 测量条件化的极端信息集族

## 1. 问题与结论

Run189 证明，仅以物理包含约束六个 facet offsets 时，完整安全盒支配所有成员，真正 extreme-set 边界退化为单元素。本章改用实际可辨识的位置测量中心，回答更小的局部门槛：一个 source mode 是否至少能产生两个互不包含且对实际测量闭合的 extreme sets。

答案是肯定的，但必须纠正一个预算概念：**真正 extreme sets 是连续族，而六维 offset 参数域是一条只有两个顶点的线段。** 两个端点是 Houska §6.4 意义下可用的 finite extreme-vertex representatives，不是整个 extreme boundary。

证据等级为 `exact_measurement_conditioned_extreme_information_family`。这不是新算法，也不是动力学、控制或递归可行性证明。

## 2. 固定合同与时序

沿用 Run183 的竖直 tracking-error 安全盒与 success 测量：

\[
\mathcal X=[-P,P]\times[-V,V],\qquad
P=1,\quad V=\frac{11}{4},\quad a=\frac1{50}.
\]

success packet 揭示位置测量中心 \(\eta\)，其一致条带为

\[
\mathcal S(\eta)=\{(p,v):|p-\eta|\le a\}.
\]

本轮只研究测量求交 \(\mathcal X\cap\mathcal S(\eta)\)，不把后验估计误差当作未来过程扰动，也不改变 control-before-packet 的全图时序。

## 3. 全部非空 posterior 的精确覆盖

求交非空当且仅当

\[
\eta\in[-P-a,P+a]=[-51/50,51/50].
\]

定义 maximal center 区间

\[
\mathcal C=[-P+a,P-a]=[-49/50,49/50]
\]

和等宽矩形

\[
\mathcal R(c)=[c-a,c+a]\times[-V,V],\qquad c\in\mathcal C.
\]

若 \(\eta\in\mathcal C\)，则 \(\mathcal X\cap\mathcal S(\eta)=\mathcal R(\eta)\)。若 \(\eta\) 位于左右边界段，求交分别被 \(\mathcal R(-P+a)\) 或 \(\mathcal R(P-a)\) 包含。因此统一覆盖映射为

\[
c(\eta)=\operatorname{clip}(\eta,[-P+a,P-a]).
\]

外侧极限 \(\eta=\pm(P+a)\) 产生位置单点 posterior，也仍被相应端点矩形包含。

## 4. Information ensemble 与真正 extreme boundary

令

\[
\mathfrak E=\{K\in\mathbb K_c^2:\exists c\in\mathcal C,\ K\subseteq\mathcal R(c)\}.
\]

对任意紧集 \(Y\)，若 \(K\subseteq\mathcal R(c)\)，则 \(K\cap Y\subseteq\mathcal R(c)\)，故 \(K\cap Y\in\mathfrak E\)。因此 \(\mathfrak E\) 满足 Houska §3.1 的 information-ensemble 求交闭包。

两个等宽矩形的包含关系满足

\[
\mathcal R(c_1)\subseteq\mathcal R(c_2)
\iff c_1-a\ge c_2-a\ \land\ c_1+a\le c_2+a
\iff c_1=c_2.
\]

所以每个 \(\mathcal R(c)\) 都是包含极大成员，且

\[
\partial\mathfrak E=\{\mathcal R(c):c\in\mathcal C\}
\]

是连续族。特别地，端点 \(c=\pm49/50\) 给出两个互不包含的真实 extreme sets，Run189 的局部门槛通过。

## 5. 六方向 offsets 与有限参数顶点

对 \(q=p-v/10\)，facet 顺序为 `(+p,+v,-q,-p,-v,+q)`。矩形 \(\mathcal R(c)\) 的六个紧支持为

\[
y(c)=\left(c+a,V,-c+a+\frac{V}{10},-c+a,V,c+a+\frac{V}{10}\right).
\]

该映射关于 \(c\) 仿射，故参数域 \(\{y(c):c\in\mathcal C\}\) 是线段，只有两个参数顶点：

\[
y_- = \left(-\frac{24}{25},\frac{11}{4},\frac{51}{40},1,\frac{11}{4},-\frac{137}{200}\right),
\]

\[
y_+ = \left(1,\frac{11}{4},-\frac{137}{200},-\frac{24}{25},\frac{11}{4},\frac{51}{40}\right).
\]

两端矩形的凸包等于完整物理盒。这与 Houska 式(57)的 extrinsic convex-hull 表示一致，但不能把参数顶点数 `2` 写成真正 extreme-set 数。

## 6. 为什么还不能进入 mode graph

位置测量没有减小速度半宽：所有 maximal members 仍有 \(V=11/4\)。六方向中的斜 facets 虽是紧支持值，但对这些矩形是冗余约束，parameter segment 位于六-facet configuration cone 的退化边界。因此：

1. 本轮恢复了由真实测量驱动的 information differentiation；
2. 本轮没有获得 regular、非退化的六-facet `H/Omega` family；
3. Run184 的 velocity-radius Farkas 环没有被移除；
4. 不能由局部 measurement closure 推出移位可行、终端不变或闭环约束满足。

## 7. 下一步唯一问题

从一个斜 facet 与速度 facet 真正活跃的相关 source polytope 出发，精确构造其全连续测量 posterior family；判断该 family 是否仍能由有限、固定且非退化的 meta configuration 表示。只有该门槛通过，才值得重新进入一步 dynamics 或完整 mode graph。
