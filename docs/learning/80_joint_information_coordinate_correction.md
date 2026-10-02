# 80. 联合信息集的坐标语义纠正：Run 142 门槛不是必要条件

日期：2026-10-02。本章不构造四维 RCI，而是修正第 79 章末尾给出的下一步判据。
第 79 章的 `0.35742` 门槛对 product target

```math
S_j=E_\eta^j\times D_j
```

是严格必要的，但把它继续当作任意 joint `(eta,d)` target 的必要条件会误杀可行候选。

## 1. 正确联合坐标

沿用

```math
\eta=x-\hat x,\qquad d=\hat x-z,\qquad e=x-z=\eta+d,
```

其中控制器可见 `d`，不可见 `eta`，硬状态约束实际作用于 `x=z+e`。竖直 success 边上，
令 `h=1/50`、observer 位置增益 `L=9/2`、
`q=eta_pz+h eta_vz`、下一位置测量噪声为 `n`，则当前合同给出

```math
\begin{aligned}
\eta_{p_z}^+&=-n,\\
\eta_{v_z}^+&=\eta_{v_z}+h r_z(T)-L(q+n),\\
d_{p_z}^+&=d_{p_z}+h d_{v_z}+q+n,\\
d_{v_z}^+&=d_{v_z}+h\delta T+L(q+n).
\end{aligned}
\tag{80.1}
```

因此共享的同一创新原语在真实 tracking error 中精确抵消：

```math
\begin{aligned}
e_{p_z}^+&=e_{p_z}+h e_{v_z},\\
e_{v_z}^+&=e_{v_z}+h\bigl(r_z(T)+\delta T\bigr).
\end{aligned}
\tag{80.2}
```

miss 边也满足式 (80.2)，只是 observer 自身按 miss 矩阵传播。故后续 joint candidate 应以
`(eta_pz,eta_vz,e_pz,e_vz)` 表示；`d=e-eta` 用于定义 observation fiber 与因果 policy，
不能再给 `d` 独立施加由 product 分解产生的宽度限制。

## 2. mode-14 条件纤维不能达到旧门槛

从合同要求的初始化 `mode=0,d=0` 出发，14 条 miss 边上的 `d` 更新不含 hidden `eta`
或物理 residual。固定同一控制/观测历史后，mode 14 的 observation fiber 仍包含 Run 136
mode-14 zonotope 的完整 `q` 投影，精确半宽为

```math
h_{E_\eta^{14}}(q)=\frac{23312147}{48000000}
\approx0.4856697292.
\tag{80.3}
```

它比第 79 章从 product `D_0` 推出的门槛

```math
\frac{57902137}{162000000}\approx0.3574205988
\tag{80.4}
```

严格大

```math
\frac{166210873}{1296000000}\approx0.1282491304.
\tag{80.5}
```

所以“靠历史把该 fiber 压到旧门槛以下”在这个必经初始化路径上做不到。但这不能推出
joint target 不可行，因为式 (80.4) 本身只来自对 `d_vz^+` 的独立 product 限幅。

## 3. 精确反例：违反 product 限幅但满足 joint target

在 mode-14 zonotope 中取一个达到式 (80.3) 正向支持的真实生成元组合，并取
`d=0`、`delta T=0`、`r_z=0`、`n=1/50`。由当前 Run 136 success 矩阵得到

```math
\begin{aligned}
\eta_{v_z}^+&=-\frac{64124993}{288000000},\\
d_{v_z}^+&=\frac{72816441}{32000000},\\
e_{v_z}^+=\eta_{v_z}^++d_{v_z}^+
&=\frac{9237859}{4500000}\approx2.0528575556.
\end{aligned}
\tag{80.6}
```

这里 `d_vz^+` 严格超过第 79 章 product target 的最大允许半宽
`61142137/36000000≈1.6983926944`；但相关的 `eta_vz^+` 抵消了这一超量，且

```math
|e_{v_z}^+|<11/4.
\tag{80.7}
```

位置坐标同样满足 `eta_pz^+=-1/50`、`e_pz^+=q<1`。完整六维 `eta^+` 位于 Run 136
mode-0 box，竖直 `e^+` 位于由物理域和 nominal hover 域给出的 source box。因此这个点
同时满足当前合同中的两个真实约束，却违反所有把 `eta` 与 `d` 独立相乘后得到的
`d_vz` 限幅。它是“旧门槛不是 joint necessity”的精确反例。

## 4. 证据等级与后续接口

本章证明的是：

> Run 142 的 `q<=0.35742` 仅是 product-fiber target 的必要条件；它不是保持
> `(eta,d)` 相关性的联合信息集必要条件。

本章没有证明四维 joint RCI 存在，也没有给出 shared-input predecessor 固定点。正确的
下一步是对 `(eta,e)` 联合集合做逐边传播，同时施加：

1. `eta` 投影落入 Run 136 mode set；
2. `e` 满足真实状态 source constraint；
3. 控制器在每个 `d=e-eta` observation fiber 上使用同一个输入；
4. success/miss 分叉与 `eta,e` 更新共享同一实际推力和扰动原语。

这条坐标纠正避免把 product 分解造成的保守性错误升级成一般 joint 信息集不可行结论。
