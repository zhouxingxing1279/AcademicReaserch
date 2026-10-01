# 成功周期提升的 zonotope 估计误差不变多集

日期：2026-09-29。承接 [第 72 章](72_time_uniform_estimator_multiset.md)。

**结论：对同一冻结六维 actual-input 估计误差 inclusion，可构造 15 模态 time-uniform 外不变多集：成功后的 mode 0 是精确有理数盒，后续年龄成员是保留有符号传播的 zonotope。17/17 原图边通过包含核查，全部坐标支持小于状态域半宽，因而估计误差 tightening 非空。它修复共同椭球的几何保守性，但不单独证明非线性残差全闭环自洽、ancillary RCI 或递归可行性。**

## 1. 为什么不能直接套有限和缩放定理

Athanasopoulos 等的图约束外不变多集 Theorem 2 和 Kouramas 等的 LDI 外 RPI Theorems 2--4 都以含原点内点的 C-set disturbance 为关键假设。当前逐拍映射

```math
\eta^+=A_\gamma\eta+G_\gamma\xi,\qquad \|\xi\|_\infty\le1
```

中的 `G_gamma[-1,1]^7` 是六维空间内的秩亏 zonotope；标签之间的扰动集合也不同。因此不能把文献的缩放公式当成本实例证书。本文改用图的确定返回周期，直接证明有限个 exact lifted inclusions。

## 2. 成功周期提升

mode 0 表示刚收到位置更新。合法下一次成功只可能经过 `L in {5,10,15}` 个 tick。令 `A_0,G_0` 为 miss edge，`A_1,G_1` 为 success edge。一个返回周期满足

```math
\eta_0^+=M_L\eta_0+v_L,
\qquad M_L=A_1A_0^{L-1},
\qquad v_L\in V_L,
```

其中 `V_L` 是沿该周期全部独立噪声生成元的精确 Minkowski 和。两个平移轴的 lifted homogeneous block 为

```math
M_L^{(x)}=\begin{bmatrix}0&0\\-5&1-0.1L\end{bmatrix},
\qquad
M_L^{(z)}=\begin{bmatrix}0&0\\-4.5&1-0.09L\end{bmatrix};
```

角度两行在 success 后齐次部分为零。这一步保留了 success innovation 中位置/速度项的符号抵消。

## 3. mode-0 盒的精确闭合

令 `B(b)={eta: |eta_i|<=b_i}`。对每个周期，zonotope `M_L B(b) oplus V_L` 包含于 `B(b)` 当且仅当六个坐标支持不超过 `b`。由于 lifted matrix 的稀疏结构，最小分量盒可逐轴精确求出：

```math
b_p=\max_L h_{V_L}(e_p),\qquad
b_v=\max_L\frac{|m_{vp,L}|b_p+h_{V_L}(e_v)}{1-|m_{vv,L}|}.
```

本实例得到

| 坐标 | `b_i` 精确值 | 十进制 |
|---|---:|---:|
| `p_x` | `1/50` | 0.020000 |
| `p_z` | `1/50` | 0.020000 |
| `v_x` | `245367017/160000000` | 1.533544 |
| `v_z` | `37857863/36000000` | 1.051607 |
| `phi` | `1/200` | 0.005000 |
| `omega` | `1/100` | 0.010000 |

`v_x` 的激活周期是 15 tick，`v_z` 的激活周期是 5 tick。验证器不是只检查最终数值；它对三个 `M_L B(b) oplus V_L subseteq B(b)` 分别重算生成元坐标支持。

## 4. 15 个年龄 zonotope 与逐边不变性

定义

```math
S_0=B(b),\qquad
S_j=A_0^jS_0\oplus\bigoplus_{i=0}^{j-1}A_0^iW_0,
\quad j=1,\ldots,14.
```

实现中不在中间年龄 boxing；`S_j` 保存为生成元矩阵。于是：

- 对 14 条 miss edge，`A_0S_j oplus W_0=S_{j+1}` 是生成元级等式；
- 对 `j=4,9,14` 的 success edge，分别对应 `L=5,10,15`，上一节的 lifted inclusion 给出 `A_1S_j oplus W_1 subseteq S_0`。

因此 17 条边全部成立，按逐边判据 `{S_j}_{j=0}^{14}` 是冻结 inclusion 的外不变多集。

## 5. 状态域兼容性与严格边界

最坏年龄 14 的坐标支持为：

| 坐标 | 支持半宽 | 状态域半宽 | 剩余半宽 |
|---|---:|---:|---:|
| `p_x` | 0.608088 | 5.000000 | 4.391912 |
| `p_z` | 0.444613 | 1.500000 | 1.055387 |
| `v_x` | 2.754283 | 3.000000 | 0.245717 |
| `v_z` | 2.052858 | 3.000000 | 0.947142 |
| `phi` | 0.005000 | 0.450000 | 0.445000 |
| `omega` | 0.010000 | 2.000000 | 1.990000 |

故 `X omin S_j` 对每个模式都非空，严格纠正 Run 135 共同椭球“所有模式 tightening 为空”的证书类失败。同一冻结模型/噪声下，mode 14 的共同椭球速度和角度支持下界分别约 10.285、7.182，而本证书为 2.754、0.005；该比较没有匹配计算预算，不能升级为性能贡献。

这里的“域兼容”只表示估计误差集合可被某个中心平移进原 state box。要让 nonlinear residual 外包在真实闭环中自洽，还必须由 nominal center、tracking error、actual thrust 与 ancillary policy 联合保证真实 `(x,u)` 留在 residual 源域。

## 6. 负对照：逐拍 boxing 会伪造发散

对 15-tick x 轴周期，真实有符号 lifted 速度系数绝对值为 `1/2`；若每拍先取矩阵绝对值再传播盒，系数变成 `23/10>1`。因此逐拍 interval-box fixed point 发散不能否定真实不变集合。该负对照被固定为回归测试，防止以后把几何丢失误写成系统不稳定。

## 7. 证据等级与下一接口

- **条件性解析证明：**上述 lifted box inclusion 与原图逐边等式推出冻结 inclusion 的 time-uniform 外不变多集。
- **精确算术证书：**矩阵、生成元、支持和域余量全部使用 `Fraction`；无浮点数参与通过判定。
- **未证明：**非线性全闭环 source-domain invariance、ancillary input/state RCI、terminal/shift、递归可行性与闭环性能。

复现：

```bash
PYTHONPATH=verification python -m unittest verification/test_cycle_lifted_zonotope.py -v
PYTHONPATH=verification python verification/check_cycle_lifted_zonotope.py --output /tmp/cycle_lifted_zonotope.json
```

下一唯一问题：把 `{S_j}` 的 exact coordinate/support oracle 接入第 71 章实际推力相关的联合 `(e,eta)` ancillary 图，在相同 state/input/residual 合同下构造或否定非空 mode-indexed RCI；禁止退回 scalar/common-metric `eta` 包。
