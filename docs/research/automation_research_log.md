# 自动研究日志

## 2026-09-23 — 任意多等式 CZ 支持查询认证

### 本轮问题

第 20 章固定后验实验只能对“3 潜变量 + 1 等式”的 CZ 重建原始顶点。连续 SMF 历史会产生多条等式，因此当前性能证书不能直接进入滚动 CZ 后验。本轮目标是补齐一般 \(A\xi=b\) 的可信支持查询接口，并核对它是否与现有文献创新边界冲突。

### 查阅/核对文献

1. Scott et al., *Automatica* 2016 — CZ 定义、精确集合运算与复杂度约减。
2. Le et al., CDC-ECC 2011 — zonotopic SMF 与 tube MPC 已有组合先例。
3. Rego et al., *Automatica* 2020 — nonlinear set-valued estimation 的 CZ guaranteed propagation/update。
4. Cong, Wang, Zhou, *Automatica* 2025 — SMF 初值稳定性与快速 CZ-SMF。
5. Qiu et al., IET CTA 2020 — ellipsoidal set-membership output-feedback MPC。

完整摘要见 `docs/literature/READ_PAPERS.md`。

### 理论推进

对 \(\mathcal Z=\{c+G\xi:A\xi=b,\|\xi\|_\infty\le1\}\) 和方向 \(p\)，任意乘子 \(\lambda\) 给支持上界

\[
U=p^\top c+\lambda^\top b+\|p^\top G-\lambda^\top A\|_1.
\]

任意经精确核验的成员 \(\xi^f\) 给下界 \(L=p^\top(c+G\xi^f)\)。因此原始/对偶证书可以解耦：数值 LP 只负责产生提案；有理数验证决定是否接受。原始重建失败不影响安全上界。

### 代码实验

`python verification/check_generic_cz_support_certificate.py --output /tmp/generic_cz_support.json --seed 20260923 --cases 600`

600 个随机有理数、多等式 CZ 全部重建出精确成员并通过 \(L\le h^\star\le U\) 审计；本批样例最大认证 gap 为 0。3 项单元测试通过。不能据此声称任意病态 CZ 都可一次重建成功。

### 保留候选与下一步

保留“可行性与性能双证书驱动的控制相关集合计算”。下一步把认证器接入连续 `predict/observe` 历史 CZ，并主动搜索 LP 数减少但总墙钟更差的反例。

---

## 2026-09-23 — 后验收缩与 observer/nominal center 漂移

### 本轮问题

检查一个递归可行性中容易被隐藏的推理：若 SMF 后验绝对集合 \(X^+\subseteq X^-\)，重新选择 observer/nominal center 后，误差 tube \(E=X-z\) 是否自动收缩？

### 新核对文献

- Köhler et al., IJRNLC 2021：RAMPC 的 set-membership update 需要 monotonic/non-increasing 条件来支撑 recursive feasibility / robust constraint satisfaction。
- Lu, Cannon, Koksal-Rivet, IJRNLC 2021：固定复杂度参数集合 + robust tube MPC，证明 recursive feasibility 与 ISS。
- Peschke & Mönnigmann, IJRNLC 2023：明确指出围绕 nominal trajectory 的 tube 在 nominal model 改变时递归可行性证明困难，并显式处理 model/target update。
- Köhler et al., Automatica 2023：CCM-based RAMPC，允许更一般 set-membership update，并在 planar quadrotor 上给数值验证。

因此“nominal 更新会影响 feasibility”不是新发现；创新候选必须更窄。

### 理论结论

设 \(E^-=X^--z^-\)、\(E^+=X^+-z^+\)。对 protected direction \(p\)，

\[
h_{E^+}(p)\le h_{E^-}(p)
\]

当且仅当

\[
h_{X^+}(p)-p^\top z^+\le h_{X^-}(p)-p^\top z^-.
\]

令 \(\delta z=z^+-z^-\)、\(\Delta h_p=h_{X^-}(p)-h_{X^+}(p)\)，得到中心漂移预算

\[
-p^\top\delta z\le \Delta h_p.
\]

这说明 posterior shrinkage 本身不足以保证 recentered tube shrinkage。该条件可以直接使用第 21 章的 certified CZ support query 实现。

### 精确反例

\[
X^-=[-1,1],\quad X^+=[-0.9,0.9],\quad z^-=0,\quad z^+=0.9.
\]

虽然 \(X^+\subset X^-\)，但

\[
E^-=[-1,1],\quad E^+=[-1.8,0],
\]

故误差 tube 包含失败。

### 代码实验

新增 `verification/check_recenter_support_budget.py`，固定 seed=20260923 做 10,000 个嵌套区间压力测试：

- 任意选择 posterior 内 nominal center 时，1,150/10,000（11.5%）出现“绝对后验收缩但 recentered error set 不再包含”的反例；
- 方向 support-budget 判断与真实 1D 包含结果 10,000/10,000 一致；
- posterior midpoint 在这个 1D interval 特例中 0/10,000 失败，但不推广到一般高维 CZ。

结果归档 `results/recenter_support_budget_20260923/checks.json`。

### 被否定/收缩的说法

- “SMF 后验集合变小，所以 Tube MPC 的误差 tube 一定变小”：否定。
- “只要 point estimate 保持在 posterior 内就能安全 recenter”：否定；精确反例和随机压力测试均给出反例。
- “中心漂移问题本身可作为创新”：否定；adaptive tube MPC 已明确处理 nominal-model update。

### 当前保留候选

把 **recenter update 转化为 MPC protected directions 上的 support-budget certificate**，并与 anytime CZ support query 合并。只有支持预算通过才允许 nominal/observer center 更新，否则保持旧 nominal、限制 center shift 或追加 support query。

这比“CZ + Tube MPC”更具体，也更接近可证明的新接口，但尚未完成首次性排重和高维闭环收益验证。

### 下一轮关键证明/实验

进入六维 rolling CZ：使用非零、真值一致测量制造真实 posterior center 漂移；比较 fixed nominal、posterior-center recenter、budget-limited recenter；构造违反预算后 tightened constraint 或 shifted candidate 失效的高维反例。若预算过严，再研究以 protected support shrinkage 为约束的 center-selection LP/QP。
