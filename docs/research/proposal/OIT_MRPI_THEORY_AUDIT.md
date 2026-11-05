# OIT、CZ 与 mRPI：命题审计和已实现控制构造

日期：2026-11-05。以下区分数学命题、实现所用充分条件、浮点数值核验和尚未证明的推广。它们不构成首创认定。实验结果见同目录 OIT_MRPI_VALIDATION_REPORT.md。

## 1. 对任务书中关键陈述的修正

1. **RPI 是后不动点条件** \(\Phi(S)\subseteq S\)，不是所有 RPI 都满足等号。最小不变集在标准 Schur/紧扰动条件下满足固定点方程。
2. **外包降阶的精确固定点自动是 RPI。** 若 \(Z=\mathcal R(FZ\oplus W)\) 且 \(T\subseteq\mathcal R(T)\)，则 \(FZ\oplus W\subseteq Z\)。实际的困难是有限次停止、数值残差、时变表示和是否真的收敛。
3. **Raković 缩放条件已经足以保证 RPI。** 对凸且含零的 \(W\)，若 \(F^NW\subseteq\alpha W,\alpha<1\)，则 \(\bar S=(1-\alpha)^{-1}\bigoplus_{i=0}^{N-1}F^iW\) 是 RPI，不需要再补一个未知条件。
4. **输出反馈不能套用纯状态反馈误差式。** 当 \(u=v+K(\hat x-z)\) 时，\(s^+=(A+BK)s-BK\varepsilon+B_ww\)。标量 \(A=B=1,K=-1,x=z=0,\hat x=1,w=0\) 给出实际下一步误差 -1，而错误公式给出 0。
5. **并集外包不会比旧预测更紧。** 若 \(\tilde E^+\supseteq F\tilde E\oplus W\)，则新观测不能让 \(\tilde E^+\) 在任何支持方向小于这个旧预测。并集方案不自动保证 MPC 移位可行。
6. **过去扰动的后验不等于未来扰动的支撑集。** 在未来扰动任意取自 \(W\) 的合同下，过去观测不能排除下一拍的任一点。在线相交必须估计跨时刻共享的参数，或使用额外变化率/分布假设。
7. **普通有限 CZ 是有界的。** 部分观测产生的无界条带需扩展 CZ、H 表示或消元后的有界窗口集合。本实现使用原论文允许的 observable/unrestricted-prior 选项，消去两个初始状态变量。
8. **literal OIT 与完整窗口轨迹一致集不同。** 分别传播各量测再相交会独立化某些历史扰动；共享同一组轨迹扰动的窗口 CZ 通常更紧。本实现分别计算两者，未把二者误称为相等。
9. **CZ 支持函数是 LP；一般 CZ 包含不是一个简单精确 LP。** 本实现返回 affine-lifting 充分证书；求解失败只返回 uncertified。
10. **Pontryagin 差的表示问题与算法成本不同。** 非空有界多面体差仍可用 CZ 表示，但没有与 Minkowski 和同样简单、普遍廉价的拼接公式。H 多面体约束的逐行支持收紧可以精确计算。

## 2. 命题 A：batch 与 sequential reduction

令 \(S_0=\{0\}\)，\(S_{i+1}=FS_i\oplus W\)，\(Z_0=\{0\}\)，\(Z_{i+1}=\mathcal R(FZ_i\oplus W)\)。要求：

- 外包：\(T\subseteq\mathcal R(T)\)；
- 集合单调性：\(T_1\subseteq T_2\Rightarrow\mathcal R(T_1)\subseteq\mathcal R(T_2)\)；
- 对两个方案使用同一个、以集合为输入的算子。

外包性质和归纳法给出 \(S_i\subseteq Z_i\)。于是
\[
S_N\subseteq\mathcal R(S_N)
=\mathcal R(FS_{N-1}\oplus W)
\subseteq\mathcal R(FZ_{N-1}\oplus W)=Z_N.
\]
不需要额外的幂等性。固定坐标 interval hull、固定可逆基的 box hull 和固定有界支持方向模板均满足这些条件。“生成元少时跳过降阶”的表示依赖实现未必满足集合单调性，不能直接继承证明。

对于任意外包降阶，不存在普遍支配结论。程序在二维稳定有理矩阵中搜索，使用根据 \(h_Z(e_1)\) 在轴对齐盒和斜坐标盒之间切换的外包算子。找到的反例及独立有理数复算见 theory.json 与 audit.json。该反例说明缺少单调性的结论不成立；并不证明任一特定标准 CZ 降阶算法必然失败。

这个命题本身是单调集合算子的直接推论，不应作为新的 mRPI 理论贡献。有限和的 batch 外包也不自动是 RPI。

## 3. mRPI 外逼近的尾项与奇异扰动处理

原系统扰动 \(B_w[-a,a]\) 是二维状态空间中的线段，通常不满足 \(F^N W\subseteq\alpha W\)。不可将状态空间扰动误认为满维。

本实现的通用尾项构造：选择 \(m\) 使 \(a_m=\|F^m\|_\infty<1\)，令
\[
B_m=\bigoplus_{j=0}^{m-1}F^j[-1,1]^n,\quad
\beta_N=\|F^ND\|_\infty,\quad
T_N=\frac{\beta_N}{1-a_m}B_m,
\]
其中 \(W=D[-1,1]^p\)，矩阵无穷范数是最大绝对行和。由
\[
FB_m\oplus(1-a_m)[-1,1]^n\subseteq B_m
\]
得到 \(FT_N\oplus F^NW\subseteq T_N\)，因此
\[
\widehat S_N=\bigoplus_{i=0}^{N-1}F^iW\oplus T_N
\]
是 RPI。代码显式保存 \(m,a_m,N\) 与尾项生成元，参考无限和误差有统一无穷范数上界。

Raković-style 基线使用 \(W_\delta=W\oplus\delta[-1,1]^n\)，同时控制正则化误差与缩放误差。它是**原系统的可靠但略保守外包**，没有声称处理线段时无需修改经典条件。冻结计划曾提出满维 disturbance block；实施时改为显式正则化，因为仅用分组条件一般只直接给出多步不变性，不能将其误报为一步 RPI。这一修正没有依赖性能结果调参。

迭代基线固定在实特征向量坐标下做 box reduction，收敛残差通过 \((I-|P^{-1}FP|)^{-1}\) 尾项补偿。它是低复杂度保守对照，不代表所有 zonotope 迭代算法。one-step 基线实现 Raghuraman–Koeln 的固定生成方向、优化缩放的充分 LP；二维/四维加入扰动传播方向，高维采用特征基。

## 4. 命题 B 与输出反馈实现

对声明的真实误差系统 \(e^+=Fe+w\)，若 \(e\in E,w\in W\) 且 \(FE\oplus W\subseteq E^+\)，则 \(e^+\in E^+\)。若 \(z+E\subseteq X\)、\(v+KE\subseteq U\) 且实际控制确为 \(u=v+Ke\)，则满足约束。后一条件必须与实际可实现控制律一致。

实际实现采用后验观测器：
\[
\hat x^-_{k+1}=A\hat x_k+Bu_k,\quad
r_{k+1}=y_{k+1}-C\hat x^-_{k+1},\quad
\hat x_{k+1}=\hat x^-_{k+1}+Lr_{k+1}.
\]
取 \(\eta=(\varepsilon,d)\)，\(\varepsilon=x-\hat x,d=\hat x-z\)，则
\[
\eta^+=
\underbrace{\begin{bmatrix}(I-LC)A&0\\LCA&A+BK\end{bmatrix}}_{\mathcal A}\eta
+\underbrace{\begin{bmatrix}(I-LC)B_w&-L\\LCB_w&L\end{bmatrix}}_{\mathcal B}
\begin{bmatrix}w\\v_{\rm noise}\end{bmatrix}.
\]
同一组噪声变量同时进入两行。状态和输入误差分别由
\[
T_x=[I\ I],\qquad T_u=[0\ K]
\]
给出；特别地 \(T_x\mathcal B=[B_w\ 0]\)，当前测量噪声在真实状态上的抵消被保留。创新条件为
\[
r_{k+1}=CA\varepsilon_k+CB_ww_k+v_{{\rm noise},k+1}.
\]
代码先在共享变量上增加这个等式，再线性映射到下一拍，避免分别更新两个误差造成虚假独立性。

设 \(S\) 是 \(\mathcal A S\oplus D[-1,1]^p\subseteq S\) 的联合 RPI 外包。对过去 \(m\) 个已到达创新，定义 \(J_k^m\)：从时刻 \(k-m\) 的 \(S\cap\{d=d_{k-m}\}\) 出发，逐步加入真实创新等式并传播。启动期取 \(\max(0,k-m)\)。在正确噪声界与 \(\eta_0\in S\) 下，真实 \(\eta_k\) 属于所有这些集合，且
\[
J_k^{m+1}\subseteq J_k^m\subseteq S.
\]
证明后一包含使用 S 的不变性；前一包含使用已知边界 d 与相同创新递推的一致性。它是已声明线性模型上的窗口联合误差条件化，不是对原论文全部 detectable 情形的复现。

### 有限复杂度、可移位的管束

窗口长度为 \(\ell\)，预测时域 \(N\ge\ell\)。取
\[
P_{i|k}=\begin{cases}
\mathcal A^iJ_k^{\ell-i}\oplus\bigoplus_{j=0}^{i-1}\mathcal A^jD[-1,1]^p,&i<\ell,\\
S,&i\ge\ell.
\end{cases}
\]
于是 \(\mathcal A P_{i|k}\oplus D[-1,1]^p\subseteq P_{i+1|k}\)。对每个相容的下一拍创新，
\[
P_{i|k+1}\subseteq P_{i+1|k}.
\]
在 \(i<\ell-1\) 时，新旧集合具有相同最早边界，新集合只多了一条已实现创新等式；边界 \(i=\ell-1\) 及其后由 S 的不变性闭合。因此不需要猜测未来量测，也不需要新旧集合取并集。

名义中心按 \(z^+=Az+Bv\) 延续，不随新后验任意重置。约束为
\[
H_xz_{i|k}+h_{P_{i|k}}(T_x^\top H_x^\top)\le b_x,\qquad
H_uv_{i|k}+h_{P_{i|k}}(T_u^\top H_u^\top)\le b_u,
\]
逐行解释支持函数。终端集合 \(X_f\) 对 \(A+BK\) 正不变，并位于使用 S 收紧后的状态/输入约束内。上一拍控制序列移位并追加 \(Kz_N\)，在新管束上仍可行。初始可行、初始误差准入、全部实际噪声符合合同是必要前提。

终端 \(P\) 满足
\[
(A+BK)^\top P(A+BK)-P=-(Q+K^\top RK).
\]
标准名义值函数移位下降得到名义状态趋于零，真实状态保持在有界联合误差管的投影内。这里是有扰动下的集合收敛/有界性结论，不是实际状态必然趋于原点。

有限窗口对预测步逐步遗忘以保证可行性的核心思想已有 Brunner 等 2018 的近邻工作；本轮证明是明确受限设置下的实现合同，不能宣称首次。

### 强对照与 10,000 条轨迹的快捷分支

“known_d_only”只在当前层使用 \(S\cap\{d=d_k\}\)，未来各层为 S，因此同样满足移位关系，具有独立闭环保证。它用于区分当前输入已知带来的收益与历史创新约束的新增收益。

如果无约束名义 QP 的全局最优解已经满足固定 S 收紧，它也满足更宽松的自适应约束，且仍是自适应问题的全局最优解。代码在这个可验证条件下跳过 LP/QP；条件不成立时才显式构造自适应管并求解。10,000 条轨迹的大多数甚至全部控制步可能落在快捷分支，必须报告实际调用数，不能把批量运行时间解释为逐拍 CZ 最坏执行时间。

## 5. 命题 C 与合法的学习模型

若 \(W_1\subseteq W_2\)，则每一有限和都满足包含；取紧集极限得
\[
S_\infty(F,W_1)\subseteq S_\infty(F,W_2).
\]
这不证明特定数值外逼近算法的输出也必然嵌套，更不证明新管截面能立即容纳已经存在的实际误差。

反例：\(W=[-1,1]\)，过去观测得 \(w_0=0\)，而下一拍允许 \(w_1=1\)。以过去扰动后验 \(\{0\}\) 取代 W 会漏掉合法未来扰动。

实现的合法示例明确假设 \(q_k=b+\epsilon_k\)，b 固定未知、\(|\epsilon_k|\le r\)。若观测给出 \(q_k\in[l_k,u_k]\)，则
\[
B_{k+1}=B_k\cap[l_k-r,u_k+r],\quad W_{k+1}=B_{k+1}\oplus[-r,r].
\]
这些集合包含同一个真实 b 及所有允许的未来 q，且嵌套。本轮没有把这个额外假设偷偷施加到标准任意有界扰动 MPC 上，也未声称已经完成状态观测驱动的通用扰动辨识器。

## 6. 命题 D：CZ affine decision rule 的 LP

设待验证集合 \(Z=\{c+G\xi:E_z\xi=f_z,|\xi|\le1\}\)，扰动 \(W=\{c_w+G_w\eta:E_w\eta=f_w,|\eta|\le1\}\)。定义
\[
p=(\xi,\eta),\quad E=\operatorname{diag}(E_z,E_w),\quad f=(f_z,f_w),
\quad H=[FG\ G_w],\quad a=(F-I)c+c_w.
\]
寻找 \(\zeta=Mp+t\)。以下是充分条件：
\[
GM=H,\quad Gt=a,\quad E_zM=UE,\quad E_zt+Uf=f_z,
\]
以及对每个输出系数 j、符号 \(\sigma\in\{-1,1\}\)，存在自由乘子 \(\lambda_{j,\sigma}\) 和非负 s，满足
\[
-s\le \sigma M_j-\lambda_{j,\sigma}^\top E\le s,\qquad
\sigma t_j+\lambda_{j,\sigma}^\top f+\mathbf1^\top s\le1.
\]
对任意 \(Ep=f,|p|\le1\)，后一式由
\[
\sigma M_jp+\sigma t_j
=\lambda^\top f+(\sigma M_j-\lambda^\top E)p+\sigma t_j
\le\lambda^\top f+\|\sigma M_j-\lambda^\top E\|_1+\sigma t_j
\]
得到。几何等式使真实后继等于 \(c+G\zeta\)，目标等式确保 \(E_z\zeta=f_z\)，双符号条件确保 \(|\zeta|\le1\)。固定 Z、W 时这是一组 LP 条件。几何等式采用全空间仿射恒等，因此可能比利用 E 的仿射包条件更保守。返回证书后，代码另解源域支持 LP 独立检查各行。

一般 CZ 形状综合中同时优化 G、E_z 和 M 会产生双线性，不能泛称 LP。本轮额外实现**固定 CZ 模板的同心比例综合**：\(Z_\alpha=\alpha Z\)，令 \(\tau=\alpha\zeta=Mp+t\)，用 \(\alpha\) 替代上述各行系数界的 1，并调整几何等式
\[
GM_\xi=\alpha FG,\quad GM_\eta=G_w,\quad
Gt=\alpha(F-I)c+c_w,\quad E_zt+Uf=\alpha f_z.
\]
最小化 \(\alpha>0\) 仍是 LP。二维三角形模板和删除等式后的方形模板提供解析可核对示例；这不是一般最优 CZ 对最优 zonotope 的优势证明。

## 7. 文献与复现边界

- Cong, Wang, Zhou, [作者稿](https://arxiv.org/abs/2203.13966)，Algorithm 3、Proposition 3、Eq. (25)。本轮复现可观二维模型与原文允许的无界初始先验窗口选项，使用新随机记录；未宣称重现原图噪声、全部 detectable 情形或 CORA 时间结果。
- Raković et al. (2005), [Invariant approximations of the minimal robust positively invariant set](https://doi.org/10.1109/TAC.2005.843854)。
- Raghuraman–Koeln, [作者稿 Section 7 / Theorem 23](https://arxiv.org/html/2009.06039v1)。本轮对应其 zonotope RPI 充分条件，不把该节称为一般 CZ 最优综合。
- Brunner et al. (2018), [Enhancing Output-Feedback MPC With Set-Valued Moving Horizon Estimation](https://doi.org/10.1109/TAC.2018.2791899)。
- Ji et al. (2022), [Robust Output Feedback MPC with Reduced Conservatism under Ellipsoidal Uncertainty](https://arxiv.org/abs/2008.04980)。
- 过程工具引用：Kassis, Agarwal, He, Patel, Brueckner (2026), [Scientific Agent Skills](https://arxiv.org/abs/2609.00065)。用于 experimental-design 工作流，不作为控制理论证据。
