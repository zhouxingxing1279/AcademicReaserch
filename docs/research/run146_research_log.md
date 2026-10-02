# Run 146：完整纤维 joint candidate 的第二下降层

日期：2026-10-03。分支 `research/run146-vertical-joint-second-sweep`。

## 1. 仓库接续

刷新远端后，最新有效研究分支为 Run 145 `08bc927`，tree
`6904217adda44d922855e6e6dc943e31907e61f3`；`origin/main=1c49659`。从远端 Run 145
建立独立 worktree。Run 145 定向6项测试按正确 discovery 路径重跑为6/6通过；直接以
package 名从仓库根执行会因历史测试使用顶层 import 而失败，这只是调用路径问题，不是
Run 145 checker 失败。

## 2. 文献准入

本轮重读 Rungger--Tabuada 2017 pp.1--6、式 (4)--(10)、Theorems 1--2；精读 Hempel
2011 Section III-A--C、Definition 2、Theorem 1、式 (3)--(11)；定向重读 Houska 2023
Sections 5.3、6.1--6.5。下降迭代、noisy-output fiber 共享输入和 information ensemble
均已有直接近邻。本轮只准入受限第二层证书，不作创新或一般不可行声明。详见
`run146_literature_gate.md`。

## 3. TDD 与实现

先写5项行为测试，锁定：14个 mode 正面积且 mode 14 塌缩；mode-14 手算宽度证书；
mode 4/9 分叉共享零修正；结论不得外推为一般 joint RCI 不存在；artifact 必须绑定全部
直接源码和文档。RED 阶段5/5因 checker 缺失按预期失败。

随后实现 exact-rational checker。它读取 Run 145 的 `D_j^0` facets，把每条 target facet
通过 miss/success `d` 动力学反拉回，并与 source `D_j^0` 相交。success 支持保持
`q+n` 为同一个原语；没有采样或浮点成员检查。

## 4. 核心结果

mode 0--13 的第二层 observation projection 保持严格正面积；mode 14 的强制 success
predecessor 为空。精确宽度证书为：

- innovation 半宽：`24272147/48000000`；
- successor `d_v` 半宽：`72816441/32000000`；
- target `D_0^0` 速度半宽：`94125081847/57600000000`；
- 严格超量：`36944511953/57600000000 > 0`。

correction 只能平移区间，不能改变半宽，所以完整 mode-14 `eta` fiber 无法进入 target。
结论仅淘汰 `complete eta fiber` 候选类；它不否定条件 `eta|d` joint information set。

## 5. 验证、交付与下一问题

首次全仓回归为 `verification/` 180/180、`tests/` 39/39。随后按 Run143 已记录问题执行
`python -m compileall -q verification tests`，稳定复现
`check_rolling_control_normal_ledger.py:72` 的 unmatched `)`；git blame 表明它来自该文件
最初提交且从未进入测试 discovery。先增加导入并执行最小 audit 的回归测试，RED 阶段按
预期报 SyntaxError；移除多余右括号后 GREEN 1/1，并把另一文件 docstring 的无效转义改为
raw string，使 compileall 无警告退出0。

修复后的全仓回归为：

- `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s verification -p 'test_*.py' -q`：
  **182/182**，90.335秒；
- `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -p 'test_*.py' -q`：
  **39/39**，1.378秒；
- 合计 **221/221**；
- `PYTHONDONTWRITEBYTECODE=1 python -m compileall -q verification tests`：退出0。

新增 checker、测试、第83章、准入卡、日志和 hash-bound JSON artifact；更新
`READ_PAPERS.md` 与短检查点。

下一轮唯一问题：停止完整纤维下降迭代，在 mode 14 建立最小非乘积条件纤维模板，使每个
可见 `d` 对应的 `q|d` 半宽严格小于 mode-0 target 可接受半宽；先验证 `14->0 success`
和初始化 miss-chain 可达性，再扩展到15模态。
