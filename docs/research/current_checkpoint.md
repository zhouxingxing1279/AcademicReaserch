# 研究短检查点（2026-10-29，Run196）

唯一主线仍为间歇测量与推力调度不确定性下的鲁棒输出反馈Tube MPC；只推进Gate A。起点远端Run195=`0e1a757`，`main=1c49659`。

冻结合同不变：当前`T`可见、未来`T`可在全区间任意跳变。精读两篇PD-RCI原文确认：仿射parameter-dependent offsets产生仿射vertices，与仿射LPV dynamics/control相乘后是不定二次调度条件，最近邻用S-procedure或Polya/LMI充分条件，不能沿用Run195端点LP。纯有理反例`S(p)=[-(1+p),1+p]`、`x+=(1-p/2)x`在任意未来`p+∈[0,1]`时共同目标为`[-1,1]`；端点后继幅度均为1，但`p=1/2`为`9/8`，故endpoint-only认证失效（`COUNTEREXAMPLE`）。不否定PD-RCI、19-pair family、六状态安全或递归可行性；Gate A仍blocked。

下一唯一问题：为19-pair affine-offset family选择声音的全参数综合松弛，并要求返回候选通过独立全区间精确二次验证。
