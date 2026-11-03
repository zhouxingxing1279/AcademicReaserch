# Run 139：增广 RCI 量词与因果信息门槛

日期：2026-10-02。分支 `research/run139-augmented-rci-contract-gate`。

## 仓库起点

只读取 `current_checkpoint.md`、Run 138 输入分配、第 71/73--75 章、对应验证器与当前配置。Run 138 本地提交 `595523e` 与远端分支虽然 commit SHA 不同，但 tree SHA 同为 `10b21cdd6c7a51c0486ee22a9513d9c34576dbe5`；工作区起点干净。远端刷新曾发生网络等待，因此分支索引以本地已有 remote refs 再做 tree 对照。

## 文献与准入

全文定向重读 Lorenzetti--Pavone 2020 Sections IV-B、IV-E--G：其 augmented error RPI 在固定 `u=bar u+K(hat x-bar x)` 后构造，输入收紧由 `[0 K]R` 得到。全文定向精读 Mejari--Mulagaleti--Bemporad 2023 Section III-C、Lemma 3 与 Problem 1：RCI 明确同时综合 invariance-inducing vertex controls。精读 Wehbeh--Kerrigan 2025 Sections II--IV、Theorems 1--2：decision-dependent uncertainty 必须只对与同一决策相容的 uncertainty 量化。

准入结论见 `run139_literature_gate.md`：只允许实现 problem-contract gate，不允许启动高维 RCI solver，也不作创新声明。

## 核心纠正

`eta=x-hat x` 不可观测，而 `d=hat x-z` 可见。普通 augmented-state RCI 的 `forall (eta,d) exists delta_u(eta,d)` 会给控制器隐藏真值误差。正确 baseline 必须对同一 observation fiber `Q_j(d)` 选一次 `delta_u=kappa_j(d,z,bar u)`，随后覆盖全部隐藏 `eta`、全部未知 successor edges 和共享 disturbances。当前配置没有冻结这一量词、policy class、nominal state domain、17-edge input timing、shared primitive graph 与非空 initialization slice，因此不存在单一可被“构造或否定”的 RCI 命题。

## 实现与验证

按 TDD 新增 `test_augmented_rci_contract.py`：先观察模块缺失及空实现失败，再实现最小只读 gate。6 项定向测试覆盖当前配置阻塞、完整 fixture、隐藏信息泄漏、非因果 edge 顺序、shared primitive 丢失和无效 initialization artifact。

该 checker 的 `blocked` 只证明问题未实例化，不证明 RCI 不存在。没有修改物理配置，也没有伪造 `K`、nominal domain 或 policy。

全仓检查还复现了一个 Run 138 遗留错误：其新增 `mpc` 输入字段改变了完整配置哈希，但 2026-09-09 的 affine/joint envelope 仍保存旧 hash，导致 `tests/` 两项以 `INVALID_MODEL_OR_CONFIG_HASH` 失败。用仓库原始生成脚本在当前配置重建两个 artifact；逐字段核对表明 envelope geometry、model 与压缩 leaves 的 SHA 均完全不变，唯一 envelope 内容差异是 `config_sha256`。据此更新两个 envelope hash 及 manifest artifact hash，而非绕过校验。修复后 `tests/` 39/39、`verification/` 131/131，共 170/170 通过。

## 主线总审视

Run 136 已闭合 estimator-error outer family；Run 137--138 只闭合输入权限必要条件/探针。本轮发现控制层接口仍未成为可审查命题。课题距离完整方法仍缺 partial-information ancillary set、可用 nominal input interior、terminal/shift、同预算严格优势和四旋翼闭环验证。当前纠正避免继续积累 certificate-class 局部否证，但本身不构成硕士课题创新。

## 下一唯一问题

冻结最小 hover-neighborhood partial-information contract：给出 17 条 edge 的 exact `(eta,d)` 更新、共享 primitive 和 causal policy class，并让 contract gate 对真实配置返回 `ready`。在此之前不运行 RCI solver。
