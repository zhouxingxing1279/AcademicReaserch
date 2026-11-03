# Run157 文献准入卡：临界 miss 前驱的仿射可见反馈

## 本轮问题与最近邻

1. **Goulart--Kerrigan--Maciejowski 2006**：精读 Introduction、Sections 2--4。有限时域
   affine state/disturbance feedback 与 robust polyhedral constraints 的凸化已有完整方法。
2. **Hempel--Kominek--Werner 2011**：重读 Section III-A--C、Definition 2、Theorem 1。
   同一 noisy-output fiber 上必须使用同一输出相关输入，并同时满足输入与后继约束。
3. **Houska 2023/2026**：重读 Sections 6.4--6.5、Theorem 3 证明。一般 information-set
   feedback 和 extreme-set convex interpolation 已覆盖，不可由零策略失败推出一般失败。

## 严格差异与证明义务

本轮不提出 affine feedback 新算法，只检查当前四旋翼竖直合同中两个 exact critical fibers：
`J_9` 第14条 miss 与 `J_14` 第9条 miss。策略限定为可见且因果的
`delta T=K_p d_p+K_v d_v`，使用与 Run156 相同的 global residual、状态硬约束和 correction
盒。最强同条件基线是 Run156 的零/label-only 策略。

必须先纠正时序：导致超限的动作分别取于 age 13 和 age 8；这两条当前边均是确定 miss，
并非 mode 4/9 的未知 success/miss 分叉。一步见证仍须 robustly 覆盖 source fiber、输入盒和
真实 `e_v` 盒，但不能冒充后续 target inclusion 或分叉闭合。

## 推动作用与可证伪条件

若任一 critical fiber 在 correction 盒内没有 gain，可继续寻求对偶不可行证书并终止该策略
类；若存在，则 Run156 的局部宽度反例已不再阻塞 affine-in-`d`，下一步应检查救援后集合的
共同 target inclusion 及 mode-9 下一控制时刻的共享分叉。浮点样本或单点成员不算通过。

## 判断

**通过精确一步可行性见证；不通过算法创新、gain 最优性、RCI 或递归可行性声明。**
