# 35. 顶点一致 residual 合同：修正第34章的低推力假阴性

日期：2026-09-24。承接第34章的约束感知 ancillary synthesis。第34章使用统一残差上界
`DX=2.1034840625` 审计所有 thrust 顶点。该做法是安全的，但当 thrust `T`
本身已知并显式进入 LPV 矩阵 `A(T)` 时，它把高推力顶点的 Taylor remainder 也
强加到了低推力顶点，造成额外保守性。本轮只解决这一模型合同问题，并重新判断第34章
的负结果中哪些真正成立。

## 1. 核心问题

语义一致的小角度横向模型为

\[
v_x^+=v_x-hT\phi+h r_x,
\]

\[
r_x=aero_x+T(\phi-\sin\phi).
\]

在全局姿态域 \(|\phi|\le\bar\phi=0.45\) 上，

\[
|\phi-\sin\phi|\le \frac{\bar\phi^3}{6},
\]

因此当 scheduling parameter \(T\) 已知时，合法的顶点相关界是

\[
\boxed{
d_x(T)=1.880+T\frac{0.45^3}{6}.
}
\]

只有在希望构造一个与 T 无关的统一 disturbance box 时，才需要使用

\[
d_x^{global}=d_x(14.715)=2.1034840625.
\]

把这个 global bound 同时用于 \(T=4.905\) 虽然不会破坏安全性，却不能再声称是
“保留 thrust scheduling 后的紧 residual contract”。

三个 thrust 顶点对应：

| T | d_x(T) |
|---:|---:|
| 4.905 | 1.9544946875 |
| 9.81 | 2.028989375 |
| 14.715 | 2.1034840625 |

## 2. 一个 controller-independent 必要条件

考虑固定允许 thrust \(T\) 和持续常值最坏残差 \(r_x\equiv d_x(T)\)。
若闭环稳定并存在包含原点、对该 disturbance 序列鲁棒的有界不变集，则其极限平衡点
必须属于该不变集。由速度平衡式

\[
0=-T\phi_*+d_x(T)
\]

得到

\[
\boxed{
|\phi_*|=\frac{d_x(T)}{T}.
}
\]

因此任意可行 RPI 都必须满足

\[
h_E(e_\phi)\ge \frac{d_x(T)}{T}.
\]

低推力顶点给出

\[
\frac{1.9544946875}{4.905}
=0.3984698649.
\]

相对于硬约束 \(|\phi|\le0.45\)，仅这个 controller-independent 平衡点必要条件就消耗

\[
\boxed{88.55\%}
\]

的姿态权限，只剩约 \(0.05153\) rad 的余量。该结论不依赖所选 K，也不依赖
RPI 外包算法，因此是当前 joint synthesis 必须面对的结构性限制。

这仍然不是“不存在反馈”的证明：0.39847 < 0.45，理论上尚有余量。

## 3. 修正第34章的 balanced candidate

第34章代表性候选

\[
K_b=[0.01360726,\;0.41658618,\;-3.07723811,\;-0.52653095]
\]

在统一 global residual 下低推力审计得到

\[
h_{R_{1000}}(e_\phi)\approx0.451106>0.45,
\]

因此当时被同时标记为 vx/phi 失败。

改用合法的 vertex-consistent \(d_x(4.905)=1.9544946875\) 后，同一 K 得到

\[
\boxed{
h_{R_{1000}}(e_\phi)=0.41915428<0.45,
}
\]

所以原来的低推力 phi violation 是**由统一高推力 residual 带来的假阴性**，必须修正。

但是

\[
h_{R_{1000}}(e_{v_x})=3.69608551>3,
\]

故该 K 仍被严格否定，只是失败原因应改为以低推力速度约束为主，而不是同时宣称姿态约束失败。

这说明后续 controller synthesis 不能一边把 T 当已知 scheduling 参数，一边在 disturbance
通道中又丢弃这种 T 依赖；否则会人为增加保守性，再错误归因于 actuator/controller 本身。

## 4. 30,000 个静态反馈的可复现实验

新增
`verification/check_vertex_consistent_ancillary_search.py`，固定随机种子
`20260924`，在

\[
K_{p_x}\in[0.005,1.2],\quad
K_{v_x}\in[0.01,3],
\]

\[
K_\phi\in[-6,-0.02],\quad
K_\omega\in[-3,-0.01]
\]

上进行 30,000 点 Latin-hypercube 搜索。每个 K 对三个 thrust 顶点检查：

1. frozen closed-loop 是否 Schur；
2. 220 项 finite disturbance reachable state supports；
3. 220 项 torque support。

这些 finite reachable supports 是任意 origin-containing RPI 的必要下界，因此“超过硬界”
可以严格淘汰 K；“没有超过”不能证明存在 RPI。

结果：

| 条件 | 数量 |
|---|---:|
| 三个 frozen vertices 均 Schur | 12,666 / 30,000 |
| Schur 且 finite torque support ≤ 0.08 | 1,196 |
| Schur 且 finite state supports 均在硬界内 | 320 |
| 同时通过 state + torque finite 必要条件 | **0** |

220 项指标下最接近的样本为

\[
K=[0.19272811,0.71565484,-3.58018519,-0.99624019],
\]

但其 normalized worst ratio 仍为 1.08824。把这个样本延长到 2000 项后：

\[
\max_T\rho(M(T))=0.99406418,
\]

\[
h_R(p_x)=7.4021>5,\quad
h_R(v_x)=3.3172>3,\quad
h_R(\phi)=0.55366>0.45,
\]

且

\[
h_R(K)=0.0853773>0.08.
\]

因此长时审计明确淘汰该“最佳样本”。

**结论等级：** 这是有固定 seed、固定搜索域的数值 falsification evidence，不是 static K 不存在的证明。
启发式/采样搜索的失败不能替代 invariant-set/controller synthesis 的不可行性证书。

## 5. 文献边界

约束感知 controller/invariant co-design 本身已有成熟基础，不能作为创新点。

- Tahir & Jaimoukha, *Robust Positively Invariant Sets for Linear Systems subject to model-uncertainty and disturbances*, IFAC 2012, DOI: 10.3182/20120823-5-NL-3013.00032：同时计算 RPI set 和 controller，并显式考虑 model uncertainty、disturbance 及 state/input constraints。
- Ben Sassi & Girard, *Controller synthesis for robust invariance of polynomial dynamical systems using linear programming*, Systems & Control Letters 2012, DOI: 10.1016/j.sysconle.2012.01.004：在 bounded disturbances 和 input constraints 下联合迭代 controller/invariant synthesis。
- Bujarbaruah, Nair, Borrelli 2020 以及 Wehbeh & Kerrigan 2025 都说明 state/decision-dependent uncertainty 应保留其依赖关系，而非无条件替换为全局统一 uncertainty box；后者还在 planar quadrotor 上比较了 state-dependent 与 uniform uncertainty robust optimal control。

因此本轮的贡献不是提出新的 synthesis 算法，而是**修正仓库自身的 disturbance-contract 语义**，避免一个安全但额外保守的统一 residual 产生错误控制结论。

## 6. 对当前研究方向的影响

当前可以可靠写出的状态是：

1. 第33章严格淘汰旧 hover-DARE K；
2. 第34章正确证明“torque-only 很小不代表 joint constraints 可行”；
3. 但第34章的低推力 phi failure 需要撤回，vertex-consistent residual 下该候选实际满足有限 phi 必要界；
4. 低推力仍然是结构性瓶颈：controller-independent equilibrium 已占用 88.55% 姿态权限，且当前候选主要在 vx 上失败；
5. 30,000 点搜索未发现 static K 通过所有 finite 必要条件，但不存在性仍未证明。

所以现在不能继续围绕 CZ posterior tightening 做性能比较。连一个 global-contract ancillary
baseline 都尚未得到完整证书。

## 7. 下一轮唯一优先问题

下一轮不再扩大随机 K 搜索，而是建立**certificate-based joint state/input synthesis baseline**：

- 使用 vertex-consistent \(W(T)\)，而不是 global \(W_{max}\) 重复制造保守性；
- 在 thrust polytope 上联合求 K 与 ellipsoidal/polyhedral invariant set；
- 把 \(|p_x|\le5, |v_x|\le3, |\phi|\le0.45, |\omega|\le2, |Ke|\le0.08\) 全部直接放入证书；
- 若求得 candidate，再用 finite reachable set 反向攻击，并用 RPI outer/tail certificate 做充分验证；
- 若优化问题不可行，只能称“该 certificate/controller class 不可行”；要上升为 static-K 不存在，还需要 dual/infeasibility certificate 或解析必要条件。

只有这一层通过之后，才能重新问 CZ-SMF 是否相对同一 baseline 严格减少真实 MPC normals 上的 tightening。

## 8. 复现

\`\`\`bash
python verification/check_vertex_consistent_ancillary_search.py \
  --output /tmp/vertex_consistent_ancillary.json \
  --samples 30000 --search-terms 220 --audit-terms 2000 --seed 20260924
\`\`\`

归档结果：
`results/vertex_consistent_ancillary_20260924/checks.json`。
