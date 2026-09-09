# 03 输出反馈 MPC、误差推导与证明义务

## 1. 实现分两级，避免把可运行误认为已证明

- V0 工程原型：神经名义 NMPC + 当前 SMF 状态集合 + 有效开环可达性候选检查。可报告有限预测域检查和经验闭环结果，不能自动宣称递归可行性。
- V1 理论版本：固定离线网络、固定或预先认证的模式相关观测增益、实际估计反馈、增广误差 tube，以及覆盖允许测量切换的终端可行集合。只有完成本章证明义务后才升级理论主张。

名义优化用 CasADi/IPOPT 原型；稳定后移植 acados。求解器成功状态不是鲁棒证书，必须独立检查约束和外包络。

## 2. 实际控制律和点观测器

用 z_i 表示名义状态，v_i 表示名义输入（与测量噪声 ν 区分）：

```math
z_{i+1}=F_\theta(z_i,v_i),\qquad u_i=v_i+K(\hat x_i-z_i).\tag{C1}
```

K 采用负反馈约定，要求局部 A+BK 稳定；若用 dlqr 返回的 K_lqr，则 K=−K_lqr。输入饱和必须在优化/验证中覆盖，不能执行后截断仍按未饱和公式分析。

V1 采用与 zonotope 更新中心一致的观测器：

```math
\hat x_{i+1}^-=F_\theta(\hat x_i,u_i),
```

```math
\hat x_{i+1}=\hat x_{i+1}^-+L_{\sigma_{i+1}}(y_{i+1}-C_{\sigma_{i+1}}\hat x_{i+1}^-).\tag{C2}
```

σ包含已到达传感器集合。丢位置时仍使用姿态/角速率行；完全没有测量才 L=0。Lσ在离线选定并认证，在线 F5用同一 Lσ；生成元降阶不改变中心。若使用 F6 的在线变化增益或额外箱交集重置中心，C2不再是原观察器，必须把重置/增益变化加入预测验证，而非继续照搬以下公式。

## 3. 线性输出反馈增广误差 [DERIVED]

设 x+=Ax+Bu+w，z+=Az+Bv，y+=Cx++ν，η=x−xhat、e=x−z。由 C1：u−v=K(e−η)。

第一步：

```math
e^+=(A+BK)e-BK\eta+w.\tag{C3}
```

第二步：x−xhat=η，实际输入在真值与观测器预测中相同：

```math
x^+-(A\hat x+Bu)=A\eta+w.
```

用测量更新：

```math
\eta^+=(I-LC)(A\eta+w)-L\nu.\tag{C4}
```

增广 ξ=[eᵀ,ηᵀ]ᵀ：

```math
\xi^+=\underbrace{\begin{bmatrix}A+BK&-BK\\0&(I-LC)A\end{bmatrix}}_{M_\sigma}\xi+
\begin{bmatrix}I\\I-LC\end{bmatrix}w+
\begin{bmatrix}0\\-L\end{bmatrix}\nu.\tag{C5}
```

遗漏 −BKη 会低估跟踪误差；把上下两块中的同一 w 视为独立扰动仍可给外包络，但更保守。尽量共享生成元保留依赖。

已附的 verification/run_checks.py 通过直接状态更新与 C5数值比较，并设置遗漏耦合的负对照。这是有限代数核查，不是非线性闭环验证。

## 4. 非线性扩展及余项 [CONDITIONAL]

围绕 (z,v) 选择 A=∂Fθ/∂x、B=∂Fθ/∂u；令 δu=K(e−η)。对真实状态和观测状态分别写

```math
F_\theta(z+e,v+\delta u)=F_\theta(z,v)+Ae+B\delta u+r_x,
```

```math
F_\theta(z+e-\eta,v+\delta u)=F_\theta(z,v)+A(e-\eta)+B\delta u+r_{\hat x}.
```

注意两个展开使用同一个实际输入。代入 C1/C2得

```math
e^+=(A+BK)e-BK\eta+r_x+w,
```

```math
\eta^+=(I-LC)(A\eta+r_x-r_{\hat x}+w)-L\nu.\tag{C6}
```

因此误差外包络递推为

```math
S_{i+1}\supseteq M_{i,\sigma}S_i\oplus D_{i,\sigma},\tag{C7}
```

D包含共享的 w、r_x以及 r_hat、ν。r_x、r_hat必须在由 S_i诱导的整个状态-输入域上认证。只用名义点的余项界无效。可用区间 Hessian 的二阶界，将状态与输入共同组成增广变量；若域太大导致界爆炸，縮短预测域或限定操作域，而非忽略项。

预测未来测量模式时对所有允许 σ分支传播，或取各分支并集的外包络。未来测量值通过 ν和一致模型隐式覆盖，不输入未来真值。动态 L的范围也需覆盖所有可能测量，初版用固定 L避免此复杂性。

## 5. 当前集合初始化与约束收紧

已知 η0∈Ehat0=Xk−xhatk。若选 z0=xhatk，则 e0=η0；应初始化相关集合

```math
S_0=\{[\eta^T,\eta^T]^T:\eta\in Ehat_0\}.\tag{C8}
```

若 z0作为优化变量，令 d=xhatk−z0，则 S0={[d+η;η]:η∈Ehat0}。把 e0、η0独立化会增大保守性。中心若不在 SMF 集内仍可定义误差集合，只需准确平移，不强行假设中心为真值。

给定硬约束 Hx x≤bx、Hu u≤bu，定义 Π_e=[I,0]，Π_η=[0,I]。利用 x=z+Π_e ξ、u=v+K(Π_e−Π_η)ξ：

```math
H_{x,j}z_i+h_{S_i}(\Pi_e^T H_{x,j}^T)\le b_{x,j},\tag{C9}
```

```math
H_{u,j}v_i+h_{S_i}((\Pi_e-\Pi_\eta)^TK^TH_{u,j}^T)\le b_{u,j}.\tag{C10}
```

这是针对估计反馈的输入收紧，不是简单 U⊖K Ehat。普通 zonotope用 F2，CZ支持函数用 LP。LP状态最优也需检查数值残差；若目标是严格上界可保存可行对偶证书并控制舍入，不能把原始可行解的目标下界当支持函数上界。

## 6. 明确的名义优化问题

初版参考轨迹使用平滑段连接，终端进入固定悬停位置；研究稳态跟踪与有限轨迹后悬停，避免未定义的任意时变终端。

```math
\min_{z_{0:N},v_{0:N-1}}\ \sum_{i=0}^{N-1}
\bigl(\|z_i-x_i^{ref}\|_Q^2+\|v_i-u_i^{ref}\|_R^2+\|v_i-v_{i-1}\|_{R_\Delta}^2\bigr)+V_f(z_N),
```

约束：

1. z_{i+1}=Fθ(z_i,v_i)；
2. 初始化 S0按 C8或其自由z0版本；
3. 误差 tube 对所有允许模式满足 C7，所有模型/余项计算域有效；
4. 状态/输入满足 C9/C10；
5. (zN,SN,phaseN,miss_countN)属于认证终端族 T_f。

建议首版 N25、h0.02；Q使用归一化状态误差的diag(10,10,1,1,2,0.2)，R使用归一化输入误差diag(0.1,0.1)，RΔ=0.01I。归一化矩阵在配置中明确，不能直接对有单位物理量套这些数字。

带输入变化惩罚不等于真实输入变化硬约束。若加入 |u_k−u_k−1|≤Δu_max，需增广上一步实际输入，并在 tube/support 中考虑相邻误差依赖；第一版仅作软性能惩罚。

## 7. 可实际落地的求解与独立验证

直接把所有集合操作嵌进 NLP可能很重。采用候选生成 + 保真验证：

```text
receive measurement, mode and timestamp
propagate filter with LAST ACTUAL input; update posterior
check nonempty, model certificate hash, certified domain
warm-start nominal NLP from shifted last solution
for at most 3 iterations within computation budget:
    solve nominal problem with current conservative tightenings
    propagate augmented error sets over candidate causal policy
    validate all state/input constraints, domain and terminal condition
    if certified feasible: accept candidate and store complete certificate
    else update tightenings / reject candidate
if no accepted candidate:
    execute stored backup policy ONLY if its applicability is certified now
    otherwise record NO_CERTIFIED_ACTION and terminate this guaranteed run
apply accepted first action; log actual action, solver and validation times
```

3次是计算预算设计，不是收敛证明。acados/IPOPT只生成候选，外部验证返回 VERIFIED_FINITE_HORIZON 或 VERIFIED_WITH_TERMINAL，不能把二者混用。候选若不能在 deadline内验证，则不能以事后通过补记为实时成功。

V0若仅以开环动作序列传播 X，能验证当前选择的整个开环序列，但下个时刻重新求解后的长期安全仍需后备/终端条件。对预计未来动作假设任意真实状态反馈，会产生不可执行的理想策略；只能使用观测历史可计算策略。

## 8. 递归可行性证明应怎样完成 [OPEN]

### 8.1 必须补齐的假设

A1 初始真值包含、X0处于可行域。
A2 全操作域模型误差、测量噪声和数值外包络有效。
A3 网络固定；实际输入等于验证输入或误差已纳入。
A4 增量可稳定性与传感器模式下的块可检测性，包含剩余测量误差/偏置。
A5 模式自动机正确：phase=0..4，miss_count=0..2，丢包仅发生在位置包机会；从miss_count2的下次机会必须成功接收。每个模式转移的剩余观测仍可能有噪声。
A6 终端控制律、终端集族覆盖所有允许切换、误差和过程噪声。
A7 下个时刻初始tube与旧tube移位兼容；新测量外包络可能更宽时，需保留旧有效预测集合与新一致集合的交集/认证外包络，而非无条件重置为大箱。

### 8.2 终端族的构造任务

先在线性悬停区域固定K、Lσ，为每个自动机节点寻找增广误差 RPI族 Sbarσ，使所有允许 σ→σ'有

```math
M_{\sigma'}\bar S_\sigma\oplus D_{\sigma'}\subseteq\bar S_{\sigma'}.
```

同时构造名义终端控制 vf(z)，及 z的区域 Zfσ，满足收紧约束和下一步终端包含。非线性余项加入D并在区域内认证。可从候选多面体/zonotope族出发，用支持函数LP和区间余项验证；只把验证成功的内可行区域保留。

简单扩大集合的RPI迭代可能不收敛或挤空约束，这是合法失败。不能声称“加一个丢包计数器”就自动建立终端不变性。

### 8.3 移位候选证明骨架

若k时刻有经过认证的因果策略序列，执行首动作后，真值/估计状态落入其第一步预测集合。证明k+1的新信息集由旧分支对应集合包含；删除已执行动作，沿旧策略的当前信息分支继续，末端追加vf。A6保障终端，A7保障初始相容，因而构成k+1可行候选。这个论证需要正式定义信息集、模式和重置操作，本文尚未完成完整非线性证明。

### 8.4 稳定性不能省略

证明终端代价下降条件及扰动影响，例如目标形式

```math
V_{k+1}-V_k\le-\alpha(\|z_k-x^{ref}\|)+\gamma(\|w_k\|+\|\nu_k\|),
```

还要联结估计误差、名义误差和实际误差，得到局部/实用ISS或最终有界。持续扰动下不承诺真值跟踪误差趋零。时变轨迹需额外可行参考和终端设计，本轮先避免。

## 9. 丢测容忍度怎样验证

对 M_packet=0,1,2,... 分别建立模式自动机，搜索满足A1–A7的终端/误差族；得到的是在指定域和设计下的**充分可容忍条件**，不是系统的全局最大可容忍丢包率。

单次位置测量不能统一收缩全部速度/姿态方向。先在线性化可检测性上检查每个允许观测块的加权观测矩阵秩/最小奇异值，再尝试误差Lyapunov不等式。数值正定不等于非线性全域证明；非线性需要域内余项和增量检测条件。

## 10. 命题—工具—证据登记

| ID | 目标 | 验证工具 | 当前状态 |
|---|---|---|---|
| P1 | F5测量外包络 | 代数推导+样本见证 | DERIVED + NUMERIC_CHECK |
| P2 | 状态包含归纳 | 人工证明+区间域证书 | CONDITIONAL；物理认证待做 |
| P3 | C5/C6误差耦合 | 代数+numpy独立更新 | C5已有限检查；C6待完整实现 |
| P4 | 后验训练比预测训练有效 | 冻结A/B/C/D配对实验 | OPEN |
| P5 | 允许丢测下宽度有界 | 模式自动机+LMI/区间校验 | OPEN |
| P6 | MPC递归可行 | 终端集/移位策略正式证明 | OPEN |
| P7 | 闭环实用稳定 | Lyapunov下降+估计误差联结 | OPEN |
| P8 | 计算实时且有外部有效性 | 尾延迟测量+独立三维/PX4 | OPEN |

理论难点无法解决时，可以诚实形成经验方法论文或负结果分析；不能删去假设后沿用定理名称。
