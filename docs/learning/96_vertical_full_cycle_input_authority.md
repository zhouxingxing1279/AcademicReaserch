# 96. `J14` 十五步 return 的策略无关输入权限反证

## 1. 为什么必须回到完整周期

Run159 只固定了 `J14` 经八次零修正 miss 后的 age-8 集合，因而没有排除更早反馈。本章从
Run148 的 `J14` mode-0 return seed 重新开始，在下一次15-tick return 的整条 miss string 上允许
控制器每拍介入，并把信息权限放宽到任意因果 full-state feedback。若该放宽问题仍不可行，原
output-feedback 问题必不可行。

竖直误差动力学与硬约束为

```math
e_{p,t+1}=e_{p,t}+h e_{v,t},\qquad
e_{v,t+1}=e_{v,t}+h u_t+g_r\rho_t,
```

```math
|u_t|\le U=\frac{572143}{160000},\qquad |e_{p,t}|\le1,
```

其中 `h=1/50`、`g_r=572143/8000000`、`|rho_t|<=1`。

## 2. 镜像轨迹的半直径下界

对任意 miss 数 `k`，在中心对称 `J14` seed 中选择一对镜像初态，使
`e_p+k h e_v` 的差达到其直径；同时为两条轨迹选择相反 residual 端点。零输入时位置半径为

```math
H_k^0=\sum_i|g_{p,i}+khg_{v,i}|
      +\frac{k(k-1)}2 h g_r.
```

允许两条轨迹由任意不同的因果控制律驱动，只要各自满足输入盒，就总有
`|u_t^+-u_t^-|<=2U`。展开双积分器得到

```math
e_{p,k}^+-e_{p,k}^-
=2H_k^0+h^2\sum_{t=0}^{k-2}(k-1-t)(u_t^+-u_t^-).
```

因此任何可达集合的位置半直径满足必要下界

```math
H_k\ge H_k^0-\frac{k(k-1)}2h^2U. \tag{96.1}
```

该推导不要求 affine、centered、同一 observation-fiber 输入，甚至允许 full-state feedback；
它只用到了每条轨迹的点态输入盒。因此是原因果 output-feedback 问题的乐观放宽。

## 3. 第13个 miss 的精确失败

exact `J14` generators 给出：

| miss数 | 零输入位置半径 | 最大可削减量 | 必要下界 |
|---:|---:|---:|---:|
| 12 | `435969371/400000000` | `18880719/200000000` | `398207933/400000000 ≈ 0.995520` |
| 13 | `2069235407/1800000000` | `22313577/200000000` | `934206607/900000000 ≈ 1.038007` |

第12个 miss 的必要条件尚未排除可行性；第13个 miss 首次满足

```math
H_{13}\ge1+\frac{34206607}{900000000}>1.
```

因此 fixed global residual、当前 `J14` seed 和 correction 盒下，不存在任何因果 bounded policy
能保证15-tick return string 的全部中间状态安全。失败早于 mode-14 forced success，故 measurement
update 或 final target hull 无法修复。

## 4. 结论边界与主线纠偏

证据等级为 `exact_policy_independent_full_cycle_position_diameter_obstruction`。它否定当前
`J14` seed/固定 residual/correction authority 的15步 recurrent constituent，但不否定更小 seed、
更强可用推力、scheduled/tighter residual、不同位置约束或完整非线性模型。

该结果已经改变整体论证：继续为同一 constituent 调 gain 没有意义。下一步必须做参数接口审计，
精确计算使 (96.1) 在 `k=14` 可通过所需的 seed contraction、residual reduction 或 correction
authority，并判断哪一项可由可靠在线集合信息实现；否则应移除15-tick dropout 合同。
