# 研究短检查点（2026-10-11，Run158）

主线：传统 SMF/鲁棒输出反馈 MPC；学习暂停。远端 `main=1c49659`、Run157=`4525d73`；控制只读可见 `d=e−eta`。

Run158 精读 Goulart--Kerrigan 2007 affine output-feedback robust constraints，重读 Hempel fiber 与 Houska information-set 量词。纠正方向：第二周期 `(14,10)`、`(9,15)` 各只有单一 constituent，先取共同外包是平凡命题；真正阻塞是 rescued `(9,15)` 的未知 success/miss 分叉。对Run157 rescued mode-9 set取 `K_p=0,K_v=-114428600/70527869`，同一输入support恰饱和`572143/160000`；miss/success两支共享 `e_p` 半宽约0.973594、`e_v`约2.719148，严格满足硬约束，estimator targets继承full-envelope精确包含。证据仅是exact one-step shared-branch safety，不是target闭合、RCI或递归可行性。

下一唯一问题：构造真正多历史的mode-0 `(0,10)`、`(0,15)` target families，合并相同target label的三条returns，并检查同一source-label策略、完整硬约束和下一层逐边inclusion；失败时给exact方向分离证书。
