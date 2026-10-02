# Run 145：15 模态竖直 joint predecessor 首次下降层

日期：2026-10-02 启动，2026-10-03 完成复核。分支
`research/run145-vertical-joint-first-sweep`。

## 1. 仓库接续与 Run 144 复核

启动时只读取 `docs/research/current_checkpoint.md` 及 Run 144 直接证书。刷新远端后，
Run 144 本地提交为 `64cf2a0`、远端为 `b3a9953`，两者 tree 均为
`78d4be8db83ddb09b27407379bfa0723612a8317`；`origin/main=1c49659`。工作树干净。
Run 144 定向7项测试重新执行为7/7通过，因此没有重复 Run 144。

## 2. 文献与准入

本轮重读 Rungger--Tabuada 2017 pp.1--6、式 (4)--(10)、Theorems 1--2：普通下降序列
的有限层一般不是 RCI，只有固定点或其专门停止证书才能升级。定向重读 Houska 2023
Sections 4.2、6.1--6.5 的 information ensemble、extreme information-set control；重读
Hempel 2011 Section III 的 noisy-output fiber 共享输入量词。

因此准入只允许实现当前冻结合同的一次 exact inner sweep；不允许把 information-set
predecessor、多面体投影或15模态非空声明为算法创新。完整准入卡见
`run145_literature_gate.md`。

## 3. TDD 与实现

先新增6项行为测试，分别锁定：15/15 模态四维正体积、mode 14 手工精确 observation
面积、17/17 graph edges、mode 4/9 分叉共享单一输入、包含 Run 144 公共 observation box，
以及“一次 sweep 不是 RCI”。首次执行6/6因新 checker 缺失按预期失败；实现最小 checker
后6/6通过。

checker 对每个 mode 构造零修正、完整隐藏 fiber 的 exact-rational observation polygon
`D_j^0`。它复用 Run 136 estimator zonotope 但独立计算 current/next tracking 半空间、面积、
顶点与全部 estimator target-facet supports。结果写入 hash-bound JSON artifact。

## 4. 核心结果与证据等级

15个 `D_j^0` 全部严格正面积，并全部包含 Run 144 的
`|d_p|<=1/5, |d_v|<=1/4`。最小面积出现在 mode 14：

`899947970530621291/691200000000000000 ≈ 1.302008`。

对应 `C_j^1={(eta,e):eta in E_j,e-eta in D_j^0}` 均为四维正体积，且17/17 estimator
edges 全部 exact support-contained。统一 `deltaT=0` 在每个 mode 的全部 observation
projection 和所有未知后继边上共享；residual 半宽仍由同一 actual thrust 上界计算。

证据等级：**exact positive-volume inner certificates for all fifteen first-sweep modes**。
这不是 maximal observation projection、固定点、RCI、全六状态或递归可行性证明。

## 5. 交付、验证与下一问题

新增：

- `docs/learning/82_vertical_joint_first_sweep.md`
- `docs/research/run145_literature_gate.md`
- `docs/research/run145_research_log.md`
- `verification/check_vertical_joint_first_sweep.py`
- `verification/test_vertical_joint_first_sweep.py`
- `results/theory_vertical_joint_first_sweep_20261002/exact_checks.json`

复核时发现最初 artifact 只绑定代码与配置，没有绑定本轮理论说明、准入卡和日志。先扩展
测试要求上述四类文档 SHA；测试按预期失败，再补齐 checker 的 source manifest 后
6/6 GREEN。最终验证为：

- `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s verification -p 'test_*.py' -v`：
  **175/175**，134.703 秒；
- `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p 'test_*.py' -v`：
  **39/39**，2.406 秒；
- 合计 **214/214**；
- 本轮 checker/test 的 `py_compile`、artifact JSON 解析、逐源文件 SHA-256 重算及
  `git diff --check` 在归档后再次核查。

远端同步状态在最终提交后以 branch SHA/tree 单独核验；本文不预写自指 commit SHA。

下一轮唯一问题：以本轮 `C_j^1` 为 target 执行第二层 exact inner predecessor，严格判断
full-fiber/zero-policy class 是否自映射或在哪个 mode 首次塌缩；若塌缩，仅否定该受限 policy
class，再准入依赖 `d` 的分段/仿射 correction policy synthesis。
