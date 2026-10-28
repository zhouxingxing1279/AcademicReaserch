# 研究短检查点（2026-10-27，Run192）

唯一主线：间歇测量与推力调度不确定性下的鲁棒输出反馈Tube MPC；当前只推进Gate A。起点Run190=`97b5ff5`，远端`main=1c49659`。

已核查四状态横向基准：当前`T`可知、未来`T`在`[4.905,14.715]`任意跳变；`W(T)`半宽为`1.880+T*0.45^3/6`，当前仿射合同可精确归约端点。现有common-`P`只证一个`K`的无扰动稳定；该`K`被torque reachable support严格否定。30,000点static-`K`搜索仅是NUMERIC_CHECK；axis-aligned box和单一19-pair cone仅是类别反例。执行器权限LP反驳“特定K失败即plant物理不可行”。审计器以源码SHA-256绑定六类证据。没有充分证书同时覆盖全部endpoint、扰动、state与`|tau|<=0.08`，故Gate A=blocked；六状态接口、终端和递归可行性均OPEN。停止局部配置锥邻接枚举。

下一唯一问题：在冻结`W(T)`与arbitrary-jump合同下，构造一个含全部state/torque约束的充分correlated controller/RCI证书（优先vertex/PWA control），再以独立support检查攻击。
