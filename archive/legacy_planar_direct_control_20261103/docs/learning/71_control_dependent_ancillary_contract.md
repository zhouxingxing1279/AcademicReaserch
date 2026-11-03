# 71. 六状态 ancillary 合同：推力修正的必要性与控制相关调度

日期：2026-09-29。承接第35章的 vertex-consistent residual 与 Run 133 的双层证书分离。本章只冻结当前六状态**跟踪误差层**的数学合同；不把它误称为完整六自由度四旋翼保证。

## 1. 状态、名义模型与信息变量

令

\[
x=(p_x,p_z,v_x,v_z,\phi,\omega),\qquad
z=(z_{p_x},z_{p_z},z_{v_x},z_{v_z},z_\phi,z_\omega),
\]

分别为真实外环状态与名义状态；定义 tracking error 与 estimation error

\[
e=x-z,\qquad \eta=x-\hat x,
\]

于是控制器可见的估计偏差为

\[
\hat x-z=e-\eta.
\]

把真实输入拆成

\[
T=\bar T+\delta T,\qquad
\tau=\bar\tau+\delta\tau,
\]

其中 `bar` 量由名义 MPC 选择，`delta` 量由 ancillary/output-feedback law 产生。一个线性特例是

\[
\begin{bmatrix}\delta T\\\delta\tau\end{bmatrix}
=K_c^j(e-\eta),
\]

但下文不预设它必须是静态线性反馈。

名义小角度模型取

\[
\begin{aligned}
z_{p_x}^+&=z_{p_x}+hz_{v_x},&
z_{p_z}^+&=z_{p_z}+hz_{v_z},\\
z_{v_x}^+&=z_{v_x}-h\bar T z_\phi,&
z_{v_z}^+&=z_{v_z}+h(\bar T-g),\\
z_\phi^+&=z_\phi+hz_\omega,&
z_\omega^+&=z_\omega+h\bar\tau/J.
\end{aligned}
\]

真实外环采用第12、35章的全域合法余项合同

\[
v_x^+=v_x-hT\phi+hr_x,\qquad
v_z^+=v_z+h(T-g)+hr_z,
\]

\[
|r_x|\le d_x(T)=1.880+T\frac{0.45^3}{6},\qquad
|r_z|\le d_z(T)=2.086+T\frac{0.45^2}{2}.
\]

仓库配置目前把额外过程噪声设为零；模型文档提到的未知力矩扰动尚无数值界。因此本章的角速度式只属于冻结 benchmark，不能外推为物理力矩扰动保证。

## 2. 精确六状态 tracking-error 递推

逐式相减得到

\[
\begin{aligned}
e_{p_x}^+&=e_{p_x}+he_{v_x},\\
e_{p_z}^+&=e_{p_z}+he_{v_z},\\
e_{v_x}^+&=e_{v_x}-h\bar T e_\phi-h\delta T z_\phi-h\delta T e_\phi+hr_x,\\
e_{v_z}^+&=e_{v_z}+h\delta T+hr_z,\\
e_\phi^+&=e_\phi+he_\omega,\\
e_\omega^+&=e_\omega+h\delta\tau/J.
\end{aligned}
\tag{71.1}
\]

横向式也可写成

\[
e_{v_x}^+=e_{v_x}-hT e_\phi-h\delta T z_\phi+hr_x.
\tag{71.2}
\]

式 (71.1) 显示 Run 133 的简单

\[
(A(T)+BK_c)E\oplus W(T)\subseteq E
\]

仍未冻结正确对象：当 `delta T` 是反馈决策时，`T=bar T+delta T` 不再是独立外生 scheduling variable；同一个实际 `T` 还决定 `d_x(T),d_z(T)`。此外 `delta T z_phi` 把误差层与名义轨迹耦合，而 `delta u=K_c^j(e-eta)` 又把 estimator error 引入控制图。

## 3. 推力修正为零时不存在紧致六状态 RPI

**命题 71.1（torque-only ancillary 的精确否定）。** 假设 `delta T=0`，允许余项在

\[
r_z\in[-d_z(T),d_z(T)]
\]

内逐步任取，其中合法推力下 `d_z(T)>0`。则不存在非空紧致 tracking-error RPI 集。

**证明。** 若紧致非空集合 `E` 鲁棒正不变，连续坐标 `e_vz` 在 `E` 上取得最大值 `M`；取一个满足 `e_vz=M` 的点。选择合法余项 `r_z=d_z(T)`。由 `delta T=0`，

\[
e_{v_z}^+=M+h d_z(T)>M.
\]

后继不可能属于 `E`，与鲁棒正不变矛盾。证毕。

这个结论只使用 outer residual 合同，不依赖集合形状、`delta tau`、反馈增益或求解器。因此任何完整六状态紧致 ancillary tube 都必须保留推力修正权限，或者改写 vertical residual/nominal model 合同；torque-only 非轴对齐集合也无法绕过该障碍。

## 4. 正确的有限证书对象

一条语义正确的 mode-edge 证书至少要对允许边 `j -> j+` 检查联合图：

\[
\begin{gathered}
e\in S_c^j,\quad \eta\in E_\eta^j,\quad
(z,\bar u)\in Z_{\rm adm}^j,\\
\delta u=\kappa_j(e-\eta,z,\bar u),\quad
\bar u+\delta u\in U,\\
T=\bar T+\delta T,\quad
|r_x|\le d_x(T),\quad |r_z|\le d_z(T),\\
e^+=F_e(e,\eta,z,\bar u,r),\qquad e^+\in S_c^{j^+}.
\end{gathered}
\tag{71.3}
\]

这里 `E_eta^j` 必须是来自可靠 SMF/observer 分析的 mode-dependent estimation-error 外包，而不是把当前 posterior state set直接当作未来过程扰动。输入余量自然是 `U-bar u`，不应先验地把 nominal 与 correction 权限重复占用。

候选数值技术可以是 configuration-constrained polytope/vertex control、augmented `(e,eta)` polytope，或对联合图使用 GSIP/separation oracle；但这些是证书工具，不是新贡献。任何有限化还必须证明连续实际推力与 residual graph 被覆盖，不能把 `A(T)` 和 `W(T)` 无条件做笛卡尔积后，用所得不可行否定原问题。

## 5. 与最近邻的边界

Mulagaleti--Bemporad 2025 已对 quasi-LPV self-scheduling 与 configuration-constrained polytopic RCI 给出联合建模和 vertex-control 证书；Wehbeh--Kerrigan 2025 及 Wehbeh--Kerrigan--Scaccia 2026 已把 state/control-dependent uncertainty 写成 GSIP，并以 worst-case separation 检查稳健约束。Hanema--Lazar--Tóth 2020 的 LPV tube 则明确使用外部且当前可测的 scheduling variable，不能直接覆盖式 (71.1) 中由反馈决定的实际推力。

因此本章不声明新 RCI 算法。可审查的新信息只是：把仓库的六状态 ancillary 语义写对，并用命题 71.1 排除 torque-only 分支。

## 6. 证据等级与下一步

- **已证明：**式 (71.1) 的代数递推；在当前 vertical outer residual 下，`delta T=0` 时不存在非空紧致六状态 tracking-error RPI。
- **合同纠正：**实际推力是控制相关 scheduling；简单 exogenous paired-endpoint RPI 不是当前完整 output-feedback 证书。
- **未决：**存在推力修正时，联合 `(e,eta,z,bar u)` 图是否存在满足硬约束的非轴对齐 RCI；其有限证书复杂度；由该 tube 导出的 nominal terminal domain；六自由度物理余项接口。

下一唯一问题：从 rolling SMF 构造或否定一个对 15-mode bounded-dropout automaton 有效的、time-uniform `E_eta^j` 包络，并逐边核查 estimator-error containment。没有这个包络，式 (71.3) 不能数值实例化，继续选 RPI 形状没有证据意义。
