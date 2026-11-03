# Run155：同标签仿射凸化交换律审计

日期：2026-10-11；分支 `research/run155-affine-convexification-gate`。

## 仓库接续

先检查远端：`main=1c49659`，Run152=`bf8ea72`、Run153=`9ab357f`、Run154=`ee769f2`。
本轮从与远端 Run154 同树 `0742f114` 的本地提交 `9d327d7` 接续，未通读旧历史。只读取
Run154 检查点、准入卡、第90章以及 Run148 三-return证书摘要。起点工作树干净。

## 文献门槛与选择

重新精读 Hempel--Kominek--Werner 2011 §III-A--C、Definition 2、Theorem 1、式(3)--(14)：
同一 noisy-output fiber 的全部相容状态共用一个输入，且输入盒与鲁棒后继同时受约束。定向
复核 Houska §6.4--6.5/Theorem 3 的 extreme information set 凸权重控制。两者表明本轮交换
律是已有一般框架的直接特化，因此只准入实施引理，不准入“新算法”或数值优化器。

## 本轮结论

在固定 global residual、线性边映射、凸扰动/硬约束及单一 affine-in-`d` policy 下，闭环边
映射是仿射的；其作用与同标签 constituent sets 的凸包严格交换，输入像亦然。因此 convex
hull 新生成的 fibers 无需逐点枚举，前提是每个 constituent set 对同一策略、同一边已有证书。
这只消除一个验证重复项，不消除逐边 target containment 或 fixed-point 义务。

同时纠正候选实例：Run148 三个首次 return seeds 在扩展自动机中属于三个不同
`last_return` 标签。跨标签共同凸包是合法但更粗的 mode-only fallback，会抹掉历史精化，不能
作为45-state recurrent family。第一个正确的同标签凸化实例应传播九条第二周期路径，并按三个
共同 target `(0,5)/(0,10)/(0,15)` 分组。

## 实现与验证决定

本轮不写求解代码：准入命题是纯代数交换律，添加采样或浮点 checker 不会提高证据等级；而
九路径实例在尚未冻结每个 source 标签的一张 affine policy 前实现，会重犯“逐路径另选控制”
错误。仅更新文献记录、实施引理、短检查点和可追溯日志。仓库既有 checker 在更新文献哈希后
应全部复验。

## 证据等级与唯一下一问题

证据等级：**精确代数引理；不是 RCI、递归可行性、性能优势或创新证明。**

唯一下一问题：在 fixed global residual 下，为 `(0,5),(0,10),(0,15)` 三个 source 标签各冻结
一张可审计 affine-in-`d` 策略（先以零策略为基线），精确传播九条第二周期 return histories，
按共同 target `last_return` 分组三个凸包，并检查所有中间 tick 的执行器/状态约束与三组 target
包含；若零策略失败，先给最早精确反例，再决定是否准入非零仿射综合。
