# 研究短检查点（2026-10-28，Run194）

唯一主线仍为间歇测量与推力调度不确定性下的鲁棒输出反馈Tube MPC；只推进Gate A。起点远端Run193=`aae3a53`，`main=1c49659`。

冻结四状态合同不变：当前`T`可见、未来`T∈[4.905,14.715]`任意跳变、`W(T)=1.880+T*0.45^3/6`。Run193的S4有102 facets（行选择为HiGHS `NUMERIC_CHECK`）。冻结该行集后，精确有理数见证证明：S4某个秩4顶点在低推力端点满足`tau_lower(alpha)-tau_upper(alpha)=(5626543/1569600)alpha+6254383/174400>0`，故任意`alpha>0`的同心`alpha*S4`即使允许调度可见vertex torque也不能RCI，且矛盾不依赖`|tau|<=0.08`（`COUNTEREXAMPLE`）。这只否定该homothetic模板类，不否定独立offset、不同法向、PWA/PD-RCI或一般RCI。Gate A仍blocked；Gate B/C、六状态接口、terminal/shift均OPEN。

下一唯一问题：实施独立offset的configuration-constrained vertex-control综合，并独立审计返回候选；不再缩放S4或增加有限层数。
