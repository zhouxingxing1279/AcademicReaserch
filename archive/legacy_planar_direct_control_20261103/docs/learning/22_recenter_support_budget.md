# 22 后验收缩不等于 Tube 收缩：观测器中心漂移的方向支持预算

2026-09-23。接续 [21 通用多等式 CZ 认证支持查询](21_generic_cz_support_certificate.md)。本轮转向此前反复出现但没有单独闭合的证明义务：**SMF 后验集合变小以后，如果 nominal/observer center 同时改变，误差 tube 是否也一定变小？**

结论是否定的。集合收缩本身不够；中心漂移必须由对应方向上的 support shrinkage 支付。

## 1. 精确命题

设绝对状态集合满足

\[
X^+\subseteq X^-,
\]

旧/新名义中心分别为 \(z^-\)、\(z^+\)，误差集合

\[
E^- = X^- - z^-,\qquad E^+=X^+-z^+.
\]

对任意方向 \(p\)，平移集合的支持函数满足

\[
h_{E^+}(p)=h_{X^+}(p)-p^\top z^+.
\]

因此在有限受保护方向集 \(\mathcal P\) 上，新的误差 tube 不比旧 tube 大，当且仅当

\[
\boxed{h_{X^+}(p)-p^\top z^+\le h_{X^-}(p)-p^\top z^-,\quad \forall p\in\mathcal P.}
\]

令 \(\delta z=z^+-z^-\)，\(\Delta h_p=h_{X^-}(p)-h_{X^+}(p)\ge0\)，等价为

\[
\boxed{-p^\top\delta z\le \Delta h_p.}
\]

这就是**方向支持预算（directional recentering budget）**：后验在方向 \(p\) 上缩小了多少，中心就最多能向使该误差支持增大的方向移动多少。

如果同时保护 \(p\) 与 \(-p\)，则得到双边中心漂移限制。这个条件是支持函数恒等式的直接推论，不依赖 CZ、zonotope 或 ellipsoid 的具体表示。

## 2. 一个精确反例

取

\[
X^-=[-1,1],\qquad X^+=[-0.9,0.9]\subset X^-.
\]

若旧中心 \(z^-=0\)，新中心更新为 \(z^+=0.9\)，则

\[
E^-=[-1,1],\qquad E^+=[-1.8,0].
\]

虽然后验绝对集合严格收缩，但新误差集合并不包含于旧误差集合。对 \(p=-1\)，后验 support 只缩小 \(0.1\)，而中心漂移造成的误差支持增长为 \(0.9\)，预算被违反。

因此下列推理是错误的：

> SMF 后验嵌套 \(X_{k+1}\subseteq X_k\) ⇒ 以更新中心定义的误差 tube 也自动嵌套。

## 3. 与递归可行性的关系

Tube MPC 的 shift proof 通常需要下一时刻误差集合不超过上一时刻为 shifted candidate 预留的集合。如果 controller 直接使用绝对 set，则后验收缩可以直接利用；但若 controller 重新选择 nominal center / point estimate，再把集合写成“中心 + 误差 tube”，则必须额外处理中心变化。

对约束法向 \(p_j\)，上一轮 tightened constraint 使用

\[
p_j^\top z + h_E(p_j)\le b_j.
\]

下一轮若后验收缩但中心变化，只有满足

\[
h_{E^+}(p_j)\le h_{E^-}(p_j)
\]

才能无条件复用旧的方向收紧。第 21 章已经能对一般历史 CZ 认证 \(h_X(p_j)\) 的上下界，因此本章条件可以实际计算，而不是抽象假设。

一个保守但可认证的实现是用

\[
U^+_j-p_j^\top z^+\le L^-_j-p_j^\top z^-
\]

作为充分条件，其中 \(U^+_j\) 是新后验支持上界，\(L^-_j\) 是旧集合支持下界。若旧支持已精确认证，则直接用精确值。若该条件失败，不等于真实包含失败，只表示当前证书不足，应查询/精化或拒绝本次 recenter。

## 4. 文献核对后的创新边界

本轮重点核对了 robust adaptive MPC 中“集合缩小 + nominal model 更新”的处理方式。

- Köhler et al. 的 RAMPC 框架明确要求参数估计集合的 monotonic/non-increasing 性质，并把这些性质用于递归可行性和约束满足；因此“嵌套 uncertainty set 帮助 recursive feasibility”不是新结论。
- Lu et al. 2021 使用在线 set-membership 参数集合与 robust tube MPC，证明递归可行与 ISS，并用固定复杂度多面体控制计算量。
- Peschke et al. 2023 明确指出：tube 围绕 nominal trajectory 时，nominal model 改变会使 recursive-feasibility proof 变困难，并采用相应的 tube/target construction 处理更新。
- Köhler et al. 2023 的 control-contraction-metric RAMPC 通过在线优化 nominal parameter，允许更一般的 set-membership update，并在 planar quadrotor 数值例中展示在线适应收益。

因此不能把“发现 nominal center/model 更新影响递归可行性”作为创新。当前可能有价值的、更窄的贡献是：

> **把 nominal/observer center 更新显式转成与 MPC 活跃约束方向一致的 support-budget certificate，并与第 21 章的 anytime CZ support certificate 合并，使 recenter 决策本身成为可中断、可认证的计算对象。**

这个表述仍只是候选创新，必须继续做近邻全文排重，并证明它在滚动 CZ-SMF + Tube MPC 中相对“固定 nominal / 不 recenter / 全量重算 tube”确实减少保守性或计算量。

## 5. 代码验证

新增 `verification/check_recenter_support_budget.py` 和 `results/recenter_support_budget_20260923/checks.json`。

复现：

```bash
python verification/check_recenter_support_budget.py \
  --output /tmp/recenter_budget.json --seed 20260923 --cases 10000
```

实际结果：

| 检查 | 结果 |
|---|---:|
| 精确 1D 反例 | 后验嵌套=true，误差 tube 嵌套=false |
| 随机嵌套后验区间 | 10,000 |
| 任意 posterior center 导致误差包含失败 | 1,150 / 10,000 = 11.5% |
| support-budget 条件与真实 1D 包含判断一致 | 10,000 / 10,000 |
| 取 posterior midpoint 时的失败数 | 0 / 10,000 |

最后一项只是 1D 区间的特殊结构，不允许推广成“一般 CZ 取中心就安全”。本实验的作用是反驳错误推理并核对方向预算公式，不是证明高维闭环性能。

## 6. 对四旋翼接口的直接意义

当前六维平面四旋翼状态顺序为 \((p_x,p_z,v_x,v_z,\phi,\omega)\)。未来 Tube MPC 至少会保护：状态硬约束法向、输入反馈诱导法向、终端集法向。中心更新 \(\delta z\) 不需要在所有方向上都很小，只需要满足这些**控制相关方向**的预算。

这与当前候选主线自然衔接：

1. SMF/CZ 保留可靠绝对后验；
2. 第 21 章按需认证控制方向支持；
3. 本章检查 recenter 是否消耗超过 support shrinkage；
4. 预算不足时选择保持旧 nominal、限制 center update，或追加支持查询；
5. 只有证书通过才把更紧 tube 交给 MPC。

相比“每次后验更新都重新完整构造高维 tube”，这个接口有潜力减少无关几何计算；相比“后验变小就直接收紧”，它避免递归可行性证明中的隐藏中心漂移漏洞。

## 7. 下一步必须完成

下一轮优先实现高维 CZ rolling test，而不是继续 1D：

1. 在 `check_constrained_zonotope.py` 的 `predict/observe` 序列上引入非零、真值一致的测量，使 posterior center 确实变化；
2. 比较固定 nominal、posterior-center recenter、support-budget-limited recenter；
3. 对全部 MPC protected directions 精确检查 \(h_{E^+}\le h_{E^-}\)；
4. 构造 center update 违反预算后导致 tightened constraint/shift candidate 失效的高维反例；
5. 若预算限制长期过严，再研究“优化 center 以最大化可用 support shrinkage”的小型 LP/QP，而不是直接加入复杂学习算法。
