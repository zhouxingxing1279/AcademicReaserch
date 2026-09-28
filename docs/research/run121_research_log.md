# Run 121：终端证书修复与文献准入

仓库基线：`main` 1c49659c；`research/run120-proof-quality-run119` 2a0b3d5。文献正文阅读、最近邻对照与准入判断见 [文献准入卡](run121_literature_gate.md)。本轮没有新颖性声明。

## 失败复现与根因

命令 `python verification/check_run120_terminal_rpi_support.py` 在旧脚本报 `AssertionError: ('px', 235.86712439707247, 5.0)`。旧版只累加前 139 项，又把所有其余块都用从 `G` 开始的同一粗块上界，导致上界远高于硬界，虽然它本身仍是安全但无用的上界。Run 120 文本指定从第 600 项开始的尾块，未同步到代码。

## 修复和证据等级

设 `alpha=||F^139||_inf<1`，`N=600`。把支持级数前 N 项用 `Fraction` 精确累加；尾部的第 `t` 块含 `F^(N+tM+j)G` (`M=139`, `0<=j<M`)。由矩阵幂交换、次乘性和 `||F^(tM)||_inf<=alpha^t`，得到

`h_S(q) <= D0 [ sum_{i=0}^{N-1}|q^T F^iG| + ||q||_1/(1-alpha) sum_{j=0}^{M-1}||F^(N+j)G||_inf ]`。

脚本运行通过，`alpha≈0.9874137875471`；位置、速度、姿态角、角速率及 `K` 方向上界分别为 `2.347203524832465, 2.4846308074960968, 0.364405517685758, 0.7007457289798581, 0.05568992614815032`，均严格低于 `5,3,0.44,2,0.0672`。屏幕小数仅供阅读；比较在 `Fraction` 中执行。`S=⊕_{i>=0}F^iW` 的正不变性还依赖该级数的定义与 `alpha<1`。这些是冻结线性模型的条件性数学证书。

仍未验证：Run 119 的 SLSQP 解、完整 OCP 约束和两种行删除的准入比较。不能从本轮终端界推断它们为已认证，更不能推断跨时刻或六自由度闭环保证。

## 运行记录

- `python verification/check_run120_terminal_rpi_support.py`：通过。
- `python -m unittest discover -s tests -v`：39 项通过。
- `python -m unittest discover -s verification -v`：80 项通过。

下一唯一问题：持久化 Run 119 的完整 OCP 与后验 LP 输入，独立核验同一候选的数值余量及测量行删除分类。
