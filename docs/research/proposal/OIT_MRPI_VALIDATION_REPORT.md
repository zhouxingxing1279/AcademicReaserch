# OIT、Constrained Zonotope 与 mRPI / Tube MPC 验证报告

日期：2026-11-05。数据目录：`experiments/results/oit_mrpi_20261105`。本次续接先检查已完成操作，确认七个实验阶段、11 项单元测试和八组图表已有记录；未重复执行数值实验。续接工作为核对原始结果、补齐交付说明和汇总报告。

## 1. 科研结论

**这条数学连接可以成立，但本轮证据不足以支持“提出了性能显著更好的新型 OIT-CZ adaptive Tube MPC”。** 在明确的线性系统、固定后验观测器、正确噪声界和初始准入条件下，联合估计—跟踪误差的有限窗口条件化能够与 RPI 尾管连接，递归可行性的移位证明可以闭合。该结论是本轮实现的适用条件，不是首创声明。

决定研究方向的关键结果是强基线对照：OIT-CZ 相对固定 RPI 管的闭环代价下降中位数为 **16.3463%**，相对只利用当前已知偏差 `d = hat_x - z` 的控制器，额外下降中位数仅 **0.005449%**。本例中，大部分相对固定管的控制收益来自当前已知信息；历史创新约束虽能继续缩小不确定集，却没有转化为相称的闭环收益。OIT-CZ 单步耗时中位数 **30.3209 ms**，360 个详细测试步均未达到 20 ms 预算。

| 控制器 / 对照 | 775 个网格点中的可行点数 | 单步耗时中位数 / p95 | 本轮闭环保证与实验范围 |
|---|---:|---:|---|
| 固定联合 RPI 管 | 459 | 0.0359 / 0.5243 ms | 固定管移位证明；12 条详细轨迹 |
| 只用当前已知 d | 535 | 8.8730 / 10.9168 ms | 当前层切片、未来固定管；独立移位证明；12 条详细轨迹 |
| 同历史普通 zonotope 外包 | 545 | 不作同口径闭环计时比较 | 同信息集合与冻结信息切片可行域对照；未证明该降阶算法的完整递归可行性 |
| OIT-CZ 相容窗口管 | 549 | 30.3209 / 37.5783 ms | 本报告的窗口移位合同；12 条详细轨迹及 10,000 条快捷分支轨迹 |

可行点数相对固定管增加 19.61%，相对当前已知 d 基线增加 2.62%，相对普通 zonotope 增加 0.734%。这些数值是固定信息切片上的网格计数，不能称为精确可行域体积或闭环成功概率。

**建议保留为可复现的研究原型和理论审计，暂不按“已有显著优势的新 MPC 方法”组织投稿。** 继续发展需要先证明相对近邻文献的具体差异，并在当前已知 d、同历史普通集合估计器和相同计算预算下找到可重复的增量收益。仅仅把 mRPI 写成 CZ，或在 MPC 前端接入 OIT，不足以构成已验证的创新。

## 2. 已完成内容及验收边界

| 任务书要求 | 结果 | 边界或未达到项 |
|---|---|---|
| 统一系统、CZ、MPC 配置与集合运算接口 | 已实现 | 普通有限 CZ 有界；一般 CZ 包含采用充分证书，求解失败返回 uncertified |
| 命题 A–D：证明、反例、数值检查 | 已完成受限命题的推导与实现 | C 的学习限于固定未知偏置加有界残差；D 限于固定集合证书及固定模板比例综合 |
| 六条算法路线 | 已实现，并额外加入有限和加认证尾项 | 静态测试的扰动是 zonotope，纯线性映射和 Minkowski 和不生成 CZ 等式约束；不能据此宣称静态 CZ 独有优势 |
| 二维、弱稳定、4/8/16/32 维、弱可观性测试 | 已完成所述基准 | 高维仅为规定的实稳定极点族和静态集合计算；没有高维闭环推广结论 |
| RPI 包含检查 | 40 个带解析 / LP 证书案例通过采样方向检查；二维另查全部多边形面 | 20 个有限截断案例是参考或消融，不标为 RPI；采样方向本身不构成完整证明 |
| 二维 / 四维 support error < 1e-3 | Raković 与有限和加尾项两条精度路线均通过 | 低复杂度迭代和固定方向 one-step 多个案例不达标，保留原始结果 |
| 至少 10,000 条轨迹无约束违反 | 10,000 × 30 = 300,000 次状态转移，记录零违反 | 内部初值、零初始误差、全部采用经可行性检查的无约束最优解；不能替代边界 / 实时性压力测试或解析证明 |
| 各时刻状态、控制、估计集和管束 | 已保存或可无损重构 | 10,000 条轨迹用模板、创新与已知 d 序列重构集合，未重复存储大量相同矩阵 |
| 八类图表 | 8 PNG + 8 SVG | 窗口图为外包多边形面积；可行域图为网格计数，均明确标注；高维精确体积 / Hausdorff 未计算 |
| 论文二维可观示例 | 复现 Eq. (25) 模型、无界边界先验窗口选项及 literal OIT 对照 | 新随机记录；不等于原作者所有图、全部 detectable 分支或 CORA 时间复现 |
| 同计算预算优势 | **未达到** | OIT-CZ 详细闭环 0% 步满足 20 ms；经验最大 53.4213 ms，不能声称 50 ms 硬实时 |
| 论文新颖性 | **尚未确立** | Brunner 2018 的有限窗口输出反馈 MPC 尤其接近，仍需完整逐定理比较 |

详细推导见 [理论审计](D:/WorkSpace/AcademicReaserch/docs/research/proposal/OIT_MRPI_THEORY_AUDIT.md)，实验前的冻结条件见 [验证计划](D:/WorkSpace/AcademicReaserch/docs/research/proposal/OIT_MRPI_VALIDATION_PLAN.md)。浮点 LP/QP 证书做了残差核验，未采用区间向外舍入，因此不应称为机器形式化证明。

## 3. 命题 A–D 的判断

### A：batch reduction 在什么条件下支配 sequential reduction？

若同一个集合算子 R 同时满足外包性和集合单调性，则

\[
S_N\subseteq R(S_N)\subseteq Z_N^{\rm seq}.
\]

证明由有限可达集与递推外包的包含归纳得到，不需要幂等性。固定坐标盒或固定可逆基的盒外包满足条件；随输入几何或生成元数量切换规则不自动满足。

去掉单调性时，二维反例已找到并用有理数独立复算：

\[
F=\begin{bmatrix}-3/5&2/5\\1/2&3/5\end{bmatrix},\qquad
D=\begin{bmatrix}-1/10&-1/10\\0&3/10\end{bmatrix},\qquad N=4.
\]

其中 \(F^2=(14/25)I\)，故严格 Schur 稳定。降阶规则在 \(h_Z(e_1)\le0.7\) 时使用轴对齐盒，否则使用基 \(\begin{bmatrix}1&1\\1&-1\end{bmatrix}\) 的盒外包。方向 \(q=(1/2,1/2)\) 上，batch 相对 sequential 的支持值差精确为 **247/2500 = 0.0988 > 0**，因此普遍包含命题为假。另有 1,600 个固定盒单调降阶比较通过。

这给出了明确条件和反例，但单调版本是直接的集合算子推论，不能单独包装为新的 mRPI 理论。有限 batch reach 本身也不自动成为 RPI。

### B：管束安全与递归可行性

任务书的归纳安全结论对真实误差系统 \(e^+=Fe+w\) 成立。输出反馈实际采用 \(u=v+K(\hat x-z)\)，必须保留估计误差；直接套用状态反馈误差式会漏项。

本轮定义 \(\eta=(\varepsilon,d)\)，\(\varepsilon=x-\hat x\)、\(d=\hat x-z\)，采用后验观测器，得到

\[
\eta^+=\underbrace{\begin{bmatrix}(I-LC)A&0\\LCA&A+BK\end{bmatrix}}_{\mathcal A}\eta+
\begin{bmatrix}(I-LC)B_w&-L\\LCB_w&L\end{bmatrix}\begin{bmatrix}w\\v_{\rm noise}\end{bmatrix}.
\]

测量和过程噪声在两个误差块中共享，创新等式在同一组潜变量上条件化。设 S 为联合误差 RPI 外包，\(J_k^m\) 为从历史边界 \(S\cap\{d=d_{k-m}\}\) 开始的 m 步相容创新集合；启动期截断到时刻 0。在初始误差属于 S 时，\(J_k^{m+1}\subseteq J_k^m\subseteq S\)。

预测管采用逐步减少历史信息的结构：

\[
P_{i|k}=\begin{cases}
\mathcal A^iJ_k^{\ell-i}\oplus\mathcal R_i(\mathcal A,\mathcal W),&i<\ell,\\
S,&i\ge\ell.
\end{cases}
\]

由共同历史边界、新增创新等式和 S 不变性，可得到

\[
\mathcal A P_{i|k}\oplus\mathcal W\subseteq P_{i+1|k},\qquad
P_{i|k+1}\subseteq P_{i+1|k}.
\]

名义中心连续传播，不随量测重置；配合同一个终端不变集和终端 Lyapunov 代价，上一拍最优序列移位后仍可行。前提包括模型与噪声界正确、初始误差准入、初始 MPC 可行、固定 K/L，以及数学上精确的集合运算。结论是名义收敛及真实状态有界于误差管，并非持续扰动下真实状态趋于原点。

新后验与旧预测取并集的外包无法比旧预测更紧，也不会自动建立移位证明。本文窗口构造与既有 moving-horizon output-feedback MPC 的联系须在新颖性判断中正面处理。

### C：嵌套扰动与扰动学习

对固定 Schur F，\(W_1\subseteq W_2\) 推出精确 mRPI 的同向包含。这不自动保证不同数值外包嵌套，也不保证缩小的新管能立即容纳已存在的误差。

任意有界扰动的过去实现值不能约束未来支撑集：在 \(W=[-1,1]\) 下，过去 \(w_0=0\) 与未来 \(w_1=1\) 完全相容。把过去后验 \(\{0\}\) 当作未来噪声界不安全。

已实现的合法学习示例假设跨时刻共享固定偏置 \(q_k=b+\epsilon_k\)。用 \(b=0.12\)、残差界 0.02、观测误差界 0.005 验证参数区间递推相交及对应未来扰动集嵌套。它不是任意扰动支撑学习，也未被混入主要 MPC 对照。

### D：CZ 的 affine-decision-rule RPI 条件

已推导固定 Z/W 的仿射潜变量映射、目标等式条件及源集合支持函数的对偶上界，得到充分 LP。实现独立检查返回的几何等式、目标等式及系数盒界，并做 5,000 个可行潜变量后继检查。LP 不可行仅表示该证书未获得，不表示真实集合包含为假。

额外实现固定 CZ 模板的同心比例综合，避免把 G、等式约束和仿射映射同时优化形成的双线性误称为 LP。对 \(F=0.5I\)、\(W=0.5\operatorname{conv}\{(0,0),(1,0),(0,1)\}\)，三角形模板最优缩放为 1，面积 0.5；删除模板等式的方形对照缩放为 1，面积 1。该例只证明保留等式约束的表示价值，不能推出对最优普通 zonotope 的普遍面积优势。

另两项修正：RPI 是 \(FS\oplus W\subseteq S\) 的后不动点条件；若外包降阶算子确有精确固定点 \(Z=R(FZ\oplus W)\)，该 Z 自动为 RPI。难点是有限次停止、数值误差与收敛，而非精确固定点仍缺少不变性。

## 4. 数值结果及解释

### 静态 mRPI / RPI 基准

系统为任务书双积分器的 LQR 与弱极点 (0.90, 0.95) 两例，加上 n=4/8/16/32、rho=0.7/0.95 的八个生成系统。生成族使用不同实稳定极点的正交相似变换，观测矩阵数值上均满可观秩；不能代表全部稳定系统，尤其不覆盖一般非正规动力学。

共 10 系统 × 6 方法 = 60 个静态案例，无执行失败。其中 40 个有 RPI 证书；12 步截断和长截断参考共 20 个只作为有限可达集。参考尾项无穷范数界小于 1e-9；二维进行显式多边形计算，高维使用隐式有限 Minkowski 和的支持函数。

| 系统 | Raković support error | batch + 认证尾项 support error | 1e-3 目标 |
|---|---:|---:|---|
| 二维 LQR | 1.9561e-4 | 1.0990e-4 | 两者通过 |
| 二维弱稳定 | 2.6220e-4 | 1.9111e-4 | 两者通过 |
| 四维 rho=0.7 | 2.7648e-4 | 3.5722e-4 | 两者通过 |
| 四维 rho=0.95 | 3.4225e-4 | 1.4997e-4 | 两者通过 |

原扰动在状态空间是线段，Raković 路线使用显式小盒正则化，并把正则化误差纳入预算。冻结计划中提出的“满维分组扰动”在实施时改为这一路线：分组条件本身通常只直接支持多步不变性；修正并非根据性能结果调参。完整公式与尾项证书见理论审计及 static.json。

保留的负结果：弱稳定系统的 12 步截断 support error=7.85791，采样不变性残差=+0.258543，明确不通过；LQR 的截断误差虽仅约 1.52e-7，仍不能据此标为 RPI。固定方向 one-step 的误差在 LQR / 弱稳定例分别为 0.0014069 / 0.536307；粗迭代外包分别为 0.698761 / 19.1045。它们可有不变性而不满足精度目标。

二维 Hausdorff 使用凸多边形双向顶点到集合距离，未用有限方向支持误差冒充：batch+尾项在 LQR / 弱稳定例分别为 1.0990e-4 / 1.9111e-4；高维该字段为 null 并注明原因。二维结果指向有限参考；若要对精确无限和陈述欧氏误差，可再加 \(\sqrt{2}\) 倍参考尾项无穷范数界。

固定尾项界 1e-5 的半径扫描中，rho=0.5/0.7/0.9/0.95/0.98 分别需要截断长度 **14/28/103/225/616**。这支持慢收缩系统需要更长历史的判断，不建立 CZ 独有的计算优势。

### 论文可观示例与相同信息对照

采用论文 Eq. (25) 的 W=V=[-1,1]、真实初始集合 [1,3]^2 和实现初值 (2,2)，使用新固定种子记录。完整历史、递推 interval hull、literal OIT 和窗口 CZ 分别计算。窗口轨迹一致集保留共享历史扰动；它包含于分别传播各量测再相交的 literal OIT，已检查 literal OIT 的全部定义面。

本条记录所有已记录估计集均包含真实轨迹；**没有观察到空集**。特别是 David 的初始集合 [-2,2]^2 虽不包含整个 [1,3]^2，却包含实际初值 (2,2)。因此本条记录不能证明错误初始集合下的有限时间恢复或启动安全，不能把交接摘要中“可能变空”的理论风险误报为已发生事件。

固定记录的窗口外包多边形面积从窗口 1 的 6.0000，降到窗口 2 的 3.5660；窗口 6 后约为 3.5297，显示该记录较早出现收益平台。弱可观性扫描把 C 缩放为 1/0.3/0.1/0.03 倍并固定实际测量噪声界，区间外包面积约为 6.61/46.64/211.67/1613.52。

相同创新序列、窗口 3、一步预测下，加入共同的下一步过程与测量噪声后，OIT-CZ 的半宽下降中位数为：

| 方向 | 相对固定管 | 相对当前已知 d 切片 | 相对普通 zonotope |
|---|---:|---:|---:|
| 位置 | 61.72% | 8.76% | 29.49% |
| 速度 | 46.18% | 10.70% | 17.80% |
| 输入 | 15.49% | 6.42% | 22.99% |

此表取 audit.json 的 `full_one_step_width_improvements`。原 matched CSV 和图 02 显示的是初始集合传播贡献，未加共同未来噪声，两种比例不可混用。普通 zonotope 为同历史最小二乘外包更新，不代表最佳可能的普通 zonotope 算法。

同信息比较最大 142 个生成系数和 8 条等式，低于声明的 256 上限。窗口 3 的七层完整支持查询任务中，OIT-CZ 耗时中位数 134.6341 ms，当前 d 切片 115.4252 ms，普通 zonotope 0.3275 ms，固定集 0.0826 ms。每个时刻的同一次任务耗时在多个方向记录中重复出现，这些行不是独立计时样本；该工作量也不同于前表闭环所需的支持查询量。

### 闭环对照和 Monte Carlo

控制基准为 A=[[1,1],[0,1]]、B=Bw=[[0.5],[1]]、C=[[1,0]]，过程扰动幅值 0.05、量测噪声幅值 0.10，X=[-5,5]×[-3,3]、U=[-1,1]，Q=I、R=0.1、N=15、主窗口=3。K 约为 [-0.61669526,-1.27031633]，L=[0.7075,0.1925]，全精度矩阵和终端集合保存在 controller.json。联合误差 S 使用有限和加认证尾项；终端集合 8 个面，在第 1 层闭合。

详细配对实验为 12 个外生噪声记录 × 30 步 × 3 控制器，共 36 次运行 / 1080 步。初始名义状态循环取 (3.8,0)、(-3.8,0)、(1.5,1)、(-1.5,-1)，实际状态、估计点与名义点初始相同。包含两个端点 / 交替噪声记录和十个随机记录。没有记录到包含、约束或移位失败。

真实状态累计代价为 \(\sum_{k=0}^{29}(x_k^\top x_k+0.1u_k^2)\)。配对下降中位数相对固定管为 16.3463%，范围 6.8288%–27.0289%；相对当前已知 d 基线为 0.005449%，最大仅 0.044875%。这 12 个记录不是对全部系统的统计总体推断；30 个相邻时刻也不是 30 个独立重复。

计时只包括管构造、支持查询和 MPC 求解，不含额外审计及文件写入；固定 / 当前 d / OIT-CZ 三组分别发生 24/24/25 次 QP 求解，其余采用经可行性检查的无约束最优解。OIT-CZ 最大耗时 53.4213 ms，99.7222% 步不超过 50 ms，0% 步不超过 20 ms。这是单机经验计时，无 WCET 保证。

独立的 10,000 条 Monte Carlo 轨迹每条 30 步，初始名义点在 [-0.8,0.8]×[-0.25,0.25] 均匀采样，初始误差为零。保存实际 / 名义 / 估计状态、控制、噪声和创新，直接数组审计得到：

- 约束失败数 0，最大带符号约束残差 -0.19568893；
- 最大计划残差 -0.0002522643，最大移位残差 -0.40490200；
- 显式联合动力学最大残差 2.0123e-16；
- 300,000 步均使用经检查可行的无约束全局最优解，在线 QP 求解数为 0；
- 140 个初始计划未通过固定管快捷条件，随后按真实自适应约束检查均通过；初始历史和 d 相同，实际只需构造 1 次不同的自适应管。

初版快捷程序曾在这 140 个计划处停止，后来补充真实自适应分支。未改初始状态或噪声种子、未删除困难记录。这是快捷条件不满足导致的开发中断，不是物理约束违反。该大样本结果验证允许使用快捷分支时的轨迹行为，**没有测试 300,000 次昂贵 CZ/受约束 QP 求解**。

## 5. 与已有工作的关系及下一步决策

Cong、Wang、Zhou 已给出 OIT 和 OIT-CZ 集合滤波；本文采用其可观情形允许的无界窗口边界先验思路，并单独计算 literal OIT，不能把这些内容列为新贡献。[原论文作者稿](https://arxiv.org/abs/2203.13966)

Raković 的有限和缩放 RPI 外逼近，以及 Raghuraman–Koeln 的固定生成方向 zonotope RPI 条件，构成直接基线。后者的 RPI 章节不能被泛称为“一般 CZ 最优形状综合”。[Raković 2005](https://doi.org/10.1109/TAC.2005.843854)、[Raghuraman–Koeln，Section 7 / Theorem 23](https://arxiv.org/html/2009.06039v1)

Brunner 等的 set-valued moving horizon output-feedback MPC 已研究在较远预测步保留更少量测以及有限复杂度、递归可行性。本轮逐步遗忘窗口的证明结构与其非常接近。已核对机构摘要，完整逐定理、信息结构和复杂度比较尚未完成；不能据此排除重复。[出版论文](https://doi.org/10.1109/TAC.2018.2791899)、[机构出版记录](https://research.uni-hannover.de/en/publications/enhancing-output-feedback-mpc-with-set-valued-moving-horizon-esti/)

联合输出反馈误差减少保守性也有已有研究；已有标题明确为 CZ Tube MPC 的工作。前者作者稿已查，后者本轮证据为题录 / 摘要，尚未独立完成全文定理审计。[Ji 等作者稿](https://arxiv.org/abs/2008.04980)、[Andrade 等 2024](https://doi.org/10.1109/ACCESS.2024.3381622)

| 方向 | 本轮决策 | 继续前需要解决的具体问题 |
|---|---|---|
| OIT-informed adaptive Tube MPC | 保留原型；暂缓主张性能型新方法 | 与 Brunner 逐定理比较；同信息、同预算的强基线；找出历史约束持续影响活跃控制约束的条件 |
| finite-window / batch mRPI | 作为算法组件与对照保留 | 单调包含证明太直接；还需新的误差—复杂度结果，并与现有尾项和降阶方法比较 |
| direct CZ-RPI synthesis | 作为条件性探索方向保留 | 固定模板例不足以证明综合优势；需公平的方向 / 形状优化对照与非中心对称扰动族 |
| 在线学习扰动集合 | 仅在显式共享参数假设下推进 | 不能从任意历史扰动后验推出未来支撑缩小；需完整参数辨识和新管准入合同 |

后续实验应另行冻结假设和比较规则，保留本轮负结果。不将增大窗口、替换系统或挑选初值后得到的收益回填为本轮结论。

## 6. 交付索引与复现

| 内容 | 文件 |
|---|---|
| 数学推导、前提、反例、控制合同 | [OIT_MRPI_THEORY_AUDIT.md](D:/WorkSpace/AcademicReaserch/docs/research/proposal/OIT_MRPI_THEORY_AUDIT.md) |
| 接口与数据使用说明 | [src/oit_mrpi/README.md](D:/WorkSpace/AcademicReaserch/src/oit_mrpi/README.md) |
| 集合、RPI、估计、控制实现 | [sets.py](D:/WorkSpace/AcademicReaserch/src/oit_mrpi/sets.py)、[rpi.py](D:/WorkSpace/AcademicReaserch/src/oit_mrpi/rpi.py)、[estimation.py](D:/WorkSpace/AcademicReaserch/src/oit_mrpi/estimation.py)、[control.py](D:/WorkSpace/AcademicReaserch/src/oit_mrpi/control.py) |
| 独立已保存结果审计 | [audit.json](D:/WorkSpace/AcademicReaserch/experiments/results/oit_mrpi_20261105/audit.json) |
| 代码与数据校验值 | [manifest.json](D:/WorkSpace/AcademicReaserch/experiments/results/oit_mrpi_20261105/manifest.json) |
| 任务书统一字段索引 | [delivery_records.csv](D:/WorkSpace/AcademicReaserch/experiments/results/oit_mrpi_20261105/delivery_records.csv)、[JSON 与映射说明](D:/WorkSpace/AcademicReaserch/experiments/results/oit_mrpi_20261105/delivery_records.json) |
| 静态精度与失败保留 | [static_sets.csv](D:/WorkSpace/AcademicReaserch/experiments/results/oit_mrpi_20261105/static_sets.csv) |
| 配对闭环逐步数据 | [closedloop_detailed.csv](D:/WorkSpace/AcademicReaserch/experiments/results/oit_mrpi_20261105/closedloop_detailed.csv) |
| 10,000 条轨迹及集合重构输入 | [monte_carlo_10000.npz](D:/WorkSpace/AcademicReaserch/experiments/results/oit_mrpi_20261105/monte_carlo_10000.npz) |

八组图表依次为：01 二维集合叠加；02 OIT 与静态管的不确定性；03 二维多边形 Hausdorff—耗时；04 生成元—时间；05 维数—耗时；06 窗口外包面积及弱可观性；07 半径—截断长度；08 冻结信息下可行网格。

![四种方法的可行网格比较](D:/WorkSpace/AcademicReaserch/experiments/results/oit_mrpi_20261105/figures/08_feasible_region.png)

已记录环境：Windows、Python 3.11.9、NumPy 2.4.6、SciPy 1.17.1、OSQP 1.1.3、Matplotlib 3.11.2。实验阶段 JSON 保留运行时源码校验值和环境。全局基准种子 20261105，各子实验固定种子见相应源文件。11 项单元测试在最终数值代码版本下已通过；此次续接没有为了更新文档重复运行。

从仓库目录执行下列命令可分别审计、绘图或运行阶段；这些是复现入口，不表示此次续接重新执行了实验。

```powershell
Set-Location -LiteralPath 'D:\WorkSpace\AcademicReaserch'
.\.venv\Scripts\python.exe -m experiments.oit_mrpi_audit
.\.venv\Scripts\python.exe -m experiments.oit_mrpi_plots
.\.venv\Scripts\python.exe -m experiments.oit_mrpi_verify --stage all
.\.venv\Scripts\python.exe -m unittest tests.test_oit_mrpi -v
```

阶段运行器默认跳过已有阶段；只有明确指定 `--replace-stage` 才重算。重新生成数据或图表后运行审计更新 manifest。不要把保存的浮点证书、有限方向测试和 Monte Carlo 零失败互相替代。

统一字段索引由 `scripts/export_oit_mrpi_records.py` 读取原始 JSON 导出，保留源文件和行号；不重新计算结果。不适用或未测量的指标保留 null，并解释计时口径。估计器原始表的运行时间混有区间查询和窗口重构，不能据此横向比较完整估计器速度。既有 `src/outerloop/finite_memory.py` 助手未纳入原阶段哈希；交付索引另外记录其当前哈希，并明确不冒充运行时记录。

实验设计参考了本地 experimental-design 工作流，其来源为 Kassis、Agarwal、He、Patel、Brueckner（2026），[Scientific Agent Skills](https://arxiv.org/abs/2609.00065)。题录在本轮前段已核对；该引用仅说明过程工具来源，不作为控制理论或新颖性证据。
