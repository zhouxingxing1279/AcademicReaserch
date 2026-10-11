# 研究短检查点（2026-10-11，Run152）

主线：传统 SMF/鲁棒输出反馈 MPC；学习暂停。本地 `main=1c49659`，Run151=`df10a61`；15模态/17边，控制只读可见 `d=e−eta`。Run150 只否定单一 translated fixed-shape 模板。

Run152 重读 Baras--Patel 1998 §IV-A、Lemma4、Remarks8--10、Theorems9--11/Corollary4，并复核 Kjellqvist 2024 与 Houska 信息集合基线。当前 mode 已表示 current miss age；三条 success 均回到 mode0，因此同义 `return-age` 冗余。若要区分 Run148 的三种 return seed，最小离散记忆应明确为上一周期长度 `{5,10,15}`。不同 history shape 不同并不否定有限抽象，因为可取共同外包；安全充分性需要初始化覆盖、可见历史一致性、共享输入/原语逐边模拟、硬约束和终端闭合五项。当前仅建立此合同，不是 RCI、递归可行性或创新证明。

下一唯一问题：扩展 `(mode,last_return)` 图，以三 return seed 为初始化像，检查固定 global residual 下共同外包能否逐边闭合；失败必须给出硬约束/共享输入的精确反证。
