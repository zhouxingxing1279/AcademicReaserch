# Run156：第二周期零策略硬约束门槛

日期：2026-10-11；分支 `research/run156-second-cycle-zero-policy-gate`。

## 仓库接续

远端核查：`main=1c49659`，Run152=`bf8ea72`、Run153=`9ab357f`、Run154=`ee769f2`、
Run155=`1a7d413`。从本地 Run155 等树提交接续，起点工作树干净。只读取短检查点、Run155
交换引理以及 Run148/150 的现有 exact generator propagation 实现，没有重扫全部历史。

## 文献与准入

重新精读 Houska §6.5/Theorem 3 完整证明：一般可行策略依赖当前 information set 的凸权重，
零策略仅是很弱的基线。重读 Yang--Ozay Introduction 对 product system 和因果安全量词的说明：
缺测周期的每个中间 tick 都必须安全。本轮因而只准入九路径零策略 exact feasibility probe。

## 精确结果

复用现有 exact rational generator maps 做不落库探针，并以独立标量递推
`h_ev(k)=h_ev(0)+k*572143/8000000` 复核。九条第二周期 histories 中六条全程满足竖直 estimator
与 true-error 约束；三条失败：`10->15` 在第14 miss，`15->10` 和 `15->15` 在第9 miss。
三处最早失败半宽相同：`99649307/36000000`，相对 `11/4` 严格超出
`649307/36000000`。失败发生在凸化之前，所以 Run155 的交换引理不能挽救零策略候选。

## 实现决定、证据等级与限制

本轮不保留新的 checker。原因是现有 exact generator maps 已给出逐 tick 原始证据，独立一维
闭式递推又完整复核了决定性坐标；复制一个只打印九格表的生产脚本不会提升证据等级。按研究
准入门槛，只提交推导、阅读记录和方向纠正，并重建因 `READ_PAPERS.md` 哈希变化受影响的五份
历史 artifact。

证据等级：**exact zero/label-only second-cycle counterexample**。它不否定 affine-in-`d`
feedback、一般 information ensemble、RCI 存在性或完整四旋翼闭环。

## 唯一下一问题

只针对临界 `last_return=10,15` source families，建立 affine-in-`d` gain 的精确支持可行性
问题；同时约束未知 success/miss 分支、执行器盒和 `e_v` 硬约束。先判断能否在第14/9 miss 前
消除 `649307/36000000` 的宽度超量，再决定是否恢复九路径传播。
