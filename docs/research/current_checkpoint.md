# 研究短检查点（2026-10-01，Run 136）

主命题：先闭合传统 SMF/输出反馈 tube MPC，学习暂停。2026-10-01 核对远端 `main` 1c49659；Run127--136 仍为本地研究链，本轮基线 Run135 `7ff1100`。

Run136 精读 Athanasopoulos 等 2017 的 reachable multi-set/外包/T-product lift，并重读 Kouramas 等 2005 的 finite-sum scaling；两者的缩放定理要求 full-dimensional C-set disturbance，不能直接用于逐拍秩亏扰动。现按 5/10/15 tick 成功返回周期精确提升：mode 0 用最小分量外包盒，年龄 1--14 保留 signed generators。精确有理数证书通过 3/3 周期和 17/17 原图边；最坏 mode14 支持 `[0.6081,0.4446,2.7543,2.0529,0.005,0.01]`，全部低于状态域半宽，估计误差 tightening 非空。逐拍 boxing 会把 15-tick x 速度 gain 从真实 `1/2` 伪造为 `23/10>1`，禁止再据其发散否证。证据仍条件于冻结 actual-input inclusion；未证明 center/tracking/input 联合域闭合。

2026-10-01 独立重跑 3/3 周期、17/17 边及 120/120 全仓测试通过。下一唯一问题：把 15-mode zonotope exact support 接入实际推力相关联合 `(e,eta)` ancillary 图，构造或否定满足 state/input/residual 合同的非空 mode-indexed RCI；通过后才进入 terminal/shift。
