# Run151：信息集合族语义准入与方向纠正

日期：2026-10-11；分支 `research/run151-information-ensemble-gate`。

从 `current_checkpoint.md` 接续 Run150，只定向核查其准入卡、日志及 Houska 阅读表。起点工作树干净，本地提交 `1a9570f`；本地 `main=1c49659`。`git ls-remote` 因网络代理不可达失败，GitHub 连接的分支搜索也未能确认全部远端 refs。因此不能声称远端以 Run150 为最新，也不重述旧聊天结论为新证据。

本轮重新核对 Houska 原文 §4.4、Lemma 2 证明、§5.5 及式(24)、§6.4–6.5 和 Theorem 3 证明。特别核实：(i) Lemma 2 的存在性假设包括底层 full-state RCI，并未保证 state-constraint feasibility；(ii) §5.5 将 **feasible invariant information ensemble** 作为终端条件，而非把任意有限期 ensemble 视为终端；(iii) §6.5 的 extreme polytopes 已是形状各异的信息集合，并为每个集合配置共享控制。相关原文：https://arxiv.org/pdf/2307.04146。

因此 Run150 后提出的“最小 return-age/history-conditioned intrinsic shape family”若仅作为新模板，与已有信息集合族方法高度重叠。更关键的是，目前没有证明 `(mode, return age)` 对历史测量相容集合充分；mode/age 相同不代表观测纤维或后继集合相同。若直接做有限周期 support fixed point，所得证书可能只是一个自选外包图，尚未认证所有允许历史、初始化和可见反馈。此判断是**文献覆盖与未闭合证明义务的审计**，不是针对该索引的数学反例，也不否定一般 ensemble RCI 存在。

本轮不写求解器，不复跑未改动的数值测试。新增文献准入卡、此日志与短检查点；仅检查文档链接、提交差异和工作树。论文级主线仍缺：可初始化的因果联合终端信息集合族，实际推力预算，完整状态/输入约束，跨时刻移位证明，以及同预算优势和四旋翼闭环。Run150 宽度阻塞只针对固定形状单模板。

下一轮唯一问题：给出当前 15-mode 合同的**有限索引充分性判据**：从真实历史相容信息集到候选 `(mode, return-age, visible offset)` 集合的保守映射，逐边证明共同原语、测量求交、未知分叉共享输入和初始化覆盖；若判据无法成立，停止有限周期模板支线，改用完整信息 ensemble 基线。
