# 33 语义一致 LPV 候选的 torque-RPI 有限时域否证

日期：2026-09-24。承接第32章。第32章已经严格证明候选反馈在无扰动 LPV 家族上 common-quadratically stable；本章检查更强也更必要的问题：在第12章语义一致 residual contract 下，是否存在包含原点、且满足 `|K e|<=0.08` 的 RPI error tube。

## 1. 模型合同

只取会进入 torque feedback 的横向四状态

\[
e=[p_x,v_x,\phi,\omega]^\top,
\]

\[
e^+=M(T)e+w,\qquad M(T)=A(T)+BK,
\]

其中 `vx+=vx-h*T*phi`，`h=0.02`，`h/J=1`，并沿用第31/32章已经认证 nominal stability 的

\[
K=[0.1425749515,0.2006738212,-1.1714620252,-0.2286054551].
\]

第12章保留 `-T phi` 后，水平 residual 为

\[
r_x=aero_x+T(\phi-\sin\phi),
\]

全域安全界为

\[
|r_x|\le 1.880+14.715\,0.45^3/6=2.1034840625.
\]

因此离散 additive disturbance 至少包含

\[
W_x=\{[0,h r_x,0,0]^\top: |r_x|\le d_x\}.
\]

这里没有重新加入 `(T-g)phi`，所以不存在第25章的模型合同错误。

## 2. 不需要无限尾项的否证

固定 `T=14.715` 本身就是允许的 scheduling path。对该固定闭环，原点出发 N 步 disturbance reachable set 为

\[
R_N=\bigoplus_{i=0}^{N-1}M^iW_x.
\]

任意包含原点的 RPI 集 `E` 必须满足 `R_N subseteq E` 对所有 N 成立。因此若某个有限 N 已有

\[
h_{R_N}(K)>0.08,
\]

则必有 `h_E(K)>0.08`，从而不可能同时满足真实 torque correction 约束 `|Ke|<=0.08`。这是必要条件否证，不依赖 mRPI 无限和的 tail approximation。

对线段 disturbance，support 可精确累加：

\[
h_{R_N}(K)=\sum_{i=0}^{N-1} d_x h\, |K M^i e_{v_x}|.
\]

## 3. 数值结果

实际运行 `verification/check_lpv_torque_rpi_obstruction.py`。

使用完整语义 residual `d_x=2.1034840625` 时，`T=14.715`：

- N=25：`h=0.06506334999`；
- N=50：`h=0.08029718766 > 0.08`；
- N=100：`h=0.09155849807`；
- 1000 项有限和：`0.09228806639`。

因此第 **50 项**已经给出严格硬输入否证。

为了判断失败是否只是 `sin(phi)-phi` Taylor remainder 导致，又做了更乐观的 lower-bound contract：完全删除 nonlinear remainder，仅保留 `|aero_x|<=1.880`。即使如此，在同一个 `T=14.715` 固定路径上，第 **69 项**已有

\[
h_{R_{69}}(K)=0.08003032078>0.08,
\]

1000 项达到 `0.08248294717`。所以当前 K 的失败不是粗糙 P-ball 假阴性，也不是 nonlinear Taylor remainder 单独造成；**仅仓库当前 aero bound 就足以否定该 K 的 robust torque tube。**

作为负对照，固定 `T=4.905` 与 `T=9.81` 的 1000 项 support 在完整 residual 下分别约 `0.06707` 与 `0.079264`，未越界。问题集中在高推力 vertex，因此不能用 hover-only RPI 代替整个 LPV contract。

## 4. 结论等级

**严格否定：** 第31/32章这个特定 K 虽然 nominal LPV stable，但在当前全域 residual contract 下不存在包含原点、同时满足 `|Ke|<=0.08` 的 RPI error tube。理由是固定高推力路径的有限 reachable set 已经违反输入 support；任何 RPI 必须包含它。

**没有否定：** 这不证明语义一致 LPV Tube MPC 不可行，也不证明所有反馈 K 都失败。它只否定当前 hover-DARE K。也不能把第31章 rolling CZ 的 `331/468` support gap 当作控制性能收益，因为该 normal 来自一个已经被 hard-input certificate 淘汰的 controller。

## 5. 对创新方向的影响

候选“CZ-SMF posterior correlation -> certified tightening on this ancillary input normal”必须降级：几何 gap 仍是真实数值事实，但不再具有正式控制器语义。

下一步不应继续优化 CZ representation，而应做**约束感知 ancillary synthesis**：直接把高推力 vertex 的 finite reachable torque support / RPI input margin 纳入 K 搜索目标。可比较：

1. common-P / vertex-stable 且最小化 `max_T h_R(K)` 的反馈；
2. gain-scheduled `K(T)`，但必须补 scheduling-dependent tube 与递归可行性；
3. 缩小 residual contract 只有在额外物理假设/SMF 在线认证可严格支持时才允许，不能为了让 K 通过而修改扰动界。

真正值得保留的候选创新不是“CZ 更紧”，而是：**SMF posterior 是否能提供经过认证的在线 residual/scheduling 收缩，使一个约束感知 ancillary tube 相对 global worst-case tube 严格扩大可行域，同时保持 shift nesting。** 在此之前，先找到至少一个在 global contract 下通过 torque-RPI 的 K；若不存在，再证明 actuator-authority obstruction。

## 6. 文献边界与复现

Raković–Kerrigan–Kouramas–Mayne, IEEE TAC 2005 已给出 mRPI 外逼近理论；本章只使用更基础的必要事实：RPI 必须包含所有有限 disturbance reachable sets。因此有限时域反例足以否证，不需要把 1000 项和误称为严格 mRPI。

运行：

```bash
python verification/check_lpv_torque_rpi_obstruction.py \
  --output /tmp/lpv_torque_rpi_obstruction.json
```

归档：`results/lpv_torque_rpi_obstruction_20260924/checks.json`。运行环境：Python 3.13.5, NumPy 2.3.5, SciPy 1.17.0。
