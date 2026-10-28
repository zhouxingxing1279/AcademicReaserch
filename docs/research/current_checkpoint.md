# 研究短检查点（2026-10-28，Run193）

唯一主线仍为间歇测量与推力调度不确定性下的鲁棒输出反馈Tube MPC；只推进Gate A。起点远端Run192=`69c3266`，`main=1c49659`。

冻结四状态合同：当前`T`在施加`tau`前已知，未来`T∈[4.905,14.715]`任意跳变，`W(T)=1.880+T*0.45^3/6`。旧projected-predecessor用`exists tau forall T`且其`canon`把整数单位法向除成float，故“全Fraction精确行构造”被可执行反例否定。新checker保持Fraction并采用真实`forall measured T exists tau(x,T)`端点局部投影。深度1--4中，调度可见路径把unique candidates由共同力矩的`17/31/99/903`减为`17/31/85/489`，但两者保留facets均为`16/28/52/102`，双向包含误差≤`4.45e-16`（NUMERIC_CHECK）。这不证明全深度相同或RCI。Gate A仍blocked；六状态接口、terminal/shift均OPEN。

下一唯一问题：综合一个充分的调度可见correlated controller/RCI证书并独立核查全部endpoint、`W(T)`、state/torque约束；失败只否定明确策略/集合类别，不再枚举局部configuration cone。
