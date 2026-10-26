# 115. mode 4 未知 success/miss 分叉的 lifted-cell 证书

日期：2026-10-26。本章把第 114 章的一条 miss 边扩展到第一个控制时尚未知 packet label
的分叉；它仍然只是冻结 cell 的一步证书，不是 terminal family 或 RCI。

## 信息时序与 source cell

取竖直联合坐标 `s=(eta_p,eta_v,e_p,e_v)`、控制器可见量 `d=e-eta`。source 固定为
Run136 mode-4 的 `eta` 精确投影乘

```math
|d_p|\leq 1/5,\qquad |d_v|\leq 1/4,
```

并令 `e=eta+d`。当前输入先于 packet outcome 选择，故 `4->5 miss` 与 `4->0 success`
必须使用同一策略。本轮冻结

```math
\delta T=0d_p+0d_v+0.
```

它不读取隐藏 `eta` 或未来 edge label。实际推力区间为
`[1356943/160000,1782257/160000]`，位于执行器盒内。source cell 的当前位置、速度硬约束
余量分别为 `1237120687/1800000000` 与 `41843563/36000000`，均严格为正。
mode-4 estimator 投影面积为
`41105550110953/240000000000000>0`；检查器把该面积与两个 `d` 半宽共同纳入四维正体积
准入条件，而不是只检查可见盒。

## 两支共享的物理图

两支都使用实际推力决定的可靠竖直余项

```math
r_z(T,\rho_z)=\left(\frac{1043}{500}+\frac{81}{800}T\right)\rho_z,
\qquad |\rho_z|\leq1,
```

其当前推力上端半宽为 `411370817/128000000`。在每一分支内，同一 `rho_z` realization
同时进入 `eta_v^+` 与 `e_v^+`，没有把估计误差改称未来扰动。

miss 更新为

```math
\eta_p^+=\eta_p+h\eta_v,\quad
\eta_v^+=\eta_v+h r_z,
```

success 令 `q=eta_p+h eta_v`、`n in [-1/50,1/50]`，并使用

```math
\eta_p^+=-n,\quad
\eta_v^+=\eta_v+h r_z-\frac92(q+n).
```

两支的真实 tracking error 都满足

```math
e_p^+=e_p+h e_v,\qquad e_v^+=e_v+h r_z.
```

因此 success 的同一测量创新虽进入 estimator error，却在 `e=eta+d` 中精确抵消。检查器把
所有 source generators、`d`、同一个 `rho_z` 与 success `n` 映射成一组联合
`(eta_p^+,eta_v^+,e_p^+,e_v^+)` primitive columns；estimator 与 tracking 支持均从这同一组列
计算，并逐列核查 residual 的 `eta/e` 系数相同及 noise 的 `e` 系数为零，而不是用布尔声明代替。

## 逐法向结果

- `4->5 miss`：mode-5 estimator 投影有 14 条 facet，加 tracking box 4 条，共 18 条；
- `4->0 success`：mode-0 estimator box 有 4 条 facet，加 tracking box 4 条，共 8 条。

26 条 exact-rational 支持不等式全部闭合。两支的 estimator 位置法向均出现精确零余量，
与 Run136 reachable-set 构造的边界相等一致；不是浮点容差。tracking 位置最小严格余量为
`4719857/7200000`，速度最小严格余量为 `63247363447/57600000000`。

## 证据边界与方向判断

**已证明：**一个固定正体积 mode-4 source cell 和一张可见仿射策略，在当前输入之后才揭示
的 miss/success 两条合法边上，同时满足输入、source domain、estimator target facets 与真实
tracking box normals；success 噪声与物理余项的共享关系被显式保留。

**未证明：**其他 source cells、cell 覆盖、重叠处策略一致性、其余 15 条初始化图边、45-state
recurrent terminal family、MPC shift/递归可行性、水平姿态耦合或完整六自由度保证。

Hempel--Kominek--Werner 已覆盖 observation-fiber 共用输入和逐 facet robustification；所以该
结果是 `exact_two_edge_unknown_label_target_normal_support_certificate`，不是新算法。它的重要性
是排除了“第一个未知 label 分叉立即使 cell 不可行”这一阻塞。

下一唯一问题：在不增加在线 cell 数和法向预算前，检查 mode-0 与 mode-4 两个已认证 cell 是否
能扩展为覆盖初始化可达 observation domain 的有限 cell family，并在 cell 重叠处给出单值、
输入可行且逐边闭合的仿射策略选择；若必须逐 history 无限细分，则停止该表示路线。
