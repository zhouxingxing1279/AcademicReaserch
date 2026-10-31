## Run225 二步鲁棒前驱与文献复核（2026-10-31；去重已读仍87篇）

**Ilya Kolmanovsky; Elmer G. Gilbert (1998)**, *Theory and computation of disturbance invariant sets for discrete-time linear systems*, *Mathematical Problems in Engineering* 4(4):317–367；DOI https://doi.org/10.1155/S1024123X98000866；出版商 https://onlinelibrary.wiley.com/doi/10.1155/S1024123X98000866 。**核验日期/层级：** 2026-10-31，重新核对出版商摘要、作者、出版信息；**未阅读正文，不新增已读计数**。**研究问题：** 有界扰动 LTI 系统在状态约束域中的最大扰动不变集。**方法/模型：** 摘要指出 Pontryagin 差、最大不变集生成算法、有限确定性条件及 Lyapunov 稳定系统扩展。**重要定理/假设：** 正文具体定理编号与适用条件未核验，不能引用为本轮非线性模型证明。**主要结论：** 摘要称可生成最大不变集的计算表示并给出数值示例。**局限：** LTI/扰动不变性框架，不能直接代替本仓库非线性推力调度和因果控制策略分析。**本课题关联/可复用：** 前驱迭代、集合差与终端核的理论背景；本轮二步包含/排除证书独立推导。**待查：** 受控不变与纯扰动不变的量词区别、非线性/部分观测情形的可计算内核、有限终止性。

**本轮自有结果：** [Run225研究日志](../research/run225_research_log.md)；两个二步可行见证、两个一步可行但二步严格排除状态。不是完整鲁棒终端核；去重已读仍87篇。

## Run224 四状态一步鲁棒前驱与文献核验（2026-10-31；去重已读仍87篇）

**Ilya Kolmanovsky；Elmer G. Gilbert（1998）**，*Theory and computation of disturbance invariant sets for discrete-time linear systems*，*Mathematical Problems in Engineering* 4(4):317–367；DOI https://doi.org/10.1155/S1024123X98000866；出版商 https://onlinelibrary.wiley.com/doi/10.1155/S1024123X98000866 。**核验日期/层级：** 2026-10-31，出版商摘要及书目复核，**未阅读正文、不新增已读计数**。**研究问题：** 有界扰动离散LTI系统在约束域中的最大扰动不变集。**模型/方法：** 摘要说明Pontryagin差、最大不变集生成算法及有限确定性条件。**重要假设/定理：** 具体编号及条件未核验，不能直接迁移至非线性推力调度模型。**主要结论：** 摘要指出给出计算表示、Lyapunov稳定系统扩展及数值例子。**局限：** 主要研究LTI系统，本仓库需要独立证明非线性、控制—扰动量词和输出反馈条件。**关联/可复用：** 鲁棒前驱与终端不变集的概念参考；Run224的一步Taylor区间证书是自行推导，不是该文定理。**待查：** 正文中有限终止条件、控制不变与扰动不变的区别、如何形成可计算内核。

**本轮自有结果：** [Run224研究日志](../research/run224_research_log.md)。安全盒第一轮前驱有两个严格可行见证和两个严格排除点；不构成非空RCI核证明。去重已读87篇不变。

## Run223 双侧倾角必要条件与文献核验（2026-10-31；去重已读仍87篇）

**Kolmanovsky, Ilya; Gilbert, Elmer G.（1998）**，*Theory and computation of disturbance invariant sets for discrete-time linear systems*，*Mathematical Problems in Engineering* 4(4):317–367；DOI https://doi.org/10.1155/S1024123X98000866 ，出版商 https://onlinelibrary.wiley.com/doi/10.1155/S1024123X98000866 。**核验日期/层级：** 2026-10-31，出版商摘要及书目核验，**未阅读正文，不计入新增已读篇数**。**研究问题：** 有界扰动离散LTI系统的最大扰动不变集。**方法/模型：** 论文摘要描述Pontryagin差、最大不变集计算及多模态调节。**重要定理/假设：** 具体编号和假设待正文核验，不能推断其适用非线性推力调度。**主要结论：** 摘要指出给出不变集计算算法及相关数值例子。**局限：** 直接讨论LTI系统，不能无额外证明移用于四状态非线性动力学。**本课题关联/可复用：** 下一轮鲁棒前驱与终端可生存核审计。**待查：** 原文前驱递推的量词、收敛和有限终止条件。

**Franco Blanchini（1999）**，*Set invariance in control*，*Automatica* 35(11):1747–1767；DOI https://doi.org/10.1016/S0005-1098(99)00113-2 。**核验日期/层级：** 2026-10-31，DBLP书目核验，**未阅读正文，不计入新增已读篇数**。**研究问题：** 控制集合不变性。**方法、重要定理/假设、主要结论、局限：** 未见原文，待核验。**关联/可复用：** 四状态终端受控不变性理论背景。**待查：** 非线性受控不变集的适用条件与前驱算子。

**本轮自有结果：** [Run223研究日志](../research/run223_research_log.md)，使用有理数Taylor上界证明任意非空RCI集合必须具有双侧倾角投影。不是上述论文定理。统一去重已读数仍87篇。

## Run222 终端不变集阻塞与文献核验（2026-10-31；去重已读仍87篇）

**Mayne, Raković, Findeisen, Allgöwer（2006）**，*Robust output feedback model predictive control of constrained linear systems*，*Automatica* 42(7):1217–1222；DOI https://doi.org/10.1016/j.automatica.2006.03.005 。**阅读日期/层级：** 2026-10-31，对Run221已阅读§2–4、Propositions 1–3、Theorems 1–2、A1–A3笔记及公开摘要定向复核，非重新全文精读。**研究问题/模型/方法：** 有界扰动约束线性系统的输出反馈Tube MPC；观测误差RPI、跟踪误差管、名义收紧及终端集合。**关键假设：** 误差集合有效、终端不变/下降条件及初始可行性。**主要结论：** 在所列条件下可保证约束与稳定性。**局限：** 不自动覆盖推力调度、姿态小角度不足以抵消横向残差的情况。**本课题关联/可复用：** Run222验证终端非空性这一前提在四状态扩展中失败；不能引用论文为失败模板背书。**待查：** 扩大倾角的联合四状态终端核是否非空？

**Franco Blanchini（1999）**，*Set invariance in control*，*Automatica* 35(11):1747–1767；DOI https://doi.org/10.1016/S0005-1098(99)00113-2；书目 https://dblp.org/rec/journals/automatica/Blanchini99.html 。**核验日期/状态：** 2026-10-31，仅DBLP书目元数据核验，**未阅读正文，不计入已读篇数**。**研究问题：** 控制不变性理论综述（仅根据题名/书目定位）。**方法、具体定理假设、主要结论、局限：** 待原文阅读核验，不编造。**本课题关联/可复用：** 后续审计四状态鲁棒受控不变核的基础参考。**待查：** 具体鲁棒可生存核算法与适用假设。

**本轮自有结果：** [Run222研究日志](../research/run222_research_log.md)，严格有理数漂移反证，仅适用于冻结横向残差不确定性合同，不是文献原定理。论文去重已读数仍87篇。

## Run221 定向原文阅读与终端安全基线（2026-10-31；去重仍87篇）

**Mayne, Raković, Findeisen, Allgöwer（2006）**，*Robust output feedback model predictive control of constrained linear systems*，*Automatica* 42(7):1217–1222；DOI https://doi.org/10.1016/j.automatica.2006.03.005；原文 https://www2.ee.ic.ac.uk/publications/p5346.pdf 。**阅读日期/层级：** 2026-10-31，直接阅读§2–4、Propositions 1–3、Theorems 1–2、A1–A3与终端条件，非全文逐页精读。**问题/模型/方法：** 有界状态与输出扰动的约束线性系统，Luenberger观测器、两个误差RPI、名义Tube MPC及Pontryagin收紧。**关键假设：** 误差闭环Schur稳定、估计误差与控制误差的RPI、初始误差属于这些集合、终端不变与Lyapunov下降条件。**结论：** 在这些前提下得到鲁棒约束满足及稳定性。**局限：** 不直接覆盖15模式位置丢包、推力跳变与控制相关非线性残差。**关联/可复用：** Run221严格构造孤立姿态通道误差RPI与终端名义集合、证明移位可行；并未满足全系统A1–A3，不引用该文证明本项目六状态稳定性。**待查：** 如何在横向—姿态耦合及不确定推力下获得非空的终端不变集合及终端下降函数？

**Lorenzetti, Pavone（2020）**，*A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*，ECC 2020，DOI https://doi.org/10.23919/ECC51009.2020.9143979；arXiv https://arxiv.org/abs/1911.07360；原文 https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf 。**阅读日期/层级：** 2026-10-31，直接阅读§II–IV-D式(7)–(11)，非全文重读。**问题/方法：** 有界测量/过程噪声下的LTI输出反馈Tube MPC，以固定误差截面和收紧名义优化控制复杂度。**关键假设：** 线性模型、可稳定化/观测性及有界噪声，存在RPI与终端控制/代价下降条件。**结论：** 在其条件下可构造高效的Tube MPC。**局限：** 不包含本仓库推力调度和缺测信息状态；固定截面可能保守。**关联/可复用：** Run221复用其固定截面、名义终端/移位设计思想，但没有完整终端下降或20ms最坏运行时间证据。**待查：** 相同终端保证和计算预算下，测量条件化SMF/CZ能否改善四状态控制可行域？

**本轮自有证据：** [Run221研究日志](../research/run221_research_log.md)；32条48拍确定性闭环、精确不变性与移位证书。上述两篇均已在历史阅读记录中出现，不增加去重篇数；不把本轮工程实现写成文献原定理或新的理论创新。

## Run220 文献核验与双约束支持算法（2026-10-31；去重仍87篇）

**Scott、Raimondo、Marseglia、Braatz（2016）**，*Constrained zonotopes: A new tool for set-based estimation and fault detection*，Automatica 69:126–136，DOI https://doi.org/10.1016/j.automatica.2016.02.036；作者稿 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。本轮阅读层级：公开摘要及仓库已有Definition 3、Proposition 1/Section 5笔记交叉核验，非全文重读。研究问题：有界噪声线性系统集合估计；方法：CZ保留线性映射、集合交与Minkowski和相关性。关键前提：有界误差与有效集合表示。结论：可精确表示多面体但复杂度需管理。局限：不直接给出本仓库Tube MPC终端安全保证。关联/可复用：历史联合半空间的控制相关支持；Run220双乘子证书为本仓库自行推导，并非论文定理。待查：真实tick193联合收益及在线预算。

**Köhler、Müller、Allgöwer（2021）**，*Robust output feedback model predictive control using online estimation bounds*，arXiv:2105.03427，https://arxiv.org/abs/2105.03427 。本轮阅读层级：公开摘要与仓库既有定理条件笔记交叉核验，非全文重读。研究问题：噪声输出和扰动下的鲁棒MPC；方法：在线估计误差界结合homothetic tube。关键前提：可靠在线界、检测性/增量可稳定性及相应终端条件。结论：可在这些假设下改善保守性并实现鲁棒约束满足，含10状态四旋翼示例。局限：不自动适用于仓库四状态有限Backup。关联/可复用：将可证上界用于MPC收紧；待查：终端受控不变集、递归可行性及实际运行时间。

**本轮自有算法与证据：** [Run220研究日志](../research/run220_research_log.md)。合成双约束支持从1降至0；GitHub Actions完整checkout实际第193拍12个候选第二半空间的额外可认证增益为0，不能由此证明完整后验无收益。不得将本轮标成新增已读论文。

# PAPER_READING_LOG — 无人机 MPC + SMF 论文阅读记录

> 首次整理：2026-10-30（Run200）。从 [READ_PAPERS.md](READ_PAPERS.md) 的85条历史“已阅读/核对”记录迁移，按**论文题名去重为84篇**；Robbins等《Online Constraint Tightening...》的Run126/161/170记录已合并在同一条下，原有阅读说明均保留。历史文件不修改，以避免破坏依赖其SHA-256的既有可复现实验。此后本文件是新增阅读和修订的唯一入口；旧文件只作为历史快照。
>
> 证据口径：“原文精读”需有明确章节/公式/定理；“正文片段核对”不能推断未见部分；“仅摘要核对”不能视作完整论文阅读。历史记录中缺失的作者、日期、定理假设、局限或待查问题一律保留为**待核验**，不编造。未来每条统一补齐：题名、作者、年份、DOI/arXiv/正式链接、阅读日期及层级、研究问题、模型与方法、关键假设/定理、结论、局限、对课题的关系、可复用技术、待查问题。

## Run219 定向复核：共享扰动历史与控制相关支持（2026-10-31；去重87篇不变）

### Scott、Raimondo、Marseglia、Braatz（2016）——既有论文，公开原稿摘要及集合估计定位复核
- **题名/作者/年份/正式出处：** Joseph K. Scott、Davide M. Raimondo、Giuseppe Roberto Marseglia、Richard D. Braatz，*Constrained zonotopes: A new tool for set-based estimation and fault detection*，2016，*Automatica* 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036；公开原稿 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。
- **阅读日期及核验状态：** 2026-10-31；本轮核对原稿摘要、引言中集合估计问题、CZ交/投影/Minkowski运算的研究定位；历史Run212/216/218已有Definition 3、Proposition 1等分节笔记，**本轮没有重新全文精读**，不新增已读计数。
- **研究问题与模型/方法：** 有界过程扰动和测量误差下的集合状态估计，使用受约束Zonotope保留集合相关性并通过保守降阶控制表示复杂度。
- **关键假设/定理：** 线性集合运算需满足所采用的有界误差模型和表示合同；历史阅读记录已核对CZ运算命题。本轮的共享扰动权重半空间由仓库Euler模型自行推导，**不是Scott等的新增定理**。
- **主要结论/局限：** CZ允许在足够表示复杂度下保留相关约束，但不自动保证鲁棒MPC的终端安全性、20ms计算预算或递归可行性。
- **与课题关联及可复用技术：** Run219证明对位置包135、165、180先合并共享扰动再取支持，可排除Run218旧关键支持极大面，精确改善 `5212367/450000000`；然而五拍速度约束仍阻塞。该单条H半空间**不是完整CZ后验**。
- **待查问题：** 如何以有限条共享扰动约束和可验证降阶实现连续SMF更新；是否能在同等测量信息、控制策略与计算预算下恢复鲁棒MPC准入并补齐终端不变性？

**本轮自有证据（非文献结论）：** [Run219研究日志](../research/run219_research_log.md)；原极大面排除裕度 `5212367/500000000`，控制相关支持改善 `5212367/450000000`，剩余单行裕度约 `-0.02473733102`。去重87篇不变。

## Run218 定向阅读：跨块历史约束的零增益支持证书（2026-10-31；去重87篇不变）

### Scott、Raimondo、Marseglia、Braatz（2016）——已有论文，本轮原稿局部复核
- **题名/作者/年份/出版：** Joseph K. Scott, Davide M. Raimondo, Giuseppe Roberto Marseglia, Richard D. Braatz, *Constrained zonotopes: A new tool for set-based estimation and fault detection*, 2016, *Automatica* 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036；作者公开稿 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf。
- **阅读日期与级别：** 2026-10-31，核对作者原文第2节集合表示与运算、Definition 3和第3节开头；**本轮不是全文重读**。
- **研究问题/方法/模型：** 在有界误差离散系统中，用受约束Zonotope的生成元与线性等式约束表达非对称相关集合；研究线性映射、广义交、Minkowski和及保守降阶。
- **重要假设/结论：** 不限制表示复杂度时可表达任意凸多面体；在所定义的表示和运算下部分集合运算可精确计算；复杂度与精度存在权衡。该结论不保证添加任意历史条带后控制相关支持必然收紧。
- **局限/课题关联/可复用技术：** Run218在第193拍发现一个属于Run216乘积外包的关键支持极大点，同时满足全部6条Run217跨块必要条带，故即使联合使用这些条带该方向增益仍精确为0；无需再对相同6条带重复昂贵的4D LP。此结果不说明完整CZ历史后验同样无增益。
- **待查问题：** 保留共享扰动和多包观测一致性的完整历史约束能否排除该极大点？如何给出可检查的可行/不可行证书？

### Köhler、Müller、Allgöwer（2021）——已有论文，本轮原稿局部复核
- **题名/作者/年份/链接：** Johannes Köhler, Matthias A. Müller, Frank Allgöwer, *Robust output feedback model predictive control using online estimation bounds*, 2021, arXiv https://arxiv.org/abs/2105.03427；公开稿 https://www.ist.uni-stuttgart.de/dokumente/public/Output.pdf。
- **阅读日期与级别：** 2026-10-31，核对摘要、第I节贡献、第II节问题设置及Assumption 1有界扰动；**不是全文重读**。
- **研究问题/方法/模型：** 在线验证状态估计误差界并结合homothetic Tube MPC实现带噪声与扰动的输出反馈约束控制；论文给出非线性四旋翼示例。
- **重要假设/结论：** 有界扰动、检测性/稳定性和相应估计误差、终端/优化条件是其递归可行与约束保证的组成部分；本仓库尚未建立这些条件。
- **局限/课题关联/可复用技术：** 本轮只证明一条有限时域安全审计行在六条历史必要约束下未改善，不是MPC递归可行性结果。在线可靠支持界可作为未来Tube MPC约束收紧的候选接口。
- **待查问题：** 何种紧凑历史一致集合能在20ms预算内提供真正的控制相关支持改善，并连接可验证终端安全集？

**本轮自有负面证据（非论文定理）：** [Run218研究日志](../research/run218_research_log.md)；关键方向6条跨块H-strip联合支持增益精确为0，五步负速度行仍严格阻塞；完整仓库集成尚未执行。去重87篇不变。

## Run217 定向核对：跨块历史相关性与控制相关支持（2026-10-31；去重87篇不变）

### Scott、Raimondo、Marseglia、Braatz（2016）——既有论文，本轮书目/摘要核对
- **题名、作者、年份与出版：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*；Joseph K. Scott、Davide M. Raimondo、Giuseppe Roberto Marseglia、Richard D. Braatz；2016；*Automatica* 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036；作者公开稿 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf。
- **阅读日期及核验级别：** 2026-10-31；本轮重新核对作者稿摘要、书目信息，并对照Run216已记载的Definition 3、Proposition 1、Theorem 1及Section 5定向笔记；**本轮未重新全文精读**。
- **研究问题/模型/方法：** 有界噪声线性系统的集合状态估计；以受约束Zonotope保留集合交、线性映射与Minkowski和中的相关性，并在复杂度增长时保守降阶。
- **重要假设/定理与结论：** CZ在不限制复杂度时可表达凸多面体，若表示适当可精确执行基本集合运算；不意味着任意H-strip程序已经实现CG形式CZ，更不自动给出鲁棒输出反馈MPC递归可行性。
- **局限/本课题关联/可复用技术：** Run217使用冻结Euler四状态模型和已知历史施加力矩构造4D跨块必要约束，再以精确一维对偶计算控制相关支持；这是相关性保留思想的特定实现，但不是该文的CZ递推。当前多条带只逐条外包，实际第193拍尚未执行完整仓库集成，20ms实时性未满足。
- **待查问题：** 跨块条带在第193拍是否使五拍速度约束的负裕度转正？多条带联合支持是否可增量优化？存在姿态模型扰动时如何扩大可靠半径？如何与终端受控不变性闭合？

## Run216 定向复核：联合历史支持与控制相关安全准入（2026-10-31；去重87篇不变）

### Scott、Raimondo、Marseglia、Braatz（2016）——既有论文，作者原文分节复核
- **题名、作者、年份、出版信息：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*；Joseph K. Scott、Davide M. Raimondo、Giuseppe Roberto Marseglia、Richard D. Braatz；2016；*Automatica* 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036；作者公开原文 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。
- **阅读日期及证据层级：** 2026-10-31；直接核对Definition 3、Proposition 1、Theorem 1、Section 5估计递推及复杂度说明；不是全篇重新精读。
- **研究问题与方法/模型：** 用CG表示的constrained zonotope保留有界误差状态估计中的线性映射、集合交及Minkowski和的相关性，并在复杂度增长后做保守降阶。
- **重要假设/定理：** Proposition 1给出CZ三种集合运算的精确恒等式；Theorem 1指出不限制表示复杂度时，CZ可表示任意凸多面体。该等价性**不表示**任意H多边形程序已实现CG形式的CZ递推。
- **主要结论与局限：** 相关性保留有潜在精度优势，但生成元、约束和计算成本会增长；该论文不直接证明本仓库的15-mode推力调度、间歇量测和五拍备份递归可行。
- **与课题关联/可复用技术：** Run216用二维H多边形顶点支持直接进入两层Backup，避免预测盒重置；真实第193拍仍被第5拍速度下界阻塞，说明仅保留(p,v)、(phi,omega)块内历史条带不够。下一步考虑完整4D跨块约束及可验证压缩。
- **待查问题：** 如何在同等历史信息下保存v与phi/omega的动态耦合，并对第193拍临界支持给出可检查的精确/对偶证书和20ms内的计算方案？

### Köhler、Müller、Allgöwer（2021）——既有论文，摘要与既有定理笔记核对
- **题名、作者、年份、链接：** *Robust output feedback model predictive control using online estimation bounds*；Johannes Köhler、Matthias A. Müller、Frank Allgöwer；2021；arXiv https://arxiv.org/abs/2105.03427 。
- **阅读日期及证据层级：** 2026-10-31；核对arXiv公开摘要与仓库既有Assumption 7/Theorem 4笔记，未重新全文精读。
- **研究问题与方法/模型：** 通过在线验证估计误差界，将输出反馈估计与homothetic Tube MPC约束收紧结合；含非线性四旋翼示例。
- **重要假设/定理：** 可靠估计误差界、增量稳定/可检测性、有效终端条件与初始可行性等是全时域保证的前提，不能从有限步Backup的局部准入直接推导。
- **主要结论与局限：** 在线估计界可改善性能/保守性，但其证明条件尚未由本仓库四状态实验满足。
- **与课题关联/可复用技术：** 控制相关支持函数可用于局部鲁棒约束审计；仍须补齐终端不变性及真正滚动MPC。
- **待查问题：** 能否构造一个范围适中、计算可行的终端安全基线，再公平比较CZ与区间SMF？

**本轮自有负面证据（非文献定理）：** [Run216研究日志](../research/run216_research_log.md)；第193拍联合H外包五拍Backup仍拒绝，精确临界行裕度约-0.03632037，原型中位计算约99ms，超出20ms。去重文献仍87篇。

## Run214 定向复核：滚动历史线性约束与 CZ 联合相关性（2026-10-31；已计数去重87篇不变）

### Scott、Raimondo、Marseglia、Braatz（2016）——已有文献，公开正文定向复核
- **题名、作者、年份、正式信息：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*；Joseph K. Scott、Davide M. Raimondo、Giuseppe Roberto Marseglia、Richard D. Braatz；2016；*Automatica* 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036 。
- **阅读日期/证据层级：** 2026-10-31；核对公开论文 PDF 的引言及 CZ 交运算、状态估计方法概述，并复核仓库 Run212 对 Definition 2/3、Proposition 1、Section 5 的阅读记录；**本轮不宣称全文重读**。
- **研究问题与模型/方法：** 如何在有界噪声线性系统中兼顾集合估计精度与运算成本；使用 CZ 表示、交集、投影、Minkowski 和保守降阶。
- **关键假设/定理：** 相关集合运算在其表示合同下成立；精确交集与无损降阶是两回事。Run214 尚未构造 CZ，不能直接继承其数值精度结论。
- **主要结论/局限：** CZ 可以保存一般线性耦合约束，但高阶表示的计算成本需要降阶；论文并未直接保证本仓库15-mode输出反馈安全闭环的终端可行性。
- **与课题关联及可复用技术：** Run214 的20个三包一维支持交集仍存在危险联合盒角点；下一步可用 CZ 保存 `(p,v,phi,omega)` 关联，而非继续增加单变量独立支持界。
- **待查问题：** 能否在相同测量历史与0.02秒控制周期内，得到可靠且可验证的联合支持/可行性证书？

### Rego、Raffo、Scott、Raimondo（2020）——已有文献，本轮仅摘要与书目复核
- **题名、作者、年份、正式信息：** *Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems*；Brenner S. Rego、Guilherme V. Raffo、Joseph K. Scott、Davide M. Raimondo；2020；*Automatica* 111:108614；DOI https://doi.org/10.1016/j.automatica.2019.108614；arXiv https://arxiv.org/abs/1908.09950 。
- **阅读日期/证据层级：** 2026-10-31 仅核对摘要与正式书目；**历史 Run179 已有分章节全文精读记录，本轮不重复声称精读**。
- **研究问题与模型/方法：** 非线性有界扰动系统的 CZ 预测外包与量测交集，采用 mean-value 和 Taylor 扩展。
- **关键假设/定理：** 适用性依赖有效非线性映射外包、误差界与量测集合；Run214 的四状态线性 Euler 恒等式不需要使用其非线性 Taylor 扩展。
- **主要结论/局限：** 相对简单集合外包，CZ 可能保留更多相关性；不能将其示例结果当成本课题的控制安全证明。
- **与课题关联及可复用技术：** 六状态/非线性扩展的候选估计基线；当前先实现可验证线性联合 CZ 与复杂度控制。
- **待查问题：** 对四状态离散动力学，如何实现精确线性 CZ 预测/交，再决定是否有必要采用非线性扩展？

**本轮自有负面结果：** 第193拍最近6个位置包的20组精确支持函数将速度下界提高 `57617501/1440000000 m/s`，但两层因果 Backup 仍拒绝；保留为外包证书阻塞，不推断物理不可生存。参见 [Run214日志](../research/run214_research_log.md)。

## Run213 定向核验：历史一致外包能否转化为控制准入（2026-10-31；去重87篇不变）

### Scott、Raimondo、Marseglia、Braatz（2016）——既有文献，摘要及Run212正文笔记复核
- **题名、作者、年份、正式信息：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*；Joseph K. Scott、Davide M. Raimondo、Giuseppe Roberto Marseglia、Richard D. Braatz；2016；*Automatica* 69:126–136；https://doi.org/10.1016/j.automatica.2016.02.036 。
- **阅读日期及层级：** 2026-10-31；核对公开原文摘要、Run212已核对的Definitions 2–3、Proposition 1和Section 5笔记；本轮未重新全文精读。
- **问题/方法：** 有界误差集员状态估计；通过CZ的线性映射、Minkowski和广义交保留状态相关性。
- **关键假设/结论：** CZ表示中的生成元约束与有效测量误差集是运算成立的前提；集合运算有精确公式，但规模会增长。
- **局限：** 不是现成的15-mode四旋翼鲁棒MPC终端不变集或安全定理。
- **课题关联/可复用：** Run213将Run212三包历史速度外包与当前SMF盒相交，使真实可达第192拍两层因果backup从空恢复为全力矩区间。该交集不是CZ实现；下一步可复用CZ保留跨步联合约束。
- **待查问题：** 以固定预算持续保留相关性后，是否能阻止第193拍再次拒绝？

### Köhler、Müller、Allgöwer（2021）——既有文献，摘要及Run211理论条件复核
- **题名、作者、年份、链接：** *Robust output feedback model predictive control using online estimation bounds*；Johannes Köhler、Matthias A. Müller、Frank Allgöwer；2021；https://arxiv.org/abs/2105.03427 。
- **阅读日期及层级：** 2026-10-31；arXiv摘要与既有Run211 Assumption 7、Theorem 4阅读笔记核对；非全文重读。
- **问题/方法：** 有界估计误差的在线更新、homothetic tube和输出反馈MPC约束收紧。
- **关键假设/结论：** 递归可行与鲁棒约束满足依赖有效在线估计误差界、终端反馈/集合及初始可行性等条件。
- **局限：** 本仓库当前尚无所需终端条件；Run213一次有限步准入不能套用其全时域结论。
- **课题关联/可复用：** 估计界改善须通过控制准入与终端可行性双重检验，不能仅用集合宽度代表控制性能。
- **待查问题：** 如何为15-mode推力调度与间歇测量建立可计算终端安全策略？

**本轮自有证据：** [Run213日志](../research/run213_research_log.md)；第192拍恢复准入，但第193拍仍拒绝；去重论文数保持87。

## Run212 定向正文复核：历史一致集员估计与 CZ 集合运算（2026-10-30；去重87篇不变）

### Scott、Raimondo、Marseglia、Braatz（2016）——既有文献，本轮原文分节核对
- **题名：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*。
- **作者、年份、出版信息：** Joseph K. Scott、Davide M. Raimondo、Giuseppe Roberto Marseglia、Richard D. Braatz；2016；*Automatica* 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036 。
- **可核验原文：** https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。
- **阅读日期与证据层级：** 2026-10-30；本轮直接核对作者公开原文 Definitions 2–3、Section 3.1 Proposition 1及Section 5估计递推片段；不是全篇重新精读。
- **研究问题：** 在有界扰动/量测误差下，如何用兼顾集合表达能力和运算复杂度的表示，保留状态估计中的测量一致性？
- **方法/模型：** CZ 表示 `{Gξ+c: ||ξ||∞<=1, Aξ=b}`，线性映射、Minkowski和广义测量交的闭合运算；Section 5 给出有界误差状态估计集合递推。
- **重要假设/定理：** Definition 3定义CZ；Proposition 1给出上述三种集合运算的精确恒等式，依赖正确的线性测量映射与有效有界集合；约束和生成元数量可能随时间增长。
- **主要结论：** CZ可在不立即丢失所有测量交相关性的情况下传播有界状态集合，并提供复杂度约简方法；集合运算本身不是本课题原创贡献。
- **局限：** CZ阶数/约束规模增长，降阶可能引入保守性；不能直接推导15-mode、未来推力跳变和无终端集合的MPC递归可行性。
- **与本课题关联/可复用：** Run212通过三次位置返包和连续姿态观测，精确排除Run211独立盒的旧速度下端；后续可将多包支持界/历史线性约束接入CZ信息状态和控制相关支持函数。Run212目前只实现严格支持外包，**不是**完整CZ后验。
- **待查问题：** 同一信息、同一控制过滤器、可比较计算预算下，保留完整历史相关性是否能让第192拍首力矩backup非空？如何限制CZ约束规模而不丢失安全证书？

**本轮自有证据（非文献定理）：** 精确三包支持界把第192拍速度下端由-2.4931037251954926收紧至-2.419767402278826 m/s，严格改善7040287/96000000 m/s；不声称已实现鲁棒MPC递归可行。详见[Run212日志](../research/run212_research_log.md)。

## Run211 定向复核：有限候选名义 MPC 与终端安全条件（2026-10-30；去重87篇不变）

### Köhler、Müller、Allgöwer（2021）——历史已读文献，本轮定向正文核验
- **题名：** *Robust output feedback model predictive control using online estimation bounds*。
- **作者/年份/来源：** Johannes Köhler、Matthias A. Müller、Frank Allgöwer；2021；arXiv:2105.03427，https://arxiv.org/abs/2105.03427 ；本轮未另行核实期刊DOI。
- **阅读日期与层级：** 2026-10-30；直接核对 arXiv HTML 的 Section II-A、Section IV-B、Assumption 7、Theorem 4及递归可行性证明片段；不是全篇重新精读。
- **研究问题：** 有噪声输出与有界扰动时，怎样利用在线可靠估计误差界减少鲁棒输出反馈MPC的约束收紧保守性？
- **方法/模型：** 可检测、增量可稳定的非线性系统；在线状态估计误差上界、homothetic tube、MPC终端约束和旧解移位。
- **重要假设/定理：** Assumption 7要求终端反馈、终端集合后继封闭、约束与终端代价条件。Theorem 4还要求其余观测器/增量Lyapunov条件、初始可行性及可靠初始误差界，才得出全时域递归可行与约束满足。
- **主要结论：** 在线有效估计误差界可以减少相对离线统一最坏界的保守性，并在上述前提下保证鲁棒约束满足。
- **局限：** 该理论不能直接继承到Run211独立区间盒、15-mode间歇测量、任意推力跳变且无终端RCI的有限候选名义优化。
- **与课题关联/可复用：** 可复用“在线估计误差界—约束收紧—终端移位”证明清单；Run211第192拍盒角点反例提示应优先检查历史相关性与误差界，而非仅优化名义轨迹。
- **待查问题：** 以历史一致CZ/轨迹可行集代替区间盒后，第192拍的伪角点是否被排除，能否给出更紧的控制相关支持函数？

### Wabersich、Zeilinger（2021）——仅出版社摘要与书目核验，不新增已读计数
- **题名：** *A predictive safety filter for learning-based control of constrained nonlinear dynamical systems*。
- **作者/年份/正式出版：** Kim Peter Wabersich、Melanie N. Zeilinger；2021；*Automatica* 129, Article 109597；DOI https://doi.org/10.1016/j.automatica.2021.109597 。
- **阅读日期与层级：** 2026-10-30；出版社摘要、引言公开节选及正式书目核验，**未全文精读、未核实定理编号**。
- **研究问题：** 如何对建议控制输入进行在线预测安全过滤，在存在模型不确定性和硬约束时寻找安全备份轨迹？
- **方法/模型：** 非线性受约束系统、数据驱动不确定性描述、模型预测安全过滤与备份轨迹。
- **重要假设/定理：** 公开摘要说明安全结论依赖模型不确定性和安全备份设计；具体假设、终端集合构造与证明细节**待全文核验**。
- **主要结论：** 论文提出预测安全过滤框架并报告非线性和四旋翼仿真案例。
- **局限：** 与本仓库四状态间歇SMF和推力调度的模型、量词与安全终端合同不相同；不能借其结论为Run211认证。
- **与课题关联/可复用：** 作为安全过滤的成熟方法基线；比较“名义计划可行”和“有终端备份的递归安全证书”的差异。
- **待查问题：** 全文中安全终端和备份可行性条件是否能在15-mode信息状态上构造；需要先核验正文而非推断。

**本轮自有证据（非文献定理）：** Run211有限候选8拍名义MPC在指定确定性轨迹中未改善Run210准入（191/200/200 → 133/200/81），并严格发现第192拍独立区间外包盒存在5拍速度不可认证角点；角点未证实与完整观测历史联合相容，不能称为物理不可生存。参见 [Run211日志](../research/run211_research_log.md)。

## Run210 新增定向正文阅读：SMF 与终端安全集的严格区分

### Didier、Wabersich、Zeilinger（2021）——新增第87篇去重文献
- **题名：** *Adaptive Model Predictive Safety Certification for Learning-based Control -- Extended Version*。
- **作者、年份、出版信息：** Alexandre Didier、Kim P. Wabersich、Melanie N. Zeilinger；2021；arXiv:2109.13033，相关 CDC 2021 会议论文；本轮未核实会议 DOI，不编造。
- **来源：** https://arxiv.org/abs/2109.13033 。
- **阅读日期及证据层级：** 2026-10-30；核对 arXiv HTML 正文 Sections II-A、II-B、III-A，Assumptions 1–2、Definition 1、Algorithm 1、Theorem 1；不是逐页全文精读。
- **研究问题：** 有界参数/扰动不确定下，如何对任意建议控制器构造具有安全终端和可恢复备份的自适应模型预测安全认证？
- **方法/模型：** 线性参数仿射系统、紧参数集合和有界加性扰动；在线参数集员辨识、鲁棒 tube、MPSC 有限时域优化及终端 safe set/backup 策略。
- **重要假设/定理：** Assumption 1 参数仿射依赖；Assumption 2 真实参数始终包含于逐步嵌套的参数集合。Definition 1 要求终端 safe set 上存在对未来全时域有效的备份控制。Theorem 1 的安全结论依赖上述假设和 Algorithm 1 的可行初始条件与终端备份，不适用于只有四拍安全准入的本仓库。
- **主要结论：** 可用模型更新与备份计划扩张改进安全过滤的可行集合；其证明的关键是终端可持续安全性，不是单纯有限步不越界。
- **局限：** 本文参数 SMF 与本课题状态后验 SMF 不同；未直接覆盖15-mode间歇位置测量和任意推力跳变。其安全结论不能从 Run210 的必要制动区间直接继承。
- **与本课题关联/可复用：** 用作后续 MPC 安全过滤的强基线；复用“终端 safe set＋旧备份移位/回退”的证明结构，严格区分可行核必要条件与终端充分条件。
- **待查问题：** 是否能在四状态模式图上构造可计算的终端备份集合，避免 Run210 正扰动第192拍拒绝？状态 SMF 外包能否保留相关性并支持该终端集合？

**本轮核验但不新增已读条目：** Wabersich、Zeilinger（2021），*A predictive safety filter for learning-based control of constrained nonlinear dynamical systems*，*Automatica* 129:109597，https://doi.org/10.1016/j.automatica.2021.109597；本轮只核对出版社摘要和书目，未逐式研读，不计入87篇。


## Run209 新增分章节阅读：Zonotope viability / discriminating kernel 与四旋翼

### Mitchell、Budzis、Bolyachevets（2019）——新增第86篇去重文献
- **题名：** Invariant, Viability and Discriminating Kernel Under-Approximation via Zonotope Scaling。
- **作者、年份及出处：** Ian M. Mitchell、Jacob Budzis、Andriy Bolyachevets；2019；arXiv预印本。
- **来源：** https://arxiv.org/abs/1901.01006 （未核实正式期刊 DOI，不编造）。
- **阅读日期与层级：** 2026-10-30，arXiv正文分章节阅读，核对 Sections 3.2、5.3、6（Proposition 6.2、Section 6.1 四旋翼例）、8；非逐页全文精读。
- **研究问题：** 对有状态/输入约束与对抗扰动的离散仿射系统，如何可扩展地构造不变、viable 和 discriminating kernels 的内近似，而不是仅做前向可达外包？
- **模型与方法：** center-generator zonotope、生成元缩放、凸规划；输入依赖状态生成元与扰动生成元；示例含双积分器和六维四旋翼纵向模型的线性化/误差包络。
- **关键命题/假设：** Section 3.2 定义不同量词下的可行核；Proposition 6.2 给出控制/扰动约束满足时，候选 zonotope 包含于有限时域 discriminating kernel 的充分条件。要求相应仿射模型与有界扰动外包有效；不是任意非线性/间歇测量信息状态的无条件定理。
- **主要结论：** 通过控制生成元与扰动集联合综合，能够计算保守的安全可行域内近似；六维四旋翼算例提供 zonotope 安全集的数值结果，展示与 ellipsoid 基线相比可能降低保守性，但依赖其冻结模型与误差界。
- **局限：** 有限时域、离散仿射近似与模型误差包络，未直接解决本仓库15-mode间歇位置测量、当前推力可见/未来推力跳变、条件化 SMF 信息状态与无限时域递归可行性。
- **与课题关联/可复用：** Run209 发现实际可达状态存在五拍内不可避免的姿态硬约束违约；因此必须在鲁棒安全过滤器前端建立 viability 必要条件，并以本文的 zonotope kernel 内近似作为可比的充分安全域基线。注意内近似失败不能证明全局无解；本轮的物理制动反例来自独立精确公式。
- **待查问题：** 是否能在相同计算预算内将姿态制动约束与 SMF/CZ 后验联合，建立既不丢弃位置—速度相关性又能保证因果控制的可行安全子域？如何向六维模型移植并保留有界扰动保证？

**未计入已读总数的候选：** Jean-Pierre Aubin（1990），A Survey of Viability Theory，SIAM J. Control Optim. 28(4):749–788，https://doi.org/10.1137/0328044；本轮仅核对出版社书目和摘要，尚未研读正文，待后续精读。

## Run208 新增书目/摘要核验：两阶段可调鲁棒优化的仿射后继策略

### Bertsimas、Goyal（2011）——新增第85篇去重文献
- **题名：** *On the Power and Limitations of Affine Policies in Two-Stage Adaptive Optimization*。
- **作者/年份/出处：** Dimitris Bertsimas、Vineet Goyal；2011；*Mathematical Programming*。
- **DOI/来源：** https://doi.org/10.1007/s10107-011-0444-4；MIT作者终稿书目及摘要 https://dspace.mit.edu/entities/publication/8fea3eec-4824-4b5c-8bb1-b7093e0bc2f2 。
- **阅读日期/证据层级：** 2026-10-30；**仅正式书目与摘要核对，未阅读全文或逐式核验**，不将此条记作精读。
- **研究问题/模型/方法：** 在右端项不确定的两阶段可调鲁棒线性优化中，比较第二阶段仿射决策规则与完全可调策略的最坏代价。
- **已核实主要结论：** 摘要指出仿射策略在一般不确定集合上可能严格次优，同时分析了某些集合结构下的适用性；具体近似比与最优性条件未逐式复核。
- **关键假设/定理：** 本轮仅核对摘要所述两阶段线性优化及不确定右端项；正文的定理编号、全部假设和证明**待核验**。
- **局限：** 论文不涉及四旋翼动力学、SMF、15-mode间歇测量或推力相关扰动；不能将其近似比定理直接移植到本仓库。
- **与本课题关联/可复用：** Run208 采用下一可见推力的仿射后继力矩规则，属于经典 adjustable robust optimization 思想。可复用“第一阶段共享动作、第二阶段仅依赖已揭示信息”的非预见性建模，但需对本仓库单独建立集合包含与硬约束证书。
- **待查问题：** 在后继姿态/位置观测可见的连续信息空间中，能否用有限复杂度观测仿射/分区策略给出严格可靠的控制可行域，并量化相对测量无关两层桥的严格收益？

**本轮复核的历史文献：** Köhler、Müller、Allgöwer（2021），*Robust output feedback model predictive control using online estimation bounds*，https://arxiv.org/abs/2105.03427；本轮只核对摘要及Run206/207已有定理阅读笔记，没有重新阅读全文。它要求的终端及递归可行性前提尚未由Run208满足。

**Run208 自有结果（不是上述论文定理）：** 四状态精确有理数两层 backup 允许下一拍非零力矩，在合法可达交变历史第95拍将Run207空准入区间严格扩展为非空；第96拍仍拒绝。新策略不使用下一测量数值，尚未证明测量条件化增益或无限时域安全。见 [Run208日志](../research/run208_research_log.md)。

**去重计数：历史84篇 + 本轮新增Bertsimas–Goyal 1篇 = 85篇；阅读层级严格区分。**

## Run207 定向核验：因果移位桥与终端可行性的差异（既有84篇，不重复计数）

### Köhler、Müller、Allgöwer（2021）
- **题名/作者/年份/链接：** *Robust output feedback model predictive control using online estimation bounds*；Johannes Köhler, Matthias A. Müller, Frank Allgöwer；2021；https://arxiv.org/abs/2105.03427 。
- **本轮日期/证据层级：** 2026-10-30；核对 arXiv 正式题名、作者、摘要及 Run206 已有的 Algorithm 1、Assumption 7、Theorem 4 历史精读记录；本轮未重新逐式阅读全文。
- **问题/方法/结论：** 有界测量噪声与扰动下，结合在线有效估计误差界、homothetic tube、约束收紧和终端条件，建立鲁棒输出反馈 MPC 的约束保证。历史精读记录指出递归可行性依赖初始可行性、增量稳定/可检测及终端条件。
- **局限/课题关系/可复用/待查：** 论文没有直接认证本仓库15-mode位置丢包、任意推力调度的盒重置一步桥。可复用“旧计划移位须保留终端可行性”的证明检查顺序；下一步需明确本仓库是否存在后继测量条件化的安全控制策略，不能把一次可移位等同于无限时域递归可行。

### Lorenzetti、Pavone（2020）
- **题名/作者/年份/链接：** *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*；Joseph Lorenzetti, Marco Pavone；ECC 2020；DOI https://doi.org/10.23919/ECC51009.2020.9143979 ；作者版 https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf 。
- **本轮日期/证据层级：** 2026-10-30；核对论文摘要及 Run204/205 已有的固定截面 tube、RPI 相关阅读笔记；不宣称本轮全文精读。
- **问题/方法/结论：** 离散线性系统中以固定截面 tube 和 RPI 误差集进行输出反馈鲁棒 MPC 设计，降低在线复杂度。
- **局限/课题关系/可复用/待查：** RPI 终端及误差管束不能由 Run207 的五拍盒重置安全约束替代。下一步可借鉴其终端设计和误差耦合思路，但需要在本仓库四状态调度与观测图上独立建立不变性。

**Run207 自有结论：** 260项精确有理约束可保证同一当前力矩之后，任意合法下一观测后验均有四拍零力矩备份；交变扰动可达场景第95拍该更强桥条件拒绝，而四拍零力矩备份仍可行。这是特定控制模板的一步条件性充分保证，不是上述论文的定理，也不是终端 RCI。详见 [Run207 日志](../research/run207_research_log.md)。

## Run206 定向复核：真实可达后验与有限时域 backup 的区别（仍为历史84篇）

### Köhler、Müller、Allgöwer（2021）
- **题名/作者/年份/链接：** *Robust output feedback model predictive control using online estimation bounds*；Johannes Köhler, Matthias A. Müller, Frank Allgöwer；2021；arXiv:2105.03427，https://arxiv.org/abs/2105.03427；作者全文 https://www.ist.uni-stuttgart.de/dokumente/public/Output.pdf 。
- **阅读日期/层级：** 2026-10-30；本轮定向重读作者全文 Section III-C（set-membership bounds）、Section IV Algorithm 1、Assumption 7、Theorem 4 及旧计划移位证明；承接 Run200 既有深读，不宣称重读全部定理。
- **研究问题/方法：** 有界扰动及噪声下的非线性鲁棒输出反馈 MPC；使用在线有效的估计误差界、homothetic tube、约束收紧及终端成分。
- **关键假设/结论：** Theorem 4 需要 Assumptions 1、3、4、5、7，δ-IOSS 与 δ-ISS CLF、初始优化可行及有效初始误差界；移位候选与终端包含支撑递归可行性及真实约束满足。单步/四拍备份安全准入不满足这些前提。
- **局限/课题关联/可复用技术/待查：** 论文提供输出反馈 MPC 证明骨架及四旋翼数值示例，但未直接认证本仓库15-mode位置缺包与推力每拍任意跳变。下一步需证明任意合法后继观测下存在同一当前动作和可行后继备份；不能仅把更紧的后验解释为安全控制器。

### Alamo、Bravo、Camacho（2005）
- **题名/作者/年份/链接：** *Guaranteed state estimation by zonotopes*；Teodoro Alamo, José Manuel Bravo, Eduardo F. Camacho；Automatica 41(6):1035–1043（2005）；DOI https://doi.org/10.1016/j.automatica.2004.12.008 。
- **阅读日期/层级：** 2026-10-30；仅正式书目、摘要和历史笔记交叉核对；**未取得可逐式核验的全文**，不引用具体未核实定理。
- **研究问题/方法/结论：** 以 zonotope 构造有界过程/测量不确定性下的可靠状态集合外包；说明保证包含与集合收紧是既有集合估计技术。
- **局限/课题关联/可复用技术/待查：** 该估计文献不提供本仓库四拍控制准入或递归终端保证；Run206 的两包速度约束是冻结离散积分恒等式，非新型 zonotope 方法。后续比较区间、CZ 与测量条件化支持函数时需控制同一信息和计算预算。

**Run206 自有结果（不是上述论文的定理）：** 真实零初态、合法扰动/观测历史的精确 Fraction 递推中，纯区间估计在第55/63/57拍首次拒绝四拍 backup；两包速度约束后对应100拍内未拒绝/第96拍拒绝/100拍内未拒绝。它仅证实三条指定轨迹上有限前缀安全和过滤器保守性差异，Gate A 仍 blocked。

## Run205 定向复核：移动中心信息盒的四拍控制准入（历史84篇内，不重复计数）

### Lorenzetti、Pavone（2020）
- **题名/作者/年份/链接：** *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*；Joseph Lorenzetti, Marco Pavone；ECC 2020；DOI https://doi.org/10.23919/ECC51009.2020.9143979；作者全文 https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf 。
- **阅读日期/证据层级：** 2026-10-30；核对摘要与作者版中的输出反馈单管束、RPI和终端条件定位；承接历史 Run203/204 已有章节复核，不声称本轮逐定理重读。
- **研究问题/模型/方法：** 离散 LTI、加性有界扰动及测量噪声的输出反馈鲁棒 Tube MPC；估计误差/跟踪误差集合、约束收紧、终端控制。
- **关键前提/结论：** 论文的递归可行性与鲁棒约束保证依赖适当 RPI/终端包含及初始可行性等条件；本轮仅固定四拍开环 backup，未满足这些条件。
- **局限/课题关联/可复用技术/待查：** 不直接覆盖15-mode间歇位置观测与未来推力任意跳变。可复用终端约束与移位可行性证明框架；待查观测条件化、控制先于后继边的统一递归策略。

### Scott、Raimondo、Marseglia、Braatz（2016）
- **题名/作者/年份/链接：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*；Joseph K. Scott, Davide M. Raimondo, Giuseppe Roberto Marseglia, Richard D. Braatz；Automatica 69:126–136 (2016)；DOI https://doi.org/10.1016/j.automatica.2016.02.036；作者全文 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。
- **阅读日期/证据层级：** 2026-10-30；核对摘要、Introduction 和集合表示/精确交投影运算的定位，结合 Run202 的既有深入记录；本轮未逐式复核全文。
- **研究问题/模型/方法：** 用 constrained zonotope 表示有界不确定状态集合并执行集合估计/故障检测。
- **关键前提/结论：** 不限制表示复杂度时 CZ 可表示凸多面体，且标准集合运算有代数表达；不能由此自动得到控制律、稳定性或递归可行性。
- **局限/课题关联/可复用技术/待查：** Run205 仅使用独立坐标区间外包，舍弃 CZ 相关性；下一轮需对可达的条件化 CZ 后验使用支持函数/外包并比较与区间过滤器的保守性。

**Run205自有结果（不是上述论文的结论）：** 固定四拍开环 backup 下，移动中心盒的原始硬约束可接受力矩区间可由精确有理数和未来推力顶点穷举计算；合成中心未证明可由冻结初态到达，Gate A 仍 blocked。

## Run204 定向复核与证据边界（仍为历史84篇，不新增计数）

### Athanasopoulos、Smpoukis、Jungers（2017）
- **题名/作者/年份/链接：** *Invariance in Constrained Switching*；Nikolaos Athanasopoulos, Konstantinos Smpoukis, Raphaël M. Jungers；2017；https://arxiv.org/abs/1702.00598；相关期刊版本题名为 *Invariant Sets Analysis for Constrained Switching Systems*，DOI https://doi.org/10.1109/LCSYS.2017.2714840（区分版本）。
- **阅读日期与层级：** 2026-10-30；核对 arXiv 摘要、Introduction、图约束切换与 invariant multi-set 定义/基本描述；未重新证明全文定理。
- **研究问题/模型/方法：** 有向自动机约束切换的离散线性扰动系统，按图节点定义 invariant multi-set，以前向/后向可达映射研究不变集合。
- **关键前提/结论：** 系统切换序列受合法图边约束，图索引集合必须满足相应边的后继包含；稳定性与普通单一不变集存在性不能简单等同。具体近似定理有稳定性等前提，本轮不援引未核实的适用性。
- **局限/课题关联/可复用/待查：** 文中主要为切换系统不变性框架，不直接解决本仓库“控制先于未知边、观测更新改变后验”的信息状态；可复用图索引不变性表述。Run204 对固定原点直积物理状态盒的排除是**本仓库冻结合同自己的推导**，不是该论文定理。下一步构造移动中心/相关后验集合上的因果后继包含。

### Lorenzetti、Pavone（2020）
- **题名/作者/年份/链接：** *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*；Joseph Lorenzetti, Marco Pavone；2020 ECC；DOI https://doi.org/10.23919/ECC51009.2020.9143979；作者全文 https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf 。
- **阅读日期与层级：** 2026-10-30；核对作者全文 Section II Assumptions 1–2、Section III-A RPI定义、Section IV-A/B/C 的式(7)–(9)与终端结构，结合原有Run203深读记录。
- **研究问题/方法：** 离散LTI、加性有界扰动/测量噪声下的输出反馈 Tube MPC；Luenberger估计、误差RPI、名义轨迹约束收紧和终端约束。
- **关键假设/结论：** 论文要求可控可观、紧有界噪声集合、合适的稳定估计器和反馈及终端条件；本轮区间SMF+饱和中点LQR没有满足其终端/误差管束条件，不能转移递归可行性结论。
- **局限/关联/复用/待查：** 原文LTI与持续观测结构不覆盖未来推力任意跳变及15-mode位置缺包；可复用终端—RPI—约束收紧—移位的证明架构。待查如何将后验移动中心和未来观测分支纳入同一可计算控制条件。

### Ping、Yao、Ding、Li（2022）
- **题名/作者/年份/链接：** *Tube-Based Output Feedback Robust MPC for LPV Systems With Scaled Terminal Constraint Sets*；Xubin Ping, Junying Yao, Baocang Ding, Zhiwu Li；IEEE Transactions on Cybernetics 52(8):7563–7576，2022；DOI https://doi.org/10.1109/TCYB.2020.3041334；PubMed PMID 33417577。
- **阅读日期与层级：** 2026-10-30；**仅正式摘要复核**，没有重读正文定理/公式；延续历史Run131的同级证据。
- **问题/方法/结论：** 有界扰动和噪声的离散LPV输出反馈Tube RMPC，离线设计查找表、在线约束收紧与scaled terminal；论文声称递归可行性/稳定性，具体定理前提需原文核对。
- **局限/关联/复用/待查：** 与本课题的LPV、输出反馈和终端收紧高度相关，但不能把其scaled terminal当作新机制；尚未核对是否支持任意快速推力跳变、间歇位置包及CZ相关性。下一步按原文逐式核对再移植。

**Run204自有实验（非论文结论）：** 15-mode五边环排除固定原点直积物理状态盒族，为精确类特定反证；四状态区间SMF中点饱和反馈9条150 tick数值探针显示多种硬约束失败。不能由此推断一般鲁棒输出反馈Tube MPC不可行。

## Run203 定向复核（历史84篇内，不重复计数）

### Lorenzetti、Pavone（2020）
- **题名/出处/链接：** *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*；ECC 2020；DOI https://doi.org/10.23919/ECC51009.2020.9143979；作者全文 https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf 。
- **阅读日期/层级：** 2026-10-30，定向重读 Section IV-C/D/E，式(9)–(13)及 Proposition 1；原84篇已有记录。
- **问题、模型和方法：** LTI离散系统、有界加性过程/测量噪声、输出反馈Tube MPC；名义优化使用终端集合与收紧约束，误差RPI支撑真实状态/输入约束。
- **关键假设/结论：** 终端控制满足正不变包含、名义约束可行，误差初态在RPI且初始优化可行，才能得到递归可行与鲁棒约束满足；本轮三拍安全准入没有这些条件。
- **局限/本课题关联/复用：** 持续观测的LTI和固定管束结构不能直接覆盖15-mode间歇位置观测及未来推力任意跳变。复用其“终端不变—误差管束—约束收紧—旧解移位”证明结构。
- **待查：** 对模式相关SMF后验如何形成因果统一的后继终端包含，不误用三拍硬约束PASS。

### Athanasopoulos、Smpoukis、Jungers（2017）
- **题名/出处/链接：** *Invariance in Constrained Switching*；arXiv:1702.00598，https://arxiv.org/abs/1702.00598；相关期刊版本 *Invariant Sets Analysis for Constrained Switching Systems*，IEEE Control Systems Letters 1(2):256–261，DOI https://doi.org/10.1109/LCSYS.2017.2714840（版本题名有别，勿混淆）。
- **阅读日期/层级：** 2026-10-30，摘要、Introduction及仓库Run135/136历史阅读记录的交叉核对；本轮未重新逐式验证全文所有定理。
- **问题、模型和方法：** 由有向自动机约束切换序列的离散线性扰动系统；使用节点索引的不变多集合研究可行的后继包含。
- **关键结论/限制：** 图约束可以让不变集合依赖模式；外逼近算法的收敛保证还需稳定性、扰动集合等前提，不可直接移植至本仓库秩亏噪声和控制前于后继边的量词结构。
- **本课题关联/可复用/待查：** 15-mode终端候选必须逐合法边满足一拍包含；下轮需验证是否存在因果反馈，且同一当前控制必须覆盖所有未揭示的后继边。

**Run203 自有结果（非论文结论）：** 在冻结四状态模型、指定零观测历史及Run202精确有理后验外包下，三拍未来推力端点枚举给出原硬约束局部PASS；永久零力矩72拍速度越界构成反例。证据只属于有限时域审计，不是RCI、递归可行性或稳定性证明。

## Run202 定向重读与新推导（原84篇内，不重复计数）

### Scott、Raimondo、Marseglia、Braatz（2016）
- **题名：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*；*Automatica* 69:126–136；DOI：https://doi.org/10.1016/j.automatica.2016.02.036；作者版：https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf
- **阅读日期/层级：** 2026-10-30，原文 Definition 2（式(6) generalized intersection）、Definition 3（式(9) CZ），Section 3.1；属于原84篇的定向重读。
- **问题/方法/假设：** 有界噪声下离散线性系统的集合状态估计；CZ以 `c+Gξ, ||ξ||∞≤1, Aξ=b` 表示，并可通过增加有界噪声生成元与等式约束精确更新测量一致集合。若不压缩生成元与约束，其规模持续增长。
- **结论/局限：** 精确线性像、Minkowski和及 generalized intersection 是既有技术；本轮四状态代码只是实例化。它不提供 MPC 终端不变性或实时求解保证；浮点 LP 投影支持不自动变成数学证书。
- **本课题复用/待查：** 固定推力下按真实姿态/位置观测更新 `(px,vx,phi,omega)` 的精确 CZ；下一步比较控制相关后验支持、固定预算约减与实际控制准入，避免把 CZ 本身当创新。

### Lorenzetti、Pavone（2020）
- **题名：** *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*；2020 ECC；DOI：https://doi.org/10.23919/ECC51009.2020.9143979；全文：https://stanfordasl.github.io/wp-content/papercite-data/pdf/Lorenzetti.Pavone.ECC20.pdf
- **阅读日期/层级：** 2026-10-30，Section II 问题模型、Section IV 的管束误差/约束收紧与终端条件；原84篇中的定向重读。
- **问题/方法/假设：** 线性离散定常系统、有界加性扰动与噪声，使用输出反馈鲁棒 MPC 与离线 RPI/终端约束；递归可行性不能仅由状态估计集合包含推出。
- **局限/关联/待查：** 本项目有间歇位置测量、当前推力可见但未来任意跳变的 LPV 合同，不符合直接套用其 LTI/持续观测证明的前提。需要独立的模式相关 backup、控制误差管束和终端证书。

**Run202新推导（非论文原定理）：** 对零位置/姿态观测历史、固定已知推力，利用两次位置观测消去初始速度，得到严格返包后速度界 `|v_n|≤2σp/(nh)+h(n+1)(Tσφ+d(T))/2`；15 tick 低/高推力下相对独立区间预测可靠收紧35.1%/36.0%。精确 CZ 递推和该恒等式是冻结模型审计，不宣称新通用滤波算法或鲁棒控制定理。

## Run200 定向复核与课题判断（下述三篇已在历史84篇内，不重复计数）

### Köhler、Müller、Allgöwer（2021）
- **题名/链接：** *Robust output feedback model predictive control using online estimation bounds*；https://arxiv.org/abs/2105.03427
- **阅读日期/层级：** 2026-10-30，原文 Section IV-B 的 Algorithm 1、Assumption 7、Theorem 4 及其证明中旧解移位部分；既有 Run127 记录亦注明精读。
- **问题与方法：** 有界扰动和噪声下的非线性输出反馈 MPC，使用在线估计误差界和 homothetic tube，满足可行性与约束保证。
- **定理假设/结论：** Theorem 4 需要 Assumptions 1,3,4,5,7、δ-IOSS Lyapunov、δ-ISS CLF、初始优化可行及初始估计误差界；证明依赖终端闭合和 shifted-plan 递推。数值例包含10状态四旋翼。
- **局限/关联/复用：** 不可把其保证直接转移至仓库有推力相关 residual、缺测图的四/六状态合同；复用的是“后验有效界—收紧—终端—移位”证明骨架，不主张方法首创。
- **待查：** 将旧计划收紧的单调性与本仓库15-mode信息集、未来未知推力调度统一建模。

### Scott、Raimondo、Marseglia、Braatz（2016）
- **题名/链接：** *Constrained zonotopes: A new tool for set-based estimation and fault detection*，Automatica 69:126–136；DOI https://doi.org/10.1016/j.automatica.2016.02.036；作者全文 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf
- **阅读日期/层级：** 2026-10-30，Definition 3、Proposition 1、式(11)–(13)；既有 Run126/129/164/167/174 等多轮核查。
- **问题与方法：** 有界误差状态估计中的集合交、线性像、Minkowski和；CZ通过等式约束表示复杂相关性。
- **关键结论：** generalized intersection 对给定实际测量的一致状态集可精确表达，复杂度随运算增长。
- **局限/关联/复用：** CZ 运算本身不提供控制终端不变性或递归可行性；本轮先用区间精确交集作为标量 SMF 基线，再与 CZ 强基线比较。
- **待查：** 实际四状态后验约束如何在固定复杂度预算下安全外包而不破坏终端包含。

### Mulagaleti、Mejari、Bemporad（2025）
- **题名/链接：** *Parameter-Dependent Robust Control Invariant Sets for LPV Systems With Bounded Parameter-Variation Rate*，IEEE TAC 70(2):1259–1266；DOI https://doi.org/10.1109/TAC.2024.3454528；预印本 https://arxiv.org/abs/2309.02384
- **阅读日期/层级：** 2026-10-30，Definition (4)–(6)、Section II 的调度可见性与后继全称量词；既有 Run197–199 重读综合 SDP。
- **问题与方法：** 已知当前 LPV scheduling 参数、后继参数在变化率集合内，联合综合参数依赖 RCI 与 vertex control。
- **关键假设/结论：** 当前参数可见后选控制；对所有后继参数与扰动同一个当前控制须满足后继集合包含。固定法向、configuration 和 SDP 是充分综合类。
- **局限/关联/复用：** 本仓库未来推力允许全区间跳变，不能虚构较小变化率界；Run199 的浮点 PrimalInfeasible 仅否定特定数值模板，不能推出一般控制不可行。
- **待查：** 将本轮标量移位证明中的 terminal inclusion 换成当前推力条件化、未来任意跳变的共同后继包含。

## 历史已阅读/核对论文条目（84篇，85条历史记录去重合并，原始阅读说明保留）

## Athanasopoulos, Smpoukis, Jungers — Invariance in Constrained Switching Systems
- 年份/全文：2017；[arXiv:1702.00598](https://arxiv.org/abs/1702.00598)。
- Run 135 精读：pp. 2--6，Assumptions 1--4、Definitions 1--3、Proposition 1、Theorems 1--3。
- Run 136 新增精读：Sections 2.1--3.2、6，重点 forward reachable recursion (7)--(16)、Theorem 2 的缩放外包及 T-product lift。确认外包定理要求每个标签扰动为 full-dimensional C-set；本项目逐拍秩亏 disturbance image 不可直接套用。
- 方法/关键结论：以图节点索引 invariant multi-set；逐边 one-step reachable inclusion 与不变性等价；在稳定、强连通和 C-set disturbance 假设下，forward reachable multi-set 收敛到 minimal invariant multi-set，并可构造有限外逼近；约束内还可后向求 maximal admissible multi-set。
- 与本项目关系：15-mode estimator-error invariant family 和 reachable-sum 外逼近已有直接理论，不能作为创新。当前部分边扰动低维，不满足其 C-set 内点假设；Run 135 的 scalar Bellman contraction 独立证明，下一轮几何外逼近不能无条件照搬其定理。

## Scott, Raimondo, Marseglia, Braatz — Constrained zonotopes: A new tool for set-based estimation and fault detection
- 年份/出处：2016, *Automatica*, 69:126–136；DOI：https://doi.org/10.1016/j.automatica.2016.02.036
- 方法/关系：CZ 定义、精确集合运算与复杂度约减；是本项目 CZ 基础，因此“CZ 保留相关性”不是创新。
- Run 126 新增核查：重读 Sections 3.1、4.1–4.3、Appendix Algorithm 1 与 (A.9)–(A.10)，并在冻结 Run-123 后验复现 lift-then-reduce 外包及控制准入临界复杂度。该复现是强基线，不是新算法。
- Run 129 新增核查：逐式重读 Appendix (A.9)–(A.10) 的基生成元放大、残余坐标逆缩放与删除顺序。论文维护几何外包，不维护到给定终端内集的包含映射；本轮携带谱系只是实现审计，不能宣称替代或改进 Scott 方法。
- Run 164 定向重读全文 Sections 2.2、3.1--3.2 的 generalized intersection、线性像与集合表示。
  CZ 可精确表示多面体和线性等式切片；固定观测值后的 fiber 是标准 generalized intersection，
  因而本轮的 fiber support LP 是已知集合运算的实例，不作 CZ 算法创新声明。
- Run 167 精读 Section 2 Definition 2、Section 3.1 Proposition 1及证明、Section 5式(31)--(33)。
  bounded-error posterior是预测集与**已实现观测**逆像的相交；精确相交或任何可靠外包都不能删除
  与先验和噪声合同一致的极端观测。因此它能缩小单个观测后的fiber，却不能自动保证所有可能观测
  的全局创新范围满足控制阈值。
- Run174 重读 Section 2 Definition 2、Section 3.1 Proposition 1及证明、Section 5估计递推。
  generalized intersection只保留与实际观测一致的预测状态；它不改变真实plant状态，因此不能
  将“posterior收缩”解释为“物理速度重置到配置初始盒”。
- Run185 核对作者版摘要与Section 1的问题定位；未重新精读降阶算法。CZ精确线性像、交集及
  固定复杂度外包仍是后续强基线；本轮单对耦合法向保留相关性不构成CZ算法创新。

## Alamo, Bravo, Camacho — Guaranteed state estimation by zonotopes
- 年份/出处：2005, *Automatica*, 41(6):1035--1043；DOI：https://doi.org/10.1016/j.automatica.2004.12.008
- Run 164 阅读层级：核查正式摘要、问题设定和可访问正文片段；未取得可稳定逐页引用的完整作者稿。
- 方法/关键结论：把先验预测与有界测量一致条带求交，并构造含真状态的一族 zonotope 外包；
  测量更新的对象是给定实际观测后的 consistent-state set，而非把所有可能观测重新并成一个集合。
- 与本项目关系：支持“先按可见观测形成 fiber、再查询控制方向 support”的信息时序；本轮不引用其
  外包最优性定理，也不据此声称新 SMF 更新。

## Kopetzki, Schürmann, Althoff — Methods for Order Reduction of Zonotopes
- 年份/出处：2017, CDC, 5626–5633；DOI：https://doi.org/10.1109/CDC.2017.8264508；作者全文：https://mediatum.ub.tum.de/doc/1442501/1442501.pdf
- Run 129 精读：Introduction、Section II 的 box/transformation methods、Section III 的 PCA/clustering/constrained optimization、Section IV 的约束与评价。
- 方法/关键结论：系统比较 zonotope 外包约减，以体积或几何误差评价；可通过变换、聚类或优化构造较紧外包。
- 与本项目关系：它是普通几何 order reduction 的强基线，但不处理 CZ equality slice，也不保证压缩集仍落在指定 terminal inner set 内。几何更紧不能替代终端包含证书。
- 本项目状态：Run 129 排重基线；不把几何约减本身当作创新。
- Run 130 新增核查：精读 Section III-D。该节直接优化 reduced generator matrix `C`，用 `sum_j |C^{-1}G|_{ij} <= 1` 保证原 zonotope 被包含，并用 determinant/volume 目标和 `fmincon` interior-point 求解。因此“非-Scott + 包含硬约束的 outer reduction”已有直接近邻。

## Robbins, Glunt, Thompson, Pangborn — Online Constraint Tightening for MPC using Constrained Zonotope Reachability Analysis and Zonotope Over-Approximations
- 年份/出处：2026, ACC 2026, pp. 585–592；IEEE：https://ieeexplore.ieee.org/document/11616451；机构记录：https://pure.psu.edu/en/publications/online-constraint-tightening-for-mpc-using-constrained-zonotope-r/
- Run 126 核查层级：取得正式摘要、书目信息和章节目录；正文在 Introduction 后要求机构/会员访问，未完成全文精读。
- 已知覆盖：摘要明确包含 nonlinear error reachability、在线 MPC tightening、无需优化的 CZ-to-zonotope 外包和 LTV 数值例。
- 边界：不能据摘要推断具体外包公式、复杂度、终端/递归可行性或是否保护控制方向；首次性保持未知。
- Run 161 新增核查（2026-10-11）：IEEE 与 Penn State 页面确认 ACC 2026 页码585--592及正式摘要；
  仍未取得正文。本轮只把它作为“online CZ reachability/tightening 已有”的排重线索，不引用算法或定理。

### Run170 补充核对（同一论文去重合并）
- 年份/出处：2026 American Control Conference；IEEE Xplore document 11616451。
- Run170阅读层级：仅核查IEEE摘要，全文未取得，首次性未知。
- 摘要层面内容：用CZ及非线性polyhedral envelopes在线传播误差；以无需优化的CZ到zonotope
  外包接Pontryagin差收紧，并在LTV MPC数值例上比较。
- 与本项目关系：这是联合非线性误差传播与在线收紧的最强近邻线索；未读正文前不能声称缺测
  SMF、跨时刻递归可行性或固定预算严格优势未被覆盖。

## Le, Stoica, Dumur, Alamo, Camacho — Robust Tube-Based Constrained Predictive Control via Zonotopic Set-Membership Estimation
- 年份/出处：2011, CDC-ECC；DOI：https://doi.org/10.1109/CDC.2011.6161131
- 方法/关系：zonotopic SMF + tube output-feedback MPC；直接说明该组合不是创新。

## Rego, Raffo, Scott, Raimondo — Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems
- 年份/出处：2020, *Automatica*, 111:108614；DOI：https://doi.org/10.1016/j.automatica.2019.108614
- 方法/关系：CZ mean-value/Taylor guaranteed nonlinear propagation/update；四旋翼非线性阶段的重要传播基线。
- Run 179 全文精读 Section 2、Section 3.1、Sections 4.1--4.5、Theorems 1--3、Lemma 1、
  Corollaries 1--2、Remarks 8--10及式(22)。其固定阶外包递推针对已知输入和已实现测量下的
  单个posterior；可作为单fiber传播原语，但不表示连续可见`d`上的information-family策略图。

## Cong, Wang, Zhou — Stability of linear set-membership filters with respect to initial conditions: An observation-information perspective
- 年份/出处：2025, *Automatica*；DOI：https://doi.org/10.1016/j.automatica.2024.111993
- 方法/关系：Observation-Information Tower、CZ-SMF 初值稳定性；须与控制闭环稳定性区分。

## Qiu, Yang, Zhu, Mousavinejad — Output feedback model predictive control based on set-membership state estimation
- 年份/出处：2020, *IET Control Theory & Applications*；DOI：https://doi.org/10.1049/iet-cta.2019.0881
- 方法/关系：ellipsoidal SMF + output-feedback MPC；是 CZ 方法必须比较的几何基线。

## Köhler, Kötting, Soloperto, Allgöwer, Müller — A robust adaptive model predictive control framework for nonlinear uncertain systems
- 年份/出处：2021, *International Journal of Robust and Nonlinear Control*；DOI：https://doi.org/10.1002/rnc.5147
- 研究问题：递归模型/参数更新后，如何仍保证 robust recursive feasibility 与 constraint satisfaction。
- 方法/关键结论：set-membership estimation 提供逐步更准确的参数不确定集合；论文明确推导 estimation algorithm 与 tube/set-based RAMPC 所需的 monotonicity / non-increasing 条件，并在 incremental-Lyapunov tube 中给出可实现条件。
- 与本项目关系：第28章 exact CZ shift-nesting 属于同一“更新必须与旧预测兼容”的大理论边界；因此 nesting 本身不是创新。真正未闭合的是 fixed-complexity CZ reduction 是否保持这种兼容性。
- 局限：处理参数不确定性 RAMPC，不是当前 output-feedback CZ state posterior 的固定复杂度压缩接口。
- 本项目状态：作为 recursive-update monotonicity 的强基线。

## Lu, Cannon, Koksal-Rivet — Robust adaptive model predictive control: Performance and parameter estimation
- 年份/出处：2021, *International Journal of Robust and Nonlinear Control*；DOI：https://doi.org/10.1002/rnc.5175
- 方法/关系：固定复杂度参数/预测集合 + robust tube MPC；证明 recursive feasibility 与 ISS，是 fixed-complexity 强基线。
- Run 161 新增精读：开放全文 Sections 3.1--3.2、Lemma 1、Section 4.1 Proposition 1、
  Section 5.2 Theorem 3。固定法向参数集合更新保持真参数包含和嵌套，预测 tube 对整个参数集与
  disturbance robustify；递归可行性另由旧解移位与 terminal 条件证明。该结构支持“可靠在线集合
  可降低保守性”，但其对象是常参数集合，不能把本项目 state posterior 直接当作 future residual。
- Run 166 重新精读开放全文 Sections 3.1--3.2、Lemma 1、Section 4.1 Proposition 1及证明，
  并复核Section 6.1的同更新律比较。固定复杂度外包须同时保持真参数包含与跨时刻嵌套；旧解移位
  和terminal条件另行承担递归可行性。因此本轮只能把可见state范围作为独立初始化合同，不能用其
  替代future process residual或物理input authority。

## Peschke, Mönnigmann — Robust adaptive tube tracking model predictive control for piece-wise constant reference signals
- 年份/出处：2023, *International Journal of Robust and Nonlinear Control*；DOI：https://doi.org/10.1002/rnc.6814
- 方法/关系：nominal model/reference 在线变化时的 adaptive tracking MPC；明确 nominal-model update 会使 nominal-centered tube 的 recursive-feasibility proof 更困难。

## Köhler et al. — Robust adaptive MPC using control contraction metrics
- 年份/出处：2023, *Automatica*；DOI：https://doi.org/10.1016/j.automatica.2023.111169
- 方法/关系：CCM + set-membership + adaptive tube，含 planar quadrotor；四旋翼阶段强近邻。

## Andrade, Normey-Rico, Raffo — Tube-Based Model Predictive Control Based on Constrained Zonotopes
- 年份/出处：2024, *IEEE Access*, 12:50100–50113；DOI：https://doi.org/10.1109/ACCESS.2024.3381622
- 方法/关系：CZ Tube MPC，24-state tiltrotor UAV + suspended load HIL；“CZ + Tube MPC + UAV”不是创新。

## Dey, Bhasin — Output Feedback MPC with Adaptive Tubes
- 年份/出处：2026, arXiv:2605.23661
- 方法/关系：adaptive observer 的 state/model/initial-condition estimates 联动 tightening、terminal ingredients 和 tube geometry；作者建立 recursive feasibility 与 robust exponential stability。与本项目 recenter/update gate 高度相邻，必须全文排重。
- Run 131 新增核查：精读 IV-C--IV-F、Criterion 1、Algorithm 1、Theorem 2 与 Appendix IV。terminal set 可随 estimates 更新，但必须通过 consecutive compatibility criterion；失败时保持旧 point estimate/回退集合，backup setup 与旧解移位封闭递归可行。故 adaptive terminal、更新准入与 fallback 不能作为本项目创新。
- Run 148 新增重读：Sections IV-A--F、Assumptions 2--4、Criterion 1、Theorem 2 与 Appendix IV。论文以 `X tilde_{t,i}` 外包 estimation error、Pontryagin difference 收紧 state-estimate constraints，再用 homothetic observer-state tube；其输出模型无 measurement noise，也不保留 bounded-dropout observation histories 内 `(eta,e)` 的路径相关联合像。因此它是在线收紧/terminal/recursive-feasibility 强基线，但不直接替代本轮三种 correlated return seed。
- Run 162 新增重读：Criterion 1、Algorithm 1、Theorem 2与Appendix IV的fallback量词。更新不兼容时
  保留旧estimate/集合，递归可行性仍依赖旧解移位和terminal闭合；不能通过删除环境允许的
  uncertainty/dropout分支恢复可行性。

## Dey, Dhar, Bhasin — Adaptive Output Feedback Model Predictive Control
- 年份/出处：2022, arXiv:2209.08908；全文：https://arxiv.org/abs/2209.08908
- Run 131 精读：IV-A、IV-D--IV-F、Algorithm 1 与 recursive-feasibility proof。
- 方法/关键结论：固定 estimation-error RPI set 加到 estimated-state homothetic tube，形成包含 true state 的 `homothetic and invariant` two-tube；terminal set 与 shifted candidate 保证 recursive feasibility。
- 与本项目关系：两层 output-feedback tube 在 2022 年已有直接先例；本项目差异只能落在 intermittent CZ-SMF、固定 support-query budget 与 mode-indexed backup family 的联合接口。

## Dey, Bhasin — Adaptive Output Feedback MPC With Guaranteed Stability and Robustness
- 年份/出处：2025, *IEEE Transactions on Automatic Control*, 70(12):8345--8352；DOI：https://doi.org/10.1109/TAC.2025.3584302；预印本：https://arxiv.org/abs/2502.04048
- Run 131 精读：IV-A--IV-D、Assumption 4、Theorem 1--2。
- 方法/关键结论：时间相关 estimation-error sets 与 state-estimate homothetic tube 构成 two-tier tube；fixed terminal set/feedback 封闭 shift，保证 recursive feasibility 和 robust exponential stability。
- 与本项目关系：“在线估计信息 + 独立 terminal 骨架”的宽泛结构已覆盖，不能改名为新架构。

## Köhler, Müller, Allgöwer — Robust output feedback model predictive control using online estimation bounds
- 年份/出处：2021, arXiv:2105.03427；全文：https://arxiv.org/abs/2105.03427
- Run 131 精读：III-C、IV-B，Assumption 7、Theorem 4 及证明。
- 方法/关键结论：当前/未来有效 estimation-error bounds 与 observer/nominal mismatch 共同进入 homothetic tube；augmented terminal ingredients 封闭旧解移位和递归可行性；含 10-state quadrotor 数值例。
- 与本项目关系：在线 estimator information 用于 finite-horizon tightening、保守 terminal envelope 负责尾端的分工已有强近邻。
- Run 137 新增重读：pp. 9--10 的 Assumption 7、Theorem 4 与 shift proof。其 estimation bound `e` 和 tracking bound `s` 已联合进入 constraints/terminal；本项目不能把 12 维联合误差图本身当作创新，差异必须来自间歇 CZ 几何在同预算下的可认证收益。
- Run 138 新增重读：从 arXiv 源码核查 “Homothetic tube-based MPC”“Simplified constraint tightening”、两组 terminal assumptions/theorems及 shift proof。真实输入约束对 feedback、estimation error 与 tracking error 联合成立；预先固定 nominal/correction 盒至多是 benchmark contract，不能替代 joint tightening 或 terminal proof。

## Lorenzetti, Pavone — A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme
- 年份/出处：2020, ECC；全文：https://arxiv.org/abs/1911.07360
- Run 137 精读：Sections IV-B、IV-E--IV-G，式 (8)、(12)--(15)、Propositions 1--2。
- 方法/关键结论：以 `estimation error + estimate-to-nominal control error` 为增广状态，计算一个 coupled RPI；其线性像同时收紧 performance/state 与 input constraints，并结合 nominal terminal MPC 给出 robust constraint satisfaction。
- 与本项目关系：这是 augmented `(eta,d)` ancillary RPI 的直接强基线。“联合估计和控制误差”不是创新；本项目首先必须冻结 nominal/correction input allocation，再比较 15-mode CZ/zonotope 几何是否能在同预算下比 constant-cross-section RPI 更紧。
- Run 138 新增重读：Sections IV-A--B、IV-E--F，尤其 `u=bar u+K(hat x-bar x)`、coupled error 式 (12)、input tightening 式 (13) 与 Proposition 1。最终 nominal input set 由 coupled RPI 的 correction 投影通过 Pontryagin difference 得到；固定输入切分只可用于前置 existence probe。
- Run 139 新增重读：Sections IV-B、IV-E--G，式 (8)、(12)--(15)、Propositions 1--2。其 RPI 对象是在固定可实现反馈 `K(hat x-bar x)` 后形成的 autonomous augmented-error system；因此 fixed-policy RPI 与逐状态存在控制的 RCI 量词不可混用，且控制只读取 estimate-to-nominal error，不读取真实 estimation error。

## Mejari, Mulagaleti, Bemporad — Data-Driven Synthesis of Configuration-Constrained Robust Invariant Sets for Linear Parameter-Varying Systems
- 年份/出处：2023, *IEEE Control Systems Letters*, 7:3818--3823；DOI：https://doi.org/10.1109/LCSYS.2023.3346128；全文：https://arxiv.org/abs/2309.06998
- Run 139 精读：Section III-C、Lemma 3、Problem 1、Section IV。
- 方法/关键结论：RCI 的量词明确要求对每个状态与给定 scheduling parameter 存在 admissible input，使后继对全部 disturbance/model realization 留在集合；configuration-constrained polytope 的 vertex inputs 通过凸插值定义 invariance-inducing controller。
- 与本项目关系：若采用 controlled-RCI 语义，controller parameterization 与 `exists control` 的位置必须显式冻结。本文允许 controller 使用完整 state；本项目的 augmented state 含不可观测 `eta=x-hat x`，所以还必须收紧为对 observation fiber 共用同一控制的 partial-information RCI。
- 本项目状态：RCI 量词与 vertex-policy 的强基线；不把 configuration-constrained set 或 controller/set co-design 声称为创新。
- Run 192 重读 Section III-C、Lemma 3、Problem 1与Section IV。其充分RCI条件同时约束
  configuration cone、vertex后继、状态和输入；仓库现有单一cone Farkas否证不能外推到
  orientation family或plant不可行。本轮不再继续局部cone邻接枚举。
- Run 193 重读 Section III-C、Lemma 3及证明、Problem 1、Sections IV--V。正文顶点输入
  `u^i`不依赖当前调度参数，属于共同vertex-input策略；可作为保守基线，但不能覆盖冻结合同
  已允许的`tau(x,T)`全部权限。
- Run 194 重读 Section III-C、Lemma 3、Problem 1、Sections IV--V，专门核查固定法向、可变
  offset和vertex-input充分证书。本轮同心`alpha*S4`只是其严格受限子类；该子类失败不能否定
  independently variable offsets或configuration-constrained联合综合。
- Run 195 定向精读Lemma 3证明(77)--(81)及Sections IV--V的式(85)--(88)。非PD CC-RCI
  为每个集合顶点配置一个输入并共同覆盖调度顶点；仓库旧19-pair LP正确复现了这一保守基线，
  但它不能代替冻结合同允许的当前推力可见端点相关力矩。

## Mulagaleti, Mejari, Bemporad — Parameter-Dependent Robust Control Invariant Sets for LPV Systems With Bounded Parameter-Variation Rate
- 年份/出处：2025, *IEEE Transactions on Automatic Control*, 70(2):1259--1266；
  DOI：https://doi.org/10.1109/TAC.2024.3454528；全文：https://arxiv.org/abs/2309.02384
- Run 192 精读：problem statement、Sections 3.1--3.2、式(14)--(28)及算法步骤。
- 方法/关键结论：以实时可测scheduling parameter及其有界下一参数集合构造
  parameter-dependent configuration-constrained RCI和parameter-dependent vertex controls；
  后继必须落入全部允许下一参数集合对应RCI的交集，同时满足状态和输入约束。
- 与本项目关系：若未来显式加入并认证推力执行器状态/变化率，该文是直接强基线；当前
  frozen benchmark只有逐点`T`区间，最小通用rate bound等于全区间宽度，不能获得transition
  reduction。PD-RCI与configuration geometry均不作为创新。
- Run 193 重读式(4)--(6)、Sections 3.1--3.2、式(12)--(25)及算法。其定义明确先读取当前
  scheduling parameter，再使用`u=u(x,p)`，同时覆盖全部允许`p+`；因此仓库旧
  `exists tau forall T` predecessor比真实信息合同更强，必须纠正为调度可见控制。
- Run 194 重读Sections 1、3.1--3.4的PD-RCI定义、PD-vertex control及SDP充分条件。任意未来
  推力跳变使后继参数集合仍为全区间；本轮只用其当前参数可见控制权限，不复现PD-set SDP。
- Run 195 精读定义(4)--(6)、Proposition 2及证明、PD vertex law(14)--(15)、Sections
  3.2--3.4的式(16)--(27)。当前参数在控制前可测且`u=u(x,p)`，因此本轮为160个状态顶点
  分配低/高推力独立力矩；未来参数全区间覆盖仍未因该权限而缩小。
- Run 196 精读Definition/Problem、Proposition 2、式(14)--(15)、(21)--(28)、SDP(33)与
  Section IV-A。仿射offset给出仿射vertices，和仿射LPV dynamics/vertex control相乘后，
  式(27)是关于当前参数的可能非凸二次不等式；作者用S-procedure/LMI给充分条件。故参数相关
  offset不能沿用Run195的endpoint-only LP认证。
- Run 197 重读式(26)--(28)、Remarks 4--5与SDP(33)。论文的一般多维多面体参数域用
  S-procedure 给充分 LMI，并明确记录潜在 duality gap；本仓库的单标量闭区间可改用单二次
  约束 S-lemma 的精确特化，但 fixed normal/configuration 与共同后继 core 仍会保守。
- Run 198 重读式(28)、SDP(33)、算法步骤4与Section IV求解环境。正文以YALMIP建模并用
  MOSEK求解SDP；solver success本身不是有理不变性证书。本仓库的每个`2 x 2` LMI可精确
  改写为三维Lorentz cone，但当前运行环境没有相应SOCP/SDP求解器。
- Run 199 重读式(26)--(28)、SDP(33)、算法步骤4及Section IV求解设置。锁定Clarabel求解
  仓库受限实例后得到可重放浮点不可行ray；这只否定当前fixed-normal、affine-offset、
  common-core充分模板的数值实例，不否定论文一般PD-RCI参数化。

## Pólik, Terlaky — A Survey of the S-Lemma
- 年份/出处：2007, *SIAM Review*, 49(3):371--418；
  DOI：https://doi.org/10.1137/S003614450444614X；
  作者存档：https://optimization-online.org/2004/10/968/
- Run 197 精读：Theorem 2.2 的 S-lemma、严格可行（Slater）条件，以及 Section 3 的
  S-procedure 形式。
- 方法/关键结论：对单个二次约束，存在严格可行点时，约束域上另一二次函数非负等价于存在
  一个非负标量乘子，使组合后二次函数全局非负；全局二次非负可写成PSD矩阵条件。
- 与本项目关系：归一化推力区间由 `s^2-1<=0` 描述，`s=0`严格可行，因此每条二次
  facet residual 的区间非负可精确写成 `2 x 2` LMI。此为经典定理直接推论，不是创新；
  多参数、多约束或更高次条件不能无条件沿用本轮“精确”标签。
- Run 199 复核Theorem 2.2与Slater条件，确认区间二次到`2 x 2` LMI的变换本身精确；
  本轮数值不确定性来自大规模锥综合和浮点ray，而不是S-lemma特化。

## Fawzi — On Representing the Positive Semidefinite Cone Using the Second-Order Cone
- 年份/出处：2019, *Mathematical Programming*, 175:109--118；
  DOI：https://doi.org/10.1007/s10107-018-1233-0；
  作者存档：https://www.repository.cam.ac.uk/handle/1810/270667
- Run 198 精读：Introduction式(1)、Theorem 1及其表示范围说明。
- 方法/关键结论：`2 x 2`实对称PSD cone与三维Lorentz cone线性同构；一般`3 x 3` PSD
  cone则不存在有限SOCP lift。本轮只用前一精确等价，绝不外推到一般SDP。
- 与本项目关系：6080个S-lemma矩阵恰好全部为`2 x 2`，所以冻结综合可作为SOCP而非一般
  SDP求解；这只改变实现接口，不改变fixed-normal/common-core保守性，也不是创新。

## Goulart, Chen — Clarabel: An Interior-Point Solver for Conic Programs with Quadratic Objectives
- 年份/出处：2026, *Mathematical Programming Computation*；
  DOI：https://doi.org/10.1007/s12532-026-00320-7；
  正文：https://link.springer.com/article/10.1007/s12532-026-00320-7
- Run 198 定向精读：Section 2.1的解/不可行解释、Section 2.2支持的nonnegative、second-order、
  PSD与zero cones，以及实现/数据可得性说明。
- 方法/关键结论：Clarabel以homogeneous embedding的内点法求一般conic program，并原生支持
  Lorentz cone与不可行性证书语义；它是本问题可复现求解器候选。
- 与本项目关系：当前环境未安装Clarabel，故本轮只冻结求解能力门，不报告数值可行/不可行。
  将来即使安装并返回optimal，仍须把候选送入独立全区间检查器。
- Run 199 重读Sections 2.1--2.2的锥、homogeneous embedding与不可行语义，并锁定
  `clarabel==0.11.1`。两种equilibration设置均返回`PrimalInfeasible`，但只按独立浮点ray
  审计记为`NUMERIC_CHECK`，未升级为精确不可行证明。

## Gupta, Mejari, Falcone, Piga — Computation of Parameter Dependent Robust Invariant Sets for LPV Models with Guaranteed Performance
- 年份/出处：2023, *Automatica*, 151:110920；DOI：https://doi.org/10.1016/j.automatica.2023.110920；全文：https://arxiv.org/pdf/2009.09778
- Run 196 精读：Sections 3--5，Definition 1、Problems 1--2、Lemma 3、式(11)、
  (14)--(28)、多项式条件(20)--(21)与LMI条件(37)--(40)。
- 方法/关键结论：当前scheduling parameter可测，但未来值未知；PD-RCI一步包含必须对全部
  future scheduling成立，等价进入全部未来切片的交。参数相关invariance/constraint条件写成
  多项式矩阵不等式，并以Polya relaxation转为充分LMI/SDP条件。
- 与本项目关系：直接否定“参数相关set后仍只需检查当前参数顶点”的无依据简化；其LMI是
  强综合基线，但充分松弛和参数化与当前19-pair offset family不同，不能直接宣称已闭合Gate A。

## Mejari, Gupta, Piga — Data-Driven Computation of Robust Invariant Sets and Gain-Scheduled Controllers for Linear Parameter-Varying Systems
- 年份/出处：2023, *IEEE Control Systems Letters*, 7:3355--3360；
  DOI：https://doi.org/10.1109/LCSYS.2023.3329291；全文：https://arxiv.org/abs/2309.01814
- Run 193 阅读：问题陈述、invariance定义及gain-scheduled controller构造相关段落。
- 方法/关键结论：利用实时可用的scheduling signal综合LPV gain-scheduled feedback与多面体
  RCI，并对调度集合和有界扰动鲁棒。
- 与本项目关系：再次确认当前推力可见反馈不是新机制；本文数据驱动不确定模型合同也不是
  当前已知模型合同的必要组成。
- Run 194 全文阅读pp.1--6，重点Problem 1、Section III-C、Theorem 1和算法。其
  gain-scheduled feedback是本轮vertex-control之外的另一强基线；同心模板失败不否定该类。

## Köhler, Soloperto, Müller, Allgöwer — A computationally efficient robust model predictive control framework for uncertain nonlinear systems
- 年份/全文：2020 extended version；https://arxiv.org/abs/1910.12081
- Run 192 精读：Sections II--III、Assumptions 1--6、MPC (11)、Theorem 1及其shift proof、
  Proposition 4；另核对Section IV的additive/LPV special cases。
- 方法/关键结论：用incremental Lyapunov函数与ancillary feedback的标量界在线传播tube size，
  对state/input-dependent uncertainty收紧约束；在terminal controller/set/cost和tube terminal
  条件全部成立时证明递归可行、硬约束满足与实用稳定。
- 与本项目关系：说明调度一致`W(T)`只是一个必要接口；common-`P`稳定、有限轨迹或单次RCI
  可行都不能替代terminal append与shift proof。该文是full-state nonlinear tube MPC，未直接
  解决本项目间歇测量的因果output-feedback信息状态。

## Ping — Dynamic Output Feedback Robust Model Predictive Control via Zonotopic Set-Membership Estimation for Constrained Quasi-LPV Systems
- 年份/出处：2015, *Journal of Applied Mathematics*, Article 875850；DOI：https://doi.org/10.1155/2015/875850
- 方法/关系：zonotopic estimation-error set 刷新后用辅助 feasibility condition 决定是否采用更新；失败时继承旧 controller parameters。“更新前 feasibility gate”不是创新。
- Run 131 新增核查：精读 4.2--4.4、Algorithm 8、Theorem 9；确认其含 zonotope order limit、在线 set refresh、一步 feasibility gate 及失败时继承旧 controller parameters。不能把 `SMF update + gate + fallback` 作为新机制。

## Hassaan, Pati, Shen, Yong — Time-Varying Tube-Based Output Feedback MPC for Constrained Linear Systems with Intermittently Delayed Data
- 年份/出处：2021, *IFAC-PapersOnLine*, 54(5):103--108；DOI：https://doi.org/10.1016/j.ifacol.2021.08.482；作者全文：https://qiangs.github.io/Papers/Conf_Hassaan2021ADHS.pdf
- Run 132 精读：Sections 2.2、3.1--3.2，Assumptions 1--3、Theorems 5--7。
- 方法/关键结论：以周期有限长度语言描述间歇时延/缺测，构造 time-varying estimator/control tubes；一个对全部周期相位有效的 common nominal terminal set 与 feedback gain 足以用旧解移位证明 recursive feasibility，并得到 robust exponential stability。
- 与本项目关系：直接覆盖 `finite dropout language + time-varying tube + terminal shift`。mode-indexed terminal family 不是默认必要条件；本项目必须先复现其 worst-phase common-terminal baseline，再证明 indexing 的严格收益。
- 局限：误差集合采用 hyperbox，系统为线性/时变而非本项目完整六自由度非线性四旋翼；没有固定预算 CZ support-query 接口。
- Run 133 新增核查：重读 Section 3.1.2、Lemma 4、Assumptions 1--2 与 Theorem 6。确认 tracking controller/control-error tube 先吸收过程噪声与 estimation error；common `K_f,X_f` 随后作用于已经收紧的 nominal system。二者不是同一个 joint controller/RPI synthesis 问题。
- Run 135 新增核查：重读 Definition 1、system/timing 与 Section 3.1.1。其 estimator 采用 finite/periodic equalized-recovery error tubes，未来 delay pattern 未知时对全部允许模式取 worst case；并不要求一个 time-uniform invariant estimation-error family。故本轮统一固定点只是更强、更保守的 backup 基线。

## Rutledge, Yong, Ozay — Finite horizon constrained control and bounded-error estimation in the presence of missing data
- 年份/出处：2020, *Nonlinear Analysis: Hybrid Systems*, 36:100854；DOI：https://doi.org/10.1016/j.nahs.2020.100854；作者全文：https://www.kwesirutledge.info/static/pdf/nahs2020.pdf
- Run 132 精读：Sections 3--4、Definition 2、equalized-recovery formulation 与 synthesis。
- 方法/关键结论：missing-data language 可表达连续丢包上界；prefix-based affine feedback 在 bounded process/measurement noise 与 state/input constraints 下保证 finite-horizon equalized recovery。Remark 3 明确指出可适配 zonotope 等 set template。
- 与本项目关系：bounded-dropout language、按前缀/模式合成反馈及 set-valued bounds 均已有近邻；有限时域结果本身不闭合 receding-horizon terminal proof。
- Run 160 阅读层级：作者全文本轮抓取超时，仅复核摘要/引言中的 equalized-recovery 问题设定，
  不引用其定理。该工作允许缺测期间使用不同中间界后恢复；当前合同要求每拍位置硬约束，故
  本轮第13 miss反证不能借 equalized recovery 绕过。

## Hassaan, Shen, Yong — Path-Dependent Controller and Estimator Synthesis with Robustness to Delayed and Missing Data
- 年份/出处：2021, HSCC；DOI：https://doi.org/10.1145/3447928.3456655；作者全文：https://qiangs.github.io/Papers/Conf_HSCC2021Hassaan.pdf
- Run 132 精读：Sections 2--5，fixed-length/reduced event language、path-dependent controller/estimator synthesis 与 examples。
- 方法/关键结论：为 time-varying affine systems 合成 path-dependent finite-horizon controller/estimator；通过 reduced event language 处理相同可观察历史的因果冲突，并以 polytopic intermediate bounds 改善只按 worst-case word 的设计。
- Run175 重读 Problem 1、Section 3与Theorems 3.2/3.4：控制器/估计器是待合成的存在量，保证对全部固定长度缺测/时延语言实现equalized recovery；不能把所有允许控制输入当成对手扰动来否定回返。
- 与本项目关系：按 dropout mode/path 索引 controller、estimator 或 error bound 不是创新；15-mode indexing 只能作为实现结构。

## Ghaemi, Del Vecchio — Control for Safety Specifications of Systems with Imperfect Information on a Partial Order

- 年份/出处：2014，IEEE Transactions on Automatic Control；作者全文：https://web.mit.edu/ddv/www/papers/RezaTACfinal.pdf
- Run176 精读：§II 的information-state定义与Problems 1--2，§III Theorem 1及证明，§IV Theorem 4及证明。
- 方法/关键结论：开环安全集采用`exists control / forall disturbances`；闭环控制映射以测量历史诱导的information state为输入，并对全部允许测量信号保持安全。极端输入判据依赖input/output order-preserving及连通性等结构假设。
- 与本项目关系：支持受控回返的正确量词和information-state策略接口；当前非线性四旋翼plant尚未证明满足其order-preserving假设，不能直接用极端推力替代五步鲁棒前驱。

## Wildhagen, Pezzutto, Schenato, Allgöwer — Self-triggered MPC robust to bounded packet loss via a min-max approach
- 年份/出处：2022, CDC extended version；arXiv：https://arxiv.org/abs/2204.00339
- Run 132 精读：problem formulation、min-max MPC、terminal control law、recursive feasibility/constraint/convergence argument。
- 方法/关键结论：在连续 packet loss 数有界时使用 min-max self-triggered MPC 与尾端控制律，对所有允许 loss realization 保证 recursive feasibility、constraint satisfaction 和 convergence。
- 与本项目关系：从网络化 MPC 方向再次覆盖 `bounded packet loss + terminal/shift proof`；但不是 SMF output feedback，也不消费 CZ posterior correlation。
- Run 163 精读 Sections II-B--II-C、Assumption 1、Section III、Algorithm 1与terminal ingredients：
  策略选择控制更新和采样间隔，可靠ACK只报告最近一次传输结果；连续丢包上界`P`仍是独立网络
  假设，min-max MPC覆盖所有满足该假设的loss sequences。故自触发调度不能单独认证缩短dropout语言。

## Mayne, Seron, Raković — Robust model predictive control of constrained linear systems with bounded disturbances
- 年份/出处：2005, *Automatica*, 41(2):219–224；DOI：https://doi.org/10.1016/j.automatica.2004.08.019
- 方法/关系：经典 bounded-disturbance robust/tube MPC 基线；当前 LQR+RPI 不能作为创新。

## Mayne, Raković, Findeisen, Allgöwer — Robust output feedback model predictive control of constrained linear systems
- 年份/出处：2006, *Automatica*, 42(7):1217--1222；DOI：https://doi.org/10.1016/j.automatica.2006.03.005
- Run174 阅读：正式摘要、引言、robust output-feedback MPC控制器结构与Theorem 1上下文；出版页正文受限，未逐式核查完整证明。
- 方法/关键结论：Luenberger估计误差由不变集包络，observer-to-nominal偏差由tube截面包络；二者共同支持收紧与真实约束满足。
- 与本项目关系：可靠输出反馈闭合依赖误差/tube不变集，不依赖观测把真实状态重置到初始物理盒。本轮只用这一结构作量词对照，不引用未核查证明细节。

## Raković, Kerrigan, Kouramas, Mayne — Invariant approximations of the minimal robust positively invariant set
- 年份/出处：2005, *IEEE Transactions on Automatic Control*, 50(3):406–410；DOI：https://doi.org/10.1109/TAC.2005.843854
- 方法/关系：mRPI 可控精度外逼近；有限 Minkowski 和必须补无限尾项才能作安全 tube。

## Kouramas, Raković, Kerrigan, Allwright, Mayne — On the Minimal Robust Positively Invariant Set for Linear Difference Inclusions
- 年份/出处：2005, CDC-ECC；公开全文：https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc05/pdffiles/papers/1964.pdf
- 本轮精读：Sections II–V，Assumption 1、Theorems 2–4、公式 (16)–(25)。
- Run 136 新增重读：Theorems 1--4 与公式 (11)--(23)，核对 finite reachable sum、`R_s subseteq alpha W` 和 `(1-alpha)^-1 D_s` 的逻辑。当前标签相关秩亏扰动不满足公共 full-dimensional `W` 假设，故仅作为理论边界，不作为本轮证书。
- 方法/关键结论：若扰动是含原点内点的 C-set 且无扰动系统绝对渐近稳定，则可由有限 reachable sums 和缩放构造包含 mRPI 的 RPI 外近似，并控制 Hausdorff 误差。
- 与本项目关系：该结果的方向是外近似，不能证明重定心候选位于原 mRPI 内；当前四维合同的 `W=D0 G[-1,1]` 为秩一线段，也不满足其 C-set 假设。不能无条件套用缩放公式。
- 本项目状态：终端集合替代方案的条件性基线，不是当前包含证书。

## Sadraddini, Tedrake — Linear Encodings for Polytope Containment Problems
- 年份/出处：CDC 2019；DOI：https://doi.org/10.1109/CDC40024.2019.9029363；arXiv:1903.05214；全文：https://groups.csail.mit.edu/robotics-center/public_papers/Sadraddini19.pdf
- Run 128 重读：Section III Theorem 1 与 (11)–(17)、Theorem 2，Section IV-A Theorem 3 与反例、Table I。
- 方法/关键结论：为 AH-polytope-in-AH-polytope 给出线性充分包含编码；zonotope 特例使用生成元的仿射系数映射。一般编码不保证必要性，论文明确给出真包含但 zonotope 证书失败的反例。
- 与本项目关系：可把 CZ 终端误差集可靠地证入有限 mRPI 内近似；可行即证明，不可行不能当作不包含反例。Theorem 1 要求 primitive inbody 满维，CZ equality slice 必须先在 affine hull 内参数化。当前 539–605 / 602-generator 实例的通用编码达到约 160–180 万变量，不适合作为在线 fixed-budget admission。
- 本项目状态：Run 125 的终端包含基线；Run 128 将其降级为离线充分审计工具，不作为在线算法。
- Run 129 新增核查：Theorem 3 的行 `l1` 生成元映射可与 CZ 等式自由度组合为逐行小 LP；这是已知充分证书的结构化特化。首个 Scott 消元的 4 个超限行均有精确对偶下界大于 1，因此该特化首步失败；失败不否定真实集合包含。
- Run 130 新增核查：阅读 17 页 expanded arXiv 版本，重点 Section V-B、Proposition 6 与式 (30)。作者已经把 reduced generator matrix 与 containment maps 联合优化，用双向包含近似 Hausdorff distance；双线性等式使问题非凸，使用 projected sequential LP/交替求解并依赖初始化。把 terminal containment witness 当作 reduction 硬约束不是空白机制。

## Diaconescu et al. — Zonotope-Based Elastic Tube Model Predictive Control
- 年份/出处：2026, arXiv:2509.19824v2（2026-05-17 修订）；全文：https://arxiv.org/abs/2509.19824
- Run 129 精读：Sections 3.1、3.4 的包含 Lemma/Proposition/Corollary 与预计算 inclusion matrix。
- 方法/关键结论：在 zonotopic elastic tube MPC 中以仿射生成元映射和逐行范数约束编码包含，并预计算固定 inclusion matrix 以减少在线辅助变量。
- 与本项目关系：“携带或预计算包含矩阵”已有明确近邻，不能作为创新。其对象是缩放 zonotope，不是 Scott CZ 消元中的 equality-adjusted terminal witness。
- 本项目状态：certificate-carrying containment 的强近邻与首次性约束。

## Hellwig, Schäfer, Qian, Platzer, Althoff — From Zonotopes to Proof Certificates: A Formal Pipeline for Safe Control Envelopes
- 年份/出处：iFM 2025，LNCS 16194（卷出版 2026）；DOI：https://doi.org/10.1007/978-3-032-10794-7_13
- Run 128 精读：pp. 10–11，containment witness、残差裕量及 Theorem 3.5。
- 方法/关键结论：把 zonotope containment 的浮点优化 witness 转成可由形式系统检查的证书；可用精确有理数，或在 `||HΓ-G||` 残差和右逆范数约束下预留严格裕量。
- 与本项目关系：终端包含不能只保存 solver success；必须归档映射 witness，并独立检查等式、box 行预算和数值裕量。
- 局限：处理 zonotope witness，不直接消除 CZ equality，也不解决当前百万变量在线规模。
- 本项目状态：可靠证书实现规范。

## Kulmburg, Schäfer, Althoff — Approximability of the Containment Problem for Zonotopes and Ellipsotopes
- 年份/出处：2025，*IEEE Transactions on Automatic Control*, 70(12):8104–8119；DOI：https://doi.org/10.1109/TAC.2025.3583624
- Run 128 阅读：期刊元数据、摘要和 arXiv 记录；全文获取失败，未核查定理编号或证明。
- 方法/关系：摘要显示其分析 zonotope/ellipsotope containment 松弛的近似质量。不能凭摘要把它当作无损、低复杂度 CZ-in-zonotope 判据。
- 本项目状态：最近邻线索，首次性保持未知，待取得全文。

## Froese et al. — Parameterized Hardness of Zonotope Containment and Neural Network Verification
- 年份/出处：2025 preprint；全文：https://arxiv.org/pdf/2509.22849
- Run 128 精读：Section 3.1、Theorem 3.1 及一般复杂度结论。
- 方法/关键结论：固定物理维数 `d` 时，可枚举 `O(n^(d-1))` 个顶点判定 zonotope containment；一般问题具有困难性。
- 与本项目关系：解释为何不应预设高生成元一般包含有便宜完整证书。该结果针对 zonotope，不直接覆盖有 equality 的 CZ。
- 本项目状态：复杂度背景，不是当前在线实现方案。

## McCormick — Computability of global solutions to factorable nonconvex programs: Part I — Convex underestimating problems
- 年份/出处：1976, *Mathematical Programming*, 10:147–175；DOI：https://doi.org/10.1007/BF01580665
- 方法/关系：单 bilinear term 的经典 convexification 基础；box-domain 线性 support 下普通 CZ 不会比 exact convex hull 更紧。

## Müller, Serrano, Gleixner — Using Two-Dimensional Projections for Stronger Separation and Propagation of Bilinear Terms
- 年份/出处：2020, *SIAM Journal on Optimization*；DOI：https://doi.org/10.1137/19M1249825
- 方法/关系：非矩形二维可行域可产生比 box McCormick 更强的 separation；支持利用真实 posterior/scheduling 域，但不提供 Tube MPC 递归可行性。

## Kochdumper, Althoff — Constrained polynomial zonotopes
- 年份/出处：2023, *Acta Informatica*, 60:279–316；DOI：https://doi.org/10.1007/s00236-023-00437-5
- 方法/关系：支持 quadratic/higher-order maps；“用 polynomial zonotope 表示乘积”已有成熟理论，只能作为实现工具。

## Kochdumper, Althoff — Sparse Polynomial Zonotopes: A Novel Set Representation for Reachability Analysis
- 年份/出处：2020, *IEEE Transactions on Automatic Control*；DOI：https://doi.org/10.1109/TAC.2020.3024348；预印本：https://arxiv.org/abs/1901.01780
- Run171 精读：§§1.1--1.2、Definition 1、Propositions 1--4。
- 方法/关键结论：用 dependent factors 与全局 identifier 保留同一不确定因子在多项式项中的重复依赖；identifier 合并可保持依赖关系，并给出 zonotope、polytope 与 Taylor model 等表示到 SPZ 的转换。
- 与本项目关系：共享非线性因子表示是成熟 reachability 基线，不构成本项目创新；若一个输入点精确满足真实单步图，任何可靠 SPZ/CZ 图外包都必须保留其像。能否排除 Run169 点取决于从初始集出发的跨时刻联合可达集，而非单步换一种集合表示。

## Jafarpour, Harapanahalli, Coogan — Interval Reachability of Nonlinear Dynamical Systems with Neural Network Controllers
- 年份/出处：2023, L4DC, PMLR 211:12--25；全文：https://proceedings.mlr.press/v211/jafarpour23a/jafarpour23a.pdf
- Run172 精读：§2 的可达集、decomposition function、inclusion function和嵌入系统；§5 Theorem 2 的区间可达外包。
- 方法/关键结论：从初始区间和扰动区间出发，通过mixed-monotone嵌入系统计算包含真实非线性闭环可达集的超矩形，并以分割平衡紧度和计算量。
- 与本项目关系：支持“必须从初始集跨时刻传播”的量词；本文针对连续时间NN闭环，不能直接替代本仓库离散Euler真值模型的证明。Run172只采用同一包含原则，给出项目特定的标量归纳界。
- Run173 新增精读：§5 Theorems 2--3与Remark 4、§6 Algorithm 1。每步对外包重分割并取并集可改善紧度，但所有子外包仍必须覆盖对应真实轨迹；本项目的分层解析盒是项目特定特例，不是新可达算法。

## Bujarbaruah, Nair, Borrelli — A Semi-Definite Programming Approach to Robust Adaptive MPC under State Dependent Uncertainty
- 年份/出处：2020, European Control Conference；预印本：arXiv:1910.04378
- 方法/关系：set-membership refinement + state-dependent uncertainty envelope + robust MPC；“SMF 信息进入 state-dependent robustification”已有先例。

## Hanema et al. — Stabilizing non-linear model predictive control using linear parameter-varying embeddings and tubes
- 年份/出处：2021, *IET Control Theory & Applications*；DOI：https://doi.org/10.1049/cth2.12131
- 研究问题：利用 nonlinear system 的 LPV embedding 构造可稳定 MPC，同时处理未来 scheduling parameter 未知。
- 方法/关键结论：限制 state evolution 于时变集合，并利用 scheduling-state 关系构造 future scheduling tube；相较静态 bounds 得到更紧未来 bounds，并以该结构建立 recursive feasibility/stability。
- 与本项目关系：第27–28章的未来 `phi` scheduling intervals 与 shift nesting 有直接近邻，因此“state set -> scheduling tube”不能作为创新。差异只能落在 CZ-SMF measurement posterior、certified finite-normal support 与 fixed-complexity reduction compatibility。
- 局限：不是 set-membership output-feedback CZ 压缩问题。
- 本项目状态：作为 scheduling-tube 强基线。

## Abbas — Linear parameter-varying model predictive control for nonlinear systems using general polytopic tubes
- 年份/出处：2024, *Automatica*, 160:111432；DOI：https://doi.org/10.1016/j.automatica.2023.111432
- 方法/关系：anticipated scheduling bounds + general polytopic tubes；“更紧未来 scheduling interval 降低保守性”不是新机制。

## Fleming, Hawari — Robust Tube MPC Using Gain-Scheduled Policies for a Class of LPV Systems
- 年份/出处：2024, *IEEE Control Systems Letters*, 8:1589–1594；DOI：https://doi.org/10.1109/LCSYS.2024.3412652
- 方法/关系：gain-scheduled policy、parameter-rate bounds、online polyhedral tubes，证明 recursive feasibility/exponential stability；decision/scheduling-dependent tube 已有成熟理论。

## Girard — Reachability of Uncertain Linear Systems Using Zonotopes
- 年份/出处：2005, HSCC, LNCS 3414:291–305；DOI：https://doi.org/10.1007/978-3-540-31954-2_19
- 研究问题：用 zonotope 可扩展地计算不确定线性系统 reachable sets，并控制表示复杂度。
- 方法/关键结论：zonotope 传播配合 generator/order reduction；经典 generator-box 外包模式保证单次 outer enclosure，但其目标不是跨两个嵌套集合保持 reduction operator 的 monotonicity。
- 与本项目关系：第29章使用同类 generator-box reduction 构造 shift-support reversal；普通 order reduction 本身不能作为创新。
- 局限：不处理 SMF measurement posterior 与 MPC shifted-candidate support compatibility。
- 本项目状态：作为 naive fixed-order reduction 基线。

## Raghuraman, Koeln — Set operations and order reductions for constrained zonotopes
- 年份/出处：2022, *Automatica*, 139:110204；DOI：https://doi.org/10.1016/j.automatica.2022.110204；预印本：https://arxiv.org/abs/2009.06039
- 研究问题：提高 zonotope/CZ 在控制集合运算中的实用性，并提供复杂度约减方法。
- 方法概要：扩展 halfspace intersection、convex hull、RPI、Pontryagin difference 等 CZ 运算，并研究 zonotope/CZ order reduction。
- 与本项目关系：说明“CZ order reduction”已有系统理论；本项目若有贡献必须落在 reduction error 与 recursive-feasibility control normals 的联动证书，而不是提出一般 reduction。
- 局限：没有给出本项目所需的 rolling SMF shift-support ledger。
- 本项目状态：作为 fixed-complexity CZ 强基线。
- Run 130 新增核查：精读 Section 5。其 zonotope/CZ order reduction 直接采用 Sadraddini--Tedrake containment encoding；CZ 经 nullspace/AH-polytope 表示构造 LP，可删一个 generator/constraint 后再缩放。该节做 inner approximation，不能作为 reliable SMF posterior 的 outer enclosure，但已排除“CZ reduction + containment constraint”本身的首次性。
- Run188 精读§2、§3开头、式(1)--(3)及Theorem 4相关表示讨论。普通zonotope中心对称；CZ的等式约束可打破中心对称性、表示任意凸polytope，并对generalized intersection闭合。因此五参数center/radius在非中心对称measurement posterior上的失败是既有表示边界，不是创新。

## Robbins, Siefert, Pangborn — Exact Representation Complexity Reduction for Constrained Zonotopes with Applications to Dynamic Systems and Control
- 年份/出处：2026, *American Control Conference (ACC 2026)*；IEEE Xplore 收录日期 2026-08-13。
- 稳定链接：https://ieeexplore.ieee.org/document/11615961
- 研究问题：反复集合运算会使 zonotope/CZ representation complexity 增长；哪些 generators/constraints 是表示冗余，能否在保持集合完全不变时删除？
- 方法/关键结论：形式化 irredundant zonotopic representation 与多类 redundancy，给出检测/删除算法；数值例包含 robust controllable sets 和 ReLU domain partitioning。其 reduction 是 exact representation reduction，不是 approximate outer enclosure。
- 与本项目关系：该方法不改变集合，所以 exact-CZ 的 shift nesting 和所有 support 都自动保持；它应成为压缩流水线第一阶段，先 exact-prune，再讨论 approximate fixed-budget reduction。
- 可借鉴点：把“表示复杂度”与“集合几何近似误差”明确分离，避免把可精确删除的冗余误算成必须牺牲 tightness 的 fixed-order 问题。
- 局限：exact pruning 不能保证长期 propagation/update 后一定达到预设固定 generator/equality budget；也没有解决 independent approximate reductions 导致的 control-normal support reversal。
- 本项目状态：已采用为设计原则；不把 exact redundancy removal 声称为本项目创新。

## Hanema, Lazar, Tóth — Stabilizing tube-based model predictive control: terminal set and cost construction for LPV systems
- 年份/出处：2017, *Automatica*, 85:137–144；DOI：https://doi.org/10.1016/j.automatica.2017.07.046；扩展版：https://arxiv.org/abs/1702.05393
- 研究问题：LPV tube MPC 如何构造 terminal set/cost 并建立 recursive feasibility 与 stability。
- 方法/关键结论：采用 controlled periodically contractive terminal sets 与适合集合的 Lyapunov-like terminal cost；给出满足参数化假设时的递归可行性与渐近稳定性，并构造 periodic homothetic tube 参数化。
- 与本项目关系：第31章保留推力 T 的横向—姿态模型天然是 LPV family；因此“LPV terminal family/periodic contractive set”不能作为创新，只能作为 ancillary/terminal 证明工具。
- 可借鉴点：若 common quadratic certificate 过强，可转向 periodic/finite-step contractive terminal construction，而不是回到语义错误的 fixed-hover LTI。
- 局限：不使用 CZ-SMF measurement posterior，也不研究 posterior correlation 在真实 input normals 上的 tightening value。
- 本项目状态：下一阶段 ancillary/terminal synthesis 的主要理论基线。

## Ping, Yao, Ding, Li — Tube-Based Output Feedback Robust MPC for LPV Systems With Scaled Terminal Constraint Sets
- 年份/出处：2022, *IEEE Transactions on Cybernetics*, 52(8):7563–7576；DOI：https://doi.org/10.1109/TCYB.2020.3041334
- 研究问题：有 bounded disturbance/noise 的离散 LPV 系统如何做低在线复杂度 output-feedback tube RMPC。
- 方法/关键结论：离线优化并存储 nested RPI estimation-error sets 与 RCI control-error sets；在线依据时变 estimation-error bounds 搜索控制参数，并使用 scaled terminal constraint sets；论文给出 recursive feasibility 与 robust stability 保证。
- 与本项目关系：LPV + output feedback + nested error sets + scaled terminal 已有强近邻，因此第31章不能把这些结构本身作为创新。差异若存在，只能落在 CZ-SMF posterior correlation 如何被真实 state/input/terminal support normals 消费并形成可认证的 tightening 改善。
- 可借鉴点：其 nested RPI/RCI lookup 与 scaled terminal 是当前语义一致 ancillary synthesis 的直接比较基线。
- 局限：不是 constrained-zonotope posterior 的 control-normal support certification问题。
- 本项目状态：列为后续 LPV output-feedback 基线。
- Run 131 核查层级：本轮仅取得正式摘要；摘要支持 nested RPI/RCI lookup、在线 tightening 与 scaled terminal 的定位，但未据此引用定理编号或证明细节。


## Tahir, Jaimoukha — Robust Positively Invariant Sets for Linear Systems subject to model-uncertainty and disturbances
- 年份/出处：2012, IFAC Proceedings Volumes 45(17):213–217；DOI：https://doi.org/10.3182/20120823-5-NL-3013.00032
- 研究问题：在线性离散系统存在 model uncertainty、additive disturbance 以及 state/input constraints 时，如何联合计算 controller 与 robust positively invariant set。
- 方法/关键结论：将 RPI set 与反馈律一起放入 LMI 优化；论文强调不要求先给定 controller 或初始 invariant set，并在固定 K、无模型不确定性的特例下给出更简单的优化。
- 与本项目关系：第34–35章的“约束感知 ancillary synthesis”已有直接方法学基础，因此 controller/invariant co-design 只能作为 baseline 工具，不能作为创新。
- 局限：其 uncertainty class 与当前 thrust-scheduled、state-dependent nonlinear remainder 不完全相同；不能直接替代本项目的 vertex-consistent residual contract。
- 本项目状态：列为下一阶段 joint state/input synthesis 的 baseline。
- Run 133 精读：Sections 2--3、Definition 3、Theorem 5、Remarks 6--9。其 joint feedback/hyperrectangle synthesis 针对 norm-bounded model uncertainty 与 additive box disturbance；一般条件是充分的，无结构 norm-bounded uncertainty 特例可达精确性。该描述不直接保持本项目同一 `T` 决定 `(A(T),W(T))` 的 correlated graph；独立外包不能用于否定 vertex-consistent certificate。

## Tahir — Efficient computation of Robust Positively Invariant sets with linear state-feedback gain as a variable of optimization
- 年份/出处：2010, ICEEE；DOI：https://doi.org/10.1109/ICEEE.2010.5608613
- Run 133 精读：Sections II--IV，式 (1)--(25)，Remarks 3--12。
- 方法/关键结论：对 LTI + additive box disturbance 同时优化 linear feedback 与 RPI set；固定形状椭球采用 S-procedure 得到充分 SDP，origin-centered axis-aligned box 采用 Farkas 条件，并可加入 state/input constraints；固定 K 时部分问题退化为 LP。
- 与本项目关系：这是 ancillary/tracking disturbance-RPI 层的直接 baseline，不是 Hassaan nominal terminal `K_f,X_f`。box 类已由第37章严格排除；ellipsoid 类仍需适配 arbitrary-jump thrust LPV 和 paired residual。
- 本项目状态：准入为方法基线，不直接实现现有公式。

## Tahir, Jaimoukha — Robust feedback MPC of constrained uncertain systems
- 年份/出处：2013, *Journal of Process Control*, 23(2):151--163；DOI：https://doi.org/10.1016/j.jprocont.2012.08.003
- Run 133 阅读层级：仅正式摘要，未取得可核验全文。
- 摘要层面关系：区分把状态导入 invariant terminal set 的 outer MPC controller 与保持 RPI 的 inner controller，支持本轮双层语义纠正。
- 限制：未核查正文、定理或算法，不据此声明其 uncertainty class 覆盖本项目。

## Ben Sassi, Girard — Controller synthesis for robust invariance of polynomial dynamical systems using linear programming
- 年份/出处：2012, *Systems & Control Letters*, 61(4):506–512；DOI：https://doi.org/10.1016/j.sysconle.2012.01.004；预印本：https://arxiv.org/abs/1107.1580
- 研究问题：bounded disturbances 和 input constraints 下，如何联合求 controller 与 invariant set。
- 方法/关键结论：给定候选 polyhedral invariant 后，把 controller synthesis 写成多项式优化并用 LP relaxation；随后迭代更新 controller 与 invariant polytope。
- 与本项目关系：再次说明“同时搜索反馈和不变集”已有成熟工作。若本项目采用类似 co-design，只能作为认证工具。
- 局限：不是 constrained-zonotope SMF posterior 与 Tube MPC 的接口问题，也不处理当前特定 LPV scheduling 语义。
- 本项目状态：作为 polyhedral joint synthesis 的方法基线。

## Wehbeh, Kerrigan — State-Dependent Uncertainty Modeling in Robust Optimal Control Problems through Generalized Semi-Infinite Programming
- 年份/出处：2025, arXiv:2503.10389；稳定链接：https://arxiv.org/abs/2503.10389
- 研究问题：当 uncertainty set 本身依赖 state/control decision 时，如何避免用全局 uniform uncertainty set 造成额外保守性。
- 方法/关键结论：用 generalized semi-infinite programming 表示 decision/state-dependent uncertainty，并通过 local reduction 求解；文中包含 planar quadrotor 案例，展示相对 uniform uncertainty bounds 的保守性改善。
- 与本项目关系：第35章的 vertex-consistent residual 修正属于同一建模原则：已知 scheduling parameter T 时，应保留 d_x(T) 的依赖关系，而不是无条件替换为 d_x(T_max)。
- 局限：该工作不是 SMF/CZ output-feedback Tube MPC，也没有解决本项目的 recursive-feasibility shift certificate。
- 本项目状态：作为“不得丢失 uncertainty dependence”的强建模基线。
- Run 134 精读：Sections II、V 及 planar quadrotor 案例。其 uncertainty set 可显式依赖 state/control，支持保留实际推力与余项的共同图；但方法针对有限时域 robust optimal control，没有给出间歇 output-feedback RCI 或 old-plan shift certificate。
- Run 137 新增重读：Sections II--IV、Theorems 1--2 与 Section V。再次确认 `T=bar T+delta T` 决定 `d_z(T)` 的图可用 GSIP 表达；但 local-reduction 求解结果不能替代 compact invariant-set 与 recursive-shift 证明。
- Run 139 新增精读：Sections II--IV、Theorems 1--2。robust constraints 只对与同一 state/control decision 相容的 uncertainty set 量化；这要求 joint `(eta,d)` graph 保留同一 actual thrust 与 residual primitive，不能把 dynamics endpoint、residual width 和两个 error coordinates 独立笛卡尔化。

## Mulagaleti, Bemporad — Learning Quasi-LPV Models and Robust Control Invariant Sets with Reduced Conservativeness
- 年份/出处：2025, *IEEE Control Systems Letters*；DOI：https://doi.org/10.1109/LCSYS.2025.3569637；全文：https://arxiv.org/abs/2505.07287
- Run 134 精读：Introduction、Section 2.1、Propositions 1--2、Section 3.1、Proposition 3 与 Corollary 1。
- 方法/关键结论：对 self-scheduling quasi-LPV 模型构造 configuration-constrained polytopic RCI；在候选 RCI 内求 scheduling 下界以缩小 multiplicative uncertainty hull，并允许 vertex controls。文中 Remark 1 提示可扩展到 `p(x,u)`，正文证书主要按 `p(z)` 展开。
- 与本项目关系：非轴对齐 polytope、configuration constraints、vertex control 和利用 self-scheduling correlation 均已有直接近邻；不能作为创新。本项目额外义务是 intermittent-SMF estimation error、nominal/correction input allocation 与实际 thrust 同时决定 dynamics/residual 的联合图。
- 本项目状态：最强 qLPV ancillary RCI baseline；待完整合同后再做同条件数值比较。
- Run 137 新增重读：Section 2.2.2 Proposition 2、Section 3.1 与 Corollary 1。configuration-constrained RCI 已把 vertex controls、state-dependent scheduling 下界和 hard input constraints放入证书；当前先缺的不是集合类，而是 nominal input reserve。

## Wehbeh, Kerrigan, Scaccia — Generalized Semi-Infinite Programming for Robust Optimal Control with Decision-Dependent Uncertainty
- 年份/出处：2026 preprint，arXiv:2609.01538v1，2026-09-01；全文：https://arxiv.org/abs/2609.01538
- Run 134 精读：Introduction、Sections II--IV、Theorems 1--3、Algorithm 1、Sections V--VI。
- 方法/关键结论：将满足正则条件的 GSIP 变换为 existence-constrained SIP，用 adaptive discretization 与 worst-case separation oracle求解；把状态轨迹并入不确定变量，可处理 state/control-dependent uncertainty。收敛定理要求有限 master/oracle 子问题全局求解。
- 验证边界：数值例使用多起点局部 NLP；论文明确因此不满足理论中的全局子问题条件。Monte Carlo 不能替代 oracle nonpositive 的稳健证书。
- 与本项目关系：可为实际 thrust、误差、名义状态与 residual 的联合图提供语义/求解基线，但不直接给出 invariant tube、间歇 output feedback 或 recursive-feasibility shift theorem。
- 本项目状态：强 decision-dependent uncertainty baseline；不能把一次局部 solver success 当作 RCI 证明。
- Run 149 重读 Introduction、Section II Assumption 1、Lemma 1、Theorem 1/Remark 1、
  Section IV Assumption 2 与 Theorem 3。当前 `r_z(barT+deltaT)` 使 disturbance image 依赖
  correction decision，属于 GSIP 语义；该文不提供 invariant information ensemble 或
  recursive-feasibility 证明，本轮只用其判定 scheduled-residual 分支的问题类别。
- Run 150 核对2026-09-01 v1元数据并复核上述全文章节的准入边界。fixed-envelope
  translated shape 已在 mode 4 出现与 current correction 无关的 `e_p` width obstruction；
  因此本轮不启动 GSIP。该结果不否定历史 control-dependent shapes，只有先得到可闭合的
  history-conditioned intrinsic family 后才评估 scheduled tightening。

## Hanema, Lazar, Tóth — Heterogeneously Parameterized Tube Model Predictive Control for LPV Systems
- 年份/出处：2020, *Automatica*；全文：https://arxiv.org/abs/1910.08449
- Run 134 重读：Introduction 与 LPV problem setting。
- 方法/关键结论：对当前可测、未来未知的外生 scheduling signal构造 heterogeneously parameterized tubes，并证明 LPV tube MPC 的递归可行性/稳定性性质。
- 与本项目关系：是 arbitrary-future scheduling 的强 baseline；但 `delta T=kappa(e-eta,...)` 时实际 thrust 是 feedback-dependent，不能直接套用其外生 scheduling 假设。
- 本项目状态：保留为外生 LPV 对照，不作为当前六状态 ancillary 合同的直接证书。


## Kothare, Balakrishnan, Morari — Robust constrained model predictive control using linear matrix inequalities
- 年份/出处：1996, *Automatica*, 32(10):1361–1379；DOI：https://doi.org/10.1016/0005-1098(96)00063-5；公开技术报告：https://authors.library.caltech.edu/records/t7km1-0q967
- 研究问题：模型不确定性下如何把 worst-case 性能、输入/输出约束和 state-feedback synthesis 统一进入 robust MPC。
- 方法/关键结论：把 worst-case infinite-horizon objective 的上界以及 input/output constraints 转成 LMI convex optimization；可行 receding-horizon state-feedback 对所考虑的不确定 plant family 给出 robust stabilization。
- 与本项目关系：第36章之后的 joint state/input ancillary synthesis 可以借用这类 constraint-aware synthesis 思路，但“把约束直接放进 K 的设计”本身不是创新。
- 局限：该工作不是 CZ-SMF posterior、不是本项目的 thrust-scheduled residual W(T)，也不提供当前 output-feedback set-membership 接口。
- 本项目状态：作为 certificate-based ancillary synthesis 的经典 baseline。
- Run 133 阅读层级：仅核对 Caltech 正式页面与摘要；未取得可稳定阅读的全文，故不引用定理编号，也不声称其 LMI 直接覆盖 correlated `(A(T),W(T))` 与 intermittent output feedback。


## Lorenzen, Cannon, Allgöwer — Robust MPC with recursive model update
- 年份/出处：2019, *Automatica*, 103:461–471；DOI：https://doi.org/10.1016/j.automatica.2019.02.023；accepted manuscript：https://ora.ox.ac.uk/objects/uuid%3A78236757-fb85-4510-8e17-d75177b667d8
- 研究问题：在线 parameter/model update 后，如何在保持 robust constraints 与稳定性保证的同时减少 MPC 保守性。
- 方法/关键结论：把 online set-membership system identification 与 homothetic prediction tubes 结合；论文将 robust constraint satisfaction 和 closed-loop stability 的要求分开处理，并给出 recursive model update 下的稳定/约束保证。
- 与本项目关系：说明“在线更精确 uncertainty set 可减少保守性”已有成熟理论背景。第36章的 scheduling-conditioned residual 只能作为更强 baseline，不是创新点。
- 局限：处理 parametric model uncertainty，不是当前 state-estimation CZ posterior，也不是四旋翼 thrust-conditioned nonlinear remainder。
- 本项目状态：作为后续 SMF/CZ 保守性比较必须超过的 adaptive robust MPC baseline。

## Goulart, Kerrigan, Maciejowski — Optimization over State Feedback Policies for Robust Control with Constraints
- 年份/出处：2006, *Automatica* 42(4):523--533；DOI：
  https://doi.org/10.1016/j.automatica.2005.08.023；作者存档：
  http://hdl.handle.net/10044/1/724
- Run 157 精读：Introduction、Sections 2--4，重点核对 affine state-feedback 与 causal
  affine disturbance-feedback 的等价参数化、polytopic uncertainty 下的凸约束接口。
- 方法/关键结论：对有界加性扰动和多面体混合约束，有限时域 affine feedback 可改写为对
  过去扰动的因果仿射策略，并转成 LP/QP/SOCP；这已覆盖“用仿射反馈改变 reachable-set
  shape 并 robustify 输入/状态约束”的一般思想。
- 与本项目关系：Run157 的 `delta T=K_v d_v` 只是该成熟参数化在两个已知 exact generator
  fibers 上的一步实例；本项目的差异仅在 noisy-output information fiber、缺测自动机和共享
  estimator/plant residual，不能据此声称新的仿射反馈算法。
- 局限：论文是全状态/扰动反馈有限时域框架，不直接给出当前15模态信息集合的 recurrent
  target inclusion，也不证明 SMF--MPC 递归可行性。

## Goulart, Kerrigan — Output Feedback Receding Horizon Control of Constrained Systems
- 年份/出处：2007, *International Journal of Control* 80(1):8--20；DOI：
  https://doi.org/10.1080/00207170600892949；作者存档：
  http://hdl.handle.net/10044/1/4386
- Run 158 精读：problem formulation、finite-horizon affine output-feedback reformulation、
  robust constraint conditions 与 invariant error outer-approximation 部分。
- 方法/关键结论：固定线性 observer 下，带状态扰动和测量误差的 constraint-admissible affine
  output-feedback 问题可等价凸化；永久约束保证还要求 observer error 的 invariant bound 与
  receding-horizon terminal/shift 条件，不能由一步安全外推。
- 与本项目关系：mode-9 同一当前输入覆盖 success/miss 是该 robust causal policy 量词的
  packet-automaton 特化；本轮 exact branch witness 只是局部实例，不是其算法的新版本。
- 局限：论文不含 bounded-dropout automaton、joint `(eta,e)` information set、共享 residual
  primitive 或 actual-thrust-dependent residual，因此不能替代当前 target-family 闭合证明。
- Run 159 定向重读：finite-horizon robust constraints、输入/状态约束与无限时保证条件。
  本轮支持函数下界只是其 affine output-feedback 约束思想在一条 dropout history 上的精确
  必要条件；不构成新的综合算法，也不提供 terminal/shift 结论。
- Run 160 重读同一正文范围。通过把信息权限放宽到任意 full-state causal policy，本轮必要
  下界比 affine output-feedback 可行域更乐观；其失败可否定当前 seed/输入盒，但仍不是一般
  output-feedback 算法或无限时定理。

## Hempel, Kominek, Werner — Output-Feedback Controlled-Invariant Sets for Systems with Linear Parameter-Varying State Transition Matrix
- 年份/出处：2011, CDC-ECC；DOI：https://doi.org/10.1109/CDC.2011.6160901；全文：https://skoge.folk.ntnu.no/prost/proceedings/cdc-ecc-2011/data/papers/1283.pdf
- Run 140 精读：Sections II--III、Definitions 1--2、Theorem 1、式 (3)--(11)。Run 141
  为 full-state/causal predecessor 比较重读 Section III-A--C、Definition 2、Theorem 1
  及控制输入计算，确认同一 noisy output 的 observation fiber 必须共用一个输入。Run 142
  重读式 (3)--(10) 与 Section V：其 Farkas 条件验证给定 OFCI polytope 并在线求输入，
  论文明确仍缺直接计算 OFCI polytope 的算法。
- 方法/关键结论：对每个 admissible noisy output 及当前已知 scheduling，选择一个只依赖输出/调度的输入，使与该输出一致的全部状态和所有过程/测量扰动满足多面体不变；给出 Farkas 验证及在线/显式 PWA 控制计算。
- 与本项目关系：直接支持 observation-fiber 共用输入的量词；因此该量词不是创新。其 scheduling 外生且当前可测，本项目 actual thrust 由 correction 决定且下一 packet outcome 未知，不能直接套用其 LPV 顶点条件。
- 本项目状态：partial-information RCI 的最强直接有限维基线。
- Run 143 重读：Section III-A--C、Definition 2、Theorem 1、式 (3)--(10)，用于核对
  joint `(eta,e)` 候选上仍必须按相同可见 `d=e-eta` fiber 共享输入；该量词不是本项目创新。
- Run 144 重读：同一章节用于核对 mode 4/9 的未知 success/miss 分叉在当前时刻仍只能
  使用同一个 fiber control；本轮的零输入内证书只是其量词的特例，不是新算法。
- Run 146 精读：Section III-A--C、Definition 2、Theorem 1、式 (3)--(11)，复核第二层
  predecessor 中每个 `d` 对应的完整隐藏 `eta` 纤维及未知 packet successor 必须共享当前
  输入；给定候选的验证与控制计算已有直接近邻。
- Run 147 重读同一章节：用于确认初始化 all-miss history 的完整 hidden `eta` fiber 不能
  按真值拆分；zero correction 生成一个中心化 return image，不是 output-feedback controller
  synthesis。Run 149 纠正：该中心位置不是任意 policy 必须容纳的 target。
- Run 155 重新精读 Section III-A--C、Definition 2、Theorem 1、式 (3)--(14)。再次确认
  同一 noisy-output fiber 的完整相容状态只能使用一个 output-dependent input，且输入约束与
  鲁棒后继属于同一量词；仿射输入在凸 fiber 上的可行性仍依赖凸输入集。
- Run 180 全文重读 §II、§III-A--C、Definitions 1--2、Theorem 1、式(3)--(14)与
  Algorithm 1，定向核查固定 output cell、PWA input 与逐 facet robustification。该框架已覆盖
  本轮 fiber-shared affine policy/target-normal oracle 的方法思想；当前差异只在 packet edge、
  joint `(eta,e)` 坐标和 actual-thrust-dependent residual 的可靠实例化。
- Run 181 重新下载全文并精读 §III-A--C、Definition 2、Theorem 1、式(3)--(14)与
  Algorithm 1，专门核查“当前输入先于未知 packet label”的 mode-4 双边证书。论文要求每个
  noisy-output fiber 共用输入并逐 facet robustify，但其 LPV scheduling 在控制时可知、扰动集
  固定；本轮仍只是在项目的 unknown-edge/shared-residual 合同上可靠实例化，不作创新声明。
- Run 182 重新下载全文，定向精读 §III-C、式(9)--(14)与 Algorithm 1。各 facet 的参数解必须
  覆盖完整 `Y(Omega)`，再交集细化为共同凸分区并在每区求单值 PWA control。因此有限 output
  partition、完整覆盖与 overlap refinement 均已有直接基线；Run180/181 若不验证 target
  `d`-cell 覆盖，就还不是可执行 partition graph。

## Houska — Intrinsic Separation Principles
- 年份/出处：2023 预印本、2026 *Automatica* 183:112661；DOI：https://doi.org/10.1016/j.automatica.2025.112661；全文：https://arxiv.org/pdf/2307.04146
- Run 182 重新下载全文并精读 §4.2、§4.4、§6.1--6.7、Definitions 4--5、Lemma 2、
  Theorem 3 与式(25)--(29)。configuration-constrained polytopes 参数化固定复杂度 information
  ensembles；extreme vertex polytopes 上的 controls 经凸插值覆盖全部 information sets；式(29)
  直接综合 invariant terminal ensemble，§6.7给出 facets、ensemble parameters 与 extreme sets
  数的复杂度权衡。故固定预算 information-family 是本项目必须复现的强基线，不是创新声明。
- Run 183 重新打开全文并定向精读 §4.2、§5.5、§6.1--6.7、式(24)--(31)与 Theorem 3
  证明。原问题固定线性 `A,B,C` 和固定多面体 `W,V`；式(29)在每个 extreme information
  polytope 上配置一个共享控制，并以不变 ensemble 作终端条件。当前实际推力相关 `W(T)` 与
  packet-dependent measurement 不能直接代入；本轮只构造执行器全域固定包络和15-mode
  edge-product适配合同，不声称已复现式(29)的数值解。
- Run 184 重新精读 §6.1--6.7、式(25)--(30)、Theorem 3及证明。原式的posterior-measurement
  后选control时序不同于当前`control_precedes_successor_edge`；本轮采用每个source一组
  extreme controls、先传播后按edge测量的因果适配。axis-aligned box实例最终由21行exact
  Farkas证书否定；该否证只针对丢失位置--速度相关性的模板，不否定一般information ensemble。
- Run185 针对相关模板重读 §6.3--6.7、式(25)--(30)与Theorem 3。纠正坐标变换后，固定
  `(p,q)` parallelogram shape不能周期闭合；尚未构造`Z/H/Omega`、extreme-set controls或
  invariant ensemble，因而不援引Theorem 3外推一般模板不可行。
- Run186 精读 §6.2--6.5、式(25)--(27)及Theorem 3构造和证明开头。单个六facet集合的
  measurement-support映射只提供`Y/G/Lambda`层接口；连续measurement centers、`Z/H/Omega`
  与extreme information sets仍须另证，不能由一次严格支持收缩升级为invariant ensemble。
- Run187 重读§4.1--4.2、§6.2--6.5、式(7)、(25)--(27)及Theorem 3证明。sensor ensemble
  `V`已通过“存在同一measurement center”的集合量词覆盖连续观测域；对六facet模板，
  measurement-compatible coordinate可精确取`Z_1=(e_0+e_3)/2`。因此无需枚举未来center，
  但剩余`Z_2/H/Omega`及control-before-packet图仍须独立构造。
- Run188 重读§6.1--6.5、式(25)--(27)、Definition 7、Theorem 3及证明。`Z`坐标影响离散精度，`H/Omega`由所选参数多面体configuration决定；可逆线性换坐标保持同一参数多面体的极点数，不能据此声称减少extreme information-set预算。
- Run189 重读§3.1--3.2、§6.2--6.7、式(25)--(30)及Definition 7。参数多面体的几何极点还需按包含极大性过滤为真正extreme sets；仅用物理包含构造的有界域含完整安全盒这一支配成员，故ensemble边界退化为单元素，不能提供information-dependent control。
- Run190 重读§3.1--3.2、§6.1--6.5、Definition 7、式(56)--(57)及Theorem 3证明接口。真实位置条带生成连续多个互不包含的真正extreme sets，但其offset参数域可是一条仅有两个顶点的线段；真正boundary与finite extreme-vertex representatives必须分开计数。
- Run 144 精读：Sections 4.4、6.1--6.7，Definition 4、Lemma 2、Theorem 3、
  Problems (24)、(27)、(29) 与 complexity discussion。
- 方法/关键结论：以 information ensemble 表示未来可能的信息集集合；用
  configuration-constrained polytopes 和 extreme vertex polytopes 得到有限维凸近似，
  每个 extreme information set 配置一个控制，(29) 可计算 invariant polytopic
  information ensemble。
- 与本项目关系：joint information set、extreme-fiber control、固定模板 polytope 与凸
  优化均已有强近邻，不能作为创新。本项目只剩 packet graph、observer split、shared
  primitive 和 actual-thrust-dependent residual 的可靠实例化及完整闭环证据链可研究。
- 局限：其通用信息 ensemble 近似没有直接给出当前15模态 contract 的精确 candidate，
  也不替代 source-domain、input allocation、terminal/shift 的逐项证明。
- 本项目状态：一般信息集合成的最强直接基线；Run 144 仅实现一个受限一步内证书。

- Run 145 定向重读：Sections 4.2、6.1--6.5、Definition 4、式 (7)、(24)--(27)，
  用于界定15模态首次下降层。extreme information-set control 与多面体信息集合成已有
  一般方法；本轮逐模态零修正内投影只是一种受限实例。
- Run 146 定向重读：Sections 5.3、6.1--6.5、式 (38)、(43)，用于区分固定完整纤维模板
  与一般 information ensemble。完整纤维第二层若塌缩，只能淘汰该保守模板，不能否定
  保留条件纤维相关性的多面体信息集方法。
- Run 147 精读全文 HTML Sections 4.4、6.2、6.4--6.5、Lemma 2、Definition 7、
  Theorem 3 及证明。极端 information set、每集合共享控制和多面体 information tube 已有
  一般方法；本轮 rank-three correlated return seed 只是当前 packet/observer 合同的一项
  必要 reachable-set 实例证书，不作集合算法创新声明。
- Run 149 重读 Sections 3.5、4.2--4.3、5.3--5.4，Definition 1、Theorem 1及证明、
  式(18)--(20)，并复核 Sections 6.5--6.7。固定加性扰动集下，控制策略改变 tight
  information tube 的 extrinsic translations 而不改变 intrinsic equivalence class；本项目
  只有使用 Run136 global envelope 时才能直接采用这一 shape/center 分离，scheduled
  `W(T)` 不满足其固定扰动集接口。
- Run 150 重新逐页精读 pp.14--17 的 Sections 4.1--4.3、Definitions 4--6、Theorem 1
  及证明，pp.23--25 的式(18)--(19)/Theorem 2，pp.29--32 的 Definition 7、Theorem 3
  及证明。确认 translation functions 和 extreme-information-set controls 已覆盖一般方法；
  本轮只对 Run148 exact shape 给出实例级 width obstruction，不能宣称新算法或一般
  information-ensemble 不可行。
- Run 154 定向精读 Sections 4.2--4.3、6.3--6.5、Definitions 5--7、Theorems 1/3 与证明。
  一步 ensemble inclusion 的量词先固定同一 policy，再外包全部后继信息集；逐层更换策略不
  产生一张可执行控制器。凸外包产生的新 information sets/fibers 也必须纳入下一步闭合。
- Run 155 定向复核 Sections 6.4--6.5、Definition 7、Theorem 3 与证明中 extreme
  information-set controls 的连续凸权重组合。固定线性边、凸扰动和同一仿射可见策略时，
  convexification-created fibers 由仿射像/凸包交换律自动覆盖；这是该一般方法的直接特化，
  不是新算法，且不能用于 control-dependent `W(T)` 或跨离散标签混合。
- Run 156 重新精读 Section 6.5、Theorem 3 的完整证明，并复核 Section 4.2 Definitions
  4--6。证明中的控制 `mu(X)` 由当前 information set 的凸权重组合 extreme controls；因此
  零/label-only 策略失败不能外推为一般 information-ensemble feedback 失败。
- Run 159 重读 Sections 6.4--6.5、Theorem 3，确认一般 information-set feedback 已有完整
  近邻；本轮只淘汰一个 fixed-residual、bounded centered-affine path，不能外推为一般方法失败。
- Run 178 全文定向重读 Sections 2、3.1--3.3、Propositions 1--3 及 extreme-set/downward-
  closure 构造。information ensemble 对任意紧集求交的闭合和最小表示已有一般理论；仓库
  `T_0/T_1` 只能描述局部边，不能替代既有 60-state/45-recurrent information-family 合同。

## Villanueva, Müller, Houska — Configuration-Constrained Tube MPC
- 年份/出处：2022，arXiv:2208.12554；全文：https://arxiv.org/pdf/2208.12554
- Run 183 实际阅读：摘要、Introduction、§2.1--2.3、§3.1--3.4（pp.1--9）。论文针对具有
  加性/乘性不确定性的线性系统，用固定 facet directions、configuration cone 和 vertex maps
  联合参数化 tube facets/vertices，并把 vertex controls 纳入凸优化；论文明确以可表示 tube/
  policy 类的集合包含定义严格“更少保守”。
- Run 184 定向重读 §2.1--2.3、§3.1--3.4，用于逐项构造box的configuration cone与vertex
  maps。4-facet box及其vertex controls是现有框架的直接实例；不可行结论来自当前仅位置测量
  下的velocity-radius环，不是CCTMPC一般方法失败。
- Run185 精读 §3.4--3.5的Theorems 1--2、式(15)--(21)，§4.1--4.2的Corollary 4、
  式(25)--(27)与Remark 5。新增facet、configuration domain和vertex-control LP均属已有方法；
  固定parallelogram外包失败不能替代保留active velocity facets的六facet configuration检查。
- Run186 精读 §3.4--3.5、Definition 6、Lemma 1、Theorems 1--2、式(4)--(8)，并重读
  Corollary 4、式(15)--(18)。六法向的24行configuration cone和六个vertex maps均是该框架
  的直接实例；本轮贡献等级仅为项目基线的精确复现与measurement接口纠错。
- Run189 重读§3.4--3.5、Definition 6、Lemma 1、Theorems 1--2。configuration cone与vertex maps可把物理state containment写成参数线性约束，但有界性本身不保证多个不可比较的最大多面体。
- Run190 重读§3.4--3.5、Lemma 1、Definition 7及Theorem 2的vertex-map证明。测量生成的offset segment落在configuration cone内，但矩形上的斜facets冗余、segment处于退化边界；这不足以认证regular六facet meta configuration。
- 与本项目关系：`Y,G,Lambda` 的配置约束几何和 vertex-control machinery 是强基线工具，不能
  作为创新。本文是 full-state robust tube，不处理当前间歇测量 information ensemble；Run183
  只借其模板接口，尚未选择模板或证明相对固定/同伦tube的同预算优势。

## Badalamenti, Mulagaleti, Villanueva, Houska, Bemporad — Efficient Configuration-Constrained Tube MPC via Variables Restriction and Template Selection
- 年份/出处：2025 IEEE CDC；DOI：https://doi.org/10.1109/CDC57313.2025.11312697；全文：https://arxiv.org/pdf/2505.14440
- Run186精读：§3.1--3.2、§4.1、Problem (19)、Algorithm 1、Proposition 3，以及§5中
  10-state quadrotor的template/computation比较。
- 方法/关键结论：以configuration triple `(F,E,V)`表示固定facet/vertex结构；Algorithm 1
  逐次切除当前vertex、重算configuration triple并解RCI QP，使性能指标非增。论文明确讨论
  facet/vertex数量与在线变量、约束及保守性的折中，并给出10状态四旋翼例。
- 与本项目关系：手工给box增加一对耦合法向以及“template refinement”本身已被更强一般方法
  覆盖，不能作为创新。本项目可研究的差异只剩间歇测量information ensemble、控制先于packet
  label的因果图、可靠SMF接口及同预算闭环收益。
- 局限：论文是full-state robust tube/RCI template设计，不直接给出当前`Z/H/Omega`、
  measurement meta-update或15-mode packet graph证书。
- Run189 重读§3.5--3.6、§4.1、Algorithm 1及复杂度讨论。限制自由度和增添template facets已有系统方法；本项目若新增offset/shape约束，必须由information结构及闭环证书驱动，不能用任意caps制造预算结果。

## Kumar, Kothyari — Set-Theoretic Output Feedback Tracking Control via Linear Programming
- 年份/出处：2026, MTNS 2026；作者公开全文：
  https://www.researchgate.net/publication/407040373_Set-Theoretic_Output_Feedback_Tracking_Control_via_Linear_Programming
- Run 144 精读：Sections 2.3--3、Definition 4、Theorem 5、式 (14)--(29)。
- 方法/关键结论：对 `x+=Ax+Bu+Ew, y=Cx` 与静态 `u=Ky+Lr`，用 zonotope containment
  线性条件联合综合 output-feedback gain、state RCI 和 admissible reference set。
- 与本项目关系：这是截至本轮检索到的2026直接 zonotopic output-feedback RCI 近邻，排除
  “zonotope + LP 联合求 gain/RCI”的首次性；其 OFCI 定义也要求同一 output fiber 共用输入。
- 局限：没有测量噪声、间歇包、observer 信息状态、mode graph 或 actual-input-dependent
  residual；因此不能直接认证 `(eta,e)` joint information candidate。
- 本项目状态：最新静态 output-feedback zonotope-LP 对照；不得把其 state RCI 结论移植为
  当前 partial-information RCI。

## Rungger, Tabuada — Computing Robust Controlled Invariant Sets of Linear Systems
- 年份/出处：2017, *IEEE Transactions on Automatic Control*, 62(7):3665--3670；DOI：https://doi.org/10.1109/TAC.2017.2672859；全文：https://arxiv.org/pdf/1601.00416
- Run 142 精读：pp.1--7，式 (4)--(10)、Lemma 1、Theorem 1 及 Section 4 的 Pontryagin difference/projection 实例。
- 方法/关键结论：从 `R_0=X, R_{i+1}=pre(R_i) intersect X` 的递减序列出发，区分一般不有限终止的 outer predecessor sequence、允许任意小约束放松的外 RCI 近似，以及用 disturbance inflation 获得的内 RCI 近似。
- 与本项目关系：给出二维多面体 predecessor、投影和证据等级的直接基线；但其控制器观察完整迭代状态。本项目只能在可见 `d` 上用该迭代，隐藏 `eta` 必须先按 observation fiber 统一 robustify。
- 本项目状态：Run 142 的 exact product-fiber predecessor 基线；迭代/投影不是创新。
- Run 145 定向重读：pp.1--6、式 (4)--(10)、Theorems 1--2 与 Remark 1。普通
  `R_1=X∩pre(X)` 只是 descending outer sequence 的一层，一般既非 RCI 也不能导出永久
  安全反馈；因此本轮15/15非空只能作为继续第二层的门槛。
- Run 146 重读：pp.1--6、式 (4)--(10)、Theorems 1--2，核对第二下降层仍只是有限
  predecessor 序列；无论非空或部分塌缩，都不能越级声称 RCI 或一般输出反馈不可行。
- Run 160 重读 Introduction、式(1)--(10)、Lemma 1 与 outer/inner RCI discussion。当前结论
  来自一条允许字符串上策略无关的硬约束必要条件，而不是有限 predecessor 非空/塌缩；仍只
  否定固定 seed/residual/input contract，不升级为一般 RCI 不存在。
- Run 194 重读定义、式(4)--(10)、有限确定讨论、Lemma 1、Theorems 1--2及证明。Run193的
  四层集合仍是一般descending outer sequence；本轮必须直接检查self-predecessor/vertex-control
  条件，不能由有限层非空推断RCI。

## Houska, Müller, Villanueva — Polyhedral Control Design: Theory and Methods
- 年份/出处：2024, arXiv:2412.13082；全文：https://arxiv.org/pdf/2412.13082
- Run 142 定向阅读：Sections 3.3--3.6、3.10，重点 pp.12--16 的 controllable/control-invariant/robust-control-tube 参数化与 pp.21--22 的 output-feedback 文献路由。
- 方法/关键结论：系统整理 vertex control、polyhedral projection、固定复杂度 polytope/zonotope 和 robust control tube/RCI 的凸优化表示。
- 与本项目关系：非轴对齐多面体、vertex input interpolation 和固定模板均已有成熟近邻；本项目若有贡献，必须来自可靠 SMF 信息接口、联合相关性及闭环 theorem，而不是集合参数化本身。
- 本项目状态：多面体综合与复杂度比较的综述基线。

## Baras, Patel — Robust Control of Set-Valued Discrete-Time Dynamical Systems
- 年份/出处：1998, *IEEE Transactions on Automatic Control*, 43(1):61--75；全文：https://terpconnect.umd.edu/~baras/publications/journals/1998_Baras_Robust_Control.pdf
- Run 140 精读：Section IV-A--B、Lemma 4、Theorems 9--11、15--16。
- 方法/关键结论：把 observation history 诱导的信息状态作为充分统计量，将 output-feedback robust game 转为 information-state feedback game，并给出有限/无限时动态规划必要与充分条件。
- 与本项目关系：说明仅使用点估计偏差 `d` 的有限 policy class 一般是保守近似，不能宣称等价于所有 output-feedback controllers。
- 本项目状态：一般信息状态概念基线；不直接数值实现其无限维动态规划。
- Run 143 定向精读：Section IV-A 的 Information State Formulation、Lemma 4、Remarks
  8--10、Theorems 9--11，复核可行状态/历史相关性必须保留，且一般信息状态是无限维。
  这支持从 product `E_eta x D` 转向 joint set，但不能把 joint set 本身声明为创新。
- Run 152 重读 Section IV-A 的 Information State Formulation、Lemma 4 证明、Remarks
  8--10、Theorems 9--11 与 Corollary 4。由完整历史信息状态压缩到有限标签，必须另证
  初始化覆盖和递归模拟；`mode/age` 标签本身不是充分统计量证明。
- Run 177 再读 Section IV-A、Lemma 4、Remarks 8--10、Theorems 9--11、Corollary 4，专门核查
  五步非线性问题的初始条件与时序。配置 prior 经 tick-0 实际测量才形成 posterior，因此应量化
  posterior 族；有限时域 Bellman 后继还必须保留 tick-5 success/miss 的不同 mode。

## Kjellqvist — Minimax Dual Control with Finite-Dimensional Information State
- 年份/出处：2024, L4DC, *Proceedings of Machine Learning Research* 242:299--311；
  全文：https://proceedings.mlr.press/v242/kjellqvist24a/kjellqvist24a.pdf
- Run 143 精读：Sections 2.1--2.2、Assumption 2、Proposition 4、式 (11)--(18) 及结论。
- 方法/关键结论：当每个测量逆像最多含固定有限个元素时，把 worst-case history 压成
  有限维递归信息状态并写成 information-state dynamic program。
- 与本项目关系：当前有界实值测量噪声产生连续无穷 observation fiber，不满足 Assumption
  2；不能援引该文宣称当前 joint information set 有精确有限维递归。论文结论也明确把
  实值传感噪声列为该有限逆像结果之外的情形。
- 本项目状态：有限维压缩的反边界；任何固定复杂度 CZ/polytope 压缩仍需单独包含证明。

## Yang, Ozay — Efficient Safety Control Synthesis with Imperfect State Information
- 年份/出处：2020, CDC, pp. 874--880；作者链接：https://web.eecs.umich.edu/~necmiye/pubs/YangO_cdc20.pdf
- Run 140 阅读层级：仅核查摘要；正文抽取失败。
- 摘要层面内容：把 estimated-state dynamics 上的 perfect-information safety game 用作一般 noisy-measurement partial-information game 的两个保守近似，并区分初态信息条件。
- 本项目状态：支持保守性标注，不引用其定理作本轮证明。

## Yang, Ozay — Safety Control Synthesis for Systems with Missing Measurements
- 年份/出处：2021, *IFAC-PapersOnLine*, 54(5):97--102；DOI：https://doi.org/10.1016/j.ifacol.2021.08.481；作者链接：https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf
- Run 140 阅读层级：核查摘要与问题陈述；正文抽取失败。
- 摘要层面内容：用 automaton 描述 missing-measurement patterns，利用 causality 构造 product system，把 partial-information safety synthesis 化为 full-information game。
- 与本项目关系：15-mode bounded-dropout product construction 已有近邻，不能作为创新；其有限安全游戏不直接处理当前连续六状态与 control-dependent residual。
- Run 153 精读 Sections 4.1--4.4、Algorithm 1、Propositions 2--5 及式 (8)--(11)。string
  automaton 在成功测量时压缩缺测串并规定因果开环输入承诺；产品不变集的安全结论仍量化全部
  允许 return string、扰动与中间状态。它支持 `(mode,last_return)` 的离散语言实现，但不把
  连续联合信息集压成有限标签，也不允许以三个首次-return seed 代替真实初始化。
- Run 159 重读同一正文范围，专门核查长 dropout string 上每个中间状态的 safety 义务；因此
  `15->15` 在 mode 11 的位置失败已经足以阻断 final-success target constituent。
- Run 160 重读 Sections 2--4、Assumption 1 与 product safety 量词。15-tick string 的第13个
  miss 已违反中间状态必要条件，即使最终 success 可重置 estimator，也不能恢复该条安全路径。
- Run 165 重读全文 Sections 3--4、Definition 3、Propositions 2--5：控制器在缺测串开始前按可见
  信息选择因果输入承诺，安全量词覆盖允许串的每个扰动实现和中间状态。本轮极端可见fiber是该
  量词在冻结连续模型上的精确反例，不是string-automaton或product-game创新。

## Do, Prodan — Tube MPC via flatness for multicopter trajectory tracking
- 年份/出处：2024, European Control Conference；全文：https://hal.science/hal-04567082/document
- Run168精读：Sections II-A、III-A--B，式(18)--(25)。
- 方法/关键结论：将多旋翼跟踪误差化为带固定有界加性扰动`W`的系统，用mRPI集`Z`构造
  nominal tube，并以`X⊖Z`、`V⊖KZ`收紧约束；设计要求扰动与增益使收紧后集合非空。
- 与本项目关系：是固定全局余项包络的直接基线，但不从在线SMF信息集生成局部未来扰动界。

## Hu, Bujarbaruah, Zhang, Borrelli — Real-Time Tube MPC Applied to a 10-State Quadrotor Model
- 年份/出处：2018, American Control Conference；全文：https://borrelli.me.berkeley.edu/pdfpub/2018_15.pdf
- Run168精读：Theorem 1、式(8)、Lemma 1及对应证明。
- 方法/关键结论：用椭球tube与RFIT条件处理四旋翼非线性；`Omega_n(q,Q)`必须包含tube中每个
  状态和允许扰动对应的非线性余项，Lemma 1给出tube-dependent解析外包。
- 与本项目关系：是局部气动余项的最强方法基线。当前后验变小不够，必须认证整个15-tick未来
  tube并证明跨时刻闭合；本轮未复现其10状态控制器。
- Run169重读§II-A、Theorem 1、式(8)、Lemma 1及证明：RFIT与nonlinearity bounder量化tube中
  每个状态/扰动。故J14要求族中一个首步合法反例即可否定当前局部余项目标，无需用有限采样替代
  全量词，也无需继续传播其余14步。
- Run170纠错：上一句的“J14要求族”只对独立残差外包成立；没有从benchmark初始集出发的
  非线性轨迹证书时，不能把外包成员称作真实plant可达，也不能据此外推物理路线不可能。

## Rego, Raffo, Terra, Scott — Reachability Analysis of Nonlinear Discrete-Time Systems Using Polyhedral Relaxations and Constrained Zonotopes
- 年份/出处：CDC 2024；作者预印本2025，arXiv:2504.11663；DOI：https://doi.org/10.1109/CDC56724.2024.10886592；全文：https://arxiv.org/abs/2504.11663
- Run170精读：§II Problem Statement and Preliminaries，式(1)--(8)；§III Definition 3、式(10)--(11)及乘法的McCormick包络。
- 方法/关键结论：从`X0`与过程不确定集`W`递归外包非线性像；把factorable函数分解为共享
  中间因子，在lifted space中相交各因子的多面体包络，再投影为CZ。包络复杂度线性增长，仍需
  CZ降阶。该方法是保留非线性计算图依赖的直接基线，不是本项目创新。
- 与本项目关系：Run169的独立逐边残差primitive丢失了状态--风--气动残差的物理图；应先按该
  类方法构造联合外包，再接缺测SMF、控制收紧和递归可行性。本文不直接解决本项目的有界丢包
  信息状态、因果控制选择或四旋翼硬约束闭环定理。

## Ning — Data-Driven Synthesis of Robust Positively Invariant Sets: From State Feedback to Output Feedback
- 年份/出处：2026, arXiv:2608.23412；全文：https://arxiv.org/abs/2608.23412
- Run 140 阅读层级：核查摘要及 problem formulation，未精读证明。
- 已知内容：从 noisy offline data 对 LTI state-feedback 与 observer-based output-feedback 同时综合 gain 和 ellipsoidal RPI。
- 与本项目关系：是 2026 新近邻，但仍先冻结 observer-based closed loop；不覆盖 observation-fiber controlled RCI、bounded-dropout automaton 和 feedback-dependent residual graph。

## Lucia, Ernesto, Castelan — Set-theoretic output feedback control: a bilinear programming approach
- 年份/出处：2023, *Automatica*, 151:110861；DOI：https://doi.org/10.1016/j.automatica.2023.110861；作者预印本：https://users.encs.concordia.ca/~wlucia/files/STOutput2023.pdf
- Run 141 精读：Sections 2--5、Definitions 2--3、Propositions 1--2、Algorithm 1、式 (7)--(31)。
- 方法/关键结论：联合综合静态输出反馈增益、terminal RCI 与嵌套 robust one-step controllable sets；rank-deficient output 情形采用不依赖隐藏状态的离线切换，满状态带噪情形才可用当前测量选择更小集合。集合包含和输入约束由 extended Farkas lemma 转成双线性条件。
- 与本项目关系：直接说明 output-feedback 与 full/noisy-state feedback 的信息权限及在线集合选择不同；因此读取隐藏 `eta` 的 vertex control 只能作乐观上界，不能作为当前 causal ancillary policy。
- 局限：论文处理 LTI、静态输出增益和嵌套多面体，不含 15-mode missing-data graph、实际推力相关余项或 SMF zonotope fiber。
- 本项目状态：作为 output-feedback set synthesis 的强方法基线；Run 141 只实例化因果性负对照，不复现其 bilinear synthesis。

## Run201 定向重读（2026-10-30；历史84篇中的 Lorenzetti & Pavone，不新增篇数）

- **论文：** Joseph Lorenzetti, Marco Pavone, *A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme*, 2020, arXiv:1911.07360v2；原文 https://arxiv.org/pdf/1911.07360 。
- **阅读层级与范围：** 2026-10-30，原文 Section II Assumptions 1–2、Section III-A RPI 定义、Section IV-D 式(10)–(11)、Section IV-E/F 式(12)–(13)及 Proposition 1；其余章节本轮未重新核验。
- **问题/方法：** LTI 系统受有界过程与测量噪声影响时，用 Luenberger observer、耦合估计/控制误差的固定截面 RPI、nominal MPC 与约束收紧建立输出反馈鲁棒约束满足。
- **关键假设/结论：** 需要 (A,B) 可控、(A,C) 可观、误差闭环稳定、存在 RPI 与满足终端包含/下降的 nominal terminal ingredients，且初始误差落入 RPI、初始 MPC 可行；Proposition 1 在这些条件下保证约束满足。固定 RPI 本身不替代 terminal/shift。
- **局限：** 连续的线性观测器测量、LTI 与固定误差截面；不直接涵盖冻结仓库的15-tick位置缺测图、推力调度任意跳变及状态相关气动 residual。
- **本项目关联/可复用：** 用耦合误差状态与 support 收紧审计四状态 SMF-MPC 接口，不能把“一个 tube + RPI + 终端”宣称新贡献。本轮的横向不可辨识下界是必须满足的必要条件，尚不是 Lorenzetti 充分控制方案。
- **待查问题：** 对每 tick 姿态观测和每5/10/15 tick位置更新，能否建立有限复杂度且 shift-compatible 的条件化后验/backup policy，并通过原四状态 Gate A？


## Run215 定向正文复核（2026-10-31；Scott等2016，既有87篇内，不新增计数）

- **题名/作者/年份/出处：** Joseph K. Scott, Davide M. Raimondo, Giuseppe Roberto Marseglia, Richard D. Braatz (2016), *Constrained zonotopes: A new tool for set-based estimation and fault detection*, *Automatica* 69:126–136。DOI：https://doi.org/10.1016/j.automatica.2016.02.036；作者公开全文：https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。
- **本轮实际阅读范围：** Definition 3 (9)，Proposition 1 (11)–(13)，Proposition 2 (19)–(20)，Theorem 1 (21)，Section 4 复杂度增长/降阶讨论，Section 5 (31)–(33) 状态估计递推；其余章节未在本轮精读。
- **研究问题/方法：** 在有界过程/观测误差下，用 CG 表示 \(Z=\{G\xi+c:\|\xi\|_\infty\le1,A\xi=b\}\) 保留集合交、线性映射与 Minkowski 和；通过约束/生成元降阶平衡精度和复杂度。
- **定理与假设：** Theorem 1 给出凸多面体与不限复杂度 CZ 表示的等价；Proposition 1 给出精确集合运算公式；Section 5 递推依赖线性离散动力学及紧有界扰动、量测误差。成员资格/非空通常需要 LP。
- **主要结论与局限：** 保留联合线性约束可避免过早区间外包；但约束数随递推增长，降阶须证明包含。论文没有为本仓库15-mode间歇测量和推力调度提供可直接套用的递归可行性定理。
- **本课题关联/可复用技术：** Run215先将位置—速度、姿态—角速度历史恒等式实现为精确有理数联合线性条带，并以三包位置支持严格排除第193拍旧盒角点。这是**H-表示外包**，虽可由 Theorem 1 转为CZ，却**没有实现CZ的CG表示、完整后验传播或降阶**；不将既有 CZ 理论宣称为新贡献。
- **阅读日期与待查问题：** 2026-10-31。需实现可复核的CG表示和联合支持优化，并在完整仓库/同等计算预算下验证能否恢复Run214第193拍控制准入；现有独立盒过滤仍拒绝。
