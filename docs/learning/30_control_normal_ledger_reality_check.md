# 30 控制法向 support ledger 的 rolling CZ 现实检查

2026-09-24。接续第 28–29 章。第 29 章已经证明一般 generator-box reduction 可在 mixed normal 上破坏嵌套，但随机二维反例并不等于当前四旋翼基准真的从 control-normal ledger 获益。本轮把判据放回现有六状态 rolling CZ。

## 1. 先区分两个命题

对 exact rolling CZ，固定预测映射下已有

\[
X_{i|k+1}\subseteq X_{i+1|k}
\Rightarrow
h_{X_{i|k+1}}(p)\le h_{X_{i+1|k}}(p).
\]

因此保存有限控制法向的 exact support ledger 确实能给 shift-compatible tightening certificate。但这只是**安全性接口**。若廉价 monotone outer approximation 在这些真实法向上已经同样紧，ledger 就没有降低保守性的价值。

当前 `planar_baseline.json` 仍有 `K=null`、`terminal_certificate=null`；仓库目前真正有来源的姿态 mixed terminal normals 是

\[
\pm(4,1).
\]

所以本轮只允许用这两个方向判断控制收益。`±(4,-1)` 仅作相关性诊断，不得冒充 MPC normal。

## 2. 最小坐标盒基线

对任意 CZ `X`，用六个坐标方向的精确 extrema 构造最小 axis-aligned box `B(X)`。它具有两个性质：

1. `X subset B(X)`；
2. 若 `A subset B`，则 `B(A) subset B(B)`，因此它天然是 monotone reduction。

所以 coordinate box 是一个很强的负对照：固定复杂度、外包含、跨时刻单调，但通常会丢失 mixed-direction correlation。

对法向 `p`，定义 ledger 收益

\[
\Delta_p=h_{B(X)}(p)-h_X(p)\ge0.
\]

只有真实 MPC normals 上 `Delta_p>0`，才有理由为 support ledger/CZ correlation 支付额外计算成本。

## 3. 六状态 rolling CZ 实验

新增 `verification/check_rolling_control_normal_ledger.py`。完全复用第 28 章的六状态 affine outer model、truth-consistent 非零测量、26 ticks、horizon 8。每个 tick/horizon 对 exact CZ 与最小坐标盒分别查询：

- `+/-[4,1]`：当前 certified attitude terminal normals；
- `+/-[4,-1]`：非控制诊断方向。

共每个方向 234 次查询。

### 结果

| direction | strict box gap | mean gap | max gap |
|---|---:|---:|---:|
| `+(4,1)` | 0 / 234 | ~1.48e-19 | 3.47e-18 |
| `-(4,1)` | 0 / 234 | ~1.26e-19 | 6.94e-18 |
| `+(4,-1)` diagnostic | 233 / 234 | 8.613e-3 | 1.10e-2 |
| `-(4,-1)` diagnostic | 233 / 234 | 7.496e-3 | 9.88e-3 |

`±(4,1)` ledger 的 shifted nesting violation 仍为 0。

这给出一个重要的否证：**当前 rolling benchmark 中确实存在 phi–omega correlation，但当前已认证 terminal normal 恰好没有从该 correlation 获得 tightening 收益。** 因此第 29 章的二维 mixed-normal reversal 不能被直接升级成当前控制器的性能问题。

## 4. 理论解释

最小坐标盒的 support 为

\[
h_{B(X)}(p)=\sum_j \max_{x\in X} p_jx_j.
\]

一般有

\[
h_X(p)\le h_{B(X)}(p),
\]

严格性取决于各坐标 extrema 是否能由同一个 `x in X` 同时实现。当前 posterior 在 `p=(4,1)` 上恰好允许共同实现相关 extrema，因此 equality 成立；在 `(4,-1)` 上不能共同实现，于是出现严格 gap。

所以“CZ 比 box 更紧”不是一个足够的控制论陈述。必须进一步要求：

\[
\exists p\in\mathcal P_{MPC}:\quad h_X(p)<h_{B(X)}(p),
\]

其中 `P_MPC` 是真实 state/input/terminal normals。

## 5. 对候选创新的影响

### 候选 A：control-normal support ledger

- 安全性：保留。exact supports 在固定预测 map 下天然 shift-compatible。
- 降保守性证据：**当前基准不支持**。真实 terminal normals 上 box 已 support-exact。
- 当前状态：降级为基础接口，不作为主创新。

### 候选 B：certificate-preserving fixed-complexity CZ reduction

- 第 29 章的一般反例仍成立。
- 但当前控制收益尚未建立；若真实 MPC normals 不消费被 reduction 破坏的相关性，则修复没有价值。
- 当前状态：条件保留，等待真实 ancillary `K` 与 terminal family。

### 候选 C：exact redundancy pruning + monotone coarse envelope

2026 ACC 的 exact CZ representation reduction 不改变集合，因此适合作为所有 approximate reduction 前的第一阶段。若剩余复杂度仍超预算，可用 coordinate/template envelope；是否值得保留更多 CZ correlation 必须由真实 control-normal gap 驱动，而不是由 volume 指标驱动。

## 6. 下一步

研究主线不应继续制造更多任意 mixed normals。当前真正的阻塞点再次暴露为 `K=null` 与缺失的完整 terminal certificate。下一轮应：

1. 在语义一致的模型合同下合成/搜索可认证 ancillary feedback；
2. 由真实 input normals `K^T q_u` 与 terminal set 自动生成 `P_MPC`；
3. 比较 exact CZ、coordinate box、ellipsoid、naive fixed-order CZ 在 `P_MPC` 上的 support；
4. 只有出现严格且持续的 control-normal gap，才恢复 certificate-preserving reduction 为主创新候选；
5. 若仍无 gap，则应放弃该方向，转向 disturbance/model contract 或 nonlinear scheduling tube 的更直接问题。

本章没有证明完整 recursive feasibility、terminal append 或 ISS。
