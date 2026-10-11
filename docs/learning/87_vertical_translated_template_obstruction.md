# 87. Run148 translated fixed-shape family 的竖直宽度阻塞

日期：2026-10-03。第85章构造了固定零修正三条初始化 return 的最小凸容器

```math
C_0=\operatorname{conv}(J_4\cup J_9\cup J_{14}).
```

第86章进一步证明，在 Run136 固定 global residual envelope 下，correction 只改变联合
`(\eta_p,\eta_v,e_p,e_v)` 集合的中心。本章检查任意中心平移能否使该 shape 闭合三条
success return。

## 1. 候选 shape family

令 `gamma=572143/8000000` 为 Run136 的一步竖直 residual 生成元。对任意中心为零的
联合 shape `C`，定义 miss shape map

```math
\Phi_0(C)=M_0C\oplus[-g_r,g_r],
\quad
M_0=\begin{bmatrix}
1&h&0&0\\0&1&0&0\\0&0&1&h\\0&0&0&1
\end{bmatrix},
\quad g_r=(0,\gamma,0,\gamma)^\top .
```

令 `C_j=Phi_0^j(C_0)`。由于线性像和同一个 convex disturbance Minkowski sum 可与有限
凸合包交换，每个 `C_j` 仍可精确表示为3个 centered zonotope 分量的凸合包；三个分量在
mode 0 的列数为 `(36,71,106)`，每次 miss 各增加一列。

success shape map 为

```math
\Phi_1(C)=M_1C\oplus[-g_r,g_r]\oplus[-g_n,g_n],
```

其中

```math
M_1=\begin{bmatrix}
0&0&0&0\\-L&1-Lh&0&0\\0&0&1&h\\0&0&0&1
\end{bmatrix},
\quad g_n=(-1/50,-9/100,0,0)^\top .
```

因此 modes 4、9、14 的 success image 三个分量列数分别为
`(42,77,112)`、`(47,82,117)`、`(52,87,122)`。这保留每条 path 内的共享 residual/noise
原语；没有把 convex hull 错写成生成元拼接的 Minkowski 和。

任意 correction `deltaT` 对两类边都只增加

```math
b\,\delta T=(0,0,0,h\delta T)^\top .\tag{87.1}
```

故它和 source/target centers 一样只产生平移，不改变 shape。

## 2. 平移包含的必要宽度条件

对紧集 `S,T`，若存在任意平移 `s,t` 使

```math
S+s\subseteq T+t,
```

则对每个方向 `a` 必须有

```math
\operatorname{width}_S(a)
=h_S(a)+h_S(-a)
\le h_T(a)+h_T(-a)
=\operatorname{width}_T(a).\tag{87.2}
```

`C_j` 和 `Phi_1(C_j)` 都是 centered symmetric convex sets，所以式(87.2)等价于比较
support 半宽。选取 `a=(0,0,1,0)`，即真实位置误差 `e_p` 方向。式(87.1)在该方向投影为零，
因此 current correction 也不能改变该半宽。

目标 shape 的精确半宽为

```math
h_{C_0}(a)=\frac{23312147}{48000000}\approx0.4856697292.
```

三个 return image 的 exact-rational 结果为：

| edge | success `e_p` 半宽 | 相对 `C0` 的严格超量 |
|---|---:|---:|
| `4->0 success` | `51293581/72000000` ≈ 0.7124108472 | `32650721/144000000` ≈ 0.2267411181 |
| `9->0 success` | `14038717/14400000` ≈ 0.9749109028 | `70450729/144000000` ≈ 0.4892411736 |
| `14->0 success` | `12222431/9600000` ≈ 1.2731698958 | `4725001/6000000` ≈ 0.7875001667 |

三项超量均严格为正。因此对任意 source center、target center 和 admissible current
correction，均有

```math
\Phi_1(C_j)+b\delta T+c_j\not\subseteq C_0+c_0,
\qquad j\in\{4,9,14\}.\tag{87.3}
```

这不是有限法向猜测：单个方向已经给出所有平移包含都必须满足、但被精确违反的必要条件。

## 3. mode 4/9 的共享输入语义

mode 4 和9各有未知的 miss/success 分叉。两条 successor 必须使用同一个当前
`deltaT=kappa(d,z,bar u)`。按定义，miss 零中心 shape `Phi_0(C_j)` 精确等于
`C_{j+1}`；非零 correction 仍只改变其中心。可是 success 单边已经被式(87.3)否定，
所以不存在能同时满足 miss 与 success 的共享 current input。该结论没有为两个 packet
outcome 偷用两套输入，也没有让控制读取隐藏 `eta`。

## 4. 证据等级与方向纠正

证据等级为 **exact `e_p` width obstruction for the Run148 translated fixed-shape
family**。已否定：以单一 `C0` 为 mode-0 intrinsic shape、由其 miss propagation 生成
`C_j`、仅优化 centers/current correction 的 family。最早阻塞发生在 mode 4，而不是等到
mode 14。

未否定：mode/history-conditioned intrinsic shapes、非平移 shape adaptation、一般
information ensemble、scheduled `W(T)` 的 decision-dependent family、六状态 RCI、terminal
或 MPC 递归可行性。特别地，scheduled residual 会改变历史 shape；本章只说明“在既定
Run148 shape 上优化当前中心或 current correction”不可能修复 `e_p` 宽度。

因此下一步不应立即启动昂贵 GSIP，也不应继续枚举 `C0` 的更多中心或法向。唯一优先问题是
构造最小 **return-age/history-conditioned intrinsic shape family**，使三条 success target
不再被强制压回同一个 `C0`；先用 exact support 检查其有限周期 fixed point，只有该骨架
存在后才评估 scheduled residual tightening 的计算收益。
