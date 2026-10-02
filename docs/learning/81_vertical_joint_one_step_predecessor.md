# 81. 竖直联合信息集：三个关键模态的一步因果 predecessor 非空

日期：2026-10-02。本章承接第 80 章的坐标纠正，只回答 forced `14->0` success 与
mode 4/9 未知分叉是否在正确 joint candidate 下已经一步为空。结论是：**三者均包含一个
四维正体积内集**。这排除了 Run 142 的 product-fiber 一步阻塞，但不是 RCI、固定点或
完整六状态证书。

## 1. 最小约束导出候选

竖直坐标取

```math
s=(\eta_p,\eta_v,e_p,e_v),\qquad d=e-\eta.
```

令 `E_j` 为 Run 136 mode `j` 六维 zonotope 在 `(eta_pz,eta_vz)` 上的**精确投影**。
由物理状态域与 nominal hover box 的差得到

```math
B_e=\{e: |e_p|\le 1,\ |e_v|\le 11/4\}.
```

不引入任何额外形状参数，候选定义为

```math
S_j=E_j\times B_e. \tag{81.1}
```

式 (81.1) 是 `(eta,e)` 的 Cartesian product，但不是被第 79 章否定的
`E_eta x D`：这里没有给可见偏差 `d=e-eta` 独立限幅。第 80 章的相关 success 见证属于
`S_0`，即使其 `d_v` 超过旧 product 限幅。

固定可见 `d` 时，控制器面对的隐藏 fiber 是

```math
Q_j(d)=\{\eta:\eta\in E_j,\ \eta+d\in B_e\}. \tag{81.2}
```

对 mode `j` 的因果 predecessor 定义为

```math
\begin{aligned}
\operatorname{Pre}_j(S)=\{(\eta,e)\in S_j:\;&\exists\delta T=\kappa_j(d),\\
&\forall\tilde\eta\in Q_j(d),\ \forall(j,k,\ell)\in\mathcal E_j,\\
&\forall\rho_z,n:\ F_{jk}^{\ell}(\tilde\eta,\tilde\eta+d,
\bar T,\delta T,\rho_z,n)\in S_k\}.
\end{aligned}\tag{81.3}
```

同一 `d` fiber 和 mode 4/9 的全部未知后继边只能使用一个 `delta T`。

## 2. 精确正体积内集

取可见 observation box

```math
D_*=\{d:|d_p|\le1/5,\ |d_v|\le1/4\} \tag{81.4}
```

以及 mode-indexed joint set

```math
C_j=\{(\eta,e):\eta\in E_j,\ d=e-\eta\in D_*\}. \tag{81.5}
```

`E_j` 的二维精确面积与 `D_*` 的非空内点都严格为正；映射
`(eta,d)->(eta,e=eta+d)` 可逆，所以 `C_j` 是四维正体积 convex set。

对整个 (81.4) 采用同一可执行策略

```math
\delta T=0. \tag{81.6}
```

冻结 nominal thrust 区间为

```math
\bar T\in[1356943/160000,1782257/160000]
=[8.48089375,11.13910625]\ \mathrm N.
```

因此 actual thrust 等于 nominal thrust；共享余项半宽在区间上端达到

```math
\bar r_z=\frac{1043}{500}+\frac{81}{800}\frac{1782257}{160000}
=\frac{411370817}{128000000}\approx3.21383451, \tag{81.7}
```

严格小于 Run 136 对全 actuator 区间认证的 `572143/160000`。同一个 (81.7) 同时进入
`eta_v^+` 与 `e_v^+`，没有分裂 residual realization。

## 3. tracking-error 的解析包含

对任意 `d in D_*`，`Q_j(d)=E_j`，因为下表的 current-fiber 余量严格为正。由

```math
e_p^+=e_p+h e_v,\qquad e_v^+=e_v+h(r_z+\delta T)
```

及 (81.6)，最坏 target 余量为

```math
\begin{aligned}
m_p^+(j)&=1-h_{E_j}(1,h)-1/5-h/4,\\
m_v^+(j)&=11/4-h_{E_j}(0,1)-1/4-h\bar r_z.
\end{aligned}\tag{81.8}
```

精确结果：

| mode | `area(E_j)` | current `p` 余量 | current `v` 余量 | next `p` 余量 | next `v` 余量 |
|---:|---:|---:|---:|---:|---:|
| 4 | `41105550110953/240000000000000` | `1237120687/1800000000` | `41843563/36000000` | `4719857/7200000` | `63247363447/57600000000` |
| 9 | `327941991138173/720000000000000` | `107843563/200000000` | `57940691/72000000` | `72044993/144000000` | `42650215447/57600000000` |
| 14 | `1414311560032909/1440000000000000` | `1279394719/3600000000` | `2012141/4500000` | `14847853/48000000` | `22053067447/57600000000` |

所有量都严格正，mode 14 的最小 next 余量仍为位置约 `0.30933`、速度约 `0.38287`。

## 4. estimator 投影与未知分叉

检查器把每个二维 `E_j` 转为 exact H-polytope：每个非零 generator `g_i` 的垂直法向
给出 facet，右端由 `sum_i |n^T g_i|` 精确计算。随后逐 target facet 检查：

- miss：`A_m=[[1,h],[0,1]]`，共享 residual direction 为 `(0,h)`；
- success：`A_s=[[0,0],[-L,1-Lh]]`，另有 measurement-noise direction `(-1,-L)`；
- residual 半宽统一使用式 (81.7)，success noise 半宽为 `1/50`。

对 `4->5 miss`、`4->0 success`、`9->10 miss`、`9->0 success` 和
`14->0 success` 的全部 target facets，支持余量均非负。部分 facet 余量为零，是 Run 136
reachable zonotope 构造的边界相等，不影响包含。mode 4/9 的两条边在投影前固定使用同一个
`delta T=0`；不存在按 packet outcome 预知分支的输入。

因此精确包含关系为

```math
C_j\subseteq S_j\cap\operatorname{Pre}_j(S),\qquad j\in\{4,9,14\}. \tag{81.9}
```

## 5. 证据等级与止损

式 (81.9) 是 **three critical one-step predecessors 的 exact positive-volume inner
certificate**。它证明正确 joint 坐标下没有 Run 142 那种 mode-14 一步宽度阻塞，并证明
mode 4/9 分叉至少存在一个因果公共输入。

它没有证明：

1. `S_j` 的全部 fiber 都有可行输入；
2. 15 个 mode 的 descending predecessor 固定点非空；
3. `C_j` 自身跨时刻不变；
4. 水平/姿态/torque、terminal、shift 或 MPC 递归可行性；
5. 当前 boundary-tight input allocation 是最终可机动 nominal MPC 域。

下一步只能实现完整 15-mode joint predecessor 的一次 descending sweep，并报告保留下来的
observation-fiber 体积/投影；只有全模态非空后才准入固定点迭代。
