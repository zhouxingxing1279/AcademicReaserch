# Run177 研究日志：五步前驱的初始族、时序与 mode 纠正

本轮只从 Run176 检查点读取必要源码：`configs/planar_baseline.json`、`plant.py`、`sensing.py`、
`filter.py`，并核对最近邻文档。源码确认 tick 0 先用实际测量更新 prior；因此配置本身不能唯一确定
posterior。`advance` 明确采用“输入—真实预测—下一 tick 测量求交”的顺序，tick 5 的 success/miss
发生在第五个输入以后。位置周期为 5 且初始 miss age 为 0，故 tick 5 的两条边都合法。

全文重读 Baras--Patel 1998 §IV-A 的 information-state recursion、表示/分离结果与有限时域动态规划。
它支持把全部相容历史压入信息状态再执行 `exists u / forall observation successor`，但不支持把配置
prior 或单个 box 当作唯一初始状态。结合源码，本轮把待证对象纠正为对全部可行 tick-0 测量的
posterior 族，并把终端拆为 success 的 mode 0 与 miss 的 mode 1 information-family。

本轮没有实现求解器。原因不是计算失败，而是准入卡不允许在 terminal family 及包含判据未定义时
实现单盒数值检查器；那会把成功测量的 estimator 收缩混成物理 reset，并漏掉 miss 后继。另一个
边界是 vertical slice 需要控制器选择 `tau=0`，故只能作为构造性受限子问题，不能产生完整六维
策略不存在的反证。

失败/停止记录：曾考虑直接对竖直 `pz,vz` box 做五步极值传播；源码审计发现这会忽略初始测量值
参数、always-observed 噪声 history 的共享输入约束及 tick-5 mode 标签，停止该实现。当前证据等级为
`timing_and_quantifier_contract_from_source_plus_primary_full_text`。

论文级主线仍未闭合：缺 mode-indexed terminal information-family、非线性可靠外包、五步回返证书、
15-mode 递归闭包、同预算强基线与四旋翼闭环。下一唯一问题：定义可计算的 `T_0/T_1` terminal
information-family 及可靠包含判据，使全部可行 tick-0 posterior 的五步 success/miss 后继都能在
同一 observation-fiber 策略下接受检验。
