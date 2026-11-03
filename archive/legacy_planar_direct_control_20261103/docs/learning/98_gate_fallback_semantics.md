# 98. 双侧支持 gate 不能把长缺测合同降级为短合同

## 1. Gate 的正确权限

Run161 的方向半直径 gate 只能决定是否采用一组**已经有完整可行性证书**的15-tick计划；它不能
改变测量到达过程。若自动机仍允许15次连续 miss，控制器在 gate 未通过时不能宣称“改用5或10
tick dropout合同”，因为下一次测量何时到达不是控制输入。

令 `L` 为候选长缺测计划，`B` 为 fallback。在线切换要保持硬约束与递归可行性，至少需要：

1. 当前 posterior 真值包含；
2. 接受 `L` 时，必须验证完整 robust feasibility/terminal compatibility，而不能只验证Run161的
   必要宽度门槛；
3. 拒绝 `L` 时，`B` 从当前全部信息状态可行；
4. 对自动机允许的每条后续 miss/success 边，`B` 的后继仍落入其认证域；
5. 若 `B` 只规划较短时域，其终端必须进入能覆盖余下缺测串的 robust invariant/backup family。

第5项缺失时，短时域只把尚未处理的长缺测风险推到优化窗外，不是安全 fallback。

## 2. 与既有 adaptive-update 证明的关系

Dey--Bhasin 的 consecutive compatibility/fallback、Lu--Cannon--Koksal-Rivet 的嵌套参数集与旧解
移位，以及 Lorenzen--Cannon--Allgöwer 的 recursive model update 都体现同一结构：新信息可改善
在线模型或收紧，但必须保留一条旧证书可移位的可行路径。它们不允许控制器通过更改不受控的
外部不确定性语言来恢复可行性。

本项目的额外困难是 dropout string 属于环境自动机，而非可选 horizon。故合法 fallback 只有三类：

- 沿用覆盖15-tick语言的旧可行计划；
- 切换到同样覆盖15-tick语言的保守 backup family；
- 明确改变系统合同，例如通信层可执行地保证更早测量到达，并把该机制纳入假设和验证。

## 3. 对 Run161 下一步的纠正

当前仓库尚无从宽 posterior 出发、覆盖剩余15-tick缺测语言的 backup family；Run160甚至证明
当前 `J14` seed/固定 residual/correction authority 下，放宽到full-state feedback仍失败。因此
不能把“gate未通过则短-dropout fallback”作为已闭合方向。

方向半直径 gate 仍有价值，但只能作为长计划的快速**拒绝条件**。要把它升级为控制规则，下一步
应二选一：证明通信调度可把允许语言真正缩短；或构造一个覆盖原15-tick语言的保守backup集合。
在此之前不实现在线切换器。

证据等级：`semantic_counterexample_to_short_dropout_fallback_under_uncontrolled_measurement_arrivals`；
这是权限/量词纠正，不是新的控制算法、RCI或递归可行性证明。

