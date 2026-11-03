# 26 `deltaT*phi` 相关性的精确 support 边界：McCormick 已经够紧，CZ 不是额外收益来源

2026-09-24。接续第25章。上一轮提出比较 independent box / McCormick / CZ-joint representation。本轮得到一个必须先固定下来的理论边界：**对于单个双线性项、矩形源域和线性 support query，McCormick relaxation 已经是凸包，因此任何仅改变为普通 CZ 表示的方案都不可能再降低 support。**

## 1. 最小联合模型

令

\[
d=\delta T\in[-a,a],\quad \phi\in[-b,b],\quad q=d\phi,
\]

当前全域边界取 `a=4.905`, `b=0.45`。考虑任意线性方向

\[
\ell(d,\phi,q)=c_d d+c_\phi\phi+c_q q.
\]

因为固定一个变量后目标对另一个变量是仿射函数，矩形上的最大值必在四个角点。因此 exact graph 的 support 可直接枚举四角得到。

## 2. 一个可直接证明的 gap 公式

独立盒把 `q` 替换为 `[-ab,ab]`，给出

\[
h_{box}=|c_d|a+|c_\phi|b+|c_q|ab.
\]

真实角点必须满足符号奇偶关系 `sign(q)=sign(d)sign(phi)`。若三个系数均非零，则：

- 当 `sign(c_q)=sign(c_d c_phi)` 时，三个独立最优符号兼容，`h_box=h_exact`；
- 当符号不兼容时，必须牺牲三个贡献中至少一个，且最优策略就是翻转最便宜的一个，所以

\[
\boxed{h_{box}-h_{exact}=2\min(|c_d|a,|c_\phi|b,|c_q|ab).}
\]

若任一系数为零，gap 为 0。

这给出了“什么时候保留相关性真的降低 tightening”的必要且充分条件（针对该对称矩形单乘积模型），比泛泛说 CZ 更紧更有用。

## 3. McCormick 与普通 CZ 的边界

单个 `q=d phi` 在 box 上的 McCormick 四个不等式给出其 graph 的凸包。support function 对集合和其凸包相同，因此

\[
\boxed{h_{exact}=h_{McCormick}}
\]

对所有线性方向成立。

Scott et al. 已证明 bounded polytope 可由 constrained zonotope 表示。因此把同一个 McCormick polytope 改写成 CZ，不会创造更小 support。**普通 CZ 的价值只能来自与 SMF 历史约束的统一表示/运算，而不是对单个 box-bilinear convex hull 的额外几何紧化。**

如果要精确保留非凸 polynomial dependency，constrained polynomial zonotope (Kochdumper & Althoff, 2023) 才是表达能力更直接的对象；但对当前线性 MPC tightening 的单步 support，它仍不可能优于 exact convex hull 的 support。

## 4. 对当前四旋翼最小物理映射的反例与正例

取联合输出

\[
y=[d,\;-g\phi-d\phi].
\]

方向 `r=(r_z,r_x)` 对应系数

\[
(c_d,c_\phi,c_q)=(r_z,-g r_x,-r_x).
\]

因此纯水平方向 `r=(0,1)` 有 `c_d=0`，**相关性完全没有 support 收益**：

- exact/McCormick = 6.62175；
- independent box = 6.62175；
- gap = 0。

这直接否定“只要保留 `deltaT*phi` 就一定能缩小 vx tightening”。

但 mixed direction `r=(-1,1)` 给出严格差异：

- exact/McCormick = 7.11225；
- independent box = 11.52675；
- gap = 4.4145。

而相反方向 `r=(1,1)` gap 又为 0。这说明 independent box 丢失的首先是**联合集合的不对称/符号相关结构**，不是每一个坐标半宽。

## 5. 代码验证

新增 `verification/check_bilinear_correlation_hull.py`，固定 seed `20260924` 测试 10,000 个随机 support directions：

- McCormick 与四角 exact support 最大误差 `3.55e-15`；
- 解析 gap 公式最大误差 `3.55e-15`；
- 5002/10000 个随机方向出现 strict independent-box gap；
- 平均 gap `0.3100087410`；
- 本批最大 gap `3.1570853516`。

归档：`results/bilinear_correlation_hull_20260924/checks.json`。

复现：

```bash
python verification/check_bilinear_correlation_hull.py --output /tmp/bilinear.json --seed 20260924 --cases 10000
```

## 6. 文献边界

McCormick (1976) 是 factorable nonconvex program convex relaxation 的经典来源；后续文献明确指出 box 上单个 bilinear graph 的 McCormick relaxation 是标准凸包描述。Müller–Serrano–Gleixner (SIAM J. Optim.) 又说明：只有当 `(d,phi)` 的可行域是 box 的严格非矩形子集时，利用二维投影/额外结构才可能比基础 McCormick 更紧。这一点与 SMF 主线高度相关：**真正可能的新收益不是 CZ vs McCormick，而是 SMF posterior 提供的非矩形相关域能否在线产生更紧、可认证的 bilinear hull/support。**

Kochdumper–Althoff (2023) 的 constrained polynomial zonotope 已支持 quadratic/higher-order maps，因此“用 polynomial zonotope 表示乘积”也不能作为创新。

## 7. 候选创新重新排序

### A. SMF-conditioned bilinear support — 保留并提高精度

把源域从静态 box 改为 SMF posterior projection `P_k`：

\[
(d,\phi)\in P_k\subsetneq[-a,a]\times[-b,b].
\]

研究 `q=d phi` 在 `P_k` 上的 certified support/hull，并只查询真实 MPC normals。若能证明

\[
h_{corr(P_k)}(p)\le h_{McCormick(box)}(p)
\]

且在可刻画条件下严格小于，就能把“SMF 降低 Tube MPC 保守性”落实为明确机制。

### B. CZ representation of box McCormick hull — 否定为创新

普通 CZ 可以作为实现容器，但不能声称比同一 McCormick convex hull 更紧。

### C. polynomial/CZ exact product representation — 降级

已有 constrained polynomial zonotope 文献覆盖 quadratic maps；除非与 SMF-conditioned online certification 形成新定理，否则不是贡献。

## 8. 下一轮证明义务

下一轮应从 rolling CZ-SMF 后验中提取真实 `(deltaT,phi)` 或相关 scheduling-state 二维投影，而不是继续使用矩形全域。重点：

1. 构造 `P_k` 的 certified polygon/CZ projection；
2. 比较 box McCormick 与 posterior-conditioned hull 的真实 MPC support；
3. 给出严格改善的充分条件和无改善反例；
4. 统计为得到这些 support 需要的 LP 数与墙钟时间；
5. 若 posterior 根本不约束 `deltaT`（它是自由控制量），则必须承认 SMF 无法直接提供 `(deltaT,phi)` 联合域，并转向 scheduling/decision-dependent robust MPC，而不能伪造相关 posterior。

第5点是下一轮最重要的模型语义审计。
