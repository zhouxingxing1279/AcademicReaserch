# Run199 文献准入卡：固定 affine-offset SOCP 数值求解与独立审计

日期：2026-10-29。

## 本轮唯一问题

Run198 已冻结6080个三维Lorentz cones及其规模，但当时没有求解器。本轮环境现可安装
`clarabel==0.11.1`，因此只回答：冻结19-pair affine-offset SOCP的可行性状态是什么，且
solver返回结果能否通过独立的完整区间/端点约束审计？

## 最近邻与实际阅读

1. Goulart、Chen，*Clarabel: An Interior-Point Solver for Conic Programs with Quadratic
   Objectives*, Mathematical Programming Computation, 2026，DOI
   `10.1007/s12532-026-00320-7`。**重读Sections 2.1--2.2的最优/不可行解释、Lorentz与zero
   cones，并核查默认容差和homogeneous embedding语义。** Clarabel的状态与残差是数值证据，
   不是仓库命题的精确有理证书。
2. Mulagaleti、Mejari、Bemporad，*Parameter-Dependent Robust Control Invariant Sets for LPV
   Systems With Bounded Parameter-Variation Rate*, IEEE TAC 70(2), 2025，DOI
   `10.1109/TAC.2024.3454528`。**重读式(26)--(28)、SDP(33)、算法步骤4及Section IV求解
   设置。** 其方法同时综合PD offsets和PD vertex controls，但fixed normals、configuration
   cone和S-procedure仍可能保守。
3. Pólik、Terlaky，*A Survey of the S-Lemma*, SIAM Review 49(3), 2007，DOI
   `10.1137/S003614450444614X`。**复核Theorem 2.2与Slater条件。** 本轮每个标量区间二次
   条件的`2 x 2` LMI/SOC表示是精确的；数值误差只来自综合求解，不来自该理论变换。

## 严格差异、强基线与可证伪标准

不提出新RCI算法。最强直接基线仍是Mulagaleti等的fixed-normal PD-RCI SDP；本轮只实例化
仓库已冻结的单标量、任意未来跳变、common-core充分模板。成功标准不是`Solved`字符串，而是：

1. 保存锁定solver版本、原始状态、迭代数及残差；
2. 独立重算全部6080个二次在`[-1,1]`的精确候选最小值；
3. 独立检查configuration、硬状态、力矩、offset非负及common-core端点约束；
4. 对浮点候选只给`NUMERIC_CHECK`，除非另有有理化严格余量证书。

若solver报告不可行但无可独立重放的精确对偶证书，只能记为数值不可行，不得升级为
configuration family或物理系统不可行。

## 准入判断

**通过“锁定Clarabel版本、执行冻结SOCP并独立审计”；不通过任何创新、六状态安全或递归
可行性声明。** 同时修复Run198工件把运行时solver inventory写进可重放报告所造成的环境依赖；
历史工件必须保存当时快照，而当前能力由Run199单独记录。
