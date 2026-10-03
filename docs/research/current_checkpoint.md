# 研究短检查点（2026-10-03，Run 148）

主线为传统 SMF/输出反馈 Tube MPC，学习暂停。基于本地 Run147 `038cacc`；其 tree
`a50ec72` 与远端 Run147 `18a2b61` 一致；远端 `main=1c49659`。合同固定15模态/17边、
共享原语、初始化 `mode=0,d=e-eta=0`，控制只读取可见 `d`。

Run148重读 Houska 2023极端信息多面体/连续凸权重控制、Hempel 2011 OFCI fiber量词和
Dey--Bhasin 2026 adaptive tube/递归可行性；统一核查固定零修正下5/10/15 tick首次success。

三条完整return seed的源/返回生成元为`34/36,69/71,104/106`，均exact rank 3并满足
竖直estimator与真值约束。最小凸模板`C0=conv(J4 union J9 union J14)`有exact
perspective lift，rank仍为3，且恒有`d_v=(9/2)d_p`。其`eta`支持
`(1/50,37857863/36000000)`恰触mode-0两坐标边界，严格estimator余量为0；`e`支持
`(23312147/48000000,152955031/72000000)`仍有严格余量。生成元直接拼接会变成
Minkowski和并违反约束。连续selector允许跨路径分数混合；`C0`只是固定零修正 reachable
baseline，不是policy-independent必要target，也不是RCI/六状态/MPC保证。

Run148修正测试当前已转绿待全仓复核。下一唯一问题：先判断`C0`在固定零修正下是否自映射；
若失败，不得外推一般策略不可行。一般causal predecessor必须显式带入可见`d`控制引起的
中心平移；禁止无余量full-dimensional外包。
