# 调度可见端点力矩下的 19-pair 精确 Farkas 否证

## 结论边界

对象仍是第48章审计过的四状态横向—姿态 19-pair configuration cone：38个对称
halfspaces、160个 simple vertices、参数无关 offsets。旧证书给每个状态顶点仅一个力矩，要求
它同时覆盖低/高推力端点；这不符合“当前推力先可见”的冻结合同。

本轮把每个顶点力矩拆为 `tau(v,T_low)` 与 `tau(v,T_high)`，因此决策从
`38+160=198` 扩为 `38+2*160=358`。完整 LP 有6080条 configuration、12160条 endpoint
invariance 和1280条 hard-state 不等式，共19520条；物理限幅与不设力矩限幅两种 HiGHS
模型均不可行（`NUMERIC_CHECK`）。

## 精确电路

从无界模型的对偶支持中选出24条原始有效不等式。checker用`Fraction`重建每个4x4 vertex
map、动力学、扰动支持和硬约束行，不依赖SymPy。所得系数矩阵秩为23，存在全部严格为正的
有理乘子，使扩展358维变量空间中的

`y^T A = 0`,  `y^T b = -3069803/88290 < 0`。

320个端点力矩列分别逐列抵消；证书不使用力矩限幅、pair-offset等式或`q>=0`边界。因此它是
该固定 configuration cone 在正确调度可见量词下仍不可行的精确 `COUNTEREXAMPLE`，且矛盾
不是执行器饱和造成。

## 端点充分性与不能推出的结论

冻结模型的`A(T)`、`W(T)`支持及两个端点力矩的仿射插值均关于`T`仿射，所以端点约束覆盖
连续推力区间。本结论仍不能排除其他法向、parameter-dependent offsets、PWA/非线性控制、
一般PD-RCI、六状态嵌入、输出反馈tube或递归可行性。

本轮纠正了旧证明的控制信息量词，但没有关闭Gate A。下一步应选择严格包含当前候选的最小
parameter-dependent-offset CC/RCI 类，并预先规定可独立核查的可行证书或Farkas否证。

