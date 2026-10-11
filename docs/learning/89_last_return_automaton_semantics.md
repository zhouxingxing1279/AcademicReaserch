# 89. `last_return` 扩展自动机：可实现语义与初始化修正

## 1. 当前图与记忆含义

当前 15-mode 图有 14 条 miss 边 `j->j+1` 和三条 success 边
`4->0, 9->0, 14->0`。`mode` 已表示当前 success 之后经过的 miss tick 数。为区分上一
完整周期的长度，引入

```math
r_k\in\{\mathrm{init},5,10,15\}.
```

`init` 表示尚未发生首次 success return，不能删去：仓库合同的真实初始化是
`(mode,d)=(0,0)` 及 Run136 的 `eta` 集，而不是 Run148 的三个 post-success seed。

扩展边定义为

```math
(j,r)\xrightarrow{\rm miss}(j+1,r),\qquad j=0,\ldots,13,
```

及

```math
(4,r)\xrightarrow{\rm success}(0,5),\quad
(9,r)\xrightarrow{\rm success}(0,10),\quad
(14,r)\xrightarrow{\rm success}(0,15).
```

该更新只依赖已观察到的 packet outcome 和旧标签，因而是因果且确定的。枚举得到 60 个状态、
68 条边；从 `(0,init)` 出发 60 个状态均可达，其中 `init` 层的 15 个状态是首次 return 前的
瞬态，另外 45 个为循环层。计数来自直接提升配置中的 15 状态/17 边，不是安全性证明。

## 2. 与 string automaton 的关系

Yang--Ozay 在成功测量时采样，并把可能的 return string 当作环境选择；控制器必须在当前
decision state 为所有允许 return length 预先承诺同一因果输入串前缀。本项目逐 tick 图把
中间 miss 状态显式展开，因此 `(mode,r)` 只是该语言的一种实现性 refinement。它没有消除
如下连续状态：与完整测量/输入历史相容的联合 `(eta,e)` 信息集。

对每个标签 `q=(j,r)`，安全集合族必须覆盖语言

```math
\mathcal H_q=\{h:\alpha(h)=q\},\qquad
\bigcup_{h\in\mathcal H_q}I(h)\subseteq K_q.
```

Run148 的 `J_4,J_9,J_14` 只覆盖从真实初始化、零修正出发的三条**首次** success 路径，故
它们可作为 `(0,5),(0,10),(0,15)` 的必要初始化样本，但不是这些标签在无限循环下的完整
初始化集合，更不是 `(0,init)` 的替代品。

## 3. 当前能证明与不能证明的命题

**已证明（离散语义）**：上述 60 状态扩展是当前 packet 图的有限、确定、因果 refinement；
它保留所有原图路径，且 `last_return` 精确记录最近一次已完成周期长度。

**尚未证明（连续充分性）**：两个具有相同 `(mode,last_return,d)` 的历史可能在更早周期中
不同，继而具有不同联合信息集。`last_return` 单独不是充分统计量。共同外包可能存在，但必须
从真实 `(0,init)` 初始集做 monotone reachable/fixed-point 包络，并对每条边使用同一当前
控制和同一物理原语。固定 global residual 只移除 thrust-scheduling 依赖，不会自动给出闭合。

**结论**：本轮修正的是 Run152 的初始化与状态语义，不是 RCI、终端集或 MPC 递归可行性。
在定义完整历史语言/包络算子前直接启动三-seed 求解器，会把首次 return 样本误当作循环状态
全集，产生不可靠的正证书。
