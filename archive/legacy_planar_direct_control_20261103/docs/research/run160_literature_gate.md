# Run160 文献准入卡：完整15步 return 的输入权限下界

## 最近邻正文核查

1. **Yang--Ozay 2021（全文重读）**：Sections 2--4、Assumption 1、product safety construction。
   missing-measurement controller 必须对自动机允许的整条 string 及全部中间状态保证安全；只检查
   return 时刻不充分。
2. **Rungger--Tabuada 2017（全文重读）**：Introduction、式(1)--(10)、Lemma 1 与 outer/inner
   RCI discussion。有限前驱层通常不是 RCI；不可行结论必须来自正确量词下的必要条件。
3. **Goulart--Kerrigan 2007（定向重读全文）**：finite-horizon affine output-feedback robust
   constraints 与无限时保证条件。仿射综合已有成熟近邻，本轮不具有算法首次性。
4. **Rutledge--Yong--Ozay 2020（仅核查作者全文的摘要/引言，正文抓取超时）**：提出 intermittent
   measurement 下的 equalized recovery；本轮不引用其定理，只记录其允许缺测期暂时放宽再恢复的
   问题设定。当前合同要求每拍 `|e_p|<=1`，不采用这种放宽。

## 差异、最强基线和证明义务

最强同条件基线是 Run159 的 age-8 affine-class obstruction。本轮从 `J14` mode-0 seed 起允许
每拍控制，并进一步放宽为任意 full-state causal policy。唯一证明义务是：在每拍 pointwise input
盒下，构造两条 admissible 镜像轨迹，给出与策略形式无关的位置半直径必要下界。

## 推动作用与可证伪条件

若在14条 miss 内所有下界均不超过1，则不能否定更早反馈，应转入有限时域综合；若某一步严格
超过1，则当前15步 recurrent constituent 在乐观放宽问题中也不可行，应停止调 gain，并转向
seed/residual/input-authority 合同审计。任何输入权重、residual 时序或 exact fraction 错误都会推翻
证书。

## 判断

**通过项目特定的 policy-independent full-cycle necessary obstruction；不通过新算法、一般
output-feedback 不可行、RCI、递归可行性或六自由度保证声明。**
