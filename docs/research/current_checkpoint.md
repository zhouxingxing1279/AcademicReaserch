# 研究短检查点（2026-10-02，Run 139）

主线为传统 SMF/输出反馈 Tube MPC，学习暂停。Run138 本地 `595523e` 与远端 `c7daacd` tree `10b21cd` 一致；远端 `main=1c49659`。

本轮重读 Lorenzetti--Pavone augmented-error RPI，精读 Mejari--Mulagaleti--Bemporad RCI 与 Wehbeh--Kerrigan decision-dependent uncertainty。当前“15-mode augmented `(eta,d)` RCI”尚未实例化：`eta=x-hat x` 隐藏，控制只能读 `d=hat x-z` 等可见量；普通 `forall(eta,d) exists u(eta,d)` 会产生非因果证书。配置还缺 quantifier、policy、nominal domain、17-edge timing、actual-thrust shared primitive 与 `S0 x {0}` 初始化。

新增只读 contract gate/6项测试；当前配置返回 `blocked`，不是 RCI 不存在证明。另修复 Run138 改配置后两个旧 envelope 的陈旧 hash；重建确认几何/leaves 未变。全仓170/170测试通过。下一唯一问题：冻结最小 hover-neighborhood partial-information contract，给出17条 edge 的 exact `(eta,d)` 更新、共享 primitive 和 causal policy class；gate 变为 `ready` 后才启动 synthesis。
