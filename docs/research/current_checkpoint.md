# 研究短检查点（2026-10-02，Run 138）

主线仍是传统 SMF/输出反馈 Tube MPC，学习暂停。起点 Run137 本地 `e3ae26d` 与远端 `310a2a0` tree `ee0fd07` 一致；远端 `main=1c49659`。

本轮重读 Lorenzetti--Pavone coupled RPI/input tightening 与 Köhler nonlinear joint tightening/terminal shift。最终 nominal input 应由认证 correction support 导出；固定切分不具创新性。现冻结最有利 RCI existence probe：actual thrust `[4.905,14.715]`，nominal `[8.48089375,11.13910625]`，correction `+-3.57589375`；两者 Minkowski 和精确等于 actual box。上侧 vertical boundary balance 用尽 correction，严格余量为0。力矩取 nominal `{0}`、correction `[-0.08,0.08]`，故该探针不能作为最终机动 MPC 域。

新增 exact verifier/3项测试；证据仅为输入预算合同，不是 causal policy、RCI、terminal 或递归可行性。下一唯一问题：保持 Run136 共享生成元和 actual-thrust residual graph，构造或严格否定15-mode augmented `(eta,d)` RCI；若存在，用真实 correction support 恢复严格内点 nominal input set。
