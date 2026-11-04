# 外环抽象模型与理论合同（接口未选定）

> **状态：THEORETICAL BASELINE / NOT FROZEN.** 当前阶段只冻结理论变量和证明假设，不冻结 PX4/ArduPilot 指令接口。位置/速度/加速度 setpoint 不是本文件中的已选控制输入，也不假设其与实际状态之间存在理想映射。

## 1. 物理仿真对象与控制权限

主仿真对象仍为完整 12 状态六自由度四旋翼刚体 plant：

\[
x_{\mathrm{phys}}=[p^\mathsf T,v^\mathsf T,\eta^\mathsf T,\omega^\mathsf T]^\mathsf T\in\mathbb R^{12}
\]

其中位置、速度、姿态和角速度各为三维。成熟飞控承担姿态/角速度稳定、控制分配、执行器限幅和电机控制。

外环研究的是成熟飞控之上的任务/轨迹层控制，不直接优化四桨推力、总推力/力矩 wrench 或姿态稳定输入。物理 plant 的状态维数不等于外环预测状态维数，也不决定外环命令接口。

## 2. 抽象外环预测模型

先用一般离散模型开展理论推导：

\[
x_{k+1}=Ax_k+Bu_k+Gw_k,\qquad w_k\in\mathcal W
\]

首个状态候选为：

\[
x=[p^\mathsf T,v^\mathsf T]^\mathsf T\in\mathbb R^6
\]

这里 \(u_k\) 仅表示抽象高层命令；具体物理语义暂不选择。矩阵 \(A,B,G\) 及采样时间都尚未冻结。扰动集合 \(\mathcal W\) 必须覆盖所有未建模动力学、外扰、离散化误差、命令延迟/保持和成熟飞控跟踪残差。

若模型含参数不确定性或非线性，必须对状态相关余项构造可靠外包；不得仅在一个工作点线性化后就把余项当作零。

## 3. 间歇位置量测合同

理论基线采用：

\[
y_k=C_px_k+v_k,\qquad C_p=[I_3\;\;0],\quad v_k\in\mathcal V
\]

量测可 success/miss，也可能带时间戳延迟。允许的模式由有限状态自动机/有限长度语言描述，至少明确：

- 最大连续 miss；
- 最大量测延迟；
- 允许的 success/miss/delay 序列；
- 时间戳和量测噪声界；
- 若有多传感器，记录测量相关性，禁止重复计数同源信息。

如果延迟量测到达，必须在其原时间戳对应的状态集合上施加约束，再重新传播至当前时刻。未定义最大失测或最大延迟时，不主张存在统一有限估计误差界。

## 4. CZ 集员估计

CZ 表示：

\[
\mathcal Z=\{c+G_z\xi:\|\xi\|_\infty\le1,\ A_z\xi=b_z\}
\]

预测：

\[
\mathcal X_{k+1|k}=A\mathcal X_{k|k}\oplus Bu_k\oplus G\mathcal W
\]

success 时以位置量测一致性集合与预测集合求交；miss 时只做预测；delay 时回到原时间戳更新并重新传播。每一步必须保证真实状态包含。复杂度控制只能采用可验证的外包降阶；内近似不允许用于硬安全证明。

空后验表示信息合同与真实系统不一致，应触发诊断/安全降级，不可静默修改噪声界继续宣称原保证。

## 5. 估计误差、跟踪误差与 Tube 的分离

从 CZ 后验中选取可验证的可行代表点 \(\hat x_k\)，定义：

\[
\mathcal E_k=\mathcal X_k-\hat x_k
\]

名义状态为 \(\bar x_k\)，真实跟踪误差为：

\[
e_k=x_k-\bar x_k,\qquad
\tilde x_k=x_k-\hat x_k,\qquad
\hat x_k-\bar x_k=e_k-\tilde x_k
\]

\(\mathcal X_k\) 是当前真实状态的一致集合；\(\mathcal E_k\) 是当前估计误差外包；未来 Tube 是真实轨迹相对名义轨迹的传播集合。三者不是同一个对象。

必须先证明有限测量语言下的相位相关估计误差管 \(\mathcal E_i\)，再合成跟踪误差管 \(\mathcal S_i^c\)。

## 6. 因果控制与约束收紧

控制器只允许使用已收到的观测历史、CZ 代表点和名义轨迹。对同一观测历史下的所有可能真实状态，实际命令必须相同。

一个候选路径相关控制律为：

\[
u_k=\bar u_k+\lambda_i+
\sum_jK_{i,j}(\hat x_{k-j}-\bar x_{k-j})
\]

其中 \(i\) 为测量自动机状态/周期相位。若 \(\tilde x\in\mathcal E\)、\(e\in\mathcal S^c\)，则：

\[
\bar x_k\in\mathcal X\ominus\mathcal S_i^c
\]

\[
\bar u_k\in
\mathcal U\ominus
\left(\{\lambda_i\}\oplus
\bigoplus_jK_{i,j}(\mathcal S_j^c\oplus(-\mathcal E_j))\right)
\]

这是安全但可能保守的独立集合外包。若要利用 \(e\) 与 \(\tilde x\) 的相关性，必须维护联合集合并证明投影包含。

## 7. 终端与递归可行性合同

需要非空共同终端集合 \(\mathcal X_f\) 和终端反馈 \(K_f\)，至少满足：

\[
\mathcal X_f\subseteq\bigcap_i(\mathcal X\ominus\mathcal S_i^c)
\]

\[
(A+BK_f)\mathcal X_f\subseteq\mathcal X_f
\]

\[
K_f\mathcal X_f\subseteq\bigcap_i\mathcal U_i
\]

并要求终端代价下降条件和初始名义问题可行。递归可行性依赖移位旧解并追加终端反馈，不是由有限时域约束满足自动推出。

持续有界扰动和持续有界估计误差下，目标是鲁棒实用稳定到误差管邻域；除非另有条件，不宣称渐近收敛到原点。

## 8. 理论冻结准入条件

1. 冻结抽象状态、输入、扰动和位置量测噪声集合。
2. 冻结 success/miss/delay 有限语言、最大连续失测和最大延迟。
3. 证明 CZ 预测/量测更新/降阶的真实状态包含。
4. 证明位置-only 间歇量测下的相位相关估计误差界/Equalized Recovery。
5. 证明共同因果输出反馈和跟踪 Tube 包含。
6. 证明收紧约束、非空终端集合、初始可行性和递归可行性。
7. 再把抽象模型及残差映射到 12 状态物理 plant；最后才选具体飞控接口并做 SITL/HIL。

## 9. 暂缓资料

PX4 ROS 2 Offboard 字段、PX4 v1.17.0 位置控制器源码、HTE 和 DDS topic 审计分别保留在 model_selection/PX4_INTERFACE_EVIDENCE.md 与 model_selection/PX4_V1_17_SOURCE_AUDIT.md，仅供后续接口映射，不属于当前理论合同。


## 10. 候选有限生成/交付与时间戳合同（Run304；尚非物理冻结）

为避免符号冲突，定义 \(M\) 为最大连续未生成测量数，\(L\) 为每个已生成样本的最大交付延迟。success 表示时间戳为当前生成时刻的样本已生成且保证在 \(0,\ldots,L\) 拍内交付；miss 表示该拍没有生成样本。允许乱序和同一接收拍多包。若 success 包可能永久丢失，则本合同不适用。

候选自动机的联合结论为：

\[
K_{\rm warm}=2(M+1)+L-1,\quad
H_{\rm age}=M+L,\quad
D_{\rm span}=M+\max\{1,L\}.
\]

从 \(k\ge K_{\rm warm}\) 起，最近两个不同已交付时间戳 \(s_1>s_0\) 存在，且 \(k-s_1\le H_{\rm age}\)、\(s_1-s_0\le D_{\rm span}\)。Run304 的有限状态监测器对 \(M,L\in\{0,\ldots,5\}\) 的全部可达状态闭包做了穷举；解析证明覆盖任意非负整数 \(M,L\)。真实传感器是否满足该合同仍需实测/设备规范证据。

在前向 Euler 平移模型 \(p^+=p+Tv,\ v^+=v+T(u+w)\) 下，若已知并扣除实际施加的命令 \(u\)，且每坐标 \(|w|\le\bar w, |\nu|\le\bar\nu\)，则两个时间戳间隔 \(d\) 的有限差分速度估计满足

\[
\beta(d)=\frac{2\bar\nu}{dT}+\frac{(d-1)T}{2}\bar w.
\]

将该历史速度估计前推到当前时刻后，可取

\[
\gamma(d)=\frac{2\bar\nu}{dT}+\frac{(d+1)T}{2}\bar w.
\]

其中 \(\beta(d)\) 是对较旧时间戳 \(s_0\) 的差分速度误差；将差分项与 \(s_0\to s_1\) 的过程残差前推项合并后，较新时间戳 \(s_1\) 的误差界为 \(\gamma(d)\)，避免重复计数同一过程残差。当前时刻 \(k=s_1+h\) 的均匀速度界可取

\[
\|e^v_k\|_\infty\le
\max_{d\in\{1,D_{\rm span}\}}\gamma(d)
+H_{\rm age}T\bar w.
\]

相应 Euler 位置界为

\[
\beta_p=\max_{d\in\{1,D_{\rm span}\}}
\left[\bar\nu+H_{\rm age}T\gamma(d)
+\frac{H_{\rm age}(H_{\rm age}-1)}{2}T^2\bar w\right].
\]

该式是后预热有限差分误差外包；不能替代精确 CZ 后验、固定滞后历史相关性或全路径 Equalized Recovery。若采用含半步加速度项的另一种离散模型，必须重新推导误差系数。

延迟 CZ 后验需将每个迟到观测施加在其生成时间戳对应的历史状态上，并保留历史状态与当前状态的相关性。候选实现为固定滞后联合轨迹 CZ 或时间戳回退重放；当前边缘集合的直接旧包更新不构成精确后验。

**启动限制：** \(K_{\rm warm}\) 只保证两个时间戳最终到齐，不提供启动期间安全。初始速度无界时，一笔位置量测不能界定隐藏速度；必须另行给定有界初始六维 CZ 集并验证共同因果首步可行性，或证明独立安全采集策略。
