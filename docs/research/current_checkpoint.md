# 研究短检查点（2026-10-03，Run 145）

主线为传统 SMF/输出反馈 Tube MPC，学习暂停。基于 Run144 tree `78d4be8`；远端
`main=1c49659`。合同固定15模态/17边、actual-input时序、共享原语及只按可见
`d=e-eta`共享输入。

Run145重读 Rungger--Tabuada 2017 的下降迭代、Houska 2023 information ensemble 和
Hempel 2011 fiber量词。相关方法已有近邻；本轮不作创新声明。

候选 `S_j=E_eta,vertical^j x {|e_pz|<=1,|e_vz|<=11/4}`。对全部15模态，以共享
`deltaT=0` 构造完整隐藏fiber的 exact observation 内投影 `D_j^0`。15/15均严格正面积，
17/17 estimator edges 精确包含，并保留 Run144 公共 observation box。最小面积在mode14，
为 `899947970530621291/691200000000000000≈1.302008`。证据仅为 first-sweep 四维正体积
内集；不是最大投影、固定点、RCI、全六状态或递归可行性。全仓214/214测试通过。

下一唯一问题：以 `C_j^1={eta in E_j,e-eta in D_j^0}` 为 target 执行第二层 exact inner
predecessor，判断 full-fiber/zero-policy 类是否自映射或在哪个mode首次塌缩；若塌缩，只
否定该受限类，再准入依赖 `d` 的分段/仿射 correction policy。
