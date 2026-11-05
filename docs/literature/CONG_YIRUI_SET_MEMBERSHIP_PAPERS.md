# 丛一睿（Yirui Cong）集员滤波相关论文链接

检索日期：2026-11-04。

硕士论文两项创新点的后续理论与仿真评估见 [最新评估报告](../research/proposal/CONG_MPC_MASTERS_EVALUATION.md)，包含同规模强基线、收益有限的结果与各路线的独立贡献要求。

**同日后续全文阅读补充：** 已取得并定向阅读主清单中的12篇全文（第1–8、10–13篇）；第9篇按用户要求不再获取。下文各条的“未取得全文”等描述保留为初始建档时状态，当前版本、实际阅读范围和文件哈希以 [全文清单](sources/cong_mpc_20261104/manifest.json) 为准。MPC结合分析及五个候选课题见 [研究方案](../research/proposal/CONG_MPC_RESEARCH_TOPICS.md)。第7篇卷期页码已由用户PDF核实为《导航定位与授时》13(3)，2026年5月，25–34。定向阅读不等于全部证明审计或实验复现。

本清单收录作者署名包含丛一睿 / Yirui Cong、且直接涉及集员滤波、集合估计、约束 zonotope（CZ）、集员平滑或有界扰动观测的论文。主清单共 **13 篇**，另列 **3 条需要区分版本或发表状态的记录**。期刊论文与其同题预印本合并，不重复计数。

作者身份依据：[IEEE ICUS 2023 官方中英文简介](https://icus.c2.org.cn/uploads/admin/20230609624/6482f26debb2b.pdf)将“丛一睿”与国防科技大学的“Yirui Cong”对应；论文出版元数据中的 ORCID 为 [0000-0003-0621-6331](https://orcid.org/0000-0003-0621-6331)。

核验范围：题名、作者、出版信息和公开摘要为主，未逐篇完成全文研读。DOI 是正式文献入口，不代表全文免费；arXiv PDF 是作者公开版本，可能与最终出版版本不同。部分 IEEE 页面访问受限，其元数据通过出版方提交到 Crossref 的记录核对。中文期刊条目的核验限制在第 7 条单独说明。本清单不宣称穷尽全部成果。

## 一、基础理论与滤波算法

### 1. Rethinking the Mathematical Framework and Optimality of Set-Membership Filtering

- 作者：Yirui Cong, Xiangke Wang, Xiangyun Zhou。
- 正式发表：IEEE Transactions on Automatic Control, **2022**, 67(5): 2544–2551。预印本首次发布于 2020 年。
- 主题：不确定变量、集员滤波数学框架、非随机 Markov 条件与最优性。
- 链接：[正式版 DOI](https://doi.org/10.1109/TAC.2021.3082508) · [arXiv 摘要](https://arxiv.org/abs/2004.04524) · [公开 PDF](https://arxiv.org/pdf/2004.04524) · [ANU 出版记录](https://researchportalplus.anu.edu.au/en/publications/rethinking-the-mathematical-framework-and-optimality-of-set-membe/)。

### 2. Stability of linear set-membership filters with respect to initial conditions: An observation-information perspective

- 作者：Yirui Cong, Xiangke Wang, Xiangyun Zhou。
- 正式发表：Automatica, **2025**, 172: 111993。arXiv 首发于 2022 年，2024 年修订。
- 主题：初始先验对滤波稳定性的影响、观测信息塔（OIT）、具有稳定性保证的 CZ 集员滤波。
- 链接：[正式版 DOI](https://doi.org/10.1016/j.automatica.2024.111993) · [出版社页面](https://www.sciencedirect.com/science/article/pii/S0005109824004874) · [arXiv 摘要](https://arxiv.org/abs/2203.13966) · [公开 PDF](https://arxiv.org/pdf/2203.13966) · [ANU 机构库](https://openresearch-repository.anu.edu.au/items/6b286fd3-a31e-49c7-b1d3-ba98f943c73a)。
- 版本说明：早期题名为 *Stability of Linear Set-Membership Filters*，不另计为一篇论文。

### 3. A Fast and Accurate Linear Constrained Zonotopic Set-membership Filter

- 作者：Xujie Qin, Yirui Cong, Xiangke Wang, Tengfei Liu。
- 出版信息：IEEE Transactions on Automatic Control, **2026**；已有 DOI。检索时 Crossref 页码为 1–8，未列正式卷期。
- 主题定位：快速、高精度的线性 CZ 集员滤波算法；本次仅核验书目信息，不据题名推断具体算法和定理。
- 链接：[正式版 DOI](https://doi.org/10.1109/TAC.2026.3712691) · [IEEE Xplore](https://ieeexplore.ieee.org/document/11604002/) · [Crossref 出版元数据](https://api.crossref.org/works/10.1109/TAC.2026.3712691)。
- 全文状态：本次未找到可核实的公开预印本；IEEE 页面访问受限。

### 4. Existence and Completeness of Bounded Disturbance Observers: A Set-Membership Viewpoint

- 作者：Yudong Li, Yirui Cong, Jiuxiang Dong。
- 正式发表：IEEE Transactions on Automatic Control, **2025**, 70(4): 2762–2769。预印本首次发布于 2023 年。
- 主题：从集员角度研究有界扰动观测器的存在条件、完备性和最坏情形最优性。
- 链接：[正式版 DOI](https://doi.org/10.1109/TAC.2024.3496581) · [arXiv 摘要](https://arxiv.org/abs/2309.02733) · [公开 PDF](https://arxiv.org/pdf/2309.02733) · [Crossref 出版元数据](https://api.crossref.org/works/10.1109/TAC.2024.3496581)。

### 5. Optimal Set-Membership Smoothing

- 作者：Yudong Li, Yirui Cong, Xiangyun Zhou, Jiuxiang Dong。
- 正式发表：IEEE Transactions on Automatic Control, **2026**, 71(5): 3327–3334。预印本首次发布于 2024 年，ANU 记录的在线发表年份为 2025 年。
- 主题：最优集员平滑框架、滤波与平滑的关系，以及线性和部分非线性系统的平滑算法。
- 链接：[正式版 DOI](https://doi.org/10.1109/TAC.2025.3632158) · [arXiv 摘要](https://arxiv.org/abs/2410.09857) · [公开 PDF](https://arxiv.org/pdf/2410.09857) · [ANU 机构库](https://openresearch-repository.anu.edu.au/entities/publication/193e6c79-c33a-4893-8001-6a5356ea4f29) · [Crossref 卷期记录](https://api.crossref.org/works/10.1109/TAC.2025.3632158)。

### 6. Asymptotic Boundedness of Distributed Set-Membership Filtering

- 作者：Yudong Li, Yirui Cong, Shimin Wang, Martin Guay, Jiuxiang Dong。
- 正式发表：IEEE Transactions on Automatic Control, **2026**, 71(11): 7463–7470。机构库记录在线发表日期为 2026-05-18；卷期页码按本次 Crossref 记录。
- 主题：分布式集员滤波的渐近有界性、图结构与观测信息之间的联系。
- 链接：[正式版 DOI](https://doi.org/10.1109/TAC.2026.3694609) · [arXiv 摘要](https://arxiv.org/abs/2509.14106) · [公开 PDF](https://arxiv.org/pdf/2509.14106) · [岭南大学出版记录](https://scholars.ln.edu.hk/en/publications/asymptotic-boundedness-of-distributed-set-membership-filtering/) · [Crossref 卷期记录](https://api.crossref.org/works/10.1109/TAC.2026.3694609)。
- 版本说明：预印本摘要使用 COIT，机构库所载正式版摘要使用 DOIT；引用具体定义或定理时应核对版本。

### 7. 线性离散系统的自适应集员滤波方法

- 英文题名：An adaptive set-membership filtering method for linear discrete-time systems。
- 作者：李育东、董久祥、丛一睿（Yudong Li, Jiuxiang Dong, Yirui Cong）。
- 出版信息：期刊官网已收录；页面 DOI 为 **10.19306/j.cnki.2095-8110.2026.03.003**。本次未核实完整卷期页码，不仅凭 DOI 中的年份字段补写书目。
- 主题：未知噪声边界条件下的自适应集员滤波、观测噪声边界学习。
- 链接：[期刊中文页面](https://dhdwyss.spacejournal.cn/article/doi/10.19306/j.cnki.2095-8110.2026.03.003) · [期刊平台英文页面](https://www.spacejournal.cn/zgkjkxjs/en/article/id/a95a6754-f76d-47b1-98a1-1ed3cbf03015) · [DOI 入口](https://doi.org/10.19306/j.cnki.2095-8110.2026.03.003)。
- 核验限制：已从期刊网站的搜索索引核对中英文题名、作者和摘要；直接访问中文页面遇到验证码，Crossref 查询未返回记录，未取得全文，也未确认 DOI 解析结果。

## 二、多智能体、定位与控制应用

### 8. Set-Membership Filtering-Based Cooperative State Estimation for Multi-Agent Systems

- 作者：Yu Ding, Yirui Cong, Xiangke Wang。
- 正式发表：2023 42nd Chinese Control Conference（CCC）, **2023**, pp. 5791–5796。
- 主题：含绝对和相对量测的协同状态估计、OIT 启发的有限时域集中式 CZ 算法与分布式 CZ 算法。
- 链接：[正式版 DOI](https://doi.org/10.23919/CCC58697.2023.10240662) · [arXiv 摘要](https://arxiv.org/abs/2305.10366) · [公开 PDF](https://arxiv.org/pdf/2305.10366) · [Crossref 出版元数据](https://api.crossref.org/works/10.23919/CCC58697.2023.10240662)。

### 9. Multi-Agent Formation Control Based on Set-Membership Filtering

- 作者：Yute Xiao, Yu Ding, Yirui Cong, Xiangke Wang。
- 正式发表：2023 IEEE International Conference on Unmanned Systems（ICUS）, **2023**, pp. 1136–1141。
- 主题：有限时域 CZ 集员状态估计与多智能体一致性／编队控制的结合。
- 链接：[正式版 DOI](https://doi.org/10.1109/ICUS58632.2023.10318289) · [IEEE 论文页面与摘要](https://ieeexplore.ieee.org/document/10318289/) · [Crossref 出版元数据](https://api.crossref.org/works/10.1109/ICUS58632.2023.10318289)。
- 全文状态：本次未找到可核实的公开全文入口。

### 10. Cooperative Filtering with Range Measurements: A Distributed Constrained Zonotopic Method

- 作者：Yu Ding, Yirui Cong, Xiangke Wang, Long Cheng。
- 正式发表：Proceedings of 2023 7th Chinese Conference on Swarm Intelligence and Cooperative Control，Lecture Notes in Electrical Engineering, vol. 1206，**2024**, pp. 487–502。
- 主题：相对距离量测、分布式协同滤波、扩展约束 zonotope。
- 链接：[正式版 DOI](https://doi.org/10.1007/978-981-97-3332-3_44) · [Springer 章节页面](https://link.springer.com/chapter/10.1007/978-981-97-3332-3_44) · [arXiv 摘要](https://arxiv.org/abs/2309.01185) · [公开 PDF](https://arxiv.org/pdf/2309.01185)。
- 年份说明：会议和预印本为 2023 年，章节在线出版于 2024-06-18。

### 11. Single-Beacon Localization for Mobile Robot: A Set Membership Filtering Approach

- 作者：Xujie Qin, Yirui Cong, Jun Lai, Jinyi Yang, Xiangke Wang。
- 正式发表：IEEE Robotics and Automation Letters, **2024**, 9(11): 9899–9906。
- 主题：单信标测距条件下的移动机器人集员定位。
- 链接：[正式版 DOI](https://doi.org/10.1109/LRA.2024.3406190) · [IEEE Xplore](https://ieeexplore.ieee.org/document/10540277/) · [Crossref 出版元数据](https://api.crossref.org/works/10.1109/LRA.2024.3406190)。
- 全文状态：本次未找到可核实的公开预印本。

### 12. An INS/GNSS Localization Method Based on Set-Membership Filter for Unmanned Aerial Vehicles

- 作者：Xujie Qin, Jun Lai, Yirui Cong, Xiangke Wang。
- 正式发表：2024 3rd Conference on Fully Actuated System Theory and Applications（FASTA）, **2024**, pp. 775–779。
- 主题：未知但有界误差条件下，利用集员滤波进行无人机 INS/GNSS 组合定位。
- 链接：[正式版 DOI](https://doi.org/10.1109/FASTA61401.2024.10595218) · [IEEE Xplore](https://ieeexplore.ieee.org/document/10595218/) · [Crossref 出版元数据](https://api.crossref.org/works/10.1109/FASTA61401.2024.10595218)。
- 全文状态：本次未找到可核实的公开全文入口。

### 13. Set-Membership Estimation Based Distributed Cooperative Localization of Multiple UAVs

- 作者：Yu Ding, Xujie Qin, Yirui Cong, Xiangke Wang。
- 正式发表：IEEE Transactions on Signal and Information Processing over Networks, **2026**, 12: 248–259。
- 主题定位：多无人机分布式协同定位与集员估计；本次核验题名、作者和出版信息，未完成全文阅读。
- 链接：[正式版 DOI](https://doi.org/10.1109/TSIPN.2026.3663852) · [IEEE Xplore](https://ieeexplore.ieee.org/document/11393625/) · [Crossref 出版元数据](https://api.crossref.org/works/10.1109/TSIPN.2026.3663852)。
- 全文状态：IEEE 页面本次要求浏览器验证；未找到可核实的公开预印本。

## 三、需要单独区分的版本与会议记录

### A. 已撤回的预印本：Distributed Set-membership Filtering Frameworks For Multi-agent Systems With Absolute and Relative Measurements

- 作者：Yu Ding, Yirui Cong, Xiangke Wang。
- arXiv 首发于 2023-05-25，**2025-05-24 的 v2 标记为 withdrawn**。
- 作者在撤回说明中指出：作为边缘框架基础的式 (4)–(6) 推导并不完全正确。此处保留链接用于辨识历史引用，不将该版本作为已确立理论的依据。
- 链接：[arXiv 记录及撤回说明](https://arxiv.org/abs/2305.15797)。
- 这与第 8 条的 CCC 论文是不同题名、不同 arXiv 编号的记录，不合并计数。

### B. 作者名单发生变化的预印本：High Performance Detection-based Tracker for Multiple Object Tracking in UAVs

- 2023 年预印本作者：Xi Li, Ruixiang Zhu, Xianguo Yu, **Yirui Cong**, Xiangke Wang。
- 主题：在无人机多目标跟踪中使用集员滤波。
- 链接：[预印本页面](https://www.preprints.org/manuscript/202310.1704) · [预印本 PDF](https://www.preprints.org/manuscript/202310.1704/v1/download)。
- 预印本页面指向的正式版为 *High-Performance Detection-Based Tracker for Multiple Object Tracking in UAVs*, Drones, 2023, 7(11): 681。但 [正式版 Crossref 作者记录](https://api.crossref.org/works/10.3390/drones7110681)列出 Xi Li, Ruixiang Zhu, Xianguo Yu, Xiangke Wang，**不包含 Yirui Cong**。因此不把该正式版计入上述 13 篇丛老师署名论文主清单。[正式版 DOI](https://doi.org/10.3390/drones7110681)。

### C. 仅核实会议议程：Particle Set-Membership Filtering-Based Distributed Localization

- 议程作者：Yute Xiao, Xujie Qin, Shuo Zhang, Xiangke Wang, Yirui Cong。
- 会议：2025 International Conference on Bio-inspired System and Robotics（ICBSR 2025），2025-12-26 至 2025-12-29。
- 链接：[会议官方最终议程 PDF，第 55 页附近](https://icbsr.org/assets/file/ICBSR%202025%20Final%20Program.pdf)。
- 状态：本次仅核实官方议程中存在题名和作者；未确认正式论文 DOI、卷页或公开全文，不将议程本身等同于论文正式发表。

## 四、检索中排除的易混淆条目

以下两篇与研究主题相关，但出版社作者名单不包含 Yirui Cong，因此没有计入主清单：

- [An Unmanned Aerial Vehicle Height Estimation Method: Based on Set-Membership Filter and Constrained Zonotope](https://link.springer.com/chapter/10.1007/978-981-96-2208-5_42)：作者为 Cheng Li, Xujie Qin, Yute Xiao, Liuhao Sheng，2025 年。
- [Set-Membership Relative Localization for Unmanned Aerial Vehicles Based on Constrained Zonotope](https://link.springer.com/chapter/10.1007/978-981-92-4392-1_44)：作者为 Shuo Zhang, Xujie Qin，2026 年。

## 五、结合当前课题的阅读顺序

以下是结合“外环 MPC＋集员估计”课题作出的阅读安排建议，不表示已经完成全文比较：

1. **第 1 篇**：先明确集员滤波的最优性、噪声相关性与非随机 Markov 假设。
2. **第 2 篇**：重点核对 OIT、初始先验稳定性与现有有限记忆 CZ 基线之间的关系。
3. **第 3 篇**：取得全文后，核对快速 CZ 算法的具体机制、复杂度和与当前方法的差别。
4. **第 9 篇**：阅读已有“集员估计＋控制”的连接方式，避免把一般组合当作创新点。
5. **第 4、5、7 篇**：分别补充扰动估计、平滑与未知噪声界方向的文献基础。

## 六、检索与核验记录

- 检索组合包括中文姓名、英文姓名与 set-membership filtering、set membership、constrained zonotope、smoothing、disturbance observer、cooperative localization 等关键词。
- 发现入口包括 [DBLP 作者目录](https://dblp.org/pid/160/8122.html)、期刊／会议官网、机构库和 arXiv；DBLP 条目随后与出版方登记的 Crossref 元数据交叉核对。
- 主清单中 12 篇英文论文的作者和出版信息已通过 Crossref、出版社或机构库核对；第 7 篇中文论文仅完成期刊网站索引级核验，限制已注明。
- 第 6 篇的机构库仍显示在线先发表状态，但 Crossref 已有卷期页码，采用后者并保留来源；第 5 篇保留了预印本、在线发表和正式卷期的年份差异。
- 未找到公开全文不等于没有公开全文；此处仅报告本次检索结果。链接的访问权限、验证码和网站可用性可能变化。
