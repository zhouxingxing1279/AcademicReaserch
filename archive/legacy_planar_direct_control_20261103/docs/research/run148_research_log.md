# Run 148：固定零修正下三种初始化 return 的统一相关模板

日期：2026-10-03。分支 `research/run148-multi-return-template`。

## 1. 仓库接续

启动时刷新远端并以 `docs/research/current_checkpoint.md` 为事实入口。远端最新有效分支为
Run147 `038cacc`；该轮已经完成14条 miss 后的单一 `14->0 success` correlated seed，故本轮
不重复 Run145/146 的 descending sweep，也不重做 Run147 单路径证书。Run147 指定的唯一
问题是统一5/10/15 tick三种初始化 return；复核后把范围收紧为先行 miss 均取零修正的基线。

## 2. 文献准入

重读 Houska 2023 Sections 6.4--6.7、Definition 7、Theorem 3及证明、Remark 6；重读
Hempel--Kominek--Werner 2011 Sections III-A--C、Definition 2、Theorem 1、式(3)--(14)；
重读 Dey--Bhasin 2026 Sections IV-A--F、Assumptions 2--4、Criterion 1、Theorem 2及
Appendix IV；复核 Artstein--Rakovic 2011 的既有全文笔记。

Houska 已明确用极端信息多面体的凸合包编码 extrinsic information，并以连续 convex weights
组合 extreme controls；Hempel 已给出同一 noisy-output fiber 共享输入量词；Dey--Bhasin
已经覆盖 adaptive tightening、terminal update、backup 和 recursive feasibility。因此本轮只
准入当前 packet/shared-primitive 合同的固定零修正 baseline，不作算法或闭环创新声明。详见
`run148_literature_gate.md`。

## 3. TDD 与实现

先新增7项行为测试，锁定三条完整初始化路径、每个 seed 的共享原语/秩、完整投影约束、
最小凸容器的 perspective lift、naive generator concatenation 负对照、证据边界和
hash-bound artifact。RED 阶段 checker 不存在，得到6项 FAIL和1项派生 ERROR，原因均为
缺失目标实现。

最小 checker 实现后，前6项核心行为转绿；artifact 测试因第85章、研究日志和归档尚未
生成而保持预期红灯。随后补齐本章、日志与归档。实现全部使用 `Fraction`、精确高斯消元、
完整生成矩阵支持函数和 exact perspective-lift 语义，没有采样或浮点可行性判定。

语义复核把含糊字段“preserves path exclusivity”进一步收紧为两项可执行语义：连续
`lambda` lift 会凸化路径，允许 `lambda=(1/2,1/2,0)`，而不是保持 one-hot path；它只
保证各路径块内的生成元列耦合由同一 `lambda_m` 缩放，并由 `sum lambda=1` 排除两个
单位尺度 selector 同时出现。

同一复核还发现旧文本把零中心 return 称为“必要 target”过强。`propagate_generators`
只证明 estimator-error 形状传播；可见 offset 的中心保持零还依赖每拍 `deltaT=0`。因此
checker 现在显式记录零修正序列与二维可见偏移，并把结论降级为 fixed-policy baseline。

## 4. 核心结果与证据等级

三条 return 的源/返回生成元数分别为 `34/36`、`69/71`、`104/106`，三者 exact rank 均为3，
且完整 `eta` 与 `e` 投影均满足当前竖直约束。最小凸容器

`C0=conv(J4 union J9 union J14)`

有标准 exact perspective lift，拼接列空间 rank 仍为3，全部列保持 `d_v=(9/2)d_p`。
其 `eta` 支持为 `(1/50,37857863/36000000)`，恰好等于 mode-0 vertical estimator limits；
`e` 支持为 `(23312147/48000000,152955031/72000000)`，对真值约束仍有严格余量。

因此单一 convex mode-0 固定零修正 baseline 存在，但 **estimator margin 为零**。直接横向拼接三组
生成元会得到 Minkowski 和，其 `eta` 支持为
`(3/50,10008843797/3600000000)`，`e_v` 支持为
`31802149/6000000`，明确违反 estimator 与真实速度约束。

证据等级：**exact rank-three minimal convex template for three fixed-zero-correction
returns**。它不是 policy-independent 必要 target、RCI、information ensemble 固定点、
全六状态保证或 MPC recursive-feasibility 证明。

## 5. 交付与下一问题

新增 exact checker、7项测试、第85章、准入卡、日志和归档；更新文献表与短检查点。

全仓第一次回归为195项，其中Run146、Run147两项artifact测试仅因本轮更新
`READ_PAPERS.md`的SHA-256失配。分别重生成后逐字段比较，确认各自唯一变化字段都是
`source_sha256/docs/literature/READ_PAPERS.md`，数值、集合和结论未变。修复后中间回归：

- `verification/`：195/195，通过，87.401秒；
- `tests/`：39/39，通过，1.220秒；
- Run148定向：7/7，通过；
- Run146/147历史artifact仅更新一项文献散列。

最终冻结后再次执行全仓回归、Python编译、JSON、source hash与`git diff --check`，结果
记录在提交前验证输出中。

下一轮唯一问题：先判断 `C0` 在固定零修正下是否是一致的自映射基线；若不是，不得把它
当作一般策略的必要 target。只有把由可见 `d` 选择的非零 correction 及其中心平移显式
纳入后，才准入 modes 4/9 分叉与 mode14 return 的 causal predecessor 综合。不得先把
低维 `C0` 外包成增加 estimator 支持的普通 full-dimensional zonotope。
