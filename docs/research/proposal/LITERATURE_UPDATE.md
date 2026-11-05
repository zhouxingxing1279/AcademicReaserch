# 2026-11-04 定向文献核验与课题差异

这是围绕当前方法的定向更新，不是穷尽性系统综述。检索日期为2026-11-04；使用题名和关键词组合：“constrained zonotope output feedback model predictive control intermittent”“finite memory set membership delayed”“online constraint tightening constrained zonotope”。优先作者稿、出版社和作者单位记录。正文未取得者不用于证明算法细节。

## 已有来源定向复核

| 来源 | 实际读取内容 | 对本题的结论 |
|---|---|---|
| Scott, Raimondo, Marseglia & Braatz (2016), *Constrained zonotopes: A new tool for set-based estimation and fault detection*, Automatica 69:126–136，[DOI](https://doi.org/10.1016/j.automatica.2016.02.036)，[作者稿](https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf) | Proposition 1 (11)–(13)、§5 (32)–(33)及降阶讨论 | 集合运算与可靠外包已有基础；窗口重建需要另证时间戳与历史关系 |
| Hassaan, Pati, Shen & Yong (2021), *Time-Varying Tube-Based Output Feedback MPC for Constrained Linear Systems with Intermittently Delayed Data*, IFAC-PapersOnLine 54(5):103–108，[DOI](https://doi.org/10.1016/j.ifacol.2021.08.482)，[作者稿](https://qiangs.github.io/Papers/Conf_Hassaan2021ADHS.pdf) | §3.1–3.2，Assumptions 1–3、Theorems 5–7与移位证明 | 误差管、共同终端及初始优化可行须分别成立；有限语言理论不能自动覆盖任意交付合同 |
| Ji, Geng & Driggs-Campbell (2022), *Robust Output Feedback MPC with Reduced Conservatism under Ellipsoidal Uncertainty*, CDC:1782–1789，[DOI](https://doi.org/10.1109/CDC51059.2022.9992704)，[作者稿v4](https://arxiv.org/pdf/2008.04980) | §II、§III-A、§V-B (34)及实验定义 | 已有12状态四旋翼算例；原文 \(C=I\)、平衡点线性化、0.2 s离散。不能称作位置-only间歇观测先例或真实飞控内环覆盖 |
| Rego, Raffo, Scott & Raimondo (2020), *Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems*, Automatica 111:108614，[作者记录](https://arxiv.org/abs/1908.09950) | 本轮只重核作者摘要/书目；此前正文阅读不升级 | 非线性预测要包络余项，不能把当前线性原型当成该论文实验复现 |

## 新增待比对候选

**Andrade, R., Normey-Rico, J. E., & Raffo, G. V. (2024).** *Tube-Based Model Predictive Control Based on Constrained Zonotopes*. IEEE Access, 12, 50100–50113. [DOI](https://doi.org/10.1109/ACCESS.2024.3381622)。Crossref DOI记录确认题名、作者、卷页；[作者学校学位论文目录](https://repositorio.ufmg.br/server/api/core/bitstreams/897c723b-7c6a-4927-83ef-de702d77b349/content)亦列出该论文。出版社正文入口不可访问。**等级：书目/作者目录核验，未读独立全文。** 仅足以否定“CZ Tube MPC 从未研究”的泛化主张，不据题名推断其观测、时延或终端细节。

**Robbins, J. A., Glunt, J. J., Thompson, A. F., & Pangborn, H. C. (2026).** *Online Constraint Tightening for MPC using Constrained Zonotope Reachability Analysis and Zonotope Over-Approximations*. ACC 2026, 585–592。[作者单位记录](https://pure.psu.edu/en/publications/online-constraint-tightening-for-mpc-using-constrained-zonotope-r/)。**等级：原始机构摘要。** 摘要明确研究在线约束收紧、CZ 误差可达性与免优化的 zonotope 外包；未取得全文，未确认其对时间戳、估计误差和递归可行性的精确条件。

**Krsmanovic, V., Kohn, F., Finkbeiner, B., & Simovic, M. (2026).** *Predictive Zonotope Reduction: Precise Runtime Monitoring under Uncertainty*. [arXiv:2609.03699](https://arxiv.org/abs/2609.03699)，2026-09-03提交。**等级：预印本摘要。** 关注运行时监测中的集合降阶与资源，提示集合紧致性/开销权衡已有研究；未核对正文，不作为本课题控制定理依据。

**Baranowski, J. (2026).** *Beyond Observability: Sharp Sample Bounds for Minimax State Reconstruction*. [arXiv:2610.26326](https://arxiv.org/abs/2610.26326)，2026-10-19提交；页面注明投稿 International Journal of Control。**等级：预印本摘要，非已核实录用。** 区分无噪精确重构和有界噪声下的最小最坏误差；其假设与本题过程扰动和网络合同尚未逐项比较。

## 对课题方案的实际修改

1. 删除“首次 CZ＋MPC/首次 SMF＋MPC”的创新表述。
2. 将两量测公式限定为给定信息类的支持界，不称完整后验最优界。
3. 把当前工作定位为有限记忆、启动准入及因果控制的可验证基线。
4. 下一贡献需要体现在**同合同下的控制收紧、初始可行域或资源上界**，仅画出更小的估计集合不足。
5. 先全文核验 Andrade/Robbins，再决定是否以模式收紧作为投稿主贡献。文章可获取性不妨碍本轮完成开题方案，但限制新颖性判断。

## 阅读与复现计数

本轮0篇新增完整全文精读；3篇既有来源定向正文复核；Rego为既有来源摘要复核；4项新增候选分别是1项书目/作者目录与3项原始摘要。无作者完整实验复现。本项目公式、代码与仿真是独立数学算例验证，不能标为文献数值实验R3。

唯一累计阅读总账仍为 [PAPER_READING_LOG](../../literature/PAPER_READING_LOG.md)；本文件是本轮论证材料，不另建竞争“已读数量”。
