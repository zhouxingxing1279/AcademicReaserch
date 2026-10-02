# 84. 初始化路径的竖直相关 return seed

日期：2026-10-03。本章纠正第83章末尾的下一问题：在当前初始化合同下，不能先把
mode-14 的 `q|d` 纤维压窄；正确对象是强制 success 后由测量创新产生的相关联合像。

## 1. 为什么不能先压缩 mode-14 条件纤维

合同要求初始 `mode=0,d=e-eta=0`。零 correction 下，miss 边满足

```math
d^+=A_d d,qquad A_d=\begin{bmatrix}1&h\\0&1\end{bmatrix}.
```

因此同一初始化 observation history 经14条 miss 后仍有 `d=0`，而 hidden estimator
error 的完整 reachable set 恰为 Run 136 的 `E_14`。对

```math
q=\eta_p+h\eta_v,qquad h=1/50,
```

其精确支持半宽为

```math
h_{E_{14}}(1,h)=\frac{23312147}{48000000}\approx0.4856697292.
```

这正是第80章已经证明的初始化可达性事实。故把 `q|d=0` 压到第79章的 product 门槛
以下，会排除合同必须包含的真实初始化路径。

## 2. 强制 success 的共享原语联合像

在 mode 14 取 `d=0` 和 `delta T=0`，下一边被合同强制为 `14->0 success`。令
`L=9/2`，下一位置噪声为 `n`，物理余项为 `r`。对每个源点
`(eta_p,eta_v) in E_14`，正确的 `(eta,e)` 更新为

```math
\begin{aligned}
\eta_p^+&=-n,\\
\eta_v^+&=-L\eta_p+(1-Lh)\eta_v+hr-Ln,\\
e_p^+&=\eta_p+h\eta_v,\\
e_v^+&=\eta_v+hr.
\end{aligned}\tag{84.1}
```

式 (84.1) 中同一个 `r` 同时进入 `eta_v^+` 与 `e_v^+`，同一个 `n` 同时进入两项
estimator error；不得分别采样或装箱。直接把 Run 136 mode-14 的104个生成元映射，再加
一个共享 residual 列和一个共享 measurement-noise 列，得到106列的精确四行 zonotope
生成矩阵 `J_0^ret`。

## 3. 精确秩与约束包含

有理数高斯消元给出

```math
\operatorname{rank}(J_0^{ret})=3.
```

低一维不是退化实现错误。由 `d=e-eta`，每个生成元都满足

```math
d_v^+=L d_p^+.\tag{84.2}
```

所以 return seed 位于四维空间中的三维仿射子空间。它是完整可达信息集，不是一条采样
轨迹；但也不能被称为四维正体积 joint candidate。

完整联合像的 estimator-error 支持为

```math
h_{\eta_p}=\frac1{50},\qquad
h_{\eta_v}=\frac{7329131969}{7200000000}.
```

相对 Run 136 mode-0 竖直盒，余量分别为

```math
0,qquad \frac{242440631}{7200000000}>0.
```

真实 tracking-error 支持为

```math
h_{e_p}=\frac{23312147}{48000000},\qquad
h_{e_v}=\frac{152955031}{72000000}.
```

相对 hover source-domain 给出的 `|e_p|<=1, |e_v|<=11/4`，余量为

```math
\frac{24687853}{48000000}>0,qquad
\frac{45044969}{72000000}>0.
```

因此不是单个极值见证，而是**整个**强制 return image 都满足当前竖直 estimator 与真值
约束。

## 4. 为什么 product target 会误拒绝该集合

`J_0^ret` 的可见偏差投影支持为

```math
h_{d_p}=\frac{24272147}{48000000},qquad
h_{d_v}=\frac{72816441}{32000000}.
```

第83章 Run146 的 product `D_0^0` 速度半宽只有

```math
\frac{94125081847}{57600000000},
```

故 `d_v` 严格超出

```math
\frac{36944511953}{57600000000}\approx0.641398.
```

但式 (84.1) 保留了 `eta_v^+` 与 `d_v^+` 的反向创新相关性，真实 `e_v^+` 仍满足硬约束。
这把第80章的单点反例升级为完整可达集合证书，并说明第83章的塌缩来自 product
分解，不是初始化路径本身不可行。

## 5. 证据等级与下一接口

证据等级为 **exact rank-three correlated return seed for the required initialization
path**。已证明：14条 miss 精确到达完整 `E_14`；强制 success 的共享原语联合像秩为3；
其完整 `eta` 和 `e` 投影满足当前竖直约束；它严格违反 Run146 的独立 `d_v` 限幅。

未证明：该 seed 或其外包受控不变、非零 correction 下仍保持式 (84.2)、其余 success
周期、水平/姿态耦合、输入/终端/移位或 MPC 递归可行性。

下一步不再追求 mode-14 `q|d` 压缩。唯一问题是对初始化可发生的5/10/15 tick 三种
success return 都构造同语义的相关 seed，并判断是否存在一个满足真实约束、保留三者
共享原语的单一 mode-0 模板；只有该门槛通过，才准入 controlled predecessor 综合。
