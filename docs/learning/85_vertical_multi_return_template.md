# 85. 固定零修正下三种初始化 success return 的统一竖直相关模板

日期：2026-10-03。第84章只处理14条 miss 后的 `14->0 success`。本章把合同允许的
5/10/15 tick 首次成功测量在**每个先行 miss 均取 `deltaT=0`** 的基线下统一起来，并
严格区分 convex hull 与生成元直接拼接。该基线不是任意因果策略都必须经过的必要集合。

## 1. 三条互斥初始化路径

令 `m in {4,9,14}`。从 `mode=0,d=e-eta=0` 出发，在修正推力序列固定为全零时，经
`m` 条 miss 后完整 hidden estimator-error fiber 的形状精确等于 Run136 的 `E_m`，同时
可见偏移中心仍为 `d=(0,0)`。图中分别存在
`4->0`、`9->0`、`14->0` success 边。对每个源生成元使用第84章同一线性映射

```math
\begin{aligned}
\eta_p^+&=-n,\\
\eta_v^+&=-L\eta_p+(1-Lh)\eta_v+hr-Ln,\\
e_p^+&=\eta_p+h\eta_v,\\
e_v^+&=\eta_v+hr,
\end{aligned}
\qquad h=\frac1{50},\quad L=\frac92,
```

并令同一 `r` 同时进入 `eta_v^+` 和 `e_v^+`、同一 `n` 同时进入两个 estimator
坐标，得到三个中心为零的相关 zonotope `J_4,J_9,J_14`。三条历史路径互斥；每条路径
内部的共享原语生成元列绝不能拆开。后续取三集合的凸包时会允许不同路径点的分数凸混合，
因此不能把连续 `lambda` 误称为保持离散路径排他性。

## 2. 三个完整 return seed

| 源mode | 源/返回生成元数 | rank | `h_eta=(p,v)` | `h_e=(p,v)` | `h_d=(p,v)` |
|---:|---:|---:|---|---|---|
| 4 | 34 / 36 | 3 | `(1/50, 37857863/36000000)` | `(1004143/7200000, 101462161/72000000)` | `(1148143/7200000, 1148143/1600000)` |
| 9 | 69 / 71 | 3 | `(1/50, 204679321/288000000)` | `(42435007/144000000, 31802149/18000000)` | `(45315007/144000000, 45315007/32000000)` |
| 14 | 104 / 106 | 3 | `(1/50, 7329131969/7200000000)` | `(23312147/48000000, 152955031/72000000)` | `(24272147/48000000, 72816441/32000000)` |

三者逐生成元都满足

```math
d_v^+=L d_p^+.
```

因此每个 seed 都是四维空间中的三维集合。完整 `eta` 投影均落在 mode-0 vertical
estimator box

```math
|\eta_p|\le\frac1{50},\qquad
|\eta_v|\le\frac{37857863}{36000000},
```

完整真实误差投影均满足

```math
|e_p|\le1,\qquad |e_v|\le\frac{11}{4}.
```

这里不是有限采样：每个坐标支持都是对完整 exact-rational generator matrix 求绝对值和。

## 3. 单一最小凸 mode-0 模板

任何要同时容纳这三条**固定零修正** return image 的凸 mode-0 template，至少必须包含

```math
C_0=\operatorname{conv}(J_4\cup J_9\cup J_{14}).\tag{85.1}
```

因此式(85.1)是集合包含意义下的唯一最小凸容器。若

```math
J_m=\{G_m\xi_m:\|\xi_m\|_\infty\le1\},
```

则它有精确 perspective lift

```math
\begin{aligned}
C_0=\big\{&\sum_m G_m v_m:\ \lambda_m\ge0,\ \sum_m\lambda_m=1,\\
&-\lambda_m\mathbf1\le v_m\le\lambda_m\mathbf1,
\quad m\in\{4,9,14\}\big\}.\tag{85.2}
\end{aligned}
```

式(85.2)保留每个 `G_m` 内 residual/noise 生成元列的跨坐标耦合；`lambda` 阻止两个或
更多分量同时以单位尺度激活，因为 `sum lambda_m=1`。但它明确允许例如
`lambda=(1/2,1/2,0)` 的跨路径分数混合；这是 convex hull 的定义，不是 one-hot 路径选择。
它是标准凸合包 lift，不是新的集合算法。

对任意方向 `a`，

```math
h_{C_0}(a)=\max_{m\in\{4,9,14\}} h_{J_m}(a).
```

因此统一模板的坐标支持为

```math
h_\eta=\left(\frac1{50},\frac{37857863}{36000000}\right),
\qquad
h_e=\left(\frac{23312147}{48000000},\frac{152955031}{72000000}\right),
```

真实误差余量为

```math
\left(\frac{24687853}{48000000},\frac{45044969}{72000000}\right)>0.
```

拼接三组生成矩阵的精确秩仍为3，且式 `d_v=Ld_p` 对全部列成立；故 convex hull 没有
引入第四个仿射方向。由于 estimator box 是凸集且三组 seed 均包含于其中，`C_0` 也包含
于其中。

但 estimator 余量恰为

```math
(0,0).
```

位置方向由三组 seed 共同触边，速度方向由 `J_4` 触边。这意味着任何增加这两个方向支持的
full-dimensional thickening、普通 box inflation 或未经约束的 fixed-order outer reduction
都会立即失去当前 Run136 estimator certificate；后续 predecessor 必须使用精确低维/lifted
表示，或先重新证明一个更大的 estimator invariant family。

## 4. 为什么不能直接拼接生成元

把 `G_4,G_9,G_14` 横向拼接得到的不是式(85.1)，而是 Minkowski 和

```math
J_4\oplus J_9\oplus J_{14}.
```

其坐标支持为三者之和：

```math
h_\eta=\left(\frac3{50},\frac{10008843797}{3600000000}\right),
\qquad
h_e=\left(\frac{11037859}{12000000},\frac{31802149}{6000000}\right).
```

该集合同时违反 mode-0 estimator box 和 `|e_v|<=11/4`。这是**表示错误的精确负对照**，
不是对统一 convex template 的否定。后续若为了方便把三条路径压成单一 zonotope，必须给出
在零 estimator 余量下仍保持包含且不越界的独立证书；普通生成元合并不成立。

## 5. 证据等级与下一接口

证据等级为 **exact rank-three minimal convex template for three fixed-zero-correction
returns**。已证明：在先行 miss 修正推力全为零时，三条初始化 miss-chain 到达相应完整
fiber；三种 success 联合像均满足当前竖直 estimator/真值约束；它们的最小凸容器有精确
perspective lift、rank 3且仍满足约束；naive generator concatenation 失败。

未证明：这三条 image 对所有因果策略都是必达的；`C_0` 是 information ensemble、受控
不变集或任何 predecessor 的固定点；未处理水平/姿态、输入、terminal、移位和 MPC 递归
可行性。下一轮应先判断以式(85.2)为 target 的 predecessor 是否只是零策略自洽基线；若要
建立一般必要性，必须把由可见 `d` 选择的非零修正和其引起的中心平移显式纳入，而不能把
本章的零中心集合预先固定为所有策略共有的 target。
