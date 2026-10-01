# Run 133 文献准入卡：先分离 ancillary tube 与 nominal terminal 两层证书

日期：2026-09-29。仓库起点为本地 Run 132 提交 `d5a726c`；远端 `main` 为 `1c49659`，远端最新研究分支仍为 Run 126 `c00d102`。本轮问题原定为“联合合成 common `K_f/X_f`”。文献核查后，先判断这个问题是否把两类不同反馈与不变集合混在了一起。

## 1. 最近邻与本轮实际阅读

| 文献 | 本轮阅读层级 | 已解决内容 | 对本轮候选的约束 |
|---|---|---|---|
| Hassaan, Pati, Shen, Yong, *Time-Varying Tube-Based Output Feedback MPC for Constrained Linear Systems with Intermittently Delayed Data*, 2021, DOI [10.1016/j.ifacol.2021.08.482](https://doi.org/10.1016/j.ifacol.2021.08.482) | **全文定向重读** Section 3.1.2、Assumptions 1--2、Lemma 4、Theorem 6 | 先由 estimator/tracking controller 得到 time-varying estimation/control-error tubes；再在全部 tightened phases 的交上定义 nominal terminal gain/set，并用旧名义计划移位证明递归可行。 | `K_f,X_f` 不是 disturbance-RPI ancillary pair；没有 tracking tube 就无法数值定义 Assumption 2 的 tightened constraints。 |
| Tahir, *Efficient computation of Robust Positively Invariant sets with linear state-feedback gain as a variable of optimization*, 2010, DOI [10.1109/ICEEE.2010.5608613](https://doi.org/10.1109/ICEEE.2010.5608613) | **全文定向精读** Sections II--IV，式 (1)--(25)，Remarks 3--12 | 对 LTI + additive box disturbance 联合优化 state-feedback 与 RPI set；给出固定形状椭球的充分 SDP，以及 origin-centered axis-aligned box 的 Farkas 条件；含 state/input constraints。 | 它合成的是 inner ancillary/RPI 层，不是 Hassaan nominal terminal 层。box 类已被仓库第37章严格排除；固定形状椭球仍须适配 LPV 与相关 residual。 |
| Tahir, Jaimoukha, *Robust Positively Invariant Sets for Linear Systems subject to model-uncertainty and disturbances*, 2012, DOI [10.3182/20120823-5-NL-3013.00032](https://doi.org/10.3182/20120823-5-NL-3013.00032) | **全文定向精读** Sections 2--3、Definition 3、Theorem 5、Remarks 6--9 | 对 norm-bounded model uncertainty、additive box disturbance、state/input constraints联合综合反馈与 origin-centered hyperrectangle RPI；一般为充分条件，无结构 norm-bounded uncertainty 特例可达精确性。 | 其 uncertainty 描述没有直接保持本项目同一 `T` 同时决定 `A(T)` 与 `W(T)` 的配对关系；独立外包会丢失 Run35 修正出的 vertex consistency。 |
| Tahir, Jaimoukha, *Robust feedback MPC of constrained uncertain systems*, 2013, DOI [10.1016/j.jprocont.2012.08.003](https://doi.org/10.1016/j.jprocont.2012.08.003) | **仅正式摘要**，未取得可核验全文 | 摘要明确区分 outer MPC controller（把状态驱入 invariant terminal set）与 inner controller（保持 RPI）。 | 只用于确认双层术语，不引用其定理、算法细节或实验结果。 |
| Kothare, Balakrishnan, Morari, *Robust constrained model predictive control using linear matrix inequalities*, 1996, DOI [10.1016/0005-1098(96)00063-5](https://doi.org/10.1016/0005-1098(96)00063-5) | **本轮仅核对 Caltech 正式页面与摘要** | 将 plant uncertainty、输入/输出约束与 robust state-feedback MPC 放入 LMI。 | 经典约束反馈综合是强基线，但本轮未取得全文，不能据此声称其条件直接覆盖 correlated `A(T),W(T)` 或 intermittent-output-feedback tube。 |

全文门槛由 Hassaan 2021、Tahir 2010 和 Tahir--Jaimoukha 2012 满足；后两篇只按其实际 uncertainty/set class 使用，不把摘要或搜索结果当证明。

## 2. 必须分离的两个证书层

令真实状态为 `x`，名义状态为 `z`，tracking error 为 `e=x-z`。Hassaan 的证明顺序可写成：

### A. tracking/ancillary 层

先选择 `K_c`（必要时随 dropout phase/path 变化），对 estimator error、过程扰动和重定心误差构造可靠集合 `S_c^j`，使

\[
e^+=(A(T)+BK_c)e+w_{\rm proc}+w_{\rm est/recenter}
\in S_c^{j^+}
\]

对所有允许数据模式转移、推力和扰动成立，同时得到 correction-input 集

\[
U_c^j=K_c S_c^j.
\]

这是 disturbance RPI/RCI 或 path-dependent tube 问题。Tahir 2010/2012 直接属于这一层。

### B. nominal terminal 层

只有 A 层闭合后，才能定义共同 tightened sets

\[
X_{\rm tight}=\bigcap_j(X\ominus S_c^j),\qquad
U_{\rm tight}=\bigcap_j(U\ominus U_c^j).
\]

随后才寻找 nominal terminal feedback `K_f` 与 `X_f`，使对所有允许 nominal LPV vertices/modes 有

\[
(A(T)+BK_f)X_f\subseteq X_f,
\quad X_f\subseteq X_{\rm tight},
\quad K_fX_f\subseteq U_{\rm tight},
\]

并满足 terminal cost decrease。Hassaan Assumption 2 与 Theorem 6 使用的是这一层。这里不应再把过程扰动直接加进 nominal terminal dynamics；它已由 A 层误差 tube 吸收。

因此 Run132 的“joint `K_f/X_f` synthesis”若直接采用 Tahir 的 disturbance-RPI LMI，会把 `K_c,S_c` 错标成 `K_f,X_f`，既没有生成 phase-dependent tightening，也无法实例化 Hassaan 的递归可行性假设。

## 3. certificate class 与当前合同的匹配审计

Tahir 2010 的 hyperrectangle 类不能进入实现。第37章已对更强的控制权限证明：对 `p^+=p+hv`，任何有限位置半宽与正速度半宽的 origin-centered Cartesian product 都在 `(p,v)=(P,V)` 处一步越界；而非零 residual 又排除 `V=0`。这不是 SDP 求解失败，而是整个集合类被精确否定。

固定形状椭球没有被该反例排除，但两篇 Tahir 方法仍未直接匹配当前合同：

1. 当前横向模型是 measured-current、arbitrary-future-jump 的 LPV family，而不是单一 LTI；
2. `A(T)` 与 `W(T)` 由同一推力 `T` 配对，`\bar d(T)=1.880+T(0.45)^3/6`。把 `A` uncertainty 与一个 global disturbance box 独立组合，会重新引入 Run35 已识别的假阴性；
3. 仓库只对 polyhedral predecessor 证明了连续 `T` 到 endpoint pairs 的精确归约，不能未经证明把这个结论搬到椭球 S-procedure；
4. 完整六状态的 estimator/recenter contribution、vertical residual 与 correction-input 分配尚未冻结，故 `X_tight,U_tight` 目前没有可填入优化器的数值定义。

一个语义正确的 A 层有限证书至少要保持 paired vertices：对每个同一推力端点对 `(A_i,W_i)` 检查

\[
(A_i+BK_c)E\oplus W_i\subseteq E,
\quad E\subseteq X_e,
\quad K_cE\subseteq U_{\rm corr},
\]

并加入 estimator/recenter 误差；不能检查所有 `A_i` 与所有 `W_j` 的无条件笛卡尔积后，把额外保守性写成物理不可行。若采用非多面体集合，还需另证 endpoint reduction 或直接覆盖连续区间。

## 4. 最强基线、推翻条件与准入结论

最强同条件比较不应是“随机搜索一个 static K”，而是：

1. 保持 correlated `(A(T),W(T))` 的 certificate-based ancillary controller/RPI tube；
2. 由其全部 dropout phases 的 worst-case tube 形成 `X_tight,U_tight`；
3. 在这些集合上求 Hassaan-style common nominal `K_f,X_f`；
4. 只有共同 terminal domain 为空或在同预算下造成实质认证损失，才比较 mode-indexed terminal family。

候选路线会被以下结果推翻：任何 admissible A 层证书都因 torque/state constraints 为空；只能通过把 `A(T)` 与 `W(T)` 独立外包才能求解；或得到的 A 层 tube 已使 tightened domain 为空。相反，仅求到一个未纳入 estimator/recenter 的横向椭球，或仅得到 solver feasible 状态，都不满足准入标准。

**直接 joint `K_f/X_f` 实现准入：不通过。双层证书规范与证明顺序纠正：通过。**

本轮不写 SDP/控制代码：已有 box class 被严格否定，ellipsoid/uncertain-system 类又缺少 correlated LPV 与完整六状态误差合同。此时实现只能验证另一个模型，不能推进当前递归可行性证据链。

## 5. 下一轮唯一问题

先冻结六状态 A 层误差动力学：明确过程 residual、SMF estimator error、重定心项、dropout phase、推力信息及 correction-input 预算；随后选择一个**非轴对齐、保持 paired `(A(T),W(T))`** 的可认证 RPI/RCI 类，形成有限 feasibility problem并求得候选或给出该 certificate class 的明确反证。只有 A 层完成后，才恢复 common nominal `K_f,X_f` 综合。
