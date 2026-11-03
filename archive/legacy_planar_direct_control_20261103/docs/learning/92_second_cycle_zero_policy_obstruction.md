# 92. 第二周期零策略的最早硬约束反例

## 1. 九条历史与检查量词

Run148 的三个首次 return seed 分别记为 `J_4,J_9,J_14`，对应扩展标签的上一周期长度
`r in {5,10,15}`。下一周期长度 `r' in {5,10,15}`，故需要检查九个 `(r,r')` 组合。

本章冻结 Run136 global residual 和 `delta T=0`。每条 history 从相应 `J_(r-1)` 开始，先走
`r'-1` 条 miss，再走一条 success。安全量词覆盖每个 miss 后的 source-age 集合以及 success
后的 target 集合，不能只检查 return 时刻。

## 2. 可独立复核的速度半宽递推

固定 global residual 下，miss 边的真实竖直速度误差满足

```math
e_v^+=e_v+g_r\rho,
\qquad |\rho|\le1,
\qquad g_r=\frac{572143}{8000000}.
```

各步 residual primitive 相互独立，因此从 centered seed 出发，`k` 条 miss 后的精确半宽为

```math
h_{e_v}(k)=h_{e_v}(0)+k g_r.\tag{92.1}
```

现有 Run148 exact generators 给出三个 seed 的初始半宽：

| 上一 `last_return` | seed | `h_ev(0)` |
|---|---|---:|
| 5 | `J_4` | `101462161/72000000` |
| 10 | `J_9` | `31802149/18000000` |
| 15 | `J_14` | `152955031/72000000` |

竖直真实速度硬约束是 `|e_v| <= 11/4`。直接代入 (92.1)：

```math
h_{e_v}^{J_9}(14)
=h_{e_v}^{J_{14}}(9)
=\frac{99649307}{36000000}
=\frac{11}{4}+\frac{649307}{36000000}.
\tag{92.2}
```

严格超量约为 `0.0180363`。

## 3. 最早失败路径

精确逐 tick 传播的九路径结果为：

| 上一 `last_return` | 下一周期 5 | 下一周期 10 | 下一周期 15 |
|---|---|---|---|
| 5 | 全程通过 | 全程通过 | 全程通过 |
| 10 | 全程通过 | 全程通过 | **第14条 miss 后失败** |
| 15 | 全程通过 | **第9条 miss 后失败** | **第9条 miss 后失败** |

失败坐标均为真实 `e_v`，而不是 estimator `eta` 或可见 offset `d`。传播同时核查了各 age 的
竖直 estimator box、`|e_p|<=1`、`|e_v|<=11/4`；三条失败 history 之前的全部 tick 及其余
六条 history 均满足这些集合约束。零修正也满足当前 correction/actuator box。

## 4. 结论边界

这是 **exact second-cycle hard-constraint counterexample for zero/label-only policy**：

1. 零策略下，九个 constituent histories 中已有三个不安全，因此不能继续把它们按 target
   `last_return` 凸化为安全 recurrent family；凸包只会包含这些不安全 constituent sets。
2. 任意只依赖离散标签、在整个集合上施加常数的 correction sequence 也只能移动中心，不能
   减小 (92.2) 的宽度，所以同样被该必要条件否定。
3. 依赖可见 `d=e-eta` 的 affine feedback 会改变闭环生成元，未被否定；scheduled `W(T)`、
   非线性策略和完整六自由度模型也不在本证书范围内。
4. 该结果不是 RCI 不存在证明、MPC 递归可行性结论或创新贡献。

## 5. 下一准入门槛

下一步不应继续计算零策略 target hull，而应只针对两个临界 source labels 构造最小
affine-in-`d` gain feasibility problem：必须用同一当前策略覆盖未知 success/miss 后继，并在
`J_9` 的第14 miss 与 `J_14` 的第9 miss 之前把 `e_v` 支持压回 `11/4`。若 gain feasibility
失败，需给对偶/宽度证书；若通过，才扩展到九路径及全部 target containment。
