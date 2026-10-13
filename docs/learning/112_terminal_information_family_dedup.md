# 112. Terminal information-family 排重与可靠包含判据

## 1. 对 Run177 的纠正

Run177 把 tick 5 的局部 success/miss 后继记为 `T_0/T_1`，这只适合说明**当前一条边**的
mode 标签，不能定义无限时域终端对象。仓库第 88、89 章及 Run154 已给出更完整的对象：
扩展标签 `q=(j,r)` 中 `j=0,...,14`，`r in {init,5,10,15}`。从 `(0,init)` 可达的 60 个
标签里，15 个 `init` 标签只覆盖首次 return 前的瞬态，45 个循环标签组成 terminal family；
循环子图有 51 条边（42 miss、9 success）。因此把终端压成两个集合会丢掉 future return
length 和不同历史造成的 information-set 差异。

这也不是本轮的新 terminal 构造。第 88 章已经用 `alpha/K/A` 写出有限信息抽象的五项充分
合同，Run154 又明确区分 transient initialization 与 recurrent terminal。Run177 的“下一步
定义 `T_0/T_1`”与这些成果重复且更弱，应撤回。

## 2. 可靠包含不是单个状态盒包含

令 `I(h)` 是可见历史 `h` 下的真实联合信息集，`alpha(h)=a` 是有限、因果抽象，`K(a)` 是其
可靠外包，`A` 是抽象 successor。一个可审查的 terminal-family 证书至少要同时验证：

1. **初始化覆盖**：每个合法 tick-0 posterior 均满足
   `I(h0) subset K(alpha(h0))`；
2. **逐边模拟**：在当前抽象状态只选一个共享控制，对每个合法真实状态、扰动、共享物理原语、
   packet outcome 和下一测量，先做真实非线性预测再求交所得 `I(h+)` 均满足
   `I(h+) subset K(A(a,ell,y+))`；
3. **硬约束**：上述量词范围内状态、余项 source domain 和执行器约束全部成立；
4. **循环闭合**：首次 return image 覆盖到对应循环标签，且 45 个循环标签上的 51 条边全部
   满足同一 policy 下的逐边模拟。

因此 inclusion oracle 的输入至少是 `(source label, target label, source information set,
shared control, edge)`，而不是“后继状态盒是否落入 `T_0` 或 `T_1`”。测量成功只能缩小
posterior，不能物理重置真实状态；不同标签也不能用一次跨标签凸包替代。

## 3. 文献边界与新的停止点

Houska 的 information ensemble 已把信息集的集合当作控制对象，并要求该族对与任意紧集的
交保持闭合；极端集合/向下闭包给出有限表示思路。这支持仓库第 88 章的抽象接口，但不替当前
非线性 plant 自动给出 `Gamma`、actual-thrust-dependent residual 的 source-domain 外包或
60-state 逐边证书。

所以本轮不实现新的 fixed point 或两集合 checker。真正未决问题下推为：先为真实非线性 plant
冻结一个最小、固定复杂度的 information-ensemble 表示 `Gamma` 与可靠 source-to-target
包含 oracle，在扩展图的一条 miss 和一条 success 边证明 sound simulation；只有通过后，才
值得求 45-state terminal fixed point。

证据等级：`repository_dedup_plus_primary_full_text_contract_correction`。这不是 RCI、递归可行性、
数值可行性或创新证明。
