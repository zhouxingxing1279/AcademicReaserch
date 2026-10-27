# 研究短检查点（2026-10-27，Run157）

主线：间歇位置测量与推力调度不确定性下的鲁棒输出反馈 Tube MPC；先闭合调度一致的 ancillary/RCI 基线，学习与 CZ 收益比较暂停。

仓库核查：main README 仍指向第36章 scheduling-conditioned residual；main 不含短检查点，Run156 分支存在检查点并记录了二周期零策略路径的精确反例。第36章 verifier 与合同已读；381/160 ticks 是 HiGHS 数值边界，不是精确最短性证书。

本轮 DERIVED：固定 (K)、固定多面体 (S={x:Hx\le q}) 下，横向四状态模型的每个 facet-at-vertex 鲁棒不变性左端对 (T) 仿射，因 (A(T)) 与 δ(T)=1.880+T(0.45)^3/6 均仿射，连续 (T\in[T_L,T_U]) 的精确最坏值在端点取得。该结论只简化固定候选验证；不解决联合 (K/S) 合成、packet 因果接口、RCI 存在性或递归可行性。

文献：Köhler et al. 2021 全文阅读 §II–IV；Bujarbaruah et al. 2020 预印本全文阅读 §II–IV、Algorithm 1、Theorem 1/证明；Fleming et al. 2024 仅摘要/作者稿片段；Mayne et al. 2006 仅摘要/元数据。无新颖性声明。

当前阻塞：尚无通过全部调度、扰动、状态及力矩约束的 common RCI 与输出反馈移位证明。下一唯一问题：对仓库已有最简单 correlated RCI candidate 实施精确双端点固定-K 检查；失败只否定该候选，不外推整个控制类。
