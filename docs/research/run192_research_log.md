# Run192 研究日志：Gate A 控制基线证据审计

日期：2026-10-27。

## 仓库与接续

起点为本地已复审 Run190 `97b5ff5`；远端 `main=1c49659`，远端 Run190 提交为
`1038184`。启动时工作树干净。按最新研究收口，停止把连续 posterior/configuration
几何当作主线，转回 scheduling-consistent ancillary/RCI 强基线。

未发布的 Run191 几何实验保留在本地分支；独立审查指出 posterior facet degeneration
和 H/V irredundancy 尚缺计算证书，故本轮未把它并入或上传为完成结果。

## 文献准入

重读 Mejari--Mulagaleti--Bemporad 2023 Section III-C、Lemma 3、Problem 1与
Section IV；精读 Mulagaleti--Mejari--Bemporad 2025 problem statement、Sections
3.1--3.2、式(14)--(28)和算法；精读 Köhler 等 2020 Sections II--III、Assumptions
1--6、MPC (11)、Theorem 1 shift proof及 Proposition 4；复核 Rungger--Tabuada
2017 predecessor 外序列边界。

准入只通过“现有 Gate A 证据审计与方向纠正”，不通过新 RCI 算法、参数相关 RCI
首次性或继续配置锥枚举。

## 审计与实现

新增只读审计器，核对八份既有归档中的关键字段，并把六类控制相关证据绑定到生成
checker 的 SHA-256。七个回归测试先以缺模块/依赖清单缺失失败，再在实现后通过；
审计自身、测试、配置和八份直接结果依赖也纳入 SHA-256，并逐次重放比较归档。审计明确区分
DERIVED、NUMERIC_CHECK 和 COUNTEREXAMPLE，并确认：

1. common-`P` 只证名义 LPV 稳定；
2. 特定 `K` 被 torque reachable support 严格否定；
3. 30,000 点 static-`K` 搜索不是不存在性证明；
4. 调度一致 residual 的有限轨迹数值可行，反驳 plant-level 物理不可行升级；
5. axis-aligned box 与一个 configuration cone 的反例只否定各自类别；
6. 当前信息合同是 current-`T` known / future-`T` arbitrary jump，端点归约精确。

没有任何归档给出同时覆盖 endpoint、`W(T)`、状态和 torque constraints 的充分
controller/RCI 证书，因此 Gate A 为 blocked。未实现新控制器，避免在准入未通过时
继续盲目调参或扩张几何模板。

最终验证：项目测试 39/39，研究验证 338/338；新增审计归档可由 checker 逐字重放。
独立审查未发现数学或范围过度主张，并提出的归档漂移缺口已由直接依赖哈希与完整归档
比较测试修复。`READ_PAPERS.md` 是14份历史工件的显式依赖，故这些工件均由各自原
checker 重新生成；差异仅为阅读索引 SHA-256 更新。

## 命题等级与限制

- DERIVED：当前调度合同、非平凡 rate bound 缺失、仿射合同端点归约、common-`P`
  名义稳定（均沿用已有证明并由审计绑定）。
- COUNTEREXAMPLE：特定 `K`、axis-aligned box、单一 configuration cone。
- NUMERIC_CHECK：30,000 点搜索、执行器权限 LP。
- OPEN：存在何种充分 correlated ancillary/RCI；四状态证书如何嵌入完整六状态模型；
  terminal append 和递归可行性。

## 下一唯一问题

在冻结 `W(T)` 与 arbitrary-jump endpoint 合同下，选择一个可返回充分证书的最小
correlated controller/RCI 综合（优先 vertex/PWA control，而非继续随机 static-`K` 搜索），
同时纳入全部 state/torque constraints；得到 candidate 后用独立 support 检查攻击。

