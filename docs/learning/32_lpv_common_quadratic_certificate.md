# 32 LPV ancillary 候选获得 common-quadratic 稳定证书

日期：2026-09-24。承接第31章：此前 hover DARE 候选只通过 frozen-vertex 与有限 switching-product 反例搜索，本章补上对整个 `T∈[4.905,14.715]` 的严格 common-quadratic 稳定证书。注意：这只闭合**无扰动 LPV ancillary 稳定性**，尚未闭合 RCI tube、硬输入约束与 terminal append。

## 1. 模型与候选反馈

沿用语义一致模型

\[
e^+=A(T)e+B\tau,\quad e=[p_x,v_x,\phi,\omega]^\top,
\]

其中 `vx+=vx-h*T*phi`，且

\[
\tau=Ke,\quad K=[0.1425749515,0.2006738212,-1.1714620252,-0.2286054551].
\]

闭环记为 `M(T)=A(T)+BK`。由于 `A(T)` 对标量 T 仿射，`M(T)` 也仿射。

## 2. Common quadratic certificate

找到对称矩阵

\[
P=\begin{bmatrix}
0.074753239&0.053671859&-0.096346099&-0.005511332\\
0.053671859&0.099182069&-0.203617926&-0.014759493\\
-0.096346099&-0.203617926&0.819244229&0.056456306\\
-0.005511332&-0.014759493&0.056456306&0.006820464
\end{bmatrix}.
\]

`lambda_min(P)=0.002844724644>0`。在两个 thrust 端点，

- T=4.905：`lambda_min(P-M'PM)=6.188232256e-4`；
- T=14.715：`lambda_min(P-M'PM)=6.188357202e-4`。

因此端点均严格衰减。

### 为什么只查端点足够

写 `M(T)=M0+T D`。对任意固定 x，

\[
f_x(T)=x^\top M(T)^\top P M(T)x
\]

关于 T 是凸二次函数，因为二次项系数

\[
x^\top D^\top P D x\ge0.
\]

凸函数在闭区间上的最大值出现在端点之一。因此若两个端点都满足

\[
M(T)^\top P M(T)\prec P,
\]

则区间内所有 T 都满足同一不等式。这给出对任意 thrust scheduling sequence 的 common-quadratic 稳定证书，而不再依赖第31章有限长度 switching enumeration。

在 P-metric 中两个端点的最大 generalized eigenvalue 分别为 `0.9928285648` 与 `0.9991271756`，故统一可取

\[
\|M(T)e\|_P\le 0.9995634926\|e\|_P.
\]

这个 contraction 很弱但严格小于 1。1001 点 dense grid 的最小 decay eigenvalue 与端点下界一致，仅作为实现交叉检查，不参与证明。

## 3. 本轮排除与保留

**被排除：**“该 K 可能因为 arbitrary switching 而不稳定”这一阻塞对当前仿射标量 thrust family 已被 common P 消除。第31章的有限 switching 搜索现在只保留为历史 falsification test。

**不能推出：** common P 不意味着 additive disturbance 下存在满足 `|tau|<=0.08` 的可接受 RCI tube。尤其最坏 contraction 接近 1，粗糙的 P-ball disturbance bound 很可能极保守。因此不能把 K 写入正式 baseline config，也不能宣称 recursive feasibility/ISS 已闭合。

## 4. 与现有文献边界

Hanema–Lazar–Tóth (*Automatica*, 2017, DOI 10.1016/j.automatica.2017.07.046) 已给出 LPV tube MPC 的 periodically contractive terminal set/cost、recursive feasibility 与 stability；所以 common-quadratic/LPV terminal certificate 本身不是创新。Sala (*Automatica*, 2019, DOI 10.1016/j.automatica.2019.01.032) 进一步研究离散 polytopic LPV 的 decay-rate stability 与参数轨迹相关证书。2024 年 Meijer–Dolk–Heemels 又研究 poly-quadratic Lyapunov certificate 的 nonexistence certificates。我们的 common P 只是把候选控制器变成后续 SMF-CZ tightening 研究可合法使用的基础对象。

## 5. 当前候选创新的状态

第31章发现 rolling CZ 在真实 input normal `±K` 上相对 coordinate box 有 331/468 次严格 support gap；本章现在消除了“K 只是数值稳定候选”的主要稳定性缺口。因此候选 A 得到加强：

> **CZ-SMF posterior correlation → certified support reduction on a common-quadratically stable ancillary controller's real input normals.**

但创新是否成立仍取决于下一关：加入语义一致的 nonlinear/aero remainder 后，构造 robust invariant error tube，并证明 CZ support gap 能转化为正的 torque margin / feasible-set inclusion。若 RCI 后 `h_E(K)>=0.08`，则该方向仍失败。

## 6. 可复现验证

```bash
python verification/check_lpv_common_quadratic_certificate.py \
  --output /tmp/lpv_common_quadratic.json
```

归档：`results/lpv_common_quadratic_20260924/checks.json`。

## 7. 下一轮

1. 从现有第12/25章 disturbance contract 中只保留与 `A(T)` 语义一致的 aero + `sin(phi)-phi` remainder，禁止重复计入 `(T-g)phi`。
2. 计算该 disturbance 对 common-P / zonotopic RCI 的影响，首先审计 `h_E(±K)<0.08` 是否可能成立。
3. 若 coarse P-ball 因 `lambda≈0.99956` 失败，不据此否定控制器；改用 direction-aware zonotope/CZ RPI 或 finite-sum + certified tail。
4. 只有 hard torque tube 通过后，才把 common-P K 升级为 baseline ancillary，并继续 terminal append / shifted-candidate recursive-feasibility proof。
