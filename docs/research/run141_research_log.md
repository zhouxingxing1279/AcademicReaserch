# Run 141：竖直 observation-fiber 一步因果性差距

日期：2026-10-02。分支 `research/run141-vertical-causality-gap`。

## 仓库与基线

只读取 Run 140 短检查点、Run 140 gate/log、第 76--77 章、Run 136 zonotope checker、
Run 138 correction box 和当前配置。刷新远端后确认 `origin/main=1c49659`；本地起点为
Run 140 补强提交 `9dad151`。

worktree 启动时存在一组未提交的 Run 141 草稿（gate、checker、4 项测试、artifact 与
阅读记录）。没有覆盖或丢弃这些文件；先审计并运行全仓基线：`verification` 147/147，
`tests` 39/39。草稿只检查了达到组合方向支持的两个见证点，不能证明整个 mode-4 fiber
位于源域；本轮据此补强，而不把草稿结果直接当成已证事实。

## 文献与准入

全文重读 Hempel--Kominek--Werner 2011 Section III-A--C、Definition 2、Theorem 1 与
输入计算：每个 noisy output 只能选择一个输入，并须覆盖与输出一致的全部状态。全文
精读 Lucia--Ernesto--Castelan 2023 Sections 2--5、Definitions 2--3、Propositions 1--2、
Algorithm 1：rank-deficient output 下使用不依赖隐藏状态的保守切换；仅 full-rank/noisy
state 情形可按当前测量选择更小集合。定向复核 Mejari--Mulagaleti--Bemporad 2023
Section III-C、Lemma 3、Problem 1、Sections IV--V：其 vertex controller 以当前完整状态
计算凸组合系数。

因此一般 observation-fiber 量词与 full-state 乐观上界均已有近邻。本轮只准入当前实际
参数的一步因果性 negative control；不准入 RCI 综合、一般不可行结论或创新声明。

## 精确命题

冻结 mode 4、hover、`d_pz=d_vz=0`。Run 136 mode-4 zonotope 给出

```math
q=\eta_{p_z}+h\eta_{v_z}\in[-q_4,q_4],\quad
q_4=1004143/7200000.
```

在未知 `miss:4->5` 与 `success:4->0` 前必须使用同一当前输入。对专门冻结的一步 target
slice，读取隐藏 `q` 的策略

```math
\delta T(q)=-\frac{108143/32000}{q_4}q
```

在 correction/actual-input 盒内，并通过 miss 两个顶点及 success 四个 `(q,n)` 顶点。
但 causal policy 在同一 observation fiber 上必须同时满足

```math
\delta T\ge108143/32000,\qquad
\delta T\le-108143/32000,
```

故公共输入交集严格为空。逐坐标支持同时证明整个 mode-4 fiber 在 hover 真值源域内。

证据等级是 **exact one-step predecessor counterexample**。它不构造不变集，不证明
causal vertical/full six-state RCI 不存在。

## TDD 与验证

在保留遗留草稿的基础上新增两个缺口测试：

1. `source_fiber_domain` 缺失时先得到预期 RED；最小实现改为计算整个 zonotope 六个坐标
   的精确支持及上下界余量，随后 GREEN。
2. `edge_vertex_checks` 缺失时先得到预期 RED；最小实现显式枚举 2 个 miss 和 4 个
   success 顶点。随后再次以缺少 position/velocity target 字段得到 RED，补全两坐标
   target 后 GREEN。
3. 提交前自审发现 `h,L` 尚未与配置和 Run 136 success map 显式绑定；先以缺少
   `audit_model_constants` 得到 RED，再核查 `dt=h`、矩阵系数 `-L` 与 `1-Lh`。首次实现
   的矩阵解包错误被测试捕获，修正后 GREEN。

定向 Run 141 测试 7/7 通过。最终全仓回归：`verification` 150/150（104.511 s），
`tests` 39/39（2.125 s），合计 189/189。artifact 用当前源码重新生成；Python 编译、JSON、
源码散列和 `git diff --check` 在提交前再次核查。

## 主线判断

Run 139--140 已把 partial-information 问题合同变为可执行；Run 141 现在提供了能识别
隐藏状态泄漏的必要回归。它只提升后续 solver 的语义可靠性，不改善控制可行域、性能或
复杂度，不能独立构成硕士课题贡献。继续制造相似局部反例没有价值。

## 下一唯一问题

在同一 vertical 四维投影、15-mode/17-edge graph、Run 136 zonotope 和 Run 138 输入盒下，
实现非轴对齐 mode-indexed observation-fiber predecessor/RCI synthesis；强制同一 fiber
与未知后继边共享 control decision，并用本轮反例作 negative-control 回归。只报告认证
候选或明确的 policy/certificate-class 反证。
