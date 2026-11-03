# 93. 两个临界 miss 前驱的仿射可见速度反馈见证

## 1. 时序纠正

Run156 的三处最早失败发生在 `J_9` 第14条 miss，以及 `J_14` 第9条 miss（后者同时影响
下一周期10和15）。因此当前控制输入分别在 age 13、age 8 选取；两条边都是确定的 miss：

```math
(13,10)\to(14,10),\qquad (8,15)\to(9,15).
```

未知 success/miss 分叉只在后续以 mode 9 为 source 再选控制时出现，不能倒置到本次救援
输入的量词中。

## 2. 精确支持问题

固定 Run136 global residual，miss 边满足

```math
d_p^+=d_p+h d_v,\quad d_v^+=d_v+h\delta T,\quad
e_v^+=e_v+h\delta T+g_r\rho,
```

其中 `h=1/50`、`g_r=572143/8000000`。取 centered affine policy

```math
\delta T=K_v d_v,\qquad K_p=0.
```

对 source zonotope 生成元 `g_i`，输入与下一真实速度的精确半宽分别为

```math
h_u(K_v)=\sum_i|K_v g_{d_v,i}|,
\qquad
h_{e_v^+}(K_v)=\sum_i|g_{e_v,i}+hK_vg_{d_v,i}|+g_r.
```

下面选择的 gain 令 `h_u` 恰好等于 correction 上界 `572143/160000`；这是可行见证，
不声称最优。

| seed / source age | `h_dv` | `K_v` | `h_ev+` | 距 `11/4` 余量 |
|---|---:|---:|---:|---:|
| `J_9` / 13 | `45315007/32000000` | `-114428600/45315007` | `8857197898290289/3262680504000000` | `115173487709711/3262680504000000` |
| `J_14` / 8 | `72816441/32000000` | `-114428600/72816441` | `4732194266975069/1747594584000000` | `73690839024931/1747594584000000` |

两项余量均严格为正，约为0.03530与0.04217。当前 correction 只进入下一 `e_v`，故同一步
`e_p` 与 estimator `eta` 的传播和 Run156 零策略完全相同；它们在首次失败前已经通过硬约束
检查。因此两个 Run156 局部超量都存在 exact one-step affine rescue。

## 3. 证据边界

该结果只证明两个具体 source fibers 的一步 robust state/input feasibility。尚未证明：

- gain 最优性或保留 actuator 余量；
- 救援后集合包含在某个 recurrent target family；
- mode 9 下一控制时刻同一输入同时覆盖 success/miss；
- 九路径策略一致性、终端条件、RCI 或 MPC 递归可行性；
- 完整六自由度四旋翼保证。

因此正确结论是：Run156 的零策略反例不能升级为 affine-in-`d` 不可行；下一步必须从
“单坐标安全”转向“共同 target inclusion 与后续分叉闭合”。
