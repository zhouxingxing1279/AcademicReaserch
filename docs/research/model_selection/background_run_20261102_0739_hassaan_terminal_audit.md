# 背景第14轮：周期有限语言Tube MPC共同终端基线与六状态选型审计（2026-11-02 07:39 UTC）

## 1. 仓库冻结基准与任务边界
- 本轮从远端main \`3362a67c3ccff95eebd5248064453bf13cba84db\` 建独立分支 \`research/model-background-20261102-0739-hassaan-terminal\`，读取 \`docs/research/CURRENT_CHECKPOINT.md\`、\`docs/literature/PAPER_READING_LOG.md\`、模型矩阵、背景第13轮、Run246和Run260研究日志及 \`configs/planar_baseline.json\`、\`docs/research/01_model_and_bounds.md\`；对比最近main提交/背景记录，避免覆盖主研究任务。
- 主任务Run260：第45拍SMM/MMS两类**特定零读数历史**的可靠外包，使用相同实际 \`T=9.81N,tau=0\`，已认证第45–60拍16个盒的有限硬安全；PR #103/#104及main CI记录见检查点。**没有**证明第60拍所有非空后验进入共同终端信息状态、无限递归可行或稳定。Run246有真实可达而不可恢复终点的严格反例，故不能把有限安全桥当作终端。
- 本背景任务只新增文献/模型证据，不改主任务检查点、MPC、SMF、配置、验证脚本或结果JSON。

## 2. 本轮实际阅读论文（已在统一总账，不重复计数）
**Syed M. Hassaan, Tarun Pati, Qiang Shen, Sze Zheng Yong (2021)**, *Time-Varying Tube-Based Output Feedback MPC for Constrained Linear Systems with Intermittently Delayed Data*, *IFAC-PapersOnLine* 54(5):103–108，DOI https://doi.org/10.1016/j.ifacol.2021.08.482 ，作者PDF https://qiangs.github.io/Papers/Conf_Hassaan2021ADHS.pdf 。

**阅读状态/范围**：2026-11-02，作者公开PDF pp.1–6分节复读：§2.2 (1)、Definition 1/3、§3.1 (2)–(19)、Lemma 4、Theorems 5–7、§3.2 Assumptions 1–3、§4仿真；未独立重证全部定理，也未核验出版排版差异。

**模型、输入、测量和扰动**：一般有界扰动离散LTV \`x+=A_k x+B_k u+W_k w\`，带有界噪声的时间戳输出 \`z=C_k x+V_k v\`，周期固定长度的延迟/缺测语言；§4实际为2状态1输入双积分器 \`A=[[1,1],[0,1]],B=[1,1]^T,C=[1,1]\`，\`w∈[-0.05,0.05]^2,v∈[-0.01,0.01]\`；状态硬盒 \`[-50,3]^2\`，输入硬界 \`[-3,3]\`，\`T_d=5,T_p=13\`。部分输出延迟1拍、部分缺失，只有数值仿真；无四旋翼、物理总推力/力矩、执行器动态或20ms WCET。状态估计为**点估计加有界hyperbox误差管**，不是测量条带交集的精确状态SMF/CZ，也不是参数SMF。

**关键假设/理论保证**：
1. (12) \`x-hat{x}∈S^e_phase\`、(18) \`x-bar{x}∈S^c_phase\` 必须通过因果动态观测器/跟踪控制器的equalized recovery先得到（Assumption 1）。
2. Theorem 5用(19b,c)的 \`X⊖S^c_phase\` 和输入Pontryagin收紧给出原始**硬状态/输入约束**，前提是优化递归可行且误差管成立；不是单独对任意系统的保证。
3. Assumption 2需要**一个跨全部周期相位均满足收紧约束**的共同 \`X_f,K_f\`，Theorem 6在初始可行时用旧解移位保证MPC递归可行；这不是“存在终端集合”的无条件定理。
4. Theorem 7另要求Assumption 3终端代价下降，结论是**到扰动决定的有界集合的鲁棒指数稳定**，不是对原点的零误差收敛。
5. §4数值例的语言每拍可观测并容许延迟/缺失，与本仓库仅每5拍有位置机会、姿态每拍测、最多连续2次位置miss的合同不同；论文误差tube为hyperbox，可能丢失Run257–259证明重要的p-v关联。

**可复用/创新边界**：最坏相位共同终端、阶段性误差管、估计误差与跟踪误差分离、收紧约束及移位论证可作为**直接竞争基线**。因此“有限失测语言+时变tube+共同终端移位”不是本项目可独占的创新；若要研究CZ关联后验或mode-indexed终端，须与该基线在相同硬合同/计算预算下比较，证明严格收益且不牺牲安全。

**另行书目/摘要核验（不记作全文已读）**：Huiping Li, Yang Shi (2013), *Output feedback predictive control for constrained linear systems with intermittent measurements*, *Systems & Control Letters* 62(4):345–354, DOI https://doi.org/10.1016/j.sysconle.2013.01.003；公开可核验摘要称periodical measurement losses、外扰、观测器误差界、约束收紧、迭代可行及稳定性。未取得可核验全文；不猜状态维数、最大丢包数、具体定理或仿真。来源 https://www.researchgate.net/publication/257012483_Output_feedback_predictive_control_for_constrained_linear_systems_with_intermittent_measurements 。

## 3. 独立模型方程、自动机和物理闭合检查
- 仓库平面六状态 \`(px,pz,vx,vz,phi,omega)\`、实际输入 \`(T,tau)\`，名义连续加速度 \`ax=-T sin(phi)/m\`、\`az=T cos(phi)/m-g\`；\`m=1,J=0.02,h=0.02\`，\`T∈[4.905,14.715]N,|tau|≤0.08Nm\`。残差上界随实际T变化，不能直接替换为论文常数W；固定T=mg的4状态模型非零倾角下 \`az=g(cos(phi)-1)<0\`，没有垂向物理闭合。Run246的真实非可生存反例仍是终端集合的必要筛选。
- \`configs/planar_baseline.json\` 原有15模式图（5拍周期×最多连续2次miss）；每3个位置机会的8种S/M词中，仅MMM被禁止，余7种合法。独立标准库验证：\`python - <<'PY'\`、\`from itertools import product; W=[''.join(p) for p in product('SM',repeat=3) if p!=('M','M','M')]; assert len(W)==7 and 'MMM' not in W; assert all('S' in w for w in W); assert 5*3==15; print(W)\`、\`PY\`，**3/3断言通过**；打印 \`SSS,SSM,SMS,SMM,MSS,MSM,MMS\`。这是对已有自动机的**组合审计**，不是新增控制验证脚本/论文结果。
- 待检验的最坏相位共同终端必要接口：对全部合法 \`(phase,mode)\`，先可靠构造 \`S^e,S^c\`，再验证 \`X_f⊆⋂(X⊖S^c)\`、\`K_f X_f⊆⋂ U_{\mathrm{tight}}\`，并要求 \`X_f\` 对名义终端动力学闭合。对六状态非线性/推力相关扰动，这些只是**候选证明义务**，并非已存在的集合/增益或可用线性Kf定理。

## 4. 选型决策与下一轮
- **条件性物理首选**：平面6状态、实际 \`T,tau\`；优点是垂向闭合，代价是两轴隐藏速度、共享推力、失测和终端非空性，**尚无递归可行/稳定性证书**。
- **保留**：4状态有限安全SMF+MPC及Run246负面基线；2状态姿态低风险保底。10/12状态暂不扩维；分层架构需另证内环误差和物理输入映射。
- 可行性：中低（无限硬安全合同），创新性：中（已有直接近邻），硕士工作量：中高至高；建议先完成可复现的有限时域安全保证，再以终端信息闭合是否可证决定是否升级主张。**Gate A blocked**。
- **下一轮唯一优先问题**：以Run260第60拍全部非空有噪后验为起点，检查最坏相位共同终端 \`X_f,K_f\` 在实际 \`T,tau\` 和推力相关残差下是否非空/可移位；优先定位失败约束，不并行造新控制器。

## 5. 本轮提交/测试状态
- 本日志、证据矩阵、统一论文总账为文档增量；未运行主任务闭环回归，未声称CI或终端证明。GitHub PR/main/CI结果在完成合并与复核后单独记录，不提前宣称成功。
