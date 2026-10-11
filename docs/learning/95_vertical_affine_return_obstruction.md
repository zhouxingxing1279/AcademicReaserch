# 95. `J14 -> 15` return 的三步位置支持下界

## 问题与时序

Run158 只证明 `J14` 路径在 age 8 救援至 mode 9 后，mode-9 的同一仿射输入可安全覆盖
success/miss。要构造 `(0,15)` target，还必须沿 miss 分支走到 mode 14 并成功返回。本章先检查
最早的中间硬约束，而不预设 Run157/158 的具体增益。

从 `J14` 经八条零修正 miss 得到 age-8 exact zonotope。随后三条 miss 到 mode 11。竖直模型为

```math
e_p^+=e_p+h e_v,\qquad e_v^+=e_v+h\delta T+g_r\rho,
```

其中 `h=1/50`，`g_r=572143/8000000`，且每拍
`h_{\delta T}\le U=572143/160000`。age 10 输入尚不能影响 mode-11 位置；age 8、9 输入的
位置系数分别是 `2h^2`、`h^2`。

## 精确下界

不施加这两次输入时，mode-11 位置支持为

```math
H_0=\sum_i|g_{p,i}+3h g_{v,i}|+3h g_r
=\frac{3714127151}{3600000000}.
```

对任意 centered affine-in-`d` 输入，只要每拍 robust input support 不超过 `U`，三角不等式给出

```math
H_p\ge H_0-(2h^2+h^2)U
=\frac{369867929}{360000000}
=1+\frac{9867929}{360000000}>1.
```

因此无论如何选择 age-8、age-9 的仿射增益，`J14 -> 15` history 都在 mode 11 之前违反
`|e_p|<=1`。该结论比 Run158 特定增益传播得到的 `1.027750...` 更强，因为它否定整个受限
affine policy class，而非单个见证。

## 证据边界与方向纠正

证据等级为 `exact_three_miss_position_support_lower_bound`。它只针对 fixed global residual、
当前 `J14` age-8 source、当前 correction 盒与 centered affine-in-`d` 类；不否定更早介入的
策略、不同初始化 family、scheduled residual、一般非线性 output feedback 或六自由度模型。

由于 `(0,15)` 所需的三个 constituent 中 `15->15` 已不安全，本轮不构造其凸包。下一步应把
控制介入点前移到 `J14` return seed，联合综合整个15步周期；若同样失败，再判断应扩大 correction
权限、收缩 seed，还是放弃该 terminal family。
