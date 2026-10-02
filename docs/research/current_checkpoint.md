# 研究短检查点（2026-10-03，Run 146）

主线为传统 SMF/输出反馈 Tube MPC，学习暂停。基于远端 Run145 `08bc927` / tree
`6904217`；远端 `main=1c49659`。合同固定15模态/17边、actual-input时序、共享原语及只按
可见 `d=e-eta` 共享输入。

Run146重读 Rungger--Tabuada 2017 的下降迭代、Hempel 2011 noisy-output fiber 量词及
Houska 2023 information ensemble。已有直接近邻；不作算法创新声明。

以 Run145 `C_j^1=E_j x D_j^0` 为 target 执行第二层 exact predecessor。mode 0--13仍有
四维正体积内集，mode14在强制 `14->0 success` 边严格为空。完整 mode14 fiber 的创新半宽
为 `24272147/48000000`，造成 `d_v+` 半宽 `72816441/32000000≈2.275514`；target
`D_0^0` 只容许 `94125081847/57600000000≈1.634116`，严格超量约`0.641398`。correction
只能平移，不能缩小半宽。因此只否定 complete-fiber 候选类，不否定条件 `eta|d` joint
information RCI。另修复历史 validator 的 unmatched `)` 并增加导入/最小运行测试。

当前验证：`verification/` 182/182、`tests/` 39/39；compileall通过。下一唯一问题：停止完整
纤维迭代，构造最小非乘积 mode14 条件纤维，使 `q|d` 半宽低于 mode0 target 门槛，并同时
核查 `14->0 success` 与初始化 miss-chain 可达性。
