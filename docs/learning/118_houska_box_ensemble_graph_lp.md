# 118. Houska box information-ensemble 图 LP 的精确不可行证书

日期：2026-10-26。Run183 已把实际推力相关竖直 residual 可靠外包成固定 `W`。本章在同一
二维线性合同上实例化最小 axis-aligned box information-ensemble 基线，并回答它能否构成
15-mode terminal family。

## 1. 时序与模板

Houska 式(25)--(29)按“测量求交、选择控制、传播”写成；当前图则明确 current control 先于
success/miss successor edge。故本章对每个 source mode 只配置一组 extreme-set controls，先
生成 predicted ensemble，再对 miss 作 identity、对 success 作位置测量求交。mode 4/9 的两条
外出边因此严格复用同一 current controls。

令 `y=(u_p,u_v,-l_p,-l_v)`，box 为 `P(y)={x | Yx<=y}`，其中

```math
Y=\begin{bmatrix}1&0\\0&1\\-1&0\\0&-1\end{bmatrix},\qquad
G=\begin{bmatrix}-1&0&-1&0\\0&-1&0&-1\end{bmatrix}.
```

四个 `Lambda_i` 直接选取上下端点。meta 参数按

```math
z=(\bar r_p,\bar c_p,-\underline c_p,\bar c_v,-\underline c_v,\bar r_v)
```

排列，`Zy=(r_p,c_p,-c_p,c_v,-c_v,r_v)`。`H z<=0`要求两个中心区间非空及两个半径非负。
meta polytope 有16个顶点，但其 downward-closed ensemble 只有4个 maximal-radius中心角点是
extreme information sets。`Z`首行恰为`r_p=(y_1+y_3)/2`，所以 success 的位置噪声半宽
`1/50`直接成为式(25)的 measurement cap。

由于ensemble按包含关系向下闭，单纯把`r_p`截为`1/50`并保留原中心区间会漏掉预测盒边缘的
小集合。实现使用端点保持外包：若predicted/posterior参数分别为`bar z`/`zeta`，则要求

```math
\zeta_{c_p^+}+\zeta_{r_p}\ge \bar z_{c_p^+}+\bar z_{r_p},\qquad
\zeta_{-c_p^-}+\zeta_{r_p}\ge \bar z_{-c_p^-}+\bar z_{r_p},
```

并令`zeta_rp>=1/50`。这样靠近任一预测位置端点、半径不超过测量噪声的小集合仍被posterior
ensemble包含。该条件由独立复审提出的`pred=(1,0,0,0,0,1)`边界反例回归测试固定。

## 2. 因果图 LP

LP含498个变量和2772条不等式：90个source参数、90个predicted参数、60个source/extreme
controls、240个auxiliary box参数和18个success posterior参数。约束逐一覆盖：

- 15个source和predicted configuration cones；
- 每个source的4个extreme sets、每个set的4个state vertices；
- 固定过程扰动、硬状态盒、硬修正推力盒；
- 14条miss与3条success后继包含；
- success测量只在动力学传播之后作用。

HiGHS报告该LP不可行，但该数值状态本身不作为证据。检查器另外构造如下精确Farkas证书。

## 3. 21行精确Farkas证书

离散速度扰动半宽为

```math
\bar w_v=\frac{572143}{8000000}>0.
```

对每个source extreme box，把上速度vertex的`+v`动力学行、下速度vertex的`-v`动力学行、
两倍`Z`的速度半径包含行相加，控制与速度中心精确消去，得到

```math
\bar r_{v,q}^{\rm pred}\ge \bar r_{v,q}+\bar w_v.
```

miss复制全部meta坐标；success虽截断位置半径，却复制速度半径。再加两倍edge inclusion，
每条边均给出

```math
2\bar r_{v,q}-2\bar r_{v,q^+}\le-2\bar w_v.
```

沿最短合法环`0->1->2->3->4->0`，4条miss各用4行，success用5行，共21个非负乘子。
所有498个变量的系数逐项消为零，而右端精确为

```math
0\le-10\bar w_v=-\frac{572143}{800000},
```

矛盾。因此该axis-aligned box/meta-template在当前非零过程扰动和仅位置测量下不存在图不变
information ensemble；结论不依赖状态/输入约束是否活跃，也不是求解器容差现象。

## 4. 证据边界与方向纠正

证据等级为`exact_axis_aligned_box_information_ensemble_infeasibility_certificate`。它否定的仅是
不保留位置--速度相关性的axis-aligned boxes。位置序列本可通过动力学可观测性约束速度，但
box measurement update丢失这种斜相关，导致速度半径只能累加过程噪声。该结果不否定带斜
facets的configuration-constrained polytope、CZ或更丰富meta-template，也不证明MPC递归可行性。

下一唯一问题：在相同15-mode、`W/V`、硬约束及extreme-control权限下，加入最小的一对
position--velocity耦合法向，构造固定预算相关多面体模板；先检查它是否打破上述速度半径
Farkas环，再求图不变LP和exact primal/dual证书。
