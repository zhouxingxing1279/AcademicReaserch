# 100. `J14` 可见纤维的精确方向半宽

## 1. 为什么整体 support 不是正确门槛

`J14` 的生成元参数记为 `xi in [-1,1]^106`。成功测量后控制器可见

```math
d=e-\eta,
```

且冻结模型中 `d_v=(103/100)d_p`，所以独立可见量只有 `D xi=d_p`。Run161使用整个 `J14` 在
`a=e_p+14h e_v` 方向的半宽

```math
\sum_i |F_i|=\frac{3889781459}{3600000000}\approx1.08049485.
```

这同时比较了具有不同 `d`、因而控制器能够区分的两点。它只适用于所有观测共享同一原点/计划的
固定合同，不是测量条件化重规划的必要条件。

## 2. 最坏fiber半直径的等价LP

对固定观测 `y`，fiber为 `{xi: |xi|_inf<=1, Dxi=y}`。任意同fiber两点的半差
`z=(xi^+-xi^-)/2` 满足 `Dz=0, |z|_inf<=1`；反向取 `xi^+=z, xi^-=-z` 即在 `y=0`
实现。因此

```math
\sup_y\frac12\operatorname{diam}F\{\xi:\|\xi\|_\infty\le1,D\xi=y\}
=\max_{\|z\|_\infty\le1,Dz=0}Fz. \tag{100.1}
```

其一维等式对偶为

```math
\min_\lambda\sum_i|F_i-\lambda D_i|. \tag{100.2}
```

取加权中位数 `lambda=29/15`，原始witness除第3号生成元（零起算）外均在 `±1`，该项为
`-26445009/75715726`。等式残差严格为零，原始与对偶目标同为

```math
\frac{16315003}{75000000}\approx0.2175333733<1.
```

故所有实际可见fiber都通过Run161的单位seed方向必要门槛；条件化相对无条件support减少
`0.8629614764`。

## 3. 纠正范围

Run160/161的代数对“整个 `J14` 共用同一tracking-error原点和计划”仍成立；错误在于把它外推到
测量后可按 `d` 重定心/重规划的策略。式(100.1)只移除了seed宽度这一项阻塞，**没有**证明：

- fiber中心在绝对位置约束内可被同一可实现名义轨迹补偿；
- 14次后续miss期间速度、输入和全部中间状态安全；
- success/miss两类后继均落入终端information family；
- 旧计划可移位，或闭环递归可行；
- 六自由度非线性四旋翼保证。

证据等级为 `exact_primal_dual_visible_fiber_width_and_quantifier_correction`。下一步应直接对参数化
fiber构造15-tick安全策略与终端包含证书，而不是继续反推无条件seed缩放。
