# C1：间歇测量误差接口兼容性核查

日期：2026-09-16。承接 [04 控制接口与有限调度环境规范](04_control_interface_and_finite_scheduler.md)。

**后续更新：[06 C2](06_mode_dependent_nestedness.md) 已完成六维与集合嵌套推导，并否定统一 Young 椭球收紧的原速度约束可行性。当前任务为 C2-R 模式条件半径传播；本文件末尾的 C2 清单保留为历史任务。**

## 1. 结论先行

C1 得到两个同时成立的结论：

1. **固定单一二次误差度量不能直接满足当前缺测 observer 的逐 tick 严格收缩。**
2. **利用已知的有限丢包自动机，可以显式构造 mode-dependent 二次度量，使所有允许模式边具有统一的严格收缩系数。**

因此当前间歇测量合同没有被理论反例否定，但不能把 Köhler–Müller–Allgöwer 原定理中的固定 (V_o) 记号原封不动套用。下一步需要把 mode-dependent 误差集合显式带入 set-membership 与 MPC tightening/nestedness 证明。

本轮没有训练 RL，没有改变原噪声、采样周期、最大丢包数或物理状态域。

## 2. 当前观测自动机

沿用 [06 因果增广模型](../theory/06_causal_augmented_model.md)：

- 位置包每 5 tick 有一次机会；
- 最多连续失败 2 次；
- 模式为 (sigma=(r,m))，共 15 个；
- 允许边共 17 条；
- 最大成功位置包间隔为 15 tick。

定义自上次成功位置更新后的 age

```math
j=5m+r\in\{0,1,\ldots,14\}.
```

成功位置包分别可能在 (L=5,10,15) tick 后到达。

水平位置观测速度增益沿用 06 的

```math
\ell_x=5,
```

竖直位置观测速度增益采用 08 已证明切换误差有界的

```math
\ell_z=9/2.
```

09 否定的是相应未限幅竖直**控制**候选的硬输入安全，不否定 08 的观测误差递推本身。

## 3. 单轴齐次误差模型

忽略有界扰动和测量噪声，只看用于收缩性的齐次部分。对任一平移轴，误差写成

```math
e=\begin{bmatrix}e_p\\e_v\end{bmatrix},
\qquad h=1/50.
```

没有位置校正时：

```math
e^+=A_0e,
\qquad
A_0=
\begin{bmatrix}
1 & h\\
0 & 1
\end{bmatrix}.
```

成功位置校正时：

```math
e^+=A_1(\ell)e,
\qquad
A_1(\ell)=
\begin{bmatrix}
0 & 0\\
-\ell & 1-\ell h
\end{bmatrix}.
```

成功间隔为 (L) 时，从上一次成功后的状态到下一次成功后的 lifted map 为

```math
M_L(\ell)
=
A_1(\ell)A_0^{L-1}
=
\begin{bmatrix}
0&0\\
-\ell&1-\ell Lh
\end{bmatrix}.
```

这与 08 中成功包速度误差系数

```math
a_L=1-\ell Lh
```

一致。

## 4. 固定二次度量的解析阻断

设希望存在固定 (P\succ0) 和 (eta<1)，使缺测步满足

```math
A_0^\top P A_0\preceq\eta P.
```

取

```math
v=\begin{bmatrix}1\\0\end{bmatrix}.
```

由于

```math
A_0v=v,
```

故

```math
v^\top A_0^\top P A_0v
=
v^\top Pv>0.
```

若上述严格收缩成立，则同时要求

```math
v^\top Pv\le\eta v^\top Pv,
```

即 (1\le\eta)，与 (eta<1) 矛盾。

所以**不存在任何固定正定二次度量能够在每一个无位置测量 tick 上严格收缩**。这解释了为什么 08 只能得到成功包之间的多步收缩，而不能直接声明满足主参考的固定逐步 observer 假设。

## 5. 模式相关二次度量的显式构造

取齐次每边收缩系数

```math
\eta_0=19/20.
```

定义

```math
P_{\nu,0}
=
\begin{bmatrix}
p_\nu&0\\0&1
\end{bmatrix},
```

其中

```math
p_x=120,
\qquad
p_z=60.
```

对 age (j=0,\ldots,14)，定义

```math
P_{\nu,j}
=
\eta_0^j
A_0^{-j\top}
P_{\nu,0}
A_0^{-j},
\qquad \nu\in\{x,z\}.
```

每个 (P_{\nu,j}\succ0)。

### 5.1 所有缺测边精确满足统一收缩

对 (j=0,\ldots,13)：

```math
A_0^\top P_{\nu,j+1}A_0
=
\eta_0P_{\nu,j}.
```

这不是数值近似，而是由定义直接得到的有理数恒等式。

### 5.2 成功边化成三个 lifted LMI

成功发生在 (j=L-1)，其中 (L\in\{5,10,15\})。要求

```math
A_1(\ell_\nu)^\top
P_{\nu,0}
A_1(\ell_\nu)
\preceq
\eta_0P_{\nu,L-1}.
```

与

```math
M_L(\ell_\nu)^\top
P_{\nu,0}
M_L(\ell_\nu)
\preceq
\eta_0^LP_{\nu,0}
```

等价。

由于

```math
M_L=
\begin{bmatrix}
0&0\\-\ell&a_L
\end{bmatrix},
```

上述 (2\times2) LMI 可化为标量充分且必要条件

```math
p_\nu\bigl(\eta_0^L-a_L^2\bigr)-\ell_\nu^2\ge0.
```

精确核查结果如下。

| 轴 | (L) | (a_L) | 标量余量 |
|---|---:|---:|---:|
| x, (ell=5,p=120) | 5 | (1/2) | (3028297/80000>0) |
| x | 10 | (0) | (11993198773403/256000000000>0) |
| x | 15 | (-1/2) | (487381089624394897/819200000000000000>0) |
| z, (ell=9/2,p=60) | 5 | (11/20) | (1284297/160000>0) |
| z | 10 | (1/10) | (7717998773403/512000000000>0) |
| z | 15 | (-7/20) | (323541089624394897/1638400000000000000>0) |

最紧的是 15 tick 分支，但余量仍严格为正。

所以对全部 17 条允许模式边，平移齐次误差都存在统一的 mode-dependent quadratic multinorm contraction。

## 6. 有界扰动下的统一标量递推

实际误差还有有界过程余项和测量噪声，可统一写为

```math
e^+
=
A_\gamma e+G_{\sigma,\gamma}d.
```

已经证明齐次部分满足

```math
\|A_\gamma e\|_{P_{\sigma'}}^2
\le
\eta_0\|e\|_{P_\sigma}^2,
\qquad \eta_0=19/20.
```

使用 Young 不等式

```math
\|a+b\|^2
\le
(1+\epsilon)\|a\|^2
+
(1+1/\epsilon)\|b\|^2.
```

选

```math
\epsilon=4/95,
```

则

```math
(1+\epsilon)\eta_0=99/100.
```

且

```math
1+1/\epsilon=99/4.
```

因此每条允许边都有

```math
V_{\sigma'}(e^+)
\le
\frac{99}{100}V_\sigma(e)
+
\frac{99}{4}
\|G_{\sigma,\gamma}d\|_{P_{\sigma'}}^2.
```

由于模式集合和边集合有限，定义

```math
c_d=
\frac{99}{4}
\max_{(\sigma,\sigma')}
\lambda_{\max}
\left(
G_{\sigma,\gamma}^\top
P_{\sigma'}
G_{\sigma,\gamma}
\right),
```

即可得到统一的可靠递推

```math
e_{t+1}
\le
\frac{99}{100}e_t
+
c_d\|d_t\|_2^2.
```

若 (|d_t|\le\bar d)，则可取

```math
\sigma_4(\bar d)=c_d\bar d^2.
```

这已经具备 04 所需的“单调标量未来传播”结构。

## 7. 对六维估计的含义

当前 (phi,omega) 每 tick 都有直接有界测量。可以把 estimator 写成：

```math
\hat x_t=
(\hat p_x,\hat p_z,\hat v_x,\hat v_z,y_t^\phi,y_t^\omega).
```

则角度与角速度的下一步齐次估计误差在直接测量更新后为零，噪声作为 additive term 进入；平移齐次部分由上面的两个 mode-dependent (2\times2) 块控制。

因此本轮结果说明：**六维 observer 的主要结构性阻断不是“间歇测量必然无法稳定”，而是“必须使用模式相关误差度量，不能假装存在固定逐 tick 收缩椭球”。**

不过完整六维 (G_{\sigma,gamma})、统一 (c_d)、状态域上的上下界常数 (alpha_5,alpha_6) 还需正式实例化后才能称为完整 Assumption-3-style certificate。

## 8. 与主参考的关系

主参考的 Assumption 3 使用逐步鲁棒 observer inequality，并在 observer 设计讨论中明确提到 time-varying (V_o) 可以用于某些 observer。其 MPC 递归可行证明真正依赖的是：

- 当前误差确实被可靠 (e_t) 覆盖；
- 下一时刻界不超过预测的 (e_{1|t})；
- (e,s) 的未来传播具有单调性；
- 收紧集合满足相应 nestedness。

本轮 mode-dependent 构造已经提供统一的标量收缩递推，但原文的 MPC 约束写成固定 (V_o(\hat x,x)\le e)。因此仍需做一层适配，不能直接把本轮结果称为 Theorem 4 已满足。

可以采用的下一接口是

```math
\mathcal E_\sigma(e)
=
\{z:z^\top P_\sigma z\le e\},
```

并对未知未来测量模式使用

```math
\mathcal E_{\mathrm{all}}(e)
=
\bigcup_{\sigma\in\Sigma}\mathcal E_\sigma(e).
```

因为对任意固定模式，(e'\le e) 都有

```math
\mathcal E_\sigma(e')\subseteq\mathcal E_\sigma(e),
```

故 union 也保持关于标量 (e) 的单调嵌套。是否用这一 union 直接收紧，还是推导更紧的 mode-conditioned future tube，应在下一步比较。

## 9. 对验证调度候选库的更新

04 中固定二次度量 (P_o=L^\top L) 的候选库需要改成**当前模式相关**：

```math
P_{\sigma}=L_\sigma^\top L_\sigma,
```

在线当前模式 (sigma_t) 已知，因此本周期候选任务为

```math
\mathcal A_t
=
\{+\ell_{\sigma_t,r},-\ell_{\sigma_t,r}\}_r
\cup\{\mathrm{STOP}\}.
```

认证标量仍定义为

```math
e_t^{\mathrm{cert}}
=
\sum_r
\max\{b_{r,+},b_{r,-}\}^2,
```

所以 04 的“方向证书 → 标量界 → RL 只能改善效率而不能签发安全边界”逻辑保持不变，只是候选方向随已知 observer mode 变化。

## 10. 精确核查

运行：

```bash
python verification/check_intermittent_metric.py \
  --output /tmp/intermittent_metric.json
```

脚本只使用 Python 标准库与 `Fraction`，核查：

- 固定 metric 的解析阻断；
- 15 个 mode metric 的正定性；
- 14 类连续缺测边的精确等式；
- (L=5,10,15) 成功边的全部 lifted LMI；
- 水平/竖直两轴的严格余量；
- Young 参数恒等式。

归档结果见 [exact_checks.json](../../results/theory_intermittent_metric_20260916/exact_checks.json)。

## 11. C1 状态与下一任务

C1 不再判定为“控制基础直接失败”，而是：

- **固定 (V_o) 直接套用：否定；**
- **有限模式相关 (V_{o,\sigma}) 的统一标量递推：构造性通过；**
- **将 mode-dependent metric 接入 set-membership/MPC 的完整递归可行证明：未完成。**

下一唯一任务记为 **C2：mode-dependent 估计集合到 MPC 的 nestedness 与收紧接口**：

1. 正式构造六维 (P_\sigma)、(G_{\sigma,\gamma})、(alpha_5,alpha_6,c_d)；
2. 比较 future-mode union envelope 与 mode-conditioned tube；
3. 证明在线 verifier 给出的 (e_t^{\mathrm{cert}}) 可作为该递推初值；
4. 重写 Theorem-4 所需的误差集合 nestedness 步骤，明确哪些条件可原样继承、哪些需要扩展；
5. C2 通过前仍不启动 Double DQN。

C2 之后才有资格实例化真实候选方向、做更大的有限调度基准，并判断是否值得进入 RL 训练。
