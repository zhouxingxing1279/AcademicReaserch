# Run158：救援后 mode-9 的共享 success/miss 安全见证

日期：2026-10-11；分支 `research/run158-affine-shared-branch`。

## 仓库接续

远端 `main=1c49659`、Run157=`4525d73`，远端 Run157 tree
`e55f24feaf9ca84ab3a6cff279c6440584ffefac` 与本地一致。只读取短检查点、第93章和 Run157
checker，未依赖聊天历史。

## 文献准入与方向纠正

精读 Goulart--Kerrigan 2007 的 affine output-feedback robust constraints 与 invariant error
approximation，重读 Hempel 2011 Section III-A--C/Theorem 1 和 Houska Section 6.5/Theorem 3。
这些工作已覆盖一般仿射输出反馈、fiber-shared input 与 information-set control。本轮只准入
当前 packet graph 上的一步 exact shared-branch witness。

进一步纠正下一问题：`(14,10)`、`(9,15)` 在当前第二周期各只有一个 constituent，先取共同
外包并不能形成非平凡命题。应先检查 `(9,15)` 下一拍的真实未知分叉，再把 success returns
并入具有多历史的 mode-0 target labels。

## 精确结果与证据等级

对 Run157 rescued mode-9 set 选 `K_p=0`、
`K_v=-114428600/70527869`。同一输入的 robust support 恰饱和 `572143/160000`。`9->10 miss`
与 `9->0 success` 两支共享真实误差半宽：`e_p` 约0.973594、`e_v` 约2.719148，分别严格小于
1与2.75；estimator targets 由 full mode-9 envelope 的既有精确 facet certificate 继承包含。

证据等级：`exact_one_step_shared_success_miss_safety_witness_after_affine_rescue`。不是 gain
最优、recurrent target inclusion、RCI、终端或递归可行性证明。

最终验证：`verification/` 215/215、基础 `tests/` 39/39、新 checker 定向4/4。九份本轮相关
artifact 由各自原 checker 重建并通过源码哈希绑定；Python compileall、JSON、checkpoint
长度与 `git diff --check` 均通过。

## 唯一下一问题

构造两个真正的多历史 mode-0 targets：把本轮 `9->0 success` 像与其余安全 `5->10`、
`10->10` returns 合并为 `(0,10)` family；把 Run157 `(14,10)` 的后续 success 像与
`5->15`、rescued `15->15` returns 合并为 `(0,15)` family。要求同一 source-label policy、
完整 `(eta,e)` 硬约束及下一层逐边 inclusion；若失败给 exact directional separator。
