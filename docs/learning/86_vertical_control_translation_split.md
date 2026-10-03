# 86. 竖直控制平移与推力相关余项的形状分离

日期：2026-10-03。第85章的零中心 `C0` 只能是零修正基线。本章进一步说明：它的**形状**
何时可作为任意策略的中心化代表，以及保留推力调度余项时为什么该结论失效。

## 1. 一步竖直联合动力学

令

```math
\eta=x-\hat x,\qquad d=\hat x-z,\qquad e=x-z=\eta+d,
```

采样时间 `h=1/50`，位置校正增益 `L=9/2`，修正推力为 `deltaT`，物理余项 realization
为 `r`。对 miss 边，

```math
\begin{aligned}
\eta_p^+&=\eta_p+h\eta_v,&
\eta_v^+&=\eta_v+hr,\\
d_p^+&=d_p+hd_v,&
d_v^+&=d_v+h\delta T,\\
e_p^+&=e_p+he_v,&
e_v^+&=e_v+h(\delta T+r).
\end{aligned}\tag{86.1}
```

对 success 边，令下一位置噪声为 `n`，

```math
\begin{aligned}
\eta_p^+&=-n,\\
\eta_v^+&=\eta_v+hr-L(\eta_p+h\eta_v+n),\\
d_p^+&=e_p+he_v+n,\\
d_v^+&=d_v+h\delta T+L(\eta_p+h\eta_v+n),\\
e_p^+&=e_p+he_v,\\
e_v^+&=e_v+h(\delta T+r).
\end{aligned}\tag{86.2}
```

精确有理数检查对两类边都验证 `e^+=eta^++d^+`。式(86.1)--(86.2)中的 `r` 是同一
物理 realization，不得在 `eta` 与 `e` 中独立采样。

## 2. 固定绝对余项集合：控制只改变中心

先固定绝对余项集合 `r in [-rbar,rbar]`。对同一当前 fiber、同一 `r,n`，比较两个修正
`deltaT_a,deltaT_b`。两类边都精确满足

```math
\Delta\eta^+=(0,0),\qquad
\Delta e^+=\Delta d^+=\left(0,h(\delta T_b-\delta T_a)\right).\tag{86.3}
```

因此 correction 不改变联合生成元矩阵，只平移 `e_v,d_v` 中心。这与 Houska
Theorem 1 的固定 `W` intrinsic-separation 接口一致：不同控制策略得到的 tight information
tube 可以具有相同 intrinsic shape，但 extrinsic translations 不同。故第85章的中心化
`C0` 不是所有策略必须包含的集合；在固定 global envelope 下，其生成元形状可作为后续
`C0+c` 模板的候选。

## 3. 推力调度余项：控制同时改变形状

真实合同使用

```math
T=\bar T+\delta T,\qquad
r_z(T)=\left(\frac{1043}{500}+\frac{81}{800}T\right)\rho_z,
\quad |\rho_z|\le1.\tag{86.4}
```

同一 `rho_z` 在联合 `(eta_p,eta_v,e_p,e_v)` 中产生共享列

```math
g_r(T)=\left(0,h\bar r_z(T),0,h\bar r_z(T)\right).\tag{86.5}
```

当前实际推力区间恰为

```math
T\in\left[\frac{981}{200},\frac{2943}{200}\right]=[4.905,14.715]\ \mathrm N.
```

端点余项半宽与一步生成元为

```math
\begin{array}{c|cc}
T & \bar r_z(T) & h\bar r_z(T)\\ \hline
981/200 & 413221/160000 & 413221/8000000\\
2943/200 & 572143/160000 & 572143/8000000.
\end{array}
```

生成元严格增加

```math
g_r(T_{max})-g_r(T_{min})=
\left(0,\frac{79461}{4000000},0,\frac{79461}{4000000}\right)\ne0.\tag{86.6}
```

所以 scheduled residual 下控制不仅平移中心，也改变 `(eta,e)` 联合形状。余项在
`d=e-eta` 中仍逐列抵消，故 visible-offset 的 residual 列为零；但这不恢复联合信息集的
固定形状。该分支是 control-dependent uncertainty，不能直接套固定 `W` 的 Houska 定理，
也不能把实际推力当成 Hempel 文中控制前给定的外生 scheduling。

## 4. Run136 全局包络与保守性选择

Run136 success 扰动矩阵的竖直 residual 一步列恰为

```math
G_1[v_z,r_z]=\frac{572143}{8000000}=h\bar r_z(T_{max}).\tag{86.7}
```

由于式(86.4)对 `T` 严格递增，式(86.7)覆盖完整实际推力区间。于是有两条语义清楚的路线：

1. **认证骨架：**固定 Run136 global envelope，使用 policy-independent intrinsic shape，
   并把可见中心平移 `c_j(d,z,bar u)` 作为 predecessor/控制变量；优点是可用固定集合包含，
   代价是丢失低推力处最多 `79461/4000000` 的一步竖直生成元 tightening。
2. **降低保守性分支：**保留 `W(T)`，把 `deltaT` 与 residual primitive 的共同图纳入
   decision-dependent robust containment/GSIP；只有得到可执行全局证书后，才能声称比
   global envelope 更紧。

Wehbeh--Kerrigan--Scaccia 2026 已给出一般 decision-dependent uncertainty 的 GSIP
框架；因此第二条路线的问题类别和通用求解思想不是本项目创新。本项目若继续，应贡献于
间歇输出反馈信息集、固定复杂度证书和 Tube MPC 递归可行性接口，而不是重新命名 GSIP。

## 5. 证据等级与下一问题

证据等级为 **exact vertical control-translation and residual-shape split**。已证明式
(86.1)--(86.7)、Run136 global 列的一致性以及两条路线的适用条件。

未证明：`C0+c` 或任何 mode-indexed family 受控不变；scheduled GSIP 可行；完整六状态、
输入内点、terminal、移位、递归可行性或性能优势。

下一轮唯一问题：采用固定 Run136 global envelope，把第85章 `C0` 从固定零中心 target
改写成带可见中心变量的 translated template `C0+c_0`，先对 `4/9` 分叉和 `14->0`
逐边求 exact shared-input containment；若固定-shape translation 类失败，只否定该类，再
决定是否值得支付 decision-dependent GSIP 的计算代价。
