# 研究短检查点（2026-10-11，Run156）

主线：传统 SMF/鲁棒输出反馈 MPC；学习暂停。远端 `main=1c49659`、Run155=`1a7d413`；控制只读可见 `d=e−eta`。

Run156 重读 Houska §6.5/Theorem3 完整证明及 Yang--Ozay 的 product safety 量词。固定 global residual 下精确传播九条第二周期零策略 histories：六条全程安全；`last_return 10->15` 在第14 miss、`15->10` 与 `15->15` 在第9 miss 首次违反真实速度硬约束。三处半宽均为 `99649307/36000000`，超过 `11/4` 恰 `649307/36000000`。常数/label-only correction 只平移集合，亦不能修复；但 affine-in-`d` feedback 可改变形状，未被否定。证据是精确二周期受限策略反例，不是 RCI、递归可行性或创新证明。

下一唯一问题：仅针对 `last_return=10,15` 临界 source families，建立 affine-in-`d` gain 的精确支持可行性问题，同时约束未知 success/miss 分支、执行器盒与 `e_v` 硬约束；先判断能否消除上述宽度超量，再恢复九路径传播。
