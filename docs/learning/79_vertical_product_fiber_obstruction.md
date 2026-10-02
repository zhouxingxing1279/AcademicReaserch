# 79. 竖直 causal product-fiber 类的精确否证

日期：2026-10-02。本章承接第 77--78 章，但结论严格限定于

```math
S_j=E_\eta^j\times D_j,
```

其中 `E_eta^j` 固定为 Run 136 的六维 zonotope，`D_j` 可取任意二维集合，控制输入只能
依赖当前可见 `d=(d_pz,d_vz)` 与 mode。结论与 `D_j` 是否轴对齐、是否多面体以及 policy
是否 PWA 无关；它不否定保持 `eta-d` 相关性的联合信息集。

## 1. 竖直 product-fiber predecessor

冻结 `h=1/50`、位置 observer 增益 `L=9/2`。第 77 章的共享物理/observer/nominal
successor 在竖直坐标上化为

```math
\begin{aligned}
d_{p_z}^+ &= d_{p_z}+h d_{v_z}+q+n,\\
d_{v_z}^+ &= d_{v_z}+h\delta T+L(q+n),\\
q&=\eta_{p_z}+h\eta_{v_z},\qquad n\in[-1/50,1/50].
\end{aligned}
\tag{79.1}
```

物理 residual `r_z(T)` 同时进入真实状态与 observer-error，但在差值
`d^+=hat x^+-z^+` 中按共享 realization 正确消去；它仍通过 Run 136 的 `E_eta^{j+}`
逐边包含受到约束。因此式 (79.1) 不是把 residual 独立重采样后的近似。

对给定 mode `j` 和 `d`，causal controller 先选一个 `delta T(d,j)`，然后必须覆盖
`E_eta^j` 中全部隐藏 `eta` 和未来测量噪声。于是 success 边在速度坐标上的不可消除
半宽为

```math
L\left(h_{E_\eta^j}([0,1,0,h,0,0]^\top)+\frac1{50}\right).
\tag{79.2}
```

`d` 与 `delta T` 只移动该区间中心，不能缩小式 (79.2) 的半宽。

## 2. 真值源域给出的 mode-0 最大目标宽度

hover nominal velocity domain 为 `z_vz in [-1/4,1/4]`，物理真值约束为
`x_vz in [-3,3]`。所以 `e_vz=eta_vz+d_vz` 的对称可用半宽最多为 `11/4`。
Run 136 mode-0 zonotope 的精确坐标支持是

```math
h_{E_\eta^0}(e_{v_z})=\frac{37857863}{36000000}.
```

任意满足全体 `eta in E_eta^0` 真值源域的 product slice 都必须满足

```math
h_{D_0}(e_{d_{v_z}})
\le \frac{11}{4}-\frac{37857863}{36000000}
=\frac{61142137}{36000000}
\approx1.6983926944.
\tag{79.3}
```

该上界对任意非轴对齐或非多面体 `D_0` 都成立，因为它只是坐标支持的必要条件。

## 3. mode 14 强制 success 的宽度矛盾

Run 136 mode-14 zonotope 在组合方向 `q=eta_pz+h eta_vz` 的精确支持为

```math
h_{E_\eta^{14}}(q)=\frac{23312147}{48000000}.
\tag{79.4}
```

mode 14 没有 miss 后继，必须走 `14 -> 0` success。由式 (79.2) 得下一速度中心误差的
不可消除半宽

```math
\begin{aligned}
r_{14}^{\rm succ}
&=\frac92\left(\frac{23312147}{48000000}+\frac1{50}\right)\\
&=\frac{72816441}{32000000}
\approx2.2755137813.
\end{aligned}
\tag{79.5}
```

与 mode-0 最大允许宽度比较：

```math
r_{14}^{\rm succ}-\frac{61142137}{36000000}
=\frac{166210873}{288000000}
\approx0.5771210868>0.
\tag{79.6}
```

因此对任意当前 `d` 和任意共享输入 `delta T(d,14)`，success image 在
`d_vz^+` 上的宽度已经严格大于任何 admissible `D_0` 的最大可能宽度。故

```math
\operatorname{Pre}_{14\to0}(D_0)=\varnothing.
\tag{79.7}
```

该结论与推力权限无关：推力修正只平移区间。exact polygon 实现以 Run 136 生成元、
当前 config 和同一个 input variable 独立重建 predecessor，第一轮唯一立即为空的 mode
正是 14；其余 14 个 mode 均生成非轴对齐 predecessor，说明不是“只试了盒”。

## 4. 从局部空 predecessor 到候选类不存在

15-mode graph 包含必经 miss 路径

```math
0\to1\to\cdots\to14
```

以及强制 `14->0` success。若 product-fiber invariant family 的 `D_14` 为空，则沿 miss
边的逐边不变性依次要求 `D_13,...,D_0` 为空；这与初始化必须包含
`E_eta^0 x {d=0}` 矛盾。因此：

> 在当前 Run 136 estimator multiset、hover nominal source domain、15-mode dropout graph
> 和 observation-fiber causal input 权限下，不存在满足初始化的非空
> `E_eta^j x D_j` product-fiber RCI family。

这是 **certificate-class nonexistence**，不是一般 output-feedback RCI 不存在。Run 141
仍作为负对照：若允许输入读取隐藏 `q`，它能用 `3.37946875 N` 极值修正通过专门的一步
target；本章的真实 causal product fiber 不允许这种隐藏状态泄漏。

## 5. 对主线的纠正

继续增加 `D_j` facet、改成椭球或运行更大的 product-set solver 都不能跨越式 (79.6)。
下一步必须改变信息集合结构，而非调几何模板：候选至少要保持 `eta` 与 `d` 的相关性，
使固定可见 `d` 下的 conditional fiber `Q_j(d)` 小于无条件 Run 136 `E_eta^j`；同时仍须
使用同一 shared primitive、同一 actual thrust 和分叉前共享输入。只有联合候选通过后，
才恢复 nominal input 内点、terminal/shift 和递归可行性工作。

