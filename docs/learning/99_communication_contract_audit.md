# 99 通信合同审计：调度发送不等于控制到达

## 结论

当前项目不能把允许的 return length 从 `{5,10,15}` 改成 `{5,10}`。仓库中的
`PacketSchedule.step(tick, drop)` 把 `drop` 当作调用者给定的环境结果，并在第三次连续丢包时
抛出合同违例；它验证 `max_missing=2` 假设，却没有产生、阻止或恢复 packet arrival。

同名的 `verification/check_scheduler_interface.py` 调度的是有限计算预算下的 support-query
任务，不是传感器采样或网络传输。配置文件也只有固定 `position_period_ticks=5` 和外生
`max_consecutive_missed_packets=2`，没有 measurement request、重传、可靠备用链路、ACK、
channel reservation 或通信资源状态进入控制动作。因此现有控制权限只有物理输入，不含可改变
dropout automaton 的通信动作。

## 时序和量词

当前合同可写成

\[
u_k=\pi(I_k),\qquad \sigma_k\in\Sigma(m_k),
\]

其中控制器选择 `u_k`，环境选择到达结果 `sigma_k`。将最长15 tick的语言替换成最长10 tick，
等价于删除“连续丢两次位置包机会”的环境边；任何状态后验 gate 或短 MPC horizon 都不能完成
这项删除。

即使增加自触发发送动作 `q_k` 和可靠 ACK，也通常只有

\[
q_k\in\{0,1\},\qquad \sigma_k\in\Sigma(q_k,m_k),
\]

ACK用于获知已经发生的成功/失败，自触发动作决定何时尝试通信。除非物理/协议合同进一步保证
例如 `q_k=1,m_k=1 => sigma_k=success`，或有经认证的冗余链路、预约时隙/重传截止期，否则调度
仍不能保证第二个机会成功。

## 最小可接受的合同改造

若以后要把语言真正收紧为 `{5,10}`，至少需要同时给出：

1. 控制器可调用的通信动作、可观测 ACK 与其精确时序；
2. 网络/协议的最坏情形服务保证，证明任意允许执行下连续两次机会不能都失败；
3. 把通信资源状态并入产品自动机，重算全部 reachable histories；
4. 证明调度策略自身满足带宽、能量、延迟和因果约束；
5. 对新语言重新验证 estimator 真值包含、全部中间硬约束、terminal closure 和旧解移位。

概率独立、平均成功率或有限 Monte Carlo 不能替代第2项的确定性证书。若只能得到随机保证，研究
问题必须明确改成 chance/stochastic MPC，不能继续声称当前 hard robust guarantee。

## 对主线的影响

通信支线在当前接口下停止。Run161 的 online 双侧 support gate 仍只能判定当前 seed 是否满足
必要条件，不能改变未来 dropout language。下一步回到原15-tick语言：先反推一个满足 Run161
必要阈值的 mode-0/J14 seed 合同，并检查它能否由合法测量更新初始化；若做不到，再考虑有明确
物理来源的 residual 或 authority 合同变化。
