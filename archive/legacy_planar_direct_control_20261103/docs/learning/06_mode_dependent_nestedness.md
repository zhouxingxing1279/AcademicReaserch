# C2：六维误差集合、未来模式与 MPC 嵌套接口

日期：2026-09-16。承接 [C1](05_intermittent_error_interface.md)。

**本轮完成 C2 的估计与集合嵌套推导，但控制使用准入被明确否定：统一 Young 标量递推配合未求交的椭球收紧，即使初始误差为零，第3步也无法满足原 ±3 m/s 速度约束。该反例否定这一保守接口组合，不否定物理系统或所有输出反馈 MPC。下一任务为 C2-R 传播保守性修复；不进入训练。**

关键修正有两项：仅有标量变小不能比较不同模式的椭球；重新计算的窗口证书不能不经预测上界截断就直接替换 MPC 初值。本轮不训练 RL，不改物理合同。

## 1. 固定合同与六维度量

沿用六维平面系统，状态次序为 $(p_x,p_z,v_x,v_z,\phi,\omega)$；这是六个状态，不是完整三维六自由度飞行器。位置可平移到高度平衡点，误差不变。记 $z=x-\hat x$，标量证书记 $e$，避免二者混淆。

采用 C1 的 $h=1/50$、$\eta_0=19/20$、$\ell_x=5$、$\ell_z=9/2$、$p_x=120$、$p_z=60$。角状态每 tick 用直接测量重置。定义

```math
V_j(z)=\eta_0^j\left[120(z_{p_x}-jh z_{v_x})^2+z_{v_x}^2
+60(z_{p_z}-jh z_{v_z})^2+z_{v_z}^2\right]
+z_\phi^2+z_\omega^2=z^\top P_jz,\quad 0\le j\le14.
```

这是原坐标的加权度量，位置/速度/角度的权重含相应单位，不把数值大小解释为无量纲物理误差。$P_j$ 在坐标对 $(p_x,v_x)$、$(p_z,v_z)$ 上分别放置 C1 的 $P_{x,j},P_{z,j}$，角度块取 $I_2$。

若零时刻位置机会失败，模式为 $j=5$，该标签仍适用；不把它解释为已经存在五步前的成功包。初始证书直接由原先验和已到达测量计算，后继边仍按自动机。

对每个平移块，令

```math
t_{\nu,j}=\eta_0^j[p_\nu+1+p_\nu(jh)^2],\quad
\delta_{\nu,j}=\eta_0^{2j}p_\nu.
```

正定二阶矩阵满足 $\lambda_{\min}\ge\det/\operatorname{tr}$、$\lambda_{\max}\le\operatorname{tr}$。因此可显式取

```math
\underline\alpha=\min\{1,\min_{\nu,j}\delta_{\nu,j}/t_{\nu,j}\},\qquad
\overline\alpha=\max\{1,\max_{\nu,j}t_{\nu,j}\},
```

从而 $\underline\alpha\|z\|_2^2\le V_j(z)\le\overline\alpha\|z\|_2^2$。它们对应所选数值坐标下的 $\alpha_5(r)=\underline\alpha r^2$、$\alpha_6(r)=\overline\alpha r^2$；不是最紧谱常数。

## 2. 六维噪声映射：显式保留当前角噪声

沿用 [因果模型 06](../theory/06_causal_augmented_model.md) 的线性中心预测，并在竖直成功校正使用 $9/2$。预测必须使用实际执行推力、力矩；使用未执行输入将破坏以下抵消关系。

在原状态域和输入域内，定义

```math
D_x=1.880+4.905(0.45)+14.715(0.45)^3/6,\qquad
D_z=2.086+14.715(0.45)^2/2.
```

令 $w_x=d_x+R_x,w_z=d_z+R_z$。原始有界向量取

```math
d=(w_x,w_z,n_\phi,n_{p_x}^+,n_{p_z}^+,n_\phi^+,n_\omega^+)^\top,
\quad |d|\le b=(D_x,D_z,0.005,0.02,0.02,0.005,0.01)^\top.
```

这里当前角噪声是当前测量产生的同一个量，满足 $z_\phi=-n_\phi$；可与状态、过程余项及其他噪声相关。把它外包在盒中只增加后继，不要求任何独立性或零均值。

记 $\gamma=1$ 为成功位置校正，否则为 0。逐项相减得到

```math
z^+=A_\gamma z+G_\gamma d,
```

其中 $A_\gamma$ 的两个平移块分别为 C1 的 $A_\gamma(\ell_x),A_\gamma(\ell_z)$，角度齐次块为零；按原状态次序

```math
G_\gamma=\begin{bmatrix}
0&0&0&-\gamma&0&0&0\\
0&0&0&0&-\gamma&0&0\\
h&0&hg&-\gamma\ell_x&0&0&0\\
0&h&0&0&-\gamma\ell_z&0&0\\
0&0&0&0&0&-1&0\\
0&0&0&0&0&0&-1
\end{bmatrix},\qquad g=9.81.
```

尤其成功时 $z_{v_x}^+=-\ell_xz_{p_x}+(1-\ell_xh)z_{v_x}+h(w_x+gn_\phi)-\ell_xn_{p_x}^+$，未遗漏创新项。

**适用范围：**这是直接角测量更新后的估计轨迹接口。当前角噪声被放入有界输入，不能由此声称对任意未重置的六维 $(x,\hat x)$ 已满足原论文全空间 observer 假设，也不能据此得到同度量的增量 IOSS 证书。离开原物理域时上述 $D_x,D_z$ 不再自动有效。

## 3. 可靠统一增益与标量预测

对所有允许边 $j\to j'$，C1 平移块与零角块给出

```math
A_\gamma^\top P_{j'}A_\gamma\preceq(19/20)P_j.
```

令 $d=\operatorname{diag}(b)\xi$，$|\xi_i|\le1$，$\bar G_\gamma=G_\gamma\operatorname{diag}(b)$。Young 不等式给出

```math
V_{j'}(z^+)\le aV_j(z)+\frac{99}{4}\xi^\top Q_{j,j'}\xi,
\quad a=99/100,\quad Q_{j,j'}=\bar G_\gamma^\top P_{j'}\bar G_\gamma.
```

两种合法计算方式：

1. 欧氏扰动形式：$c_d^{\rm upper}=(99/4)\max\operatorname{tr}(Q_{j,j'})$，则附加项不超过 $c_d^{\rm upper}\|\xi\|_2^2$。这是对最大特征值的可靠上界，不伪称求得精确 $\lambda_{\max}$。
2. 保留盒：$c_\Box=(99/4)\max_{j\to j'}\max_{s\in\{-1,1\}^7}s^\top Q_{j,j'}s$。PSD 二次函数在盒上凸，每点是顶点凸组合，最大值必可在顶点取得。17 条边各 128 个顶点可用有理数精确核查。

后续固定使用较直接的盒递推

```math
F(e)=ae+c_\Box,\qquad
F^i(e)=a^ie+\frac{1-a^i}{1-a}c_\Box.
```

所有成功边取得同一最大噪声能量，独立闭式为

```math
\max s^\top Qs=120\varepsilon_p^2+
[h(D_x+g\varepsilon_\phi)+5\varepsilon_p]^2
+60\varepsilon_p^2+[hD_z+(9/2)\varepsilon_p]^2
+\varepsilon_\phi^2+\varepsilon_\omega^2.
```

结果 JSON 同时记录精确分数和显示小数。$e_\infty=c_\Box/(1-a)$ 仅是此保守递推的不动点，不是实际稳态误差，也不意味着从任意初始值立即被该值覆盖。全域余项、独立盒及 Young 分离均引入保守性，不能仅凭 $a<1$ 判断当前 MPC 有可行解。

| 已核查常数 | 显示小数（精确分数见 JSON） |
|---|---:|
| $\underline\alpha$ | 0.4453381643 |
| $\overline\alpha$ | 121 |
| $c_d^{\rm upper}$，归一化欧氏扰动形式 | 2.5436500667 |
| $c_\Box$，盒递推的常数项 | 3.2980673638 |
| $e_\infty$ | 329.8067363823 |

### 3.1 原速度约束下的解析阻断

对水平或竖直速度法向，$h_{\mathcal E_j(e)}(c)^2=e\eta_0^{-j}\ge e$。任何平移后的对称椭球要包含在速度区间 $[-3,3]$ 内，必要条件为 $e\le9$；改变 nominal 中心不能缩小集合宽度，加入控制 tube 也不能使该宽度减少。

由于在线 $e_t\ge0$，统一未来预测必满足

```math
e_{3|t}=F^3(e_t)\ge c_\Box(1+a+a^2)>9.
```

故所有模式、所有非负初始误差界下，第3步的**完整椭球或其并集**已经无法满足速度约束；原 horizon=25 包含该步。这是精确有理不等式，不依赖采样、MPC 求解器、增量反馈或终端候选。

此结论仅针对“统一 Young 递推 + 未求交的椭球收紧”组合。若额外保留经认证的方向约束/相关性并求交，或采用更紧的合法模式传播，集合可能变小；其可行性必须另证。不能通过把未来尚未得到的测量证书预先当作已知，来降低预测半径。

## 4. SMF 支持证书与不可省略的预测截断

为避免有理数验证器处理平方根系数，将 $P_j=L_j^\top L_j$ 改写成等价的加权有理方向分解：

```math
V_j(z)=\sum_{r=1}^6 w_{j,r}(q_{j,r}^\top z)^2,
```

其中六个 $q$ 分别抽取 $z_{p_x}-jh z_{v_x},z_{v_x},z_{p_z}-jh z_{v_z},z_{v_z},z_\phi,z_\omega$，权重为 $(120\eta_0^j,\eta_0^j,60\eta_0^j,\eta_0^j,1,1)$。在线候选仍是 12 个有明确度量来源的正负方向；权重在本周期冻结。

令 $X_t^c$ 为给定历史和初始合同的相容集。窗口外包 $B_t$ 必须包含它。验证器针对当前 $z=x-\hat x_t$ 和当前模式 $j_t$ 返回双侧上界 $b_{r,+},b_{r,-}$，则

```math
\beta_r=\max\{0,b_{r,+},b_{r,-}\},\qquad
e_t^{\rm cert}=\sum_rw_{j_t,r}\beta_r^2
\quad\Longrightarrow\quad V_{j_t}(x-\hat x_t)\le e_t^{\rm cert}.
```

`max(0,...)` 避免把带符号支持直接平方造成实现歧义。真值相容且集合非空时至少一侧支持非负；若可靠性检查报告空集冲突，应处理模型/数据合同故障，不能把空集当作零误差。每次接受 `min(old,verified)`，故本周期证书非增。模式或中心变化后必须重新计算或严格转换支持边界，不能照抄旧方向数值。

实际交给 MPC 的值必须为

```math
e_0=e_0^{\rm certified},\qquad
e_{t+1}=\min\{F(e_t),e_{t+1}^{\rm cert}\}.
```

**证明。**初始相容真值被 $e_0$ 覆盖。若当前被 $e_t$ 覆盖，第 3 节保证下一真值被 $F(e_t)$ 覆盖；独立窗口证书也覆盖同一个真实后验误差，故两者最小值仍覆盖。归纳得到

```math
V_{j_t}(x_t-\hat x_t)\le e_t,\quad
e_{t+1}\le F(e_t),\quad
F^i(e_{t+1})\le F^{i+1}(e_t).
```

窗口遗忘后新外包可能变宽，这不破坏上述标量关系，因为预测证书被独立保留。无新证书/超时采用 $F(e_t)$。若希望显式状态集合也包含预测信息，可保留交集 $B_t\cap(\hat x_t+\mathcal E_{j_t}(e_t))$，或作为分开的证明约束；不能把椭球约简丢弃后仍声称集合保持该包含。

截断的必要性反例：令重新计算值为 $e_{t+1}^{\rm cert}=F(e_t)+1$，它仍可能是可靠的松上界，但直接采用它已经违反 $e_{t+1}\le F(e_t)$。可靠性和预测一致性是两个不同要求。

此外，调度奖励应与 MPC 真正读取的 $e=\min\{e^{\rm pred},e^{\rm cert}\}$ 对齐。当证书仍大于预测上界时，继续降低 $e^{\rm cert}$ 尚未产生控制接口收益。此时两侧互补之外还存在预测截断阈值，不能把未穿过阈值的改进统计为已实现控制收紧。

## 5. 三种未来模式处理与严格关系

定义 $\mathcal E_j(e)=\{z:z^\top P_jz\le e\}$，$S_i(j)$ 为从 j 出发走 i 条允许边后能达到的模式集合。未来包到达情况未知，不能只选成功分支。

| 处理 | 未来误差集合 | 关系及成本 |
|---|---|---|
| 全模式包络 | $\mathcal E_{\rm all}(e)=\bigcup_{j=0}^{14}\mathcal E_j(e)$ | 最简单；可能含当前步不可能出现的模式 |
| 可达模式包络（本轮选定） | $\mathcal U_{i|t}=\bigcup_{j\in S_i(j_t)}\mathcal E_j(F^i(e_t))$ | 不松于全模式；每层至多15项，无需指数场景树 |
| 模式路径条件 tube | 每条路径分别传播 $a e+c_{j,j'}$ 及控制 tube | 潜在更紧；需单独证明路径合并、tube 半径与非预见性 |

本轮只采用第二种，共享标量 $F^i(e_t)$，控制决策保持同一 nominal 策略，不允许根据尚未收到的包提前选择输入。按终点模式做精确可达递推，可将模式集合压缩为15位 mask。

**命题：移位后的误差包络嵌套。** 对任意实际允许边 $j_t\to j_{t+1}$ 及 $i\ge0$，

```math
S_i(j_{t+1})\subseteq S_{i+1}(j_t),\qquad
\mathcal U_{i|t+1}\subseteq\mathcal U_{i+1|t}.
```

证明第一式只需在新路径前补上已经发生的一条边。第二式由第 4 节的标量移位界以及**同一个终点模式内**的椭球单调性推出。不能直接写 $\mathcal E_{j'}(e')\subseteq\mathcal E_j(e)$，因为两个矩阵不同。

严格比较见证：对水平速度法向 $c=(0,0,1,0,0,0)$，

```math
h_{\mathcal E_j(e)}(c)^2=e\eta_0^{-j}.
```

已知当前模式0时包络支持为 $\sqrt e$，全模式包络为 $\eta_0^{-7}\sqrt e$，对 $e>0$ 严格更大。这只是方向上的严格见证；既不宣称所有方向严格改进，也不宣称15个椭球彼此按 age 排序。反例取 $e'=0.9e,j'=14,j=0$，尽管标量下降，该速度方向支持仍增大。

全模式包络与可达模式包络一般非凸。对线性约束，使用其凸包不改变支持值；不能因而声称一般非线性约束或后继传播也不受凸化影响。

## 6. 控制收紧与条件移位命题

定义 nominal 状态 $\bar x$、估计中心 $\hat x$，控制侧 tube 条件为 $V_\delta(\bar x,\hat x)\le s$。在未来模式集合 $S$ 下，采用联合不确定对

```math
\mathcal C(\bar x,s,e,S)=\{(\hat x,x):V_\delta(\bar x,\hat x)\le s,
\ x-\hat x\in\bigcup_{j\in S}\mathcal E_j(e)\}.
```

收紧要求对集合中**全部** $(\hat x,x)$ 都有 $(x,\kappa(\hat x,\bar x,\bar u))\in\mathcal Z$。因此减少 e、s 或 S 不会删除原先可行的同一 nominal 决策，只要终端条件也对这些量向下闭合且其余参数不变。

例如另有可靠增量误差集 $\Delta(s)$ 满足 $\hat x-\bar x\in\Delta(s)$，线性状态约束 $c^\top x\le d$ 可收紧为

```math
c^\top\bar x+h_{\Delta(s)}(c)
+\max_{j\in S}\sqrt{e\,c^\top P_j^{-1}c}\le d.
```

若反馈为 $u=\bar u+K(\hat x-\bar x)$，联合约束 $H_xx+H_uu\le b$ 的第 r 行可用

```math
(H_x\bar x+H_u\bar u)_r+
h_{\Delta(s)}((H_x+H_uK)_r^\top)
+\max_{j\in S}\sqrt{e\,(H_x)_rP_j^{-1}(H_x)_r^\top}\le b_r.
```

这只是给定合法 $K,\Delta$ 后的支持公式，不表示仓库中已有合格增益。

**条件移位命题。** 假设既有控制构件能保证：

- 保持移位 nominal 轨迹，$\bar x_{i|t+1}=\bar x_{i+1|t}$；
- $s_{0|t+1}\le s_{1|t}$，且 $s^+=\rho s+\gamma(e)$ 对 $(s,e)$ 单调，常数覆盖全部允许模式；
- 终端集合/控制对全部允许后继模式闭合，并对 e、s 向下闭合；
- 初始可行、实际输入一致，所有涉及余项的源状态与输入均处于已验证域。

则由 $e_{i|t+1}\le e_{i+1|t}$、$s_{i|t+1}\le s_{i+1|t}$ 和第 5 节得到

```math
\mathcal C(\bar x_{i|t+1},s_{i|t+1},e_{i|t+1},S_i(j_{t+1}))
\subseteq
\mathcal C(\bar x_{i+1|t},s_{i+1|t},e_{i+1|t},S_{i+1}(j_t)).
```

故非终端各级收紧约束可继承旧解，末端由假设的终端控制补齐。这替换了固定 observer metric 下的集合嵌套步骤。若改用 nominal 重新置中，必须另加相应中心偏移证书；不能仅凭半径变小沿用本式。

**本轮没有证明上列控制构件成立。** 尤其观测误差收缩不能代替估计中心对 nominal 的 tube 传播，也不能代替 $\hat f-f$ 注入界与增量稳定反馈。递推不动点很大时，收紧可能已为空；这必须在进入控制实验前判定。

## 7. 与主参考的准确对应

核查原文：[Köhler、Müller、Allgöwer, arXiv:2105.03427v1](https://arxiv.org/pdf/2105.03427)。作者第一名为 Johannes，04 的作者首字母 L. 应改为 J.。

- §III-C，式(17)、Theorem 2：支持“集员界与观测预测界取最小值”的接口。本轮增加有限模式和可靠支持上界适配。
- §IV-B，Theorem 4 Part I，PDF第10–11页：核查标量移位、tube 移位、联合不确定对嵌套这三个分开的环节。本轮重写的是模式相关集合的环节。
- Assumption 3 的注入界、Proposition 2 的控制 tube，以及 Assumption 7 的终端构件仍须具体核查。§III-C 的集合估计路线无需机械沿用 IOSS 标量更新；这不等于原 Theorem 4 的其他前提自动删除或已经满足。

上述段落定位为文献依据；第1–6节是本项目条件下的推导，不作为原论文现成结论引用，不主张这些基础集合恒等式本身是论文创新。

## 8. 精确核查与下一任务

```bash
python verification/check_mode_nestedness.py --output /tmp/mode_nestedness.json
```

只用标准库 `Fraction`。输出路径必须不存在。脚本核对全部六维度量的谱包络、17条边的齐次矩阵条件、2176个噪声盒顶点、成功边的独立闭式、预测时域内的模式移位关系、严格支持见证和两个负对照；保存来源哈希。有限步图检查是实现核查，一般时域的证明在第5节。脚本不是定理证明器，不测试 RL 或闭环轨迹。

结果见 [exact_checks.json](../../results/theory_mode_nestedness_20260916/exact_checks.json)。

**下一唯一任务 C2-R：修复未来误差传播的保守性。** 首先保留每条允许模式边的噪声能量 $q_{j,j'}=\max_{|\xi|\le1}\|\bar G_\gamma\xi\|_{P_{j'}}^2$，使用三角不等式的半径传播

```math
r^+\le\sqrt{\eta_0}\,r+\sqrt{q_{j,j'}},\qquad r=\sqrt e,
```

按未来终点模式取所有前驱路径的最大值，重新验证移位与原约束非空必要条件。该界不引入 $99/4$ 的 Young 常数，但不预先声称已经足够。先给出通过或否定证据；若仍阻断，再报告是否必须保留方向相关集合，而不盲目搜索控制增益、不缩小原噪声合同。只有误差接口可用后才进入 observer 注入、增量反馈与终端的 C3 核查。

本轮状态：C2 估计/集合代数成立；统一椭球控制接口被否定，转 C2-R；完整控制合同、学习独立优势、实际跟踪改善均未通过。新增计算是精确代数核查，不是飞行实验或独立同行评审。
