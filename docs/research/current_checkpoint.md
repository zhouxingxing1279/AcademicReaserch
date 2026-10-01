# 研究短检查点（2026-10-01，Run 137）

主命题：先闭合传统 SMF/输出反馈 tube MPC，学习暂停。远端 `main` 为 `1c49659`；Run136 远端 `3c3944f` 与本地 `6e389c1` tree `8bc8945` 一致。

Run137 精读 Lorenzetti--Pavone coupled-error RPI，重读 Köhler terminal shift、Mulagaleti--Bemporad qLPV RCI 与 Wehbeh--Kerrigan GSIP。联合 `(e,eta)` RCI 已被覆盖，不作创新声明。配置仅有 actual thrust `[4.905,14.715] N`，无独立 nominal bounds。由 `e_vz+=e_vz+h(deltaT+r_z)`、`d_z(T)=2.086+0.10125T` 精确证明：非空紧致 vertical RCI 的固定 nominal thrust 必须属于 `[7.48763125,11.13910625] N`；持续 endpoint plan 有严格正/负漂移，有限 mode family 也无法修复。hover `9.81 N` 通过；必要区间不证明 RCI 存在。

新增 exact-rational verifier 与2项测试；全仓122/122通过。下一唯一问题：冻结独立 nominal thrust/torque allocation，再构造或反驳消费 Run136 zonotope support 的 mode-indexed augmented `(eta,d)` RCI；未冻结前禁止启动高维求解器。
