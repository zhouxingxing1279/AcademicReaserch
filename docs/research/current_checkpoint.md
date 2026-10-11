# 研究短检查点（2026-10-11，Run157）

主线：传统 SMF/鲁棒输出反馈 MPC；学习暂停。远端 `main=1c49659`、Run156=`0528186`；控制只读可见 `d=e−eta`。

Run157 精读 Goulart--Kerrigan--Maciejowski affine-feedback Sections 2--4，重读 Hempel fiber 量词与 Houska information-set control。纠正时序：Run156 超限动作取于 age13/8，两条当前边均为确定 miss，不需同一步 success/miss 共享。对 `J_9` age13、`J_14` age8 exact fibers，取 `deltaT=K_v d_v`、`K_p=0`，精确 gains 分别 `-114428600/45315007`、`-114428600/72816441`，robust input support 均恰饱和 `572143/160000`；下一 `e_v` 半宽约2.71470、2.70783，低于2.75且余量严格为正。故Run156局部超量可一步修复。证据仅为 exact one-step witness，不是gain最优、target inclusion、RCI或递归可行性。

下一唯一问题：对救援后的 `(14,10)`、`(9,15)` exact sets 建立按target标签分组的共同外包，检查完整 `(eta,e)` target inclusion；随后在 `(9,15)` 下一控制时刻为 success/miss 两分支综合同一 affine-in-`d` 输入。
