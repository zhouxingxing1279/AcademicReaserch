# 理论框架：间歇位置量测下的 CZ 集员估计与外环输出反馈 Tube MPC

> **研究状态：理论架构已收敛为可检验的证明路线；项目级定理尚未证明。** 本文先处理抽象离散外环模型，不冻结 PX4/ArduPilot 的具体指令接口，不声称已经完成 SITL、控制器实现或硬安全认证。

## 0. 当前理论问题与边界

当前要回答的不是“如何把 SMF 与 MPC 拼在一起”，而是：

**在只有间歇/异步位置量测、速度不可直接获得、过程扰动和外环模型残差有界的条件下，能否构造一个可靠包含真实状态的 CZ 后验；再用有限测量模式下的估计误差界，合成一个对同一观测历史中的所有可能真实状态都可执行的因果控制命令，并通过 Tube 收紧与终端条件证明硬约束满足和递归可行？**

研究对象仍分层：

- 高保真物理对象：12 状态六自由度四旋翼刚体模型，成熟飞控承担姿态、角速度、分配和电机闭环。
- 理论外环状态：先以三维位置—速度候选状态 \(x=[p^\mathsf T,v^\mathsf T]^\mathsf T\in\mathbb R^6\) 建立证明基线。它是待验证的外环抽象状态，不是已经确认的飞控闭环模型。
- 外环输入 \(u\)：当前仅是抽象的高层控制/参考变量。具体 PX4 指令字段、位置/速度/加速度模式比较、固件参数和 SITL 接口辨识全部暂缓。
- 本阶段不研究电机级控制，不把虚拟 wrench 或四桨推力当作外环优化输入。

## 1. 抽象离散模型与不确定性合同

理论基线先写成一般离散时间模型：

\[
x_{k+1}=Ax_k+Bu_k+Gw_k,\qquad w_k\in\mathcal W
\]

\[
y_k=C_px_k+v_k,\qquad v_k\in\mathcal V
\]

其中：

- \(x_k\in\mathcal X\subset\mathbb R^{n_x}\) 是外环预测状态；首个候选为 \([p;v]\) 六状态。
- \(u_k\in\mathcal U\) 是实际发给成熟飞控的高层命令变量。它不是理想物理加速度，也不意味着飞控无误差跟踪。
- \(\mathcal W\) 必须外包风扰、模型离散化误差、飞控跟踪误差、命令保持/延迟和未建模动态对外环预测的合成影响。
- \(\mathcal V\) 是位置测量噪声的有界集合。
- 位置-only 候选观测矩阵为 \(C_p=[I_3\;0]\)。若后续预测状态增广，必须重新检查可观测性，不能沿用六状态结论。

若真实模型含参数不确定性，例如 \(A(\theta)\)，不得未经证明直接把 \(\Delta A x\) 当作与状态无关的常数扰动。可在有界状态域 \(\mathcal X\) 上构造状态相关误差外包 \(\mathcal D_A(\mathcal X)\)，或保留多面体/LPV 模型分支；只有证明其统一包含后，才可合并进固定 \(\mathcal W\)。

**硬安全前提：** \(\mathcal W,\mathcal V,\mathcal X,\mathcal U\) 必须是有物理或辨识依据的紧集合。若跟踪误差、命令延迟或传感器误差没有可信上界，只能给经验性能结果，不能给确定性硬安全结论。

## 2. 间歇、异步与延迟测量：先定义允许的信息语言

令测量模式 \(\sigma_k\) 描述本拍是否收到位置量测，以及该量测的时间戳/延迟。允许模式不是任意随机序列，而应由一个明确的有限状态自动机或有限长度语言 \(\mathcal L\) 描述，例如：

- 最大连续丢包数 \(L\)；
- 最大测量延迟 \(d_{\max}\)；
- 一个周期/滑动窗口内允许的 success/miss/delay 模式；
- 各传感器各自的时间戳、更新率和相关性合同。

如果存在延迟量测，量测必须作用于它**产生时刻**的状态约束，而不是误当成当前时刻的新鲜量测。实现上需保留至少 \(d_{\max}\) 的状态/输入历史，并对受影响的历史时刻施加量测约束后重新传播；若要保持精确的跨时刻相关性，应维护延迟窗口内的联合轨迹集合，不能只把旧读数直接套在当前状态上。

### 2.1 位置-only 对六状态平移模型的可观测性检查

作为理论例子，考虑常速度离散运动学：

\[
A_d=\begin{bmatrix}I_3&T_sI_3\\0&I_3\end{bmatrix},
\qquad C_p=\begin{bmatrix}I_3&0\end{bmatrix}
\]

两个不同时间戳的位置量测相隔 \(d\ge1\) 拍时：

\[
\mathcal O_d=
\begin{bmatrix}C_p\\C_pA_d^d\end{bmatrix}
=
\begin{bmatrix}I_3&0\\I_3&dT_sI_3\end{bmatrix}
\]

只要 \(T_s>0\)，该矩阵满列秩 6。因此在无噪声、模型精确的常速度基线下，两次不同时间戳的位置量测足以区分位置与速度；有界噪声和有界过程扰动会留下非零误差集合，但在测量间隔有上界时有机会得到有限误差界。

若过程扰动可写成逐拍有界加速度 \(a_j\)，满足 \(\|a_j\|_\infty\le\bar a\)，位置噪声满足 \(\|v_j\|_\infty\le\bar\nu\)，两个位置量测相隔 \(d\) 拍，则有限差分速度估计满足一个直接的保守界：

\[
\left\|\frac{y_{k+d}-y_k}{dT_s}-v_k\right\|_\infty
\le
\frac{2\bar\nu}{dT_s}+\frac{dT_s}{2}\bar a
\]

该式说明：测量噪声项随间隔增大而下降，过程扰动项随间隔增大而上升；当 \(d\le L+1\) 时界是有限的。它只是可观测性/有界性解释，不是最终 CZ 后验的紧界，也不能替代完整集合更新。

**必要边界：** 若连续失测长度没有上界，且速度受未知有界加速度扰动影响，位置-only 信息通常无法给出统一有限的速度误差界；此时任何基于固定有限估计管的无限时域硬安全证明都缺少前提。对六自由度 12 状态 plant，仅有位置输出并不自动保证姿态和角速度可观测；必须另做结构可观测性与误差外包分析。

## 3. Constrained Zonotope（CZ）集员滤波的可靠包含递推

采用 CZ 表示：

\[
\mathcal Z=
\{c+G\xi:\|\xi\|_\infty\le1,\ A_c\xi=b_c\}
\]

其优势是可以显式保留生成元之间的线性约束相关性。对线性映射、Minkowski 和以及线性量测广义交集，CZ 可在不限制表示复杂度时进行精确集合运算；复杂度受限时必须使用**外包降阶**，不能使用可能切掉真实状态的内近似。

### 3.1 预测

若 \(\mathcal X_k\) 是当前后验，已施加命令 \(u_k\) 已知，则：

\[
\mathcal X_{k+1|k}
=A\mathcal X_k\oplus Bu_k\oplus G\mathcal W
\]

线性映射与 Minkowski 运算可由 CZ 代数精确执行。若动力学非线性，应使用有证明的 mean-value 或 first-order Taylor 外包，并把余项集合加入预测；仅在名义点线性化而不包络余项不构成可靠预测。

### 3.2 位置量测更新

若量测为 \(y_k=C_px_k+v_k\)，且 \(\mathcal V=G_v\mathbb B_\infty\)，当前预测 CZ 为：

\[
\mathcal X^-_k=\{c+G\xi:\|\xi\|_\infty\le1,\ A_c\xi=b_c\}
\]

则与量测一致的后验为：

\[
\mathcal X_k=
\mathcal X^-_k\cap\{x:y_k-C_px\in\mathcal V\}
\]

可通过增加量测噪声生成元并施加线性等式，把该交集精确写成新的 CZ：

\[
c^+=c,\quad G^+=[G\;\;0]
\]

\[
A_c^+=
\begin{bmatrix}
A_c&0\\
C_pG&G_v
\end{bmatrix},
\qquad
b_c^+=
\begin{bmatrix}
b_c\\
y_k-C_pc
\end{bmatrix}
\]

这里新增的噪声生成元只参与等式约束，不改变状态向量。若量测噪声本身带有 CZ 约束，还必须把其约束矩阵/右端项一并并入。

- **success：** 用当前带时间戳量测执行上述交集。
- **miss：** 不做量测交集，保留预测集合。
- **delay：** 对原始时间戳对应的历史集合施加交集，再按已记录输入和扰动合同重新传播到当前时刻。
- **empty posterior：** 表示初始集合、动力学、噪声界、时间戳或传感器合同至少有一项被违反。必须报告一致性失败/故障，不能静默扩大集合后继续声称原有保证成立。
- **order reduction：** 每次降阶必须验证 \(\mathcal X_k\subseteq\overline{\mathcal X}_k\)。外包过大可能导致 MPC 不可行；外包过小则失去真实状态包含保证。

仓库现有 numerical_sets.py 目前是 float64 Box/Zonotope 通用工具，不是 CZ 滤波器，也不是向外舍入的形式化数值证书。不能把它描述为已完成上述 CZ 递推。

## 4. 从 CZ 后验到时变估计误差管：Equalized Recovery

从每个非空后验 \(\mathcal X_k\) 中选择一个**经可行性验证、确实属于集合内部**的代表点 \(\hat x_k\)。CZ 的参数 \(c\) 在一般约束 \(A_c\xi=b_c\) 下不一定属于 CZ，因此不能无条件把 \(c\) 当作可行状态估计；可通过 LP 找到满足生成元约束的可行见证 \(\xi^\star\)，再取 \(\hat x=c+G\xi^\star\)。

定义估计误差集合：

\[
\mathcal E_k=\mathcal X_k-\hat x_k
\]

需要为允许的测量语言建立相位/模式相关的外包集合 \(\mathcal E_i\)，使所有允许量测值、扰动和 success/miss/delay 模式均满足：

\[
x_k-\hat x_k\in\mathcal E_{q_k}
\]

其中 \(q_k\) 是测量自动机状态或周期相位。有限长度语言下可采用 **Equalized Recovery**：估计误差允许在周期中间阶段变大，但每个恢复周期末回到规定的初始误差界；这比强求一个逐拍不变的固定误差集合更灵活。

这里有一个明确的理论移植缺口：

- Hassaan et al. (2021) 已给出有限长度缺测/延迟语言下的动态点估计器、相位相关估计误差盒和 Equalized Recovery 设计。
- Rego et al. (2020) 已给出非线性有界不确定系统的 CZ 预测外包和有界量测交集。
- **本项目还没有证明：将 CZ 后验/外包降阶接入有限语言后，能得到满足 Equalized Recovery 的相位相关估计误差界。** 这就是理论第一道 Gate，不可用“CZ 可以做交集”替代。

### 4.1 路径相关 observer + CZ 误差集合：优先证明的基线

先考虑无延迟、只有 success/miss 的测量自动机。使用一个可实施的预测—校正 observer：

[
\hat x_{k|k-1}=A\hat x_{k-1|k-1}+Bu_{k-1}
]

success 时：

[
\hat x_{k|k}=\hat x_{k|k-1}
+L_q(y_k-C_p\hat x_{k|k-1})
]

miss 时令 \(\hat x_{k|k}=\hat x_{k|k-1}\)。这里 \(q\) 是当前自动机状态/已观察到的模式前缀，允许校正增益随可观察历史变化。

令预测误差集合为 \(\mathcal E^-_k\)。由 \(y_k=C_px_k+v_k\) 可直接得到：

- success 校正后：
  \[
  \mathcal E_{k|k}\supseteq
  (I-L_qC_p)\mathcal E^-_k\oplus(-L_q)\mathcal V
  \]
- miss 时：
  \[
  \mathcal E_{k|k}=\mathcal E^-_k
  \]
- 下一拍预测：
  \[
  \mathcal E^-_{k+1}\supseteq
  A\mathcal E_{k|k}\oplus G\mathcal W
  \]

合并校正和预测，可写成两类线性集合递推：

[
F_q^{s}=A(I-L_qC_p),quad
D_q^{s}=G\mathcal W\oplus(-AL_q)\mathcal V
]

[
F^{m}=A,quad D^{m}=G\mathcal W
]

对自动机中每条允许转移 \(q\xrightarrow{\sigma}q'\)，寻找 CZ 误差集合族使：

[
\mathcal E_{q'}\supseteq
F_{q,\sigma}\mathcal E_q\oplus D_{q,\sigma}
]

**包含引理：** 若初始误差属于对应集合，且每条允许自动机转移均满足上述包含，则由归纳法可知所有允许 success/miss 序列下真实估计误差始终落在相应 CZ 误差集合内。若还存在一个周期/恢复词使周期末集合回到初始误差集合，即可得到 Equalized Recovery 的集合版本。

这个基线的优点是误差传播对给定增益是显式线性集合递推，能直接用 CZ 表示；它不是精确后验交集，必须报告其外包保守性。增益与集合同时求解时可能出现双线性/非凸包含条件，不能未经推导宣称是一个 LP/LMI。建议先固定可验证 observer gains，检查所有有限模式词的误差包含，再研究增益综合。

若有延迟量测，上述简单递推不够：必须将延迟状态/历史纳入增广 observer，或采用 Hassaan 等的动态延迟观测器结构；不能把旧时间戳量测当作当前量测直接代入。

### 4.2 精确 CZ 后验：作为精度改进路线

在上述误差界基线成立后，再维护完整一致集合 \(\mathcal X_k\)，用第 3 节的精确量测交集更新。由可行见证选择 \(\hat x_k\)，形成 \(\mathcal E_k=\mathcal X_k-\hat x_k\)，再对所有允许量测历史求相位外包。该路线可能更紧，但最坏量测分支、集合分支数和 CZ 降阶复杂度更高。

因此当前理论优先顺序为：

1. 先证明路径相关 observer + CZ 误差集合的有限语言包含与 Equalized Recovery；
2. 再比较精确 CZ 后验能否在相同信息合同和计算预算下严格缩小 \(\mathcal E_i\)；
3. 最后才把估计误差管接入 Tube MPC。

## 5. 因果输出反馈：同一观测历史必须使用同一个控制命令

令名义系统为：

\[
\bar x_{k+1}=A\bar x_k+B\bar u_k
\]

定义跟踪误差 \(e_k=x_k-\bar x_k\)，估计误差 \(\tilde x_k=x_k-\hat x_k\)。控制器可使用的估计偏差满足：

\[
\hat x_k-\bar x_k=e_k-\tilde x_k
\]

因此，输出反馈不能写成依赖真实状态的 \(u=\bar u+K(x-\bar x)\)，除非真实状态确实可测。可执行的因果路径应只依赖估计器输出和已发生的观测历史，例如：

\[
u_k=\bar u_k+\lambda_i+
\sum_{j=0}^{T_d-1}K_{i,j}
(\hat x_{k-j}-\bar x_{k-j})
\]

其中 \(i\) 是有限语言的周期相位/自动机状态，增益只依赖当前可观测的历史前缀。对所有与同一历史相容的真实状态，这个公式给出同一个实际控制命令；不能为每个隐藏真实状态分别挑选一个不同输入。

若已有跟踪误差管 \(e_{k-j}\in\mathcal S^c_j\)，估计误差管 \(\tilde x_{k-j}\in\mathcal E_j\)，则控制修正的安全外包为：

\[
\lambda_i\oplus
\bigoplus_{j=0}^{T_d-1}
K_{i,j}\big(\mathcal S^c_j\oplus(-\mathcal E_j)\big)
\]

相应名义约束收紧为：

\[
\bar x_k\in\mathcal X\ominus\mathcal S^c_i
\]

\[
\bar u_k\in
\mathcal U\ominus
\left(
\{\lambda_i\}\oplus
\bigoplus_{j=0}^{T_d-1}
K_{i,j}(\mathcal S^c_j\oplus(-\mathcal E_j))
\right)
\]

这是保守的独立外包。由于 \(e\) 与 \(\tilde x\) 来自同一真实状态和同一观测历史，二者通常相关；后续可维护联合 CZ \(\mathcal J_i\) 并直接计算 \(K(e-\tilde x)\) 的投影，以减少保守性。**先证明独立外包版本正确，再做联合集合紧化**，不能一开始就依赖尚未证明的相关性收益。

## 6. Tube、终端集合与递归可行性

若每个测量模式相位 \(i\) 存在跟踪误差集合 \(\mathcal S^c_i\)，且控制器满足：

- 初始 \(e_0\in\mathcal S^c_0\)；
- 所有允许的估计误差、过程扰动和测量模式下，中间误差 \(e_i\in\mathcal S^c_i\)；
- 每个恢复周期末 \(e_{T_d}\in\mathcal S^c_0\)；

则它构成控制误差的 Equalized Recovery 管。它与估计误差管 \(\mathcal E_i\) 是两个不同对象，不能把 SMF 后验直接称为未来 Tube。

对名义 MPC，最直接的递归可行基线是使用**跨所有允许相位有效的共同终端集合和共同终端反馈**：

\[
\mathcal X_f\subseteq
\bigcap_i(\mathcal X\ominus\mathcal S^c_i)
\]

\[
(A+BK_f)\mathcal X_f\subseteq\mathcal X_f
\]

\[
K_f\mathcal X_f\subseteq\bigcap_i\mathcal U_i
\]

其中 \(\mathcal U_i\) 是前述相位相关输入收紧集合。再要求终端代价满足：

\[
V_f((A+BK_f)\bar x)-V_f(\bar x)
+\ell(\bar x,K_f\bar x)\le0,
\quad \bar x\in\mathcal X_f
\]

并要求初始名义 MPC 可行。这样可用标准移位论证：下一拍将上一拍最优序列左移，并在末端追加终端反馈；共同终端集合保证所有相位下的末端约束仍成立。

若共同终端集合为空，不能直接宣称系统不可生存。应先区分：估计误差界过大、跟踪管过大、输入收紧过严、终端集合构造过保守，还是物理可行域本身为空。只有进一步求解模式相关终端集合或信息状态前驱，才能判断是否存在较不保守的可行策略。

## 7. 项目级条件定理模板（待证明，不是现成结论）

**假设 A — 模型与集合合同。** 真实外环状态满足第 1 节离散模型；初始 CZ 包含真实状态；过程/测量噪声及模型残差始终落在已知紧集合内；所有 CZ 降阶均为可靠外包。

**假设 B — 测量模式与估计器。** 测量时间戳/延迟/缺测序列属于已冻结有限语言；CZ 估计器对所有允许分支保持非空一致性和真实状态包含；存在相位相关的有限估计误差管 \(\mathcal E_i\)，满足 Equalized Recovery。

**假设 C — 因果跟踪管。** 存在只依赖已收到的观测历史的控制器，以及相位相关的跟踪误差管 \(\mathcal S^c_i\)，对全部允许的估计误差、过程扰动和测量模式满足 Equalized Recovery；控制修正采用第 5 节的共同因果输入合同。

**假设 D — 名义 MPC 终端条件。** 约束按第 5 节收紧；存在非空共同终端集合 \(\mathcal X_f\)、终端反馈 \(K_f\) 和终端代价下降条件；初始名义优化问题可行。

**条件结论。** 在 A–D 全部成立时：

1. 真实状态逐拍满足原始状态约束，实际施加输入逐拍满足原始输入约束；
2. 只要每拍采用可行最优解的首个控制动作，名义 MPC 通过移位并追加终端反馈保持递归可行；
3. 若终端代价满足标准下降条件，则名义状态具有相应的稳定性结论；在持续有界扰动和持续有界估计误差下，真实状态只能保证收敛/保持在由误差管决定的鲁棒邻域内，不能无条件宣称收敛到原点。

**证明分工：**

- A+B：归纳证明 \(x_k\in\mathcal X_k\)，以及 \(\tilde x_k\in\mathcal E_i\)。
- B+C：证明共同因果控制律下 \(e_k\in\mathcal S^c_i\)。
- C+D：由 Pontryagin 收紧推出真实状态/输入约束满足。
- D：用最优序列移位和终端反馈证明递归可行；用终端 Lyapunov 下降证明名义稳定性。
- 最后还需单独证明：高保真 12 状态物理 plant 的真实闭环轨迹被所选抽象外环模型及其残差集合覆盖。没有这一步，条件定理只适用于抽象外环模型，不等于完整四旋翼物理安全定理。

## 8. 已有理论先例与真正的缺口

| 文献 | 已经解决的部分 | 没有解决的本项目问题 |
|---|---|---|
| Scott et al. (2016), Automatica, DOI 10.1016/j.automatica.2016.02.036 | CZ 表示、线性映射、Minkowski 和、广义交集及可靠外包降阶 | 没有间歇位置量测下的四旋翼 Tube MPC 递归可行性 |
| Rego et al. (2020), Automatica, DOI 10.1016/j.automatica.2019.108614 | 非线性有界不确定系统的 CZ 预测外包、量测交集和降阶包含 | 没有测量缺失自动机、输出反馈 Tube MPC 或终端递归可行证明 |
| Hassaan et al. (2021), IFAC-PapersOnLine, DOI 10.1016/j.ifacol.2021.08.482 | 有限长度时延/缺测语言、Equalized Recovery、时变估计/跟踪管、共同终端集合与移位递归可行 | 误差集合为 hyperbox；没有 CZ 后验和四旋翼外环模型 |
| Hassaan et al. (2022), IEEE Control Systems Letters, DOI 10.1109/LCSYS.2021.3050300 | 延迟/缺测语言下的路径相关估计器和 Equalized Recovery | 不是 CZ 后验，也没有四旋翼 MPC |
| Qiu et al. (2020), IET CTA, DOI 10.1049/iet-cta.2019.0881 | 椭球 SMF、输出反馈 MPC、约束处理和终端 RPI 条件 | 没有本项目的间歇位置量测自动机和四旋翼模型 |
| Ji et al. (2022), CDC, DOI 10.1109/CDC51059.2022.9992704 | 12 状态四旋翼椭球 SMF + Tube 输出反馈 RMPC；Theorem 1 给条件性递归可行与约束满足 | \(C=I_{12}\) 全状态逐拍量测、虚拟 wrench 输入；没有部分/间歇位置量测或逐桨物理输入 |
| Niknejad et al. (2025), arXiv:2509.05201 | CZ 感知误差外包 + Tube MPC + 终端集的近邻结构 | 每拍量测；实验 CZ 由 95% 数据拟合，不是确定性全样本包含；无本项目缺测语言 |
| Delansnay et al. (2025), CoDIT, DOI 10.1109/CoDIT66093.2025.11321702 | 六旋翼 Pixhawk 内环上的 CZ Tube-MPC 实飞证据 | 无 SMF 后验、无间歇位置量测；4 状态速度/yaw 模型、200 ms 周期 |

因此，不能宣称“首次将 SMF 与 MPC 用于四旋翼”，也不能宣称“首次将 CZ 用于多旋翼 Tube MPC”。**待验证的窄研究空间**是：将 CZ 可靠状态后验/误差外包与有限测量语言下的 Equalized Recovery、共同因果输出反馈 Tube、共同终端集合连接起来，并在四旋翼外环抽象模型上证明所有允许量测分支下的硬约束和递归可行性。

## 9. 理论研究的执行顺序与准入 Gate

1. **Gate T1 — 信息合同：** 冻结抽象状态、输入含义、过程残差、位置噪声、时间戳/延迟、success/miss 有限语言和最大连续失测；暂不冻结 PX4 接口。
2. **Gate T2 — CZ 包含：** 完成线性 CZ 预测/交集/空集检测/可靠外包降阶的逐式推导；非线性外包只在余项界可证时引入。
3. **Gate T3 — Equalized Recovery：** 证明位置-only 测量模式下存在有限相位估计误差界；先做有限差分/可观测性必要条件，再做 CZ 或路径相关 observer 的最坏分支综合。
4. **Gate T4 — 共同因果 Tube：** 证明估计误差和跟踪误差两个集合的关系，推导输入/状态收紧；明确所有同一观测历史相容状态共享一个输入。
5. **Gate T5 — 终端与递归可行：** 求非空共同终端集合和终端反馈；若为空，分解是模型、误差管、输入收紧还是终端条件导致。
6. **Gate T6 — 证明闭合：** 写出完整定理、假设、量词、归纳/移位证明及持续扰动下的稳定性结论。
7. **Gate T7 — 物理模型映射：** 只有理论基线闭合后，再把抽象残差合同映射到 12 状态六自由度物理 plant，并安排飞控接口和 SITL 验证。

## 10. 当前明确不做的事

- 不继续 PX4 position/velocity/acceleration 接口 A/B，不继续 Offboard 消息字段辨析，不把 PX4 v1.17.0 参数或 HTE 作为当前理论主线。
- 不将历史平面直接推力/力矩模型的有限安全结果移植到当前成熟飞控外环。
- 不将概率置信区间、Monte Carlo 覆盖率或 95% 数据拟合误差界改写为确定性硬安全包含。
- 不把 SMF 后验、估计误差管、跟踪误差 Tube 和未来可达集混为一个集合。
- 不在初始可行性、共同因果输入和终端集合未闭合前声称递归可行或无限时域安全。

## 参考文献与仓库证据

- Scott et al. (2016): https://doi.org/10.1016/j.automatica.2016.02.036
- Rego et al. (2020): https://doi.org/10.1016/j.automatica.2019.108614 ; https://arxiv.org/abs/1908.09950
- Hassaan et al. (2021): https://doi.org/10.1016/j.ifacol.2021.08.482 ; https://qiangs.github.io/Papers/Conf_Hassaan2021ADHS.pdf
- Hassaan et al. (2022): https://doi.org/10.1109/LCSYS.2021.3050300
- Qiu et al. (2020): https://doi.org/10.1049/iet-cta.2019.0881
- Ji et al. (2022): https://doi.org/10.1109/CDC51059.2022.9992704 ; https://arxiv.org/abs/2008.04980
- Niknejad et al. (2025): https://arxiv.org/abs/2509.05201
- Delansnay et al. (2025): https://doi.org/10.1109/CoDIT66093.2025.11321702

以上论文阅读等级、逐篇假设和未核验项以唯一总账 docs/literature/PAPER_READING_LOG.md 为准；本文是理论综合，不新增“全文已读”计数。


## Run303 — startup information set versus one-step robust predecessor

Before claiming safety from k=0, require `exists u_0 measurable w.r.t. received history, forall x_0 in X_0(y_0), forall w_0 in W: Ax_0+Bu_0+Gw_0 in X`. This is a common-input robust predecessor condition, stronger than pointwise `forall x_0 exists u_0`. For a symmetric 1D double-integrator information box, the exact iff and a failing numerical example are in [Run303](run303_startup_one_step_gate.md). This is an initial necessary gate, not recursive feasibility or a terminal set.
