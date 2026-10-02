# 研究短检查点（2026-10-02，Run 141）

主线为传统 SMF/输出反馈 Tube MPC，学习暂停。起点 Run140 `9dad151`，远端 `main=1c49659`。Run140 已冻结 15-mode/17-edge、actual-thrust/shared-primitive、只观察 `(d,mode,z,bar u)` 的合同，但仍无 RCI。

Run141 重读 Hempel 2011、Lucia 2023 和 Mejari 2023 的 output-fiber/full-state RCI；因果量词已有近邻，不作创新声明。

精确一步 negative control：mode 4 的 `q=eta_pz+h eta_vz` 支持为 `+/-1004143/7200000`。读取隐藏 `q` 的策略需极值 correction `108143/32000 N`，对 miss/success 六个顶点及输入盒可行；同一 observation fiber 的 causal 输入却须同时大于该正值并小于其负值，交集严格为空。整个 mode-4 zonotope 位于 hover 源域。证据仅为 one-step predecessor 分离，不是 RCI/一般不可行证明；全仓 189/189 通过。

下一唯一问题：实现非轴对齐 vertical mode-indexed observation-fiber predecessor/RCI synthesis，强制同一 fiber 与未知后继边共享控制，并用 Run141 作负对照；只报告认证候选或 policy/certificate-class 反证。
