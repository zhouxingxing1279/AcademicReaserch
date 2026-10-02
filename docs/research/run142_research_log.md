# Run 142：竖直 causal product-fiber predecessor 否证

日期：2026-10-02。分支 `research/run142-vertical-causal-predecessor`。

## 仓库起点与接续

启动时只读取 Run 141 短检查点及其直接原始证据，随后刷新远端。远端最新有效研究分支
仍是 `research/run141-vertical-causality-gap`；本地 `2b02af0` 与远端 `0fa5c75` 的 tree
均为 `cf2234cfaa972a6f7b1b8be7ad3bac5516324390`。`origin/main=1c49659`，尚未包含
Run 127--141。Run 141 的 8 项定向测试及 artifact 齐全；其证据严格是一条 observation
fiber 的 one-step negative control，不是 RCI 不存在。

## 文献与准入

定向重读 Hempel--Kominek--Werner 2011 Section III-A--C、Definition 2、Theorem 1、式
(3)--(10) 及 Section V：其方法对给定 OFCI polytope 做 Farkas 验证并按当前 output 在线
求共享输入，但不直接生成 polytope。精读 Rungger--Tabuada 2017 pp.1--7、式 (4)--(10)、
Lemma 1、Theorem 1 与 Section 4：递减 predecessor 一般不有限终止，有限前缀不是 RCI；
其量词是 full-state feedback。定向阅读 Houska--Müller--Villanueva 2024 Sections 3.3--3.6、
3.10：非轴对齐 polytope、projection、vertex control 和固定复杂度参数化均已有成熟方法。

准入只允许因果 product-fiber 基线与类特定判定，不允许算法创新、一般 output-feedback
不可行或完整 Tube MPC 声明。详细对照和推翻条件见 Run 142 文献准入卡。

## 候选类与 exact predecessor

冻结 `S_j=E_eta^j x D_j`，其中 `E_eta^j` 是 Run 136 zonotope，`D_j` 是任意二维
`(d_pz,d_vz)` 集合。实现 Fraction 二维半空间相交、凸包去冗余和 scalar-input
Fourier--Motzkin projection；同一 mode 的全部后继边在一次 projection 中共享一个
`delta T`。success disturbance 使用 Run 136 生成元直接计算的
`q=eta_pz+h eta_vz` support 与下一测量噪声；miss 无该项。真值 source box 对每个 mode
按 `E_eta^j` 坐标支持精确收紧。

第一轮对 0--13 模态产生 4--6 facet 的非轴对齐 predecessor；mode 4、9 分别同时消费
miss/success 两边。mode 14 却直接为空。调试确认不是半空间方向或消元错误，而是一个
与 `D_j` facet 无关的宽度矛盾：

```math
L(h_{E^{14}}(q)+1/50)=72816441/32000000,
```

而真值速度域和 `E_eta^0` 允许任何 product target `D_0` 的最大速度半宽仅

```math
61142137/36000000.
```

严格超量为 `166210873/288000000 > 0`。`d` 与推力修正只能移动区间中心，不能压缩
hidden-fiber 半宽，因此 `Pre_14->0(D_0)` 对整个 admissible source domain 为空。graph
包含必经 `0->...->14` miss 路径及强制 `14->0` success，故任何满足 mode-0 初始化的
product-fiber invariant family 均不存在。

证据等级是 **exact nonexistence for the product-fiber candidate class**。它不否定 joint
`(eta,d)` information set 或 history-dependent controller。Run 141 hidden-state policy 继续
作为 negative control：允许读取 `q` 时其专门 target 可行；真实 causal robustification
正确拒绝。

## TDD、调试与验证

1. 首先新增 4 项测试，因 checker 缺失得到预期 RED；实现 exact polygon、共享输入投影、
   Run 136 support bridge 与 Run 141 negative control 后 GREEN。
2. 新增 first-iteration/证据等级 2 项测试，因 API 缺失得到 RED；最小实现后一项预期
   “15 模态均非空”失败。按系统化调试逐 mode 检查，定位 mode 14，手算得到上述严格
   support 矛盾；没有放宽参数。
3. 将错误预期改为类特定 obstruction，并先增加精确分数测试得到 RED，再实现
   `mode14_product_fiber_obstruction`；最后先增加不越权 claim 测试 RED，再实现 artifact
   entrypoint。定向测试 8/8 通过。
4. 最终全仓：`verification/` 158/158（85.667 s），`tests/` 39/39（1.262 s），合计
   **197/197**。artifact 由当前源码生成；另执行 Python compile、JSON/hash 复核和
   `git diff --check`。

## 主线判断

该结果终止“固定 Run 136 无条件估计 zonotope，再独立综合 observed-center tube”的支线。
继续增加 `D_j` 法向、改椭球/CZ 或扩大求解器都不能修复宽度矛盾。要保留控制可行性，
必须让候选 joint set 记录 `eta-d` 相关性，使固定 `d` 下的 conditional `q` fiber 缩小。

mode 14 闭合的必要阈值是

```math
h_{Q_{14}(d)}(q)\le
\frac{61142137/36000000}{9/2}-\frac1{50}
=\frac{57902137}{162000000}\approx0.3574206,
```

相对无条件 support `0.4856697` 至少减少 `0.1282491`（约 26.4%）。这给下一轮 joint
information-set synthesis 一个可推翻的定量门槛。

## 下一唯一问题

在竖直四维 `(eta_pz,eta_vz,d_pz,d_vz)` 上构造最小的 mode-indexed joint
information-set candidate，保持 success/miss 的 shared primitive 与 actual-input 时序；
首先判断 reachable mode-14 conditional fiber `Q_14(d)` 能否把 `q` support 压到
`57902137/162000000` 以下。若不能，给出 joint candidate-class 反证；若能，再综合因果
shared-input predecessor。

