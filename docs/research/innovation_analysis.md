# 阶段 3 · 创新性证据与反方审查

2026-11-05。**目前有两类不同强度的结果。** A 有足以排除一个指定恢复目标的精确反例。B 有相同当前准入且两侧均可行时，已收创新改变最优首步的二维存在性证书。C 目前能分开即时和晚一拍交付的一步例子。三项都能形成可检验的问题，现有证据尚不足以认定一项新的通用控制方法。[八项空白检查及验收](research_gap.md) · [完整候选卡](candidate_topics.md)

## 逐项核对潜在贡献

| 候选 | 前作已经回答 | 还有区分度的结果 | 现有证据能支持到哪里 | 什么结果会使它降级 |
|---|---|---|---|---|
| A · 指定恢复盒 | M8/M9 在有限语言与公共可见前缀上设计 ER。最优因果微分、信息半径和相容估计都有先例 | 在预先指定的块长和边界记忆下，把全部合法数据的可达上界与不可达下界相配，并量化遗忘旧包的代价 | 四拍中一个特定可见历史的精确位置/速度坐标半径为 \(7/200,1/25\)。默认固定管使用的速度统一上界为 \(9/100\)。后者包含启动与所有允许相位，二者的比值不能用作算法改善率 | 若只需重写已有有限窗微分公式或在 M8 原设定重新调界，保留反例，撤回该层方法创新 |
| B · 历史改变首步的条件 | M2 已用预测步依赖的量测遗忘。联合误差、不活跃行删除、最优解对约束右端的参数依赖也已有 | 同一可达历史与端点下，用可查条件识别哪些历史等式能经某已知约束行传递到最优首步，以及何时必然冗余 | 新核对的四拍算例同时有最优首步严格不同与原点相同的情况。旧支持最大化面判据只解决单个方向。间歇或延迟情形仍缺证明 | 若仅重述秩、最优面相交或参数 QP，或仅比较两个完整 QP 的解，作用限于解释算例 |
| C · 单包交付期限 | M9 的前缀因果性、Yang–Ozay 的部分信息安全控制、Chen 等的递增时延安全博弈已经涉及此问题的重要部分 | 针对连续位置而速度隐藏的合同，为相邻期限证明“所有分支可行”与“任何因果策略都失败”，并说明哪些连续状态结构使证书可算 | 一步例有解析正反证据。多步可行端须覆盖未枚举的实数观测。反面须覆盖所有控制策略 | 若已有博弈能直接构造同等代价、同等精度的证书，或负例只排除一种仿射策略，缩小或撤回主张 |

### 最可能的三项反对意见及处理

1. **A 的半径可能早由最优恢复理论给出。** 对规则采样，Haimovich 等 Thm. 1 的辅助函数含 \(LTd/2+2N/(Td)\)，与本地两戳速度半径 \(\beta_d\) 同形。先消去已知输入，固定噪声单位，再逐项对齐函数类、初始先验、乱序戳和跨块信息。半径公式的重合有直接证据。在途记忆是否产生前作无法直接处理的必要条件仍未解决。[作者接收稿](https://arxiv.org/pdf/2106.05320) · [本地推导 §4](proposal/FINITE_MEMORY_THEORY.md)
2. **B 的“改进”可能只是删了无关约束，或使用了不可达名义点。** 三拍端点对照和原点支持这种质疑。四拍专项的混合非零历史给出了有鲁棒前缀的严格分离，足以反驳“首步总相同”。若要主张新判据，仍须对参数 QP 的现成活动分区和等价删约束定理给出逐假设差异，并说明怎样在求完整计划前使用它。[专项报告 §§1–3](proposal/OIT_MRPI_WINDOW4_CERTIFICATE.md) · [Nouwens 等 Thm. 1](https://arxiv.org/pdf/2303.16581)
3. **C 可能只是标准安全博弈的重命名。** 递增延迟、消息丢失、自动机与共同控制均有前作。连续状态本身也已进入 Yang–Ozay 的结论。只在能以连续观测几何证明相邻期限、且比已有精确前驱多给出结构或计算结果时，才有独立理论问题。当前一步例无法化解这项反对意见。[Yang–Ozay，Props. 4–5](https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf) · [Chen 等](https://link.springer.com/article/10.1007/s00236-020-00374-7)

## 2026-11-05 定向查新记录

项目证据只取自本地工作树和本地提交。学术检索基于阶段 2 阅读卡、总账与公开学术网页，按标题和 DOI 回到作者或出版社。下列为本轮可复用的实际查询式，分组仅用于定位。定向查新不具有系统检索的完整召回率。阶段 2 的 OpenAlex 限流缺口、M2 与 D4 的期刊定理访问边界继续保留。[阶段 2 检索范围](../literature/stage2/search_protocol.md) · [原有 OIT 检索与命中记录](proposal/OIT_MRPI_FOLLOWUP_EVIDENCE.json)

| 编号 | 查询式 | 用于判断 |
|---|---|---|
| A1 | optimal estimation minimax set membership linear systems irregular sampled bounded acceleration noise nonuniform sampling velocity missing measurements causal differentiation lower bound | 用 Haimovich 作者稿核对规则采样的可达误差 |
| A2 | set membership state estimation minimax radius bounded errors information based complexity chebyshev center optimal recovery linear system missing delayed measurements | Garulli 等的信息复杂性先例；另用准确题名核对元数据 |
| A3 | optimal set membership state estimation intermittent delay set membership filtering bounded error smoothing missing discrete minimax radius observer | Wang 等的不完整观测；与 M5/M7 的时间戳处理对照 |
| B1 | constraint adaptive MPC redundant measurement history control law Nouwens large-scale linear systems 111243 | 追到 Nouwens 作者稿 Thm. 1 |
| B2 | "The explicit linear quadratic regulator for constrained systems" Bemporad Morari Dua Pistikopoulos multiparametric QP active set DOI | 原文 Thm. 2 的局部参数解；另定向复查 Brunner 期刊机构记录 |
| C1 | "10.1007/s00236-020-00374-7" delay resilient control Chen safety games arxiv | 增时延、乱序与有界消息丢失的有限图基线 |
| C2 | maximum allowable transmission interval delayed output measurement control safety reachability delayed measurement age continuous states robust output feedback controlled invariance deadline | 区分传输间隔与某一生成戳的交付截止时刻；另按 Yang–Ozay 准确题名回查正文 |

### 与创新判断直接相关的原文

| 文献与版本 | 核查位置、范围及对本题的限制 |
|---|---|
| H. Haimovich, R. Seeber, R. Aldana-López, D. Gómez-Gutiérrez，*Differentiator for Noisy Sampled Signals With Best Worst-Case Accuracy*，IEEE Control Systems Letters，2021 接收版，2022 卷年，DOI 10.1109/LCSYS.2021.3087542 | 作者稿式 (12)、(14)–(17)、Thm. 1。连续有界二阶导数，规则采样，最佳因果导数精度；对本项目的跨块过期包和约束可行代表点须重新建模。[原文](https://arxiv.org/pdf/2106.05320) |
| A. Garulli, A. Vicino, G. Zappa，*An Information-Based Complexity Framework for Optimal Induced-Norm and Set Membership State Estimation*，IFAC Proceedings Volumes，1997，DOI 10.1016/S1474-6670(17)42832-1 | Crossref 核题录，出版社检索摘要支持范数有界噪声及相容估计；正文访问返回 403，具体定理和算法完备性未核。[出版社摘要](https://www.sciencedirect.com/science/article/pii/S1474667017428321) |
| Y. Wang, J. Huang, D. Wu, Z.-H. Guan, Y.-W. Wang，*Set-Membership filtering with incomplete observations*，Information Sciences 517，2020，37–51，DOI 10.1016/j.ins.2019.12.087 | 正式版 §4.3、Def. 4.1、Thms. 4.1–4.2 的条件关系。使用估计椭球，以缺测持续时间与缺测率约束误差；与逐个带戳前缀下要求的块末坐标半径分别比较。[原文](https://lab.bciml.cn/wp-content/uploads/2020/08/Set-Membership-Filtering-with-Incomplete-Observations.pdf) |
| S. A. N. Nouwens, M. M. Paulides, W. P. M. H. Heemels，*Constraint-adaptive MPC for linear systems: A system-theoretic framework for speeding up MPC through online constraint removal*，Automatica 157，2023，111243，DOI 10.1016/j.automatica.2023.111243 | 作者稿 Def. 1、式 (13)、Thm. 1，给删状态约束后保持可行域和最优解的条件。本题放松的是历史等式，改变潜变量支持，再改变 MPC 约束右端。[作者稿](https://arxiv.org/pdf/2303.16581) |
| A. Bemporad, M. Morari, V. Dua, E. N. Pistikopoulos，*The explicit linear quadratic regulator for constrained systems*，Automatica，2002，DOI 10.1016/S0005-1098(01)00174-1 | Thm. 2 讨论正定代价、独立活动行和相应参数区间内的最优解。本题须另证哪些已交付历史能产生那些右端变化，以及前缀可达性。[作者提供的出版正文](https://cse.lab.imtlucca.it/~bemporad/publications/papers/automatica-mpqp.pdf) |
| L. Yang, N. Ozay，*Safety Control Synthesis for Systems with Missing Measurements*，IFAC-PapersOnLine，2021，DOI 10.1016/j.ifacol.2021.08.481 | 总账已有条目。本轮重查 Props. 4–5，自动机与系统的乘积上可刻画获胜集。成功时可得状态的合同，需与本题仅位置且有噪、过时的交付区分。[作者稿](https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf) |
| L. Yang, N. Ozay，*Efficient Safety Control Synthesis with Imperfect State Information*，IEEE CDC，2020，DOI 10.1109/CDC42340.2020.9303780 | 作者稿 Thm. 1、两类启动信息。构造的是有保证的获胜子集，空子集不构成所有策略失败的证据。[作者稿](https://web.eecs.umich.edu/~necmiye/pubs/YangO_cdc20.pdf) |
| M. Chen, M. Fränzle, Y. Li, P. N. Mosaad, N. Zhan，*Indecision and delays are the parents of failure—taming them algorithmically by synthesizing delay-resilient control*，Acta Informatica 58，2021 卷年，497–528，DOI 10.1007/s00236-020-00374-7 | 出版正文 §1 与算法部分，有限图上逐级增大延迟并处理非保序与有界丢失。本题若离散化连续观测，要证明抽象的方向和精度才能使用负证书。[出版正文](https://link.springer.com/article/10.1007/s00236-020-00374-7) |

M1 的条件性终端/移位、M8 的 ER 合成、M9 的联合控制/估计、N1 的 zonotope-SMF Tube、N2 的在线误差预算、N16 的六维仅位置重构均沿用已核记录。N16 的式 (42)–(43) 两种排列须同步置换，作者仿真内部排列待核。M2 机构摘要仅支持其预测步依赖的量测记忆和递归可行动机。本轮未据此指定其终端公式或迟到处理能力。[阶段 2 原文定位](../literature/stage2/key_comparison.md) · [Brunner 等机构记录](https://research.uni-hannover.de/en/publications/enhancing-output-feedback-mpc-with-set-valued-moving-horizon-esti/) · [Lorenzetti–Pavone §IV-E](https://arxiv.org/pdf/1911.07360)

## 本地数学与数值证据分账

| 来源 | 哪些数据经核对 | 如何解释 |
|---|---|---|
| 新独立有理数核算，A | 两条轨迹在戳 1、2 均交付零读数，到第 4 拍有相反的极值。用加速度硬界和初始位置推得同值上界。运行报告内的 Python 代码可复核 | 这一历史上零代表点同时达到两个最小坐标半径。反驳指定四拍目标；跨块正向保证未建立。[推导和可执行例](research_gap.md) |
| 已有浮点记录，B | 三拍两组 549/775，四拍两组 551/775。零创新网格外点 (4.0233,1.20805)，端点/未来层全创新最大行残差的极小值分别约 +0.001132 与 −0.000431。另一点 (4.02,1.211) 两侧均失败 | 网格计数相同不能判域相同；旧边界点由后续证书检出上一拍前驱障碍。数字来自原始存档，未重新作网格搜索。[旧记录](proposal/OIT_MRPI_FOLLOWUP_EVIDENCE.json) |
| 本地工作树的四拍精确证书，B，本轮只读复跑 | zero、plus、minus、mixed 四组通过。逐拍位置观测的混合记录在 \(z=(3.5,-1.25)\) 有共同可行前缀，名义最优首步差严格大于 0.0028856；加相同 \(Kd_4\) 后差值相同。另一点 \(z=(4.6,0.1)\) 出现仅完整创新可行的名义首步区间 [0.018,0.024] | 取同一序列化参数、未来硬界和终端。前缀命令均有鲁棒续接，历史前缀本身按可行命令构造；单一方法最优闭环遇到此情形的频率仍未知。两种方案在原点均有零代价最优计划。[专项报告](proposal/OIT_MRPI_WINDOW4_CERTIFICATE.md) · [校验器](../../experiments/oit_window4_certificate.py) · [证书数据](../../experiments/results/oit_window4_certificate.json) |
| 仓库已有解析算例，C | 无包时同一决策须满足 \(u_0\le-1/2\) 和 \(u_0\ge1/2\)，及时到包则一律可达标 | 该一步反例针对含隐藏速度的连续初始集合，多步有噪合同仅列为假设。[候选 I-02](proposal/OIT_MRPI_FOLLOWUP_IDEAS.md) |
| 其他负结果 | 旧 OIT 详细运行 360 步均超过 20 ms，相对当前已知偏差基线的代价改善中位数仅 0.005449%。同面数几何压缩对照也缺乏稳定闭环优势 | 工程备选 I-03 要求另建强实时基线。以上是历史实验，同恢复半径和首步分离各自计量。[OIT 审查](proposal/OIT_MRPI_IDEA_CRITIQUE.md) · [压缩验证](proposal/CONG_MPC_VALIDATION_REPORT.md) |

版本取本地 main 的 HEAD 9882220234a20d730a38d648d5c08ac47c3b9d6d 加工作树。运行命令为 **.venv\Scripts\python.exe -B experiments/oit_window4_certificate.py**。证书 JSON、核验器和冻结 controller.json 的 SHA-256 分别为 **ef0ffce053518ec3dacef5eaed75d674a2c227b0e07eb5f2a6edaccce71fb059**、**6ea056df403218ec4bce908fe9655e2b7076b57a1d8817feb04616ce0ffa4aa3**、**ecb66affbe1ee2aa265d1381f4f9c2f67d1a3077cf0598a08d9c63a2714b7b1c**。校验器以有理数检查不等式，终端打印值为浮点简写。没有重新生成证书或重新运行闭环。技能的结构检查仅检查候选材料是否齐备；创新性仍待同行审查和逐假设比对。
