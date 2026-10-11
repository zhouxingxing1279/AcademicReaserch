# Run157：临界 miss 前驱的精确仿射救援

日期：2026-10-11；分支 `research/run157-affine-rescue-witness`。

## 仓库接续

核查远端 `main=1c49659`、Run156=`0528186`，本地 Run156 tree
`577bcd0c4d960ca0e35d0b7e51e910c468123f10` 与远端一致。只读取短检查点、Run156 反例和
Run148/150 exact generator maps；未重扫全部历史。

## 文献与准入

精读 Goulart--Kerrigan--Maciejowski 2006 Introduction、Sections 2--4，重读 Hempel 2011
Section III-A--C 与 Houska Sections 6.4--6.5。仿射 robust feedback、fiber-shared input 和
information-set control 均已有直接近邻。本轮只准入项目特定的一步 exact witness。

## 精确结果

先纠正 Run156 下一问题的时序：超限 miss 的输入取于 age 13/8，两条当前边没有未知分叉。
对两个 exact source zonotope 取 `delta T=K_v d_v`、`K_p=0`，并令 robust input support 恰好
饱和 `572143/160000`。所得精确 gains 为
`-114428600/45315007` 与 `-114428600/72816441`；下一真实速度半宽分别约2.71470、2.70783，
相对 `11/4` 有严格余量约0.03530、0.04217。故 Run156 的三个局部零策略失败均有一步
affine rescue（后两个共享同一个 `J_14` 前驱见证）。

## 实现、验证与证据等级

新增 exact-rational checker 与三个定向测试，直接从 Run148 seed 生成元传播，不使用样本成员
或浮点优化器作证书。证据等级为
`exact_one_step_affine_in_visible_velocity_rescue_witness`。不声称 gain 最优、target inclusion、
shared-branch closure、RCI 或递归可行性。

最终验证：`verification/` 211/211，基础 `tests/` 39/39；新 checker 定向4/4。七份受
`READ_PAPERS.md` 哈希绑定的历史 artifact 均由原 checker 重建，除该哈希字段外内容不变。
Python compileall、全部 JSON 解析、checkpoint 长度与 `git diff --check` 均通过。

## 唯一下一问题

对救援后的 `(14,10)` 与 `(9,15)` exact sets 建立按 target `last_return` 分组的共同外包；先
检查其完整 `(eta,e)` target inclusion，并在 `(9,15)` 的下一控制时刻为 success/miss 两分支
综合同一 affine-in-`d` 输入。若共同 target 不存在，给出精确支持/对偶反证。
