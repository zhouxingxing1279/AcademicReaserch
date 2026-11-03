# 97. `k=14` 安全必要条件的三因素精确权衡

## 1. 参数化必要条件

沿用第96章的 `J14` seed、竖直双积分器与14次 miss。令

- `alpha`：seed 在控制相关方向 `a=e_p+14h e_v` 上的半直径缩放；对一般非中心对称集合
  `X`，该量是 `[h_X(a)+h_X(-a)]/2`，不是单侧支持；
- `beta`：未来 residual 半宽相对当前 global bound 的缩放；
- `gamma`：correction authority `U` 的缩放。

精确分离 seed、future residual 与 bounded input 后，第96章的镜像轨迹论证给出

```math
L_{14}(\alpha,\beta,\gamma)
=\alpha S_{14}+\beta D_{14}-\gamma C_{14}\le1,
```

其中

```math
S_{14}=\frac{3889781459}{3600000000},\qquad
D_{14}=C_{14}=\frac{52065013}{400000000}.
```

`D_14=C_14` 不是一般性质，而是当前参数恰有 `g_r=hU`。因此 baseline
`(alpha,beta,gamma)=(1,1,1)` 的 residual 增长与最乐观输入削减精确相消，下界完全由 seed
方向半直径决定：`L_14=S_14≈1.08049485`。

## 2. 单因素阈值

固定其余两项为 baseline，必要边界为：

| 可改单因素 | 必要阈值 | 相对变化 |
|---|---:|---:|
| seed directional half-diameter | `alpha <= 3600000000/3889781459 ≈ 0.925502` | 至少缩小 `7.4498%` |
| future residual | `beta <= 16254878/42598647 ≈ 0.381582` | 至少缩小 `61.8418%` |
| correction authority | `gamma >= 68942416/42598647 ≈ 1.618418` | 至少增加 `61.8418%` |

最后一项要求 `U>=47397911/8190000≈5.78729`。这些阈值只让一个必要位置半径条件取等，
并不证明速度约束、输入实现、success branch、target inclusion 或递归可行性。

更一般地，全部混合修改必须落入同一个半空间

```math
\alpha\frac{3889781459}{3600000000}
+(\beta-\gamma)\frac{52065013}{400000000}\le1. \tag{97.1}
```

该式可作为后续设计的拒绝门槛，但不能作为可行性证书。

## 3. 哪个量能由在线集合信息合法改变

| 对象 | 当前 SMF 可直接改变？ | 保证边界 |
|---|---|---|
| realized state seed half-diameter `alpha` | 可以 | 测量求交可缩小当前真状态后验的方向宽度；必须同时查询 `a` 和 `-a`，保留真值包含，并对未达到阈值的测量结果提供 fallback |
| future residual set `beta` | 不可以 | 状态估计误差不是未来扰动；只有另行建立 disturbance/model set estimator、持久性假设及未来有效包含，才可缩小 |
| physical correction authority `gamma` | 不可以 | 这是执行器/名义输入分配合同；重分配还必须重新检查 nominal feasibility 和总输入硬约束 |

所以本轮唯一与“可靠在线集合信息降低保守性”直接相连的候选，是查询当前联合后验在
`±(e_p+14h e_v)` 两个方向的支持，以方向半直径比 `alpha<=0.925502` 作为15-tick constituent
的必要 admission gate。后验方向中心 `[h_X(a)-h_X(-a)]/2` 不影响镜像直径下界，但仍会影响
绝对硬约束，必须在后续充分安全检查中处理。要得到统一闭环结论，还需证明：未通过 gate 时可
安全回退到短 dropout 合同；通过后完整路径与 terminal/shift 条件均闭合。

## 4. 证据边界与方向判断

证据等级为 `exact_k14_three_factor_necessary_tradeoff_and_information_interface_audit`。它把当前
不可行性的最小合同修改量定量化，并阻止把 posterior contraction、future disturbance reduction
和 actuator authority 混为一谈；它不是新 MPC 算法，也不是充分可行性、RCI、递归可行性或
六自由度保证。

