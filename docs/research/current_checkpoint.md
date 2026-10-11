# 研究短检查点（2026-10-11，Run155）

主线：传统 SMF/鲁棒输出反馈 MPC；学习暂停。远端 `main=1c49659`、Run153=`9ab357f`、Run154=`ee769f2`；15模态/17边，控制只读可见 `d=e−eta`。

Run155 重新精读 Hempel 2011 §III-A--C/Definition2/Theorem1，并复核 Houska §6.4--6.5/Theorem3。固定 global residual、线性边、凸扰动/约束及同一 source 标签的一张 affine-in-`d` 策略时，闭环边映射与同标签凸包严格交换；constituent-set 证书自动覆盖凸化新增 fibers，但仍须逐边证明 target 包含，且不适用于 `W(T)`、不一致分片策略或非凸约束。Run148 三首次 return seeds 分属 `(0,5)/(0,10)/(0,15)`，跨标签凸包会退化为 mode-only 外包，不能证明历史精化。证据仅为精确代数实施引理，不是 RCI/创新。唯一下一问题：冻结三 source 标签的零/仿射策略，精确传播九条第二周期路径，按共同 target `last_return` 分组三个凸包并核查全程硬约束与包含。

下一唯一问题：在 fixed global residual 下，先为三个 recurrent source 标签冻结零策略，精确传播九条第二周期 return histories；按共同 target `last_return` 分组三个凸包，核查全部中间硬约束和 target 包含。若失败，给最早精确反例，再决定是否准入非零 affine-in-`d` 综合。
