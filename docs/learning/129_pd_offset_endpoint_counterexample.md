# 参数相关 offset 不能只查调度端点

## 量词先于综合

设当前调度 `p` 可见，但下一调度 `p+` 可在 `[0,1]` 任意跳变。参数相关 RCI family
`S(p)` 的一步条件不是只进入当前切片或某个预测切片，而是

`F(p,S(p)) subseteq intersection_{p+ in [0,1]} S(p+)`。

这与 Mulagaleti--Mejari--Bemporad 的 PD-RCI 定义和 Gupta 等式(11)一致。未来调度没有
rate bound 时，共同后继目标不能按当前 `p` 缩小。

## 精确最小反例

取无输入、无扰动标量 LPV 系统

`x+ = (1-p/2)x`,  `p in [0,1]`,

及参数相关切片

`S(p)=[-(1+p),1+p]`。

全部未来切片的交为 `[-1,1]`。从当前正顶点出发的最坏后继为

`g(p)=(1-p/2)(1+p)=1+p/2-p^2/2`。

两个端点均给 `g(0)=g(1)=1`，所以 endpoint-only 条件全部通过；但 `g` 在
`p=1/2` 取严格最大值 `9/8`，越过共同目标 `1/8`。这是一条纯有理数
`COUNTEREXAMPLE`：仿射动力学乘仿射顶点后是二次式，端点不再自动支配内部。

## 可独立核查的固定候选接口

对一维调度下已经给定的候选，每个 facet/vertex residual 可写为
`a p^2+b p+c`。闭区间精确最大值只需比较两个端点，并在 `a<0` 且
`p*=-b/(2a)` 位于区间内部时加入该驻点。checker 全程使用 `Fraction`，不以网格采样或
浮点优化替代理论判断。

这只解决 **fixed-candidate verification**。在联合综合时，`a,b,c` 本身含决策变量，驻点也
随决策变化，一般不再是 LP。最近邻分别使用 S-procedure/SDP 或 Polya 松弛构造充分条件；
下一步若采用任何松弛，返回候选仍必须通过这里冻结的独立全区间验证。

## 不能推出什么

反例不说明 parameter-dependent RCI 不存在，也不说明 19-pair family 不可行；它只否定
“参数相关 offset 后继续只查推力端点即可证明不变性”。六状态嵌入、输出反馈 tube、硬约束
闭合与递归可行性仍全部开放，因此 Gate A 仍为 blocked。
