# Run163 文献准入卡：主动通信能否认证10-tick缺测上限

## 最近邻核查

| 工作 | 本轮阅读范围 | 与本轮问题的关系 |
|---|---|---|
| Wildhagen, Pezzutto, Schenato, Allgöwer, *Self-triggered MPC robust to bounded packet loss via a min-max approach*, CDC 2022 / arXiv:2204.00339 | **全文定向精读** Sections II-B--II-C、Assumption 1、Section III、Algorithm 1、terminal ingredients | MPC共同选择控制更新和采样间隔，ACK反馈最近一次成败；但最多`P`次连续丢包是独立Assumption 1。min-max预测覆盖所有满足该假设的loss realization，调度本身不创造该上界。 |
| Hassaan, Pati, Shen, Yong, *Time-Varying Tube-Based Output Feedback MPC for Constrained Linear Systems with Intermittently Delayed Data*, IFAC-PapersOnLine 2021 | **全文重读** Sections 2.2--2.3、3.1及Definition 3 | missing/delayed patterns由给定周期有限语言限制；estimator/controller对语言内全部前缀设计。论文不把到达语言作为MPC动作。 |
| Dolk, Heemels, *Event-triggered control systems under packet losses*, Automatica 2017 | 本轮仅核查机构页摘要与书目信息 | ACK/无ACK两种事件触发架构及最大连续dropout与性能/触发间隔权衡；因未取得正文，本轮不引用其定理。 |
| Rutledge, Yong, Ozay, *Finite horizon constrained control and bounded-error estimation in the presence of missing data*, NAHS 2020 | 复核既有全文记录及本轮作者稿题录 | missing-data language是外部给定约束；prefix-based控制/估计不改变语言。 |

## 差异、最强基线与推翻条件

本轮不是设计通信调度算法，而是审计当前仓库是否已有改变dropout语言的权限。最强基线是
Wildhagen等的“可控采样间隔 + ACK + 外生有界丢包”结构。即使比当前仓库多了通信动作和ACK，
其安全证明仍要求独立的连续丢包上界；所以仅增加request action仍不足。

若仓库存在可调用的重传/预约/冗余链路接口，并附确定性最坏服务证书，或能从已有硬件/协议规范
证明任意两个位置包机会至少一个成功，则本轮结论被推翻。当前定向源码与配置审计未发现这些接口。

## 判断

**不通过主动通信fallback实现；通过接口审计与方向停止。** 把`max_missing`从2改成1只会修改假设，
不是控制器证明。下一轮应在原15-tick语言下改变可证的seed/residual/authority合同。
