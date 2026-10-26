# Run182：Run180/181 局部 cells 的边可组合性纠正

启动基线：远端 `main=1c49659`；实际续接分支
`research/run181-mode4-unknown-branch-lifted-cell@46f33d2`。本轮只读短检查点、Run179 的
`Gamma` 类型审计、Run180/181 checker 与 history-complete envelope 合同。

本轮重新下载并精读 Hempel--Kominek--Werner 2011 §III-C、式(9)--(14)、Algorithm 1；重新
下载并精读 Houska 2026 §4.2、§4.4、§6.1--6.7、Definitions 4--5、Lemma 2、Theorem 3 和
式(25)--(29)。前者已给完整 output partition/common refinement/PWA control，后者已给固定模板
polytopic information ensemble、extreme-set control interpolation、terminal invariant ensemble
及复杂度旋钮。因此本轮不把有限 cell family 或 overlap selector 当作创新。

仓库审计发现 Run180/181 都只验证 estimator target facets 与 tracking box normals，没有验证
`d^+=e^+-eta^+` 进入 target source cell。准入卡据此通过 exact composability audit，而不准入
新的 cover solver。

按测试先行新增四组回归。RED 阶段 checker/module 不存在，四项均按预期失败。最小实现复用
Run180/181 已认证结果，并从 Run181 的联合 primitive columns 计算 visible supports。精确结果：

- `0->1 miss`、`4->5 miss`：`d_p^+` 半宽 `41/200`，比 target `1/5` 大 `1/200`；
- `4->0 success`：`d_p^+` 半宽 `2624143/7200000`，`d_v^+` 半宽
  `1548143/1600000`，分别超出 `1184143/7200000`、`1148143/1600000`。

因此三个已认证 local edges 均不进入相同 centered `D_0`；Run180/181 是可靠模块检查，但不是
可组合 cell graph。该反例不否定其他 cells 或 PWA policy。论文级主线停止手工 cell 枚举，下一
唯一问题改为：在竖直 15-mode 线性/可靠 residual-envelope 合同上复现 Houska 式
configuration-constrained polytopic information-ensemble terminal baseline，先闭合强基线再谈
nonlinear CZ oracle 或同预算优势。
