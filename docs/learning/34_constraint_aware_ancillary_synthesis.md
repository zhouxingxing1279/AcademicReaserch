# 34. 约束感知 ancillary synthesis：第33章不是 actuator-authority 不可能性证明

## 1. 本轮问题

第33章严格否定了 hover-DARE 候选反馈：在允许的固定高推力路径上，仅有限 disturbance reachable set 已使 `h_R(K)>0.08`。但该结论只否定**那个 K**，不能外推成“当前执行器权限下不存在任何 robust ancillary controller”。本轮主动搜索反例，目标是尝试推翻这种过度解释。

语义保持与第31--33章一致：

\[
e^+=M(T,K)e+w,\qquad T\in[4.905,14.715],
\]

\[
w=[0,\;h r_x,\;0,\;0]^\top,\qquad |r_x|\le 2.1034840625,\quad h=0.02.
\]

硬约束至少包括

\[
|Ke|\le0.08,\qquad |v_x|\le3,\qquad |\phi|\le0.45.
\]

对固定允许推力 T，定义有限 reachable set

\[
R_N(T,K)=\bigoplus_{i=0}^{N-1}M(T,K)^iW.
\]

任意包含原点的 RPI 集 E 都必须包含 `R_N`，所以 `h_{R_N}(p)` 是任何 RPI tightening 在方向 p 上的**必要下界**。这使我们能快速否证候选，但通过有限和绝不是充分证书。

## 2. 反例：torque-only 可行反馈确实存在

使用固定 seed `20260924` 的 SciPy differential evolution，以 endpoint spectral radius 和 150--400 项 torque reachable support 为目标进行启发式搜索，得到

\[
K_{\tau}=[0.00153696,\;0.00744545,\;-0.09093386,\;-0.09567285].
\]

三个 frozen-thrust 顶点的谱半径均小于 1：约 `0.9951253, 0.9945032, 0.9951253`。1000 项 torque support 分别只有

\[
0.00753,\quad0.00948,\quad0.01216 < 0.08.
\]

因此第33章**不能升级为 actuator-authority impossibility theorem**：至少从固定顶点稳定性和有限 torque reachable lower bound 看，存在远离 0.08 的反馈候选。

但它通过把误差 tube 放大到了不可接受的状态范围来换取 torque 裕度。在低推力 `T=4.905`：

\[
h_{R_{1000}}(e_{v_x})=9.7573>3,
\qquad
h_{R_{1000}}(e_{\phi})=0.8058>0.45.
\]

所以 torque-only synthesis 是错误研究目标。

## 3. joint state/input trade-off 压力测试

第二次搜索同时惩罚 normalized supports

\[
\max\left\{
\frac{h_R(K)}{0.08},
\frac{h_R(e_{v_x})}{3},
\frac{h_R(e_\phi)}{0.45}
\right\}.
\]

得到代表性候选

\[
K_b=[0.01360726,\;0.41658618,\;-3.07723811,\;-0.52653095].
\]

其三个顶点的 1000 项 torque support 为 `0.06328, 0.06822, 0.07257`，但低推力处仍有

\[
h_{R_{1000}}(e_{v_x})=3.9778>3,
\qquad
h_{R_{1000}}(e_\phi)=0.451106>0.45.
\]

此外该候选的 endpoint spectral radii 约 `0.99931--0.99934`；虽然小于1，但没有 common-Lyapunov certificate，不能称为 LPV robust stable controller。

## 4. 本轮严格结论与非结论

**已严格成立（针对每个被审计的固定 T 和给定 K）**：有限 reachable support 是任何 origin-containing RPI set 的必要下界；因此只要该下界超过硬约束，该 K 必然不可行。

**数值观察**：存在 torque support 很小的稳定 endpoint 候选，故第33章的旧 K 失败不能解释为执行器权限本身不可能；但状态约束与 torque 约束存在明显 trade-off，低推力 `T=4.905` 是当前瓶颈。

**尚未证明**：是否存在一个 K 同时满足连续 thrust family 的 robust stability、完整 state/input constraints、additive remainder 下的 RPI invariance。随机/启发式搜索失败不能作为不存在证明。

## 5. 文献边界

Kothare--Balakrishnan--Morari (Automatica 1996, DOI 10.1016/0005-1098(96)00063-5) 已将 polytopic/model uncertainty、worst-case performance 与 input/output constraints 统一为 LMI robust MPC synthesis；因此“约束感知 K synthesis”本身不是创新。

Pluymers--Kothare--Suykens--De Moor (ACC 2006) 进一步把 mixed state/input constraints 和 polyhedral invariant sets 纳入 robust state-feedback synthesis，以减少 ellipsoidal constraint handling 的保守性。当前工作必须把这些作为 synthesis baseline，而不是把“同时优化 K 和 invariant set”声明为贡献。

## 6. 保留的候选创新

本轮不新增一个算法创新，而是把候选空间收缩为三条可证伪路线：

1. **Baseline synthesis**：先用成熟 LMI/polyhedral RCI 方法寻找合法 `K,E`。这是工具链，不是创新。
2. **SMF-conditioned tightening**：只有 baseline `K,E` 合法后，才检查 rolling CZ posterior 在真实 `K^T q_u`、state、terminal normals 上是否严格优于 box/ellipsoid，并把 support gap 映射为 nominal feasible-set 增益。
3. **若线性 K 不存在**：再研究 gain-scheduled / controlled-invariant policy，而不是直接宣称 actuator impossibility。不存在性必须来自优化 dual certificate、RCI emptiness certificate 或解析必要条件，而不是 heuristic search。

## 7. 下一轮证明义务

优先建立一个**可证书化的 joint state/input synthesis**。最低要求是：

- 对 thrust polytope 顶点求 common quadratic / polyhedral invariant certificate；
- 把 `|v_x|<=3`, `|phi|<=0.45`, `|Ke|<=0.08` 直接放进 synthesis/audit；
- 对最终候选使用 finite Minkowski lower bound 主动否证，再用安全 tail/RPI outer bound 做充分认证；
- 若不可行，必须区分“所选 controller class 不可行”和“物理执行器权限不可能”。

只有这一层闭合后，CZ-SMF 的几何优势才有资格重新进入主论证。
