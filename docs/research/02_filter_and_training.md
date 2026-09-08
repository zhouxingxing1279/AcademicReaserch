# 02 集员滤波与模型训练算法

## 1. 先完成可核查的区间基线

状态箱 X=[l,u]，中心 c=(l+u)/2、半径 r=(u−l)/2。对线性映射 Wx+b：

$$c'=Wc+b,\quad r'=|W|r,$$

或使用上下界形式 \(l'=W^+l+W^-u+b,\ u'=W^+u+W^-l+b\)，其中 W⁺=max(W,0)、W⁻=min(W,0)。tanh 单调，因此输出界为 [tanh(l'),tanh(u')]。两层逐层递推得到 aθ(X,u) 的 IBP 界；sin/cos 要检查区间内极值，不能只计算端点。全部下界向下舍入、上界向上舍入才是严格区间实现。

对 M1 直接区间传播：

$$X^-_{k+1}=\operatorname{Box}\bigl(X_k+h f_c^0(X_k,u_k)+hE_ca_\theta(X_k,u_k)\bigr)\oplus W_\theta.$$

逐项计算会重复使用 x 并丢失依赖，是保守外包络，不是精确可达集。保持同一传播方法比较 A/B/C/D，避免把集合表示改善混入训练收益。

对于观测第 j 个状态 y_j=x_j+v_j、|v_j|≤vbar_j：

$$l_j^+=\max(l_j^-,y_j-\bar v_j),\quad u_j^+=\min(u_j^-,y_j+\bar v_j).\tag{F1}$$

没有观测的分量不修改。任意 l_j⁺>u_j⁺ 为 EMPTY_SET，保留日志后停止该次保证声明，不能自动放大噪声界并把运行算作成功。该基线不能利用位置-速度相关性，可能无法有效修正速度误差；若长时宽度持续增长，这可能是箱表示的不足，而非 SMF 原理失败。

## 2. 更紧的 zonotope 基线

### 2.1 表示及支持函数

$$Z(c,G)=\{c+G\xi:\|\xi\|_\infty\le1\},\quad G\in R^{n\times p}.$$

线性映射 AZ+b=Z(Ac+b,AG)，Minkowski 和通过拼接生成元得到。方向 a 的支持函数为

$$h_Z(a)=a^Tc+\|G^Ta\|_1.\tag{F2}$$

这一公式仅对普通 zonotope 成立；有等式约束的 CZ 必须解对应 LP 或使用有效对偶上界。

### 2.2 非线性预测的中心线性化

固定实际输入 u，令 F=Fθ，选择 A_c=∂F/∂x(c,u)。对所有 x∈Z：

$$F(x,u)=F(c,u)+A_c(x-c)+r_{nl}(x).$$

使用覆盖整个 Z 的 Hessian 绝对上界 \(\bar H_{j,ab}\)：

$$|r_{nl,j}|\le\frac12\sum_{a,b}\bar H_{j,ab}\,r_a^{box}r_b^{box},\quad r^{box}=|G|\mathbf1.\tag{F3}$$

于是

$$Z^-_{k+1}=Z\bigl(F(c,u),[A_cG,\operatorname{diag}(\bar r_{nl}+\bar w_\theta)]\bigr).\tag{F4}$$

Hessian 是网络+物理模型的整域上界；自动微分在中心得到的 Hessian 不够。备选是区间 Jacobian：用均值定理界定 (J(X)−A_c)(X−c)，可能较松但不要求二阶可微。tanh 便于平滑导数，ReLU 不得直接套 F3。

### 2.3 测量条带更新及推导 [DERIVED]

给定测量 y=Cx+v，v=Vζ，|ζ|∞≤1，任意增益 Λ 都有

$$x=c+G\xi+\Lambda(y-Cc-CG\xi-v)$$

$$=c+\Lambda(y-Cc)+(I-\Lambda C)G\xi-\Lambda V\zeta.$$

因此条带与原集合的交集被下式包含：

$$c^+=c+\Lambda(y-Cc),\quad G^+=[(I-\Lambda C)G,-\Lambda V].\tag{F5}$$

可取最小化生成元 Frobenius 范数的增益：令 P=GGᵀ、R=VVᵀ，

$$\min_\Lambda\operatorname{tr}((I-\Lambda C)P(I-\Lambda C)^T+\Lambda R\Lambda^T),$$

对 Λ 求导置零得

$$\Lambda=PC^T(CPC^T+R)^{-1}.\tag{F6}$$

这是几何目标下的代数解，不将 P/R 解释为真实协方差。R 正定时可解；实现用 solve，不显式求逆。若加正则仅改变 Λ，F5 的包含性对任意 Λ 仍成立，但不能再称原目标精确最优。F5 外包络未必是 Z 的子集；需要额外相交才能声称不扩张。可选择 Λ=0 作保守基线，但同样保持旧集合时要避免无用生成元。

### 2.4 可选 CZ 精确测量约束

将观测噪声变量加入：

$$x=c+[G,0]\begin{bmatrix}\xi\\\zeta\end{bmatrix},\quad
[CG,V]\begin{bmatrix}\xi\\\zeta\end{bmatrix}=y-Cc,\quad |\xi|,|\zeta|\le1.$$

这精确保留线性观测交集（在输入预测集合为精确给定集合的意义下），代价是约束/变量增长。CZ 只是后续可选更紧基线，不预先宣称 CZ 本身创新。

### 2.5 降阶规则

G=[G_keep,G_drop] 时，以 diag(|G_drop|1) 外包 dropped 生成元：

$$Z(c,G)\subseteq Z(c,[G_{keep},\operatorname{diag}(|G_{drop}|\mathbf1)]).\tag{F7}$$

冻结预算，如每步最多 n×5=30 个生成元，保留排序准则在验证集确定。不要直接删除生成元。CZ 不得直接删除等式仍声称同一集合；删除等式给出更大集合但可能非常松，必须记录预算与松弛代价。

## 3. 集员包含性命题 [CONDITIONAL，标准归纳]

假设 x0∈X0，真实一步动态包含于预测映射+Wθ，真实测量误差属于 V，所有传播/修正/降阶均为外包络运算。若 xk∈Xk，则实际使用 uk 后 xk+1∈Xk+1^-。测量到达时真值满足观测条带，故属于交集及其外包络；缺失时保留先验。归纳得到所有域内时刻 xk∈Xk。

此结论不保证：时间序列集合嵌套；宽度趋零；观测性；MPC 可行；连续时间约束满足。每步采样都包含也不证明采样间安全。

## 4. 训练数据与标签

G1 解析轨道允许训练数据拥有仿真真值；在线控制接口不允许。加速度标签取解析真值模型的 a_*(s,β) 或离散速度增量扣除名义增量：

$$\tilde a_k=\frac1h\begin{bmatrix}v_{x,k+1}-v_{x,k}\\v_{z,k+1}-v_{z,k}\end{bmatrix}-\begin{bmatrix}-T\sin\phi/m\\T\cos\phi/m-g\end{bmatrix}.$$

真实日志中差分速度含噪且误差被1/h放大；需记录标签生成器、滤波延迟与误差界。不能把 SMF 中心产生的伪标签当成无误差真值。优先用多步输入输出拟合或区间标签，但这是后续扩展，不混入首轮 A/B/C/D。

## 5. 四组模型与可实现损失

训练前冻结结构、数据、优化步数、初始化 seed 和调参预算。用固定尺度 S_a 对输出误差归一化。

$$L_{fit}=\frac1{B}\sum_{j=1}^{B}\|S_a^{-1}(a_\theta(s_j)-\tilde a_j)\|_2^2.$$

- A：L_fit。
- B：L_fit+λ_J mean(||∂aθ/∂s||_F²)，Jacobian 正则只是训练指标，不是全域 Lipschitz 证书。
- C：L_fit+λ_set mean(Σ_i width_Q(X_i^-))；从同一 X0 开始，在损失展开期间关闭所有测量修正，以隔离纯预测可达集目标。
- D：相同 L_fit 与权重预算，展开实际测量更新和丢测模式，优化后验集合宽度。

$$width_Q(X)=\sum_{j=1}^6 q_j\frac{u_j-l_j}{s_j^{state}},\quad
s^{state}=[5,3,3,3,0.45,2]^T,$$

初版 q_j=1/6；速度等未直接测得维度的宽度单独报告，避免位置条带直接截断主导结果。训练后用 zonotope/CZ 的支持函数也计算同一定义的轴向宽度，不能比较不一致单位的体积。

对一个训练窗口和噪声实现 ν：

$$L_D(\theta)=L_{fit}+\lambda_{set}\frac1B\sum_b \max_{\sigma\in\Sigma_{M,H}}\sum_{i=1}^H width_Q(X_{b,i}^{\theta,\sigma,\nu_b}).\tag{T1}$$

H=25；每5 tick一次位置机会，最多5个二值事件，最多32种枚举模式，过滤超过连续2次丢包者，携带窗口起点的相位和先前丢包计数。角度/角速率测量在所有组的真实评估中都存在；C 仅训练损失展开时关闭修正。做“仅保留持续姿态修正”的 C_variant 作为次要消融，不替代冻结主对比。

T1 对丢包模式可在短窗口精确枚举，但对测量噪声只使用训练样本，是经验训练目标；不是最坏噪声证书。更长窗口采用模式采样/对抗搜索时，明确从 exact_schedule_max 降级为 sampled_schedule_max。

## 6. 可微实现及残差界的一致性

IBP、tanh、max/min 可通过 PyTorch 自动微分；交集的不可微边界使用其子梯度。空交集不能 clamp 成零宽度：该 batch 标记 invalid，并施加一致性惩罚或拒绝 checkpoint。若使用平滑 max/min，平滑结果只用于训练代理，不能自动当作安全集合。

可微代理可能投机，因此每个 checkpoint 都用独立不参与梯度的集合实现重放验证。

残差处理两种可接受实现：

1. 第一版在所有候选参数允许范围上使用已证明有效的统一 W_train（可能很保守）；训练后分别认证 Wθ，报告统一界及各自界两套结果。
2. 交替训练/认证：每轮固定网络→认证界→在受控参数邻域内推导新网络变化界→训练→重新认证。未经邻域变化界，不能把旧网络的 Wθ 固定后任意更新权重，还继续声称训练展开覆盖真值。

早期训练使用经验 W 也允许，但标记 EMPIRICAL_TRAINING_PROXY，最后评价必须使用合法重新计算的包络。学习损失不是安全证书，不能因优化成功自动升格。

## 7. 训练伪代码（待实现）

```text
freeze(data_split, architecture, state_scaling, masks, seeds, tuning_budget)
for initialization_seed in seeds:
    initialize identical parameters for A, B, C, D
    for method in methods:
        for batch in training_episodes:
            pred_loss = supervised_residual_loss(batch)
            if method uses set loss:
                for allowed mask in enumerate_masks(batch.phase, batch.miss_counter):
                    X = common_initial_set(batch)
                    width_cost = 0
                    for t in window:
                        X = predict_outer(X, actually_recorded_u[t], model, proxy_error_bound)
                        if D and measurement_arrives(mask,t+1):
                            X = measurement_outer_update(X, recorded_y[t+1], noise_bound)
                        assert_or_penalize_nonempty(X)
                        width_cost += normalized_width(X)
                    append(width_cost)
            update_parameters(loss)
        certificate = certify_model_over_domain(model)
        evaluate_on_validation(model, certificate, independent_filter_implementation)
select hyperparameters on validation only
freeze checkpoint hashes and certificates before opening test set
```

训练窗口必须保留所有预定测量机会的潜在带噪观测，再按每个 mask 隐藏；不能把原日志已经缺失的值凭空补作真实观测。解析模拟可以离线生成这些观测，各组共用噪声实现。

训练控制序列来自离线日志，所有组相同；闭环测试各组可以产生不同动作，使用相同环境初值、噪声种子与丢测模式配对。

## 8. 关键对照与复杂度

必须区分真实不确定性与外包络冗余：用低维大量样本/局部精确优化构造“可达样本内集”只作为冗余诊断，不作为真值外包络证书。如果 D 把漏包当成宽度优化，不接受。

箱预测成本大致与网络矩阵乘法一致；zonotope 预测增至 O(n²p) 并增加余项认证；CZ 支持函数每方向需要 LP。训练枚举增加最多32倍窗口开销，可GPU批处理；在线不训练网络。记录真实耗时，不以复杂度阶数替代实时性测量。
