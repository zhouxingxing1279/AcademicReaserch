# Run 143：联合信息集门槛的语义纠正

日期：2026-10-02。分支 `research/run143-joint-information-semantics`。

## 仓库起点与中断草稿审计

启动时只读取 Run 142 短检查点及其直接证书。刷新远端后确认最新有效研究分支为
`origin/research/run142-vertical-causal-predecessor=be558f8`，其 tree 与本地 Run 142
提交 `799d730` 一致；`origin/main=1c49659`。工作树已有三个未跟踪 Run 143 草稿，时间早于
本轮启动，故先审计而未覆盖。文学准入卡与 Run 142 唯一问题一致；检查器已有三项通过
测试和一项因 `joint_target_counterexample` 缺失而失败的 RED 测试，未形成成果。

## 文献与准入

本轮从原始全文定向精读 Baras--Patel 1998 Section IV-A，尤其 Information State
Formulation、Lemma 4、Remarks 8--10、Theorems 9--11；其递归 information state 保留与
观测/控制历史相容的可行状态，且一般是无限维。重读 Hempel--Kominek--Werner 2011
Section III-A--C、Definition 2、Theorem 1、式 (3)--(10)，确认同一 noisy output fiber
必须共享输入。精读 Kjellqvist 2024 Sections 2.1--2.2、Assumption 2、Proposition 4、式
(11)--(18)：有限维递归依赖每个测量逆像至多含有限个元素；实值有界噪声导致连续 fiber，
不满足该假设。

因此 joint information state 与 fiber robustification 都已有一般理论，不能作为创新。
准入仅允许当前合同的坐标语义审计和精确反例；不允许直接启动四维 RCI 求解器。详细对照
见 `run143_literature_gate.md`。

## 核心发现

Run 142 的旧计划要求 mode-14 条件 `q` fiber 压到
`57902137/162000000` 以下。精确复核得到两点：

1. 初始化 `d=0` 后的 14 条 miss 边，`d` 更新不含 hidden `eta` 或 residual；所以固定
   同一 observation history 时，mode-14 fiber 保留完整 `q` 半宽
   `23312147/48000000`，严格超门槛 `166210873/1296000000`。
2. success 边的创新 `L(q+n)` 在 `eta_v^+` 与 `d_v^+` 中符号相反，故在
   `e_v^+=eta_v^++d_v^+` 中精确抵消。物理状态约束作用于 `e`，配置没有独立 `d`
   硬约束。因此旧门槛只是 product `E_eta x D` 的必要条件，不是 joint target 的必要条件。

构造 mode-14 支持见证，取 `d=0,deltaT=0,r_z=0,n=1/50`。结果
`d_v^+=72816441/32000000` 超过 product 限幅，但
`eta_v^+=-64124993/288000000` 与之相关，得到
`e_v^+=9237859/4500000<11/4`；位置和完整 `eta^+` 也分别满足 source box 与 Run136
mode-0 box。这是 exact counterexample，不是采样观察。

证据等级：**exact counterexample to the product threshold as a joint necessity**。它不证明
joint RCI 存在，也不否定一般 output-feedback controller。

## TDD 与实现

继承的第四项测试首先因 `joint_target_counterexample` 缺失按预期失败；又先收紧 artifact
测试，要求证据等级、miss-path 结论、joint 反例和源码散列，得到预期 RED。随后最小实现：

- 直接从当前 config 和 Run136 生成元重建 mode-14 支持见证；
- 用当前 `A1,G1` success map 传播同一噪声/残差原语；
- 分别检查 mode-0 `eta` box、真实 tracking-error source box 与 product `d` 限幅；
- 归档精确分数、证据等级、限制和源码 SHA256。

定向测试随后 4/4 GREEN。最终 `verification/` 为 162/162（84.387 秒），`tests/` 为
39/39（1.387 秒），合计 201/201；另通过本轮新增 Python 文件编译、JSON/源码散列复核
和 `git diff --check`。全目录 `compileall` 仍会被基线中已存在的
`verification/check_rolling_control_normal_ledger.py:72` 语法错误阻断；该文件未由本轮修改，
且不在 unittest discovery 导入路径。归档结果由最终源码重新生成。

## 主线纠偏

不能继续把“conditional q support 是否小于 0.35742”作为 joint set 的准入门槛。正确有限
候选应改用 `(eta_pz,eta_vz,e_pz,e_vz)` 坐标：约束施加在 `eta` 投影和 `e` 上，控制策略
仍按 `d=e-eta` 的 observation fiber 共享输入。若仍在 `(eta,d)` 坐标求解，也必须保留
`eta+d` 联合约束，不能单独给 `d` 盒。

## 下一唯一问题

在竖直 `(eta,e)` 坐标上定义最小 mode-indexed convex joint candidate，写出对固定
`d=e-eta` fiber 的 shared-input predecessor；先检查 forced `14->0` success 与 mode 4/9
分叉是否存在非空一步 predecessor，再决定是否进行固定点迭代。
