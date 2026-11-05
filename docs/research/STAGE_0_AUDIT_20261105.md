# 阶段 0｜四旋翼外环 MPC + SMF 项目现状与验收报告

审查日期：2026-11-05（上海）。**结论：可以提交阶段 0 验收；尚未批准进入阶段 1，亦未定题。**

主分支有可复算的六维 CZ **一步**共同输入判据。本地另有一条在三轴独立 ZOH 双积分模型上、从时间戳窗口到统一 Tube 和终端的条件性闭环推导，以及一条逐拍有量测的联合误差管路线。两者不是同一信息合同，均未合入主分支。首要理论瓶颈是：在控制器实际能区分的交付历史上，能否对**每个**允许恢复块证明 CZ 估计误差的相位恢复，并把该界用在更新后仍可移位的控制收紧上？现有证据没有回答这个一般问题。阶段 0 仅核查证据及其适用范围。

## 1. 版本和材料范围

| 层次 | 已核实事实 | 在本报告中的用途 |
|---|---|---|
| GitHub main | [9882220234a20d730a38d648d5c08ac47c3b9d6d](https://github.com/zhouxingxing1279/AcademicReaserch/commit/9882220234a20d730a38d648d5c08ac47c3b9d6d)，[PR #213](https://github.com/zhouxingxing1279/AcademicReaserch/pull/213) 已合并，合并前基线 8486cac。Git HTTPS 直连超时；通过 GitHub branches/main API 独立读到同一完整 SHA | 按该提交的树和隔离导出的源码认定主线成果，不以工作区文件是否位于 main 分支目录判断 |
| 主分支 CI | [push 运行 41798695579](https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41798695579) 对应精确 SHA，导航、17 项测试所在步骤、启动数学证书步骤均成功；[步骤记录](stage0_20261105/main_ci.json)。#213 的 PR head 48197929 对应[运行 41797415560](https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41797415560)，API 未列出正式提交的 review | 是已提交版本的 CI；不能充当当前工作区 CI 或独立数学审查 |
| 本地 | 唯一已检出工作树 main，HEAD、缓存 origin/main 与远端一致。审查开始时已有 **13 个已跟踪文件修改、284 个未跟踪文件**（排除本次证据目录），无暂存条目。另有本地分支 codex/cz-fixed-lag-local-20261104（与 main 同 SHA）、codex/cz-startup-predecessor-20261104（48197929） | [原始状态](stage0_20261105/initial_git_status.txt)、[审查前文件哈希](stage0_20261105/initial_file_manifest.json)。前者含采集时刚产生的 PR 快照一项，已从上述计数扣除。后者覆盖 docs/src/tests/experiments/configs/.github 的 333 个文件，非全盘备份 |
| 项目规则与归档 | 启动时工作树和 main 没有项目 AGENTS.md，本轮新增[仓库工作规范](../../AGENTS.md)。活动检查点只有[这一份](CURRENT_CHECKPOINT.md)。[归档索引](../../archive/legacy_planar_direct_control_20261103/ARCHIVE_INDEX.md)登记从旧活动路径移动 1,164 个文件；归档中有仅大小写不同的两个 checkpoint 路径 | 保留归档及原有修改；在 Windows 不批量暂存归档、不以其中一个文件覆盖另一个。Run246 的反例、Run260/261 的条件结果、Run278 的旧合同障碍均不外推到新外环 |

核查入口包括 [模型合同](MODEL_CONTRACT.md)、[理论框架](THEORY_FRAMEWORK.md)、[路线图](RESEARCH_MAP.md)、[模型选型矩阵](model_selection/MODEL_SELECTION_EVIDENCE.md)、[外环文献证据](model_selection/OUTER_LOOP_MPC_LITERATURE.md)、42 篇模型选型背景记录的目录、[唯一阅读总账](../literature/PAPER_READING_LOG.md)及[历史书目索引](../literature/READ_PAPERS.md)。本地 proposal 下的选题、理论、验证文件按时间和证据类型分开；未把全部历史文章重读或全部长实验重放记作本轮工作。旧检查点原字节保留为[只读历史快照](stage0_20261105/checkpoint_before_stage0.txt)，其中“下一步接口辨识”等旧指令不再生效。

## 2. 已完成的研究、算法与适用范围

**模型层级。** 活动理论变量为六状态 x=[p;v]，位置输出 Cₚ=[I₃ 0]，动力学为 x⁺=Ax+Bu+Gw，量测误差与扰动分别在给定有界集合内。一般模型的 B、G、采样周期和物理误差界尚未冻结，u 是抽象高层命令。十二状态 [p;v;姿态;角速度] 非线性刚体只是高保真对象；姿态、角速率、分配、电机由成熟飞控闭环。下表 ZOH 的 u 具有加速度量纲，不指定实际飞控输入。不以高斯置信区间充当硬扰动界，不将 SMF 与 EnKF 混称。

| 工作包／版本 | 文档、实现与已有结论 | 条件与缺口 |
|---|---|---|
| 六维启动门／main | [专题及证明](cz_startup_predecessor.md)、[有理数实现](../../src/outerloop/startup_gate.py)、[实验入口](../../experiments/cz_startup_predecessor.py)。给定同一历史的信息集 S，通过支持函数逐行消去隐藏状态和扰动，可求精确共同输入集 | S 非空紧、已知线性合同、未来扰动按 S×W；初始 S⊆X 单独检查。仅保证下一拍。一般 float64 [Box/Zonotope 工具](../../src/common/numerical_sets.py)不构成在线时间戳 CZ 滤波器 |
| 有限记忆估计／本地 | [限定模型推导 §§1–4](proposal/FINITE_MEMORY_THEORY.md)、[估计器](../../src/outerloop/finite_memory.py)。每轴已知 ZOH，G=B；完整位置包、最大连续未生成 M、生成后至多 L 拍必交付。通过已收时间戳和已施加输入重建窗口轨迹，在生成时刻约束相同噪声变量后投影至当前。最晚 Q=2M+L+1 时窗口内有两个不同时间戳，最新时间戳年龄至多 M+L；每轴生成元至多 2Q+1 | 启动不足两戳时传播已知紧先验；重复戳不作第二独立观测。不使用未交付队列。遗忘旧约束得到外包，非精确全历史后验。允许未生成、乱序和同拍多包，不允许任意永久丢失已生成包；不能直接推广为分轴异步传感或一般 G |
| 统一 Tube、收紧与终端／本地 | [同一推导 §§5–6](proposal/FINITE_MEMORY_THEORY.md)、[控制实现](../../src/outerloop/tube_mpc.py)。对固定增益 K、F=A+BK 且 F²=0，有显式两项 RPI 管；同一历史使用同一命令。固定名义状态记忆，构造跨模式共同终端集，在收紧非空、初始误差准入及初始名义可行时完成移位与终端代价下降 | 三轴独立、盒约束、数学算例、理想算术。持续扰动只保证真状态趋于管邻域；统一最坏相位界不等于指定恢复水平的相位 ER。仍无一般耦合系统、物理残差和浮点向外舍入认证。已有[候选方案](proposal/RESEARCH_PROPOSAL.md)未经本流程定题 |
| 抗扰与压缩试验／本地历史 | [抗扰报告](proposal/ROBUSTNESS_RESULTS.md)登记 226 条计划轨迹、37,770 分轴步，136 条合同内轨迹各项数值检查均通过。默认 M=L=1 时重新设计的严格正预算边界 a<82/1775；[压缩验证](proposal/CONG_MPC_VALIDATION_REPORT.md)在两个二维稳定模型、96 个配对场景、1,056 条轨迹中，控制贪心与同面数几何贪心的成本变化中位数均为 0% | 前者不是将固定 a=0.02 控制器的保证扩大，也不是系统最优界；后者未通过其定题门槛。两者均非本轮新增实验 |
| OIT/CZ/mRPI／本地历史 | [理论审计](proposal/OIT_MRPI_THEORY_AUDIT.md)、[验证报告](proposal/OIT_MRPI_VALIDATION_REPORT.md)、[代码与数据接口](../../src/oit_mrpi/README.md)。逐拍创新、固定观测器、联合估计与跟踪误差：越远预测步保留越少历史，利用窗口嵌套和固定 RPI 尾管移位 | 与间歇延迟窗不是同一合同。相对固定管的闭环代价下降中位数约 16.35%，相对只用当前已知偏差基线仅 **0.005449%**；详细 360 步均未满足 20 ms。另 10,000 条内部初值轨迹走快捷分支，不是 300,000 次受约束 QP 或实时证书 |
| 历史物理接入／本地失败证据 | [既有失败记录](../simulation/CZ_SITL_RESULTS.md)与[既有诊断记录](../simulation/INTERFACE_IDENTIFICATION_RESULTS.md)：4 次正式接入；3 次连续位置组 k=1 失包含、k=2 空后验；失测/延迟组 k=5 离开 Tube、k=23 越速度界 | 直接否定所试物理闭环与当时理想数学合同的等同。没有否定合同内数学推导。阶段 0 仅读取记录；本轮没有开展接口研究、SITL 或新控制器开发 |

## 3. 判据与尚未闭合的依赖

对 X={x:Hx≤h}，令 σ 为支持函数。主分支给出的每一行条件为

\[
 H_iBu\le h_i-\sigma_S(A^\top H_i^\top)-\sigma_W(G^\top H_i^\top).
\]

与 u∈U 联立后非空，等价于**存在一个** u 对**全部** (x,w)∈S×W 安全；理由是固定 u 后对每行取最坏值，产品合同使两项支持可分。若 S 是精确后验的外包，拒绝此外包不能推出真实后验无解。每个隐藏状态各自有安全输入，并不保证存在共同输入。Euler 与 ZOH 一步输入矩阵不同，不能合并其速度界。

| 顺序 | 可复用的数学事实 | 后续必须判定的命题（本阶段不推进） |
|---|---|---|
| 1. 时间戳与真值包含 | 初值、过程和量测界正确时，预测外包与正确历史状态的量测交集保留真实轨迹。有限记忆特例已给出连续噪声见证；图枚举仅检查离散时序 | 对拟选六状态合同给出可见历史、生成/交付/永久丢失的允许语言与充分先验。区分“未收到”与“不再交付”。无界信息陈旧或未包络的物理残差可破坏恢复；空集和数值未决需分开 |
| 2. Equalized Recovery | 特例有启动界及预热后摆脱初始速度半径的界；CZ 的代数中心一般不可行，任取可行代表点时两样本半径界需计因子 2 | 对每个可达起始相位、每个允许事件词及数据，证明中间包含、块末返回**指定**恢复界，或给出失败词。不能以某一有利词、图有限或统一最坏界替换相位收益 |
| 3. 因果 Tube | 估计误差 ε=x−x̂、跟踪误差 e=x−z 满足 x̂−z=e−ε。以 u=ū+K(x̂−z) 时 e⁺=(A+BK)e−BKε+Gw | 每条可见历史分支上给出误差传播与共同命令；估计后验本身不是未来跟踪管。若不同隐藏队列产生同一已收历史，在线策略不得分别选输入 |
| 4. 收紧 | 在 e∈Sᶜ、ε∈E 下，状态按 X⊖Sᶜ、输入按 U⊖K(Sᶜ⊕(−E)) 取保守充分条件 | 信息更新后所有可能后继的收紧还应容纳上一解的移位。当前集合缩小不等于未来管可移位，也不等于控制成本改善 |
| 5–6. 共同终端与递归可行 | 统一管特例已给出正不变终端集及代价恒等式；初始名义可行、终端反馈可执行并保持约束时才可移位 | 对前述**同一个**分支合同核验共同终端非空、所有相位终端输入、初始准入、移位和下降。一步门、安全预热、全时域可行互不等价。12 状态覆盖和数值实现保证是另外的义务 |

保留的反例包括：盒外包丢失位置–速度相关性造成虚假不可行；名义中心任意重置破坏移位；固定设计的扰动放大到 2 倍已有包含失败，4 倍起部分 CZ 空后验；[验证记录](proposal/VALIDATION.md)的 16 组参数中有 6 组未获正输入预算证书。对外包或充分条件的失败，记为“不获证”，不改写为物理不可行。

## 4. 现有文献与引用核查

总账按轮次组织，同一 DOI 可反复出现；章节数、DOI 出现数、PDF 数都不是去重已读论文数。早期 READ_PAPERS 已停止追加。本地[丛一睿专题](../literature/CONG_YIRUI_SET_MEMBERSHIP_PAPERS.md)是专项索引：主清单 13 篇，含 12 份有哈希的 PDF，第 9 篇按原记录未获取；本轮 12/12 文件校验匹配，未把哈希匹配当作全文精读。活动 docs 中未见统一 BibTeX 数据库。以下仅抽核已有关键引用，并注明本轮实际读到的层级。

| 既有文献 | 本轮证据 | 对当前判断的作用 |
|---|---|---|
| J. K. Scott, D. M. Raimondo, G. R. Marseglia, R. D. Braatz, *Constrained zonotopes: A new tool for set-based estimation and fault detection*, Automatica 69, 2016. [DOI](https://doi.org/10.1016/j.automatica.2016.02.036) | [作者站期刊 PDF](https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf)，Prop. 1，式 (11)–(13) | 线性像、和、广义交集有显式 CZ 表示；不赋予任意迟到量测历史或终端控制保证 |
| B. S. Rego, G. V. Raffo, J. K. Scott, D. M. Raimondo, *Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems*, Automatica, 2020. [DOI](https://doi.org/10.1016/j.automatica.2019.108614) | [作者稿摘要及关联 DOI](https://arxiv.org/abs/1908.09950)；总账另有正文分节记录 | 非线性预测需可靠包络，更新需有界误差；没有由此获得本项目的四旋翼残差界 |
| S. M. Hassaan, T. Pati, Q. Shen, S. Z. Yong, *Time-Varying Tube-Based Output Feedback MPC for Constrained Linear Systems with Intermittently Delayed Data*, IFAC-PapersOnLine, 2021. [DOI](https://doi.org/10.1016/j.ifacol.2021.08.482) | [作者稿](https://qiangs.github.io/Papers/Conf_Hassaan2021ADHS.pdf)，摘要、Assumptions 1–3 和 Thm. 6 的移位条件；DOI 网页本轮未返回正文 | 有限长度语言、ER、时变管与递归可行已有直接先例。需比对其动态估计器与本项目按戳条件化的 CZ，而非把整条框架称为原创 |
| F. D. Brunner, M. A. Müller, F. Allgöwer, *Enhancing Output-Feedback MPC With Set-Valued Moving Horizon Estimation*, IEEE TAC 63(9), 2018. [DOI](https://doi.org/10.1109/TAC.2018.2791899) | [作者单位题录与摘要](https://research.uni-hannover.de/en/publications/enhancing-output-feedback-mpc-with-set-valued-moving-horizon-esti/) | 对远端预测步使用较少历史量测以维持可行性已有先例。未逐定理比对，不能认定本地 OIT 窗口构造有新颖性 |
| T. Ji, J. Geng, K. Driggs-Campbell, *Robust Output Feedback MPC with Reduced Conservatism under Ellipsoidal Uncertainty*, IEEE CDC, 2022. [DOI](https://doi.org/10.1109/CDC51059.2022.9992704) | [作者稿](https://arxiv.org/pdf/2008.04980)，§V 的二维与十二状态数值算例；DOI 网页本轮未返回正文 | 椭球误差与输出反馈收紧已有四旋翼算例。其总推力/力矩输入与本项目六状态外环权限不同，不作为仅位置间歇输出的证明 |
| Y. Cong, X. Wang, X. Zhou, *Stability of Linear Set-Membership Filters With Respect to Initial Conditions: An Observation-Information Perspective*, Automatica 172, 2025. [DOI](https://doi.org/10.1016/j.automatica.2024.111993) | [作者预印本版本记录](https://arxiv.org/abs/2203.13966)和[本地 PDF 清单](../literature/sources/cong_mpc_20261104/manifest.json) | OIT 用于考察初始先验影响。逐量测传播后相交与共享历史扰动的轨迹窗口不是同一集合；估计稳定性不等于 MPC 移位 |

外环架构已有 Santos–Lagoa（[ISA Transactions](https://doi.org/10.1016/j.isatra.2021.12.002)）等线索；本轮沿用[仓库核验范围](model_selection/OUTER_LOOP_MPC_LITERATURE.md)，未获得该文逐式新证据。Elokda 等的[期刊论文](https://doi.org/10.1002/rnc.5686)在总账区分十二状态物理模型与厂商内环之上的外部输入；本轮 PMC 全文入口返回访问验证页，未提升阅读等级。以上抽查不是阶段 1 背景综述或阶段 2 系统检索。

## 5. 未合并工作与重复风险

GitHub open 查询与含 head SHA 的清单均返回 **44 个开放 PR，其中 7 个 draft**。完整编号、摘要、链接见[查询快照](stage0_20261105/github_open_prs.json)；精确 head、base、draft、审查及可合并性字段见[版本快照](stage0_20261105/open_pr_heads.json)。旧 [PR 分类](PR_TRIAGE_20261103.md)有用，但不是实时状态。

| 类别（编号不重复） | 已有工作及处置 |
|---|---|
| #196–205、#208–210、#212（14） | 有限窗速度界、信息年龄与生成/交付自动机、恢复和启动反例。优先复用下列四个 PR；#201/#203 的 nilpotent 或全成功性质不足以证明所有合法缺测词恢复。不得把这些分支的实验计入 main |
| #195、194、193、190、188、186、184、170、162、160（10） | 外环模型、隐藏延迟、接口与文献；部分证据已选择性写入主线文献文档。保留溯源，暂缓接口实施 |
| #192、189、187、185、182、178、175、173、171、169、167、164、161（13） | 合成十二状态、可观性、集合降阶、量测相位及其修正。#178 的标签已有纠错，#192 的有限数值重跑仍不是当前信息合同下的闭环证明 |
| #177、172、168、166、159、157、135（7） | 执行器权限、旧平面/带姿态量测条件的估计或终端证据。保留边界和反例，不直接移入活动模型 |

- [#208](https://github.com/zhouxingxing1279/AcademicReaserch/pull/208)（f5dea23e）区分最大连续未生成 M、最大交付延迟 L；候选界为最新戳年龄 ≤M+L、最近两已交付异戳间隔 ≤M+max(1,L)、预热 2M+L+1。其速度计算为 Euler 合同；不与 ZOH 证书拼接。
- [#209](https://github.com/zhouxingxing1279/AcademicReaserch/pull/209)（9235d321）用启动不可辨识说明最终恢复不能补救早先不安全；[#210](https://github.com/zhouxingxing1279/AcademicReaserch/pull/210)（455548e8）给一维 ZOH 对称盒的共同输入特例，#213 已独立覆盖相应特例。#208/209/210 快照均为 DIRTY（GitHub 合并冲突状态），不是建议合并。
- [#212](https://github.com/zhouxingxing1279/AcademicReaserch/pull/212)（261ac455，draft）给有条件两时间戳速度包络，不给 ER。另查到 closed-unmerged 的 #206、207、211、158：分别涉及交付与两戳、恢复量词、时间戳新鲜度、执行器预测。关闭不等于合并，某些思想可在后续版本重新出现。

## 6. 本轮验证与复现边界

Windows，Python 3.11.9；工作区 .venv 实测 NumPy 2.4.6、SciPy 1.17.1、OSQP 1.1.3、Matplotlib 3.11.2，与本地 requirements-research.txt 一致。main 的启动门只需 Python 标准库；归档测试未纳入活动测试计数。

| 本轮实际命令（python 为上述解释器） | 结果与原始日志 |
|---|---|
| 从已核实 SHA 用 git archive 导出 src、tests、experiments 到独立临时目录；在该目录运行 python -m unittest discover -s tests -v | [17/17 通过](stage0_20261105/main_tests.txt) |
| 同一隔离目录运行 python -m experiments.cz_startup_predecessor --check | [数学证书匹配](stage0_20261105/main_certificate.txt)：64 例（30 可行、34 不可行），8,976 个联合顶点；无重写证书 |
| 工作区运行 python -m unittest discover -s tests -v | [46/46 通过](stage0_20261105/local_tests.txt)：同一组启动门 17，有限记忆 11，抗扰 4，压缩 3，OIT/mRPI 11。**不能将 17 与 46 相加** |
| 工作区运行 python -m experiments.finite_memory_certificate --check | [证书匹配](stage0_20261105/local_finite_memory_certificate.txt)：328 个端点组合；默认 E 半径 (2/25,9/100)，输入裕量扣除量 121/50，共同终端内接盒半径 79/350。这里只复核默认证书 |
| 对已存原始文件计算 SHA-256（仅读取） | [对照明细](stage0_20261105/hash_checks.json)：丛氏专题 12/12、OIT manifest 已列项 53/53 匹配。有限记忆运行记录的 4 个源码中 3 个字节匹配；experiments/finite_memory_tube.py 原始 e0756387…，仅把 CRLF 规范化为 LF 后即匹配存档 d665f39e…。未改写源文件。OIT 早期运行时哈希未包含传递依赖 finite_memory.py |

26 组/6,240 分轴步、226 条抗扰轨迹、1,056 条压缩轨迹、OIT 的 10,000 条轨迹和工程接入数据，均为**本地历史数据**。本轮未运行这些长实验，亦未重建任何仿真数据、修改模型、标准或种子。浮点测试不是精确包含证明；两组代数证书也不覆盖硬件或全部参数。

## 7. 交付、验收与后续顺序

| 阶段 0 验收项 | 本次交付 |
|---|---|
| 项目状态、已完成与未解决清单 | 本报告 §§1–3：分版本、分合同，逐链列出成果、未证命题及反例 |
| 研究任务依赖 | §3 给出数学依赖；[工作规范](../../AGENTS.md)规定项目阶段 0→10 及各阶段准出条件。理论 Gate T1–T7 是技术依赖，不等同于用户阶段验收 |
| 文献与未合并工作 | §§4–5：实际阅读等级、近邻、重复风险、全部开放 PR 和 closed-unmerged 线索 |
| 测试、文件与失败 | §6、[审查证据目录](stage0_20261105/)；新增本报告、仓库规范和审查快照/日志，更新统一检查点、README 与路线图的导航，以及文献总账的核验指针。未变更算法、测试、CI 配置或原始实验 |
| 统一恢复入口 | [CURRENT_CHECKPOINT.md](CURRENT_CHECKPOINT.md)记录版本、假设、证明状态、失败、实跑结果及唯一下一步；不以历史 proposal 当作已批准课题 |

**验收判断：阶段 0 的现状审查条件已满足，签收权在用户。** 若获确认，阶段 1 的唯一首项是基于既有总账建立“量测时序—可用信息—估计误差保证—可移位收紧”技术路线对照，以 Hassaan、Scott/Rego、Brunner 和直接四旋翼外环文献为起点，扩展到规定的八类背景；标明依据和未核实处。再按顺序进入系统文献库与横向比较（2–3）、用户定题（4）、模型与理论（5–6）、算法与独立十二状态仿真（7–8）；工程验证（9）另行授权，最后整理论文（10）。本次停在阶段 0。
