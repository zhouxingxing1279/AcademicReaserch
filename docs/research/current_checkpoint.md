# 研究短检查点（2026-10-11，Run153）

主线：传统 SMF/鲁棒输出反馈 MPC；学习暂停。本地 `main=1c49659`，Run152=`07ac10f`；15模态/17边，控制只读可见 `d=e−eta`。Run150 只否定单一 translated fixed-shape 模板。

Run153 精读 Yang--Ozay 2021 §4.1--4.4、Algorithm1、Propositions2--5。有限缺测自动机编码 return language、决策时刻和因果输入串，不自动压缩连续信息集合。Run152 的 `{5,10,15}` 初始化遗漏首次成功前历史：正确记忆为 `last_return in {init,5,10,15}`。提升图有60状态/68边，从 `(0,init)` 全部可达；15个 `init` 状态为瞬态，45个为循环层。Run148 三 seed 只是固定零修正的首次 return 像，可作必要样本，不能代替真实 `(0,init)` 初始集或覆盖多周期同标签历史。当前证据仅为离散语义/可达性，不是信息充分性、RCI或递归可行性。

下一唯一问题：定义各 `(mode,last_return)` 的全部可见历史语言，并写出固定 global residual 下从 `(0,init)` 起始的 monotone common-outer-cover 算子及硬约束接口；语义确定后才实现一次迭代。
