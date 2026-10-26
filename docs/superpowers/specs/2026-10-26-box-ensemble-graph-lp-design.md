# Box information-ensemble graph LP 设计

## 目的与边界

在 Run183 的二维竖直固定包络合同上，复现一个可审计的 configuration-constrained
information-ensemble 强基线。目标是构造 box 的 `Y/G/Lambda`、一个紧凑的
`Z/H/Omega`，并形成保留 15 modes、17 edges 及分叉前共享控制的线性规划。本轮是已有
Houska/CCTMPC 工具的项目化复现，不声称算法创新，也不外推到六自由度非线性四旋翼。

## 文献时序修正

Houska 式 (25)--(29) 的顺序是 posterior measurement intersection、control、dynamics。
仓库合同的 `control_precedes_successor_edge=true` 则规定 current control、dynamics、随后揭示
success/miss。因此不能给每条 edge 独立套一份式 (29)，否则 mode 4/9 的 success 与 miss 会
获得不同 current controls。设计改为每个 source mode 只建立一次 predicted ensemble：

1. source extreme information boxes 共用一组 source controls，生成 predicted ensemble；
2. miss edge 将 predicted ensemble 直接包含于 target；
3. success edge 先在 meta level 施加位置测量求交的式 (25) 外包，再包含于 target。

## 模板

状态 box 写成 `P(y)={x | Yx<=y}`，其中 `Y=[I;-I]`、`y=(u_p,u_v,-l_p,-l_v)`。
`G y<=0` 只要求两个坐标的上下界不交叉，四个 `Lambda` 是四个 box vertex maps。

把 box 参数改写为中心/半径 `(c_p,c_v,r_p,r_v)`。meta-template 用 6 个上界参数：
`z=(r_p,c_p^+,-c_p^-,c_v^+,-c_v^-,r_v)`。`Zy<=z` 因而描述中心矩形与两个半径上界；
`H z<=0` 只要求中心区间非空、半径非负。完整 meta polytope 有 16 个 vertex maps，极端
information sets 仅取两个半径都在上界的 4 个中心角点。第一行 `Z1` 是 `r_p`，success
测量噪声半宽 `1/50` 正好给出式 (25) 的 `v=1/50`。

## LP 与证书

每个 mode 有 source `z_q`、predicted `bar_z_q`、4 个 extreme controls 及对应 auxiliary
box parameters。逐 source extreme box 的四个 state vertices 施加动力学、固定 `W`、状态盒和
输入盒；所有外出 edge 复用同一 source controls 与 `bar_z_q`。目标最小化所有 source ensemble
的中心区间宽度与半径上界之和，只用于取得可复现基线。

实现先用 HiGHS 求数值 primal/dual，再把候选有理化并逐不等式精确重放。只有 exact primal
feasibility 才能形成数学证书；数值 dual 只报告残差与 gap，不冒充 exact 最优性证明。若精确
primal 不可恢复，则本轮降级为 LP 构造与数值观察，并保存失败原因。

## 通过与停止条件

通过条件：模板恒等式、16/4 vertex 枚举、17 edge 时序、mode 4/9 control sharing、全部 exact
primal inequalities 和硬约束同时闭合。失败条件：任何 success edge 需要 branch-specific current
control、meta-template 不能表达测量集合、或有理候选存在正违反量。失败时不得调小扰动或放宽
硬约束掩盖问题。
