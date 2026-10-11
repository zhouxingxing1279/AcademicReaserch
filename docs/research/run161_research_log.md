# Run161：`k=14` 三因素合同权衡与信息接口审计

日期：2026-10-11；分支 `research/run161-k14-tradeoff-interface`。

## 仓库接续与文献门槛

从本地 Run160 `84a01a6` 接续，其 tree `04163b0b` 与远端 Run160 `c11faa0` 一致；远端
`main=1c49659`。只读取短检查点、第96章及其 checker。新增精读 Lu--Cannon--Koksal-Rivet
2021 的 set update、tube、recursive-feasibility 与 fixed-complexity convergence 章节；定向重读
Köhler 2021 与 Dey--Bhasin 的 online bound/compatibility 条件；Robbins 2026 仍只有正式摘要。
准入仅限 exact necessary trade-off 与信息对象审计。

## 核心结果

对 seed directional half-diameter、future residual、correction authority 分别引入缩放
`alpha,beta,gamma`，得到

`alpha*(3889781459/3600000000) + (beta-gamma)*(52065013/400000000) <= 1`。

当前 `g_r=hU`，故 baseline residual 增长与乐观输入削减精确相消。单因素通过必要条件至少要求：
seed方向半直径缩小7.4498%，或未来residual缩小61.8418%，或correction authority增加61.8418%。
一般后验的第一项必须由正反两个support计算；单侧support不等于非中心集合的半直径。只有第一项
可能由当前可靠 SMF posterior 直接提供；第二项需要独立的未来扰动/模型集合保证，
第三项是物理执行器与输入分配合同。阈值仅是 admission 必要条件，不是充分安全证书。

## 实现与验证

按 TDD 先观察模块不存在及新增分解字段缺失的失败，再实现 exact-rational checker。最终测试与
artifact 结果在提交前冻结记录。第一次全量 verification 的9项失败均来自 `READ_PAPERS.md`
哈希变化；用各自原 checker 重建后，删除 `source_sha256` 的历史载荷9/9完全一致。最终基础
测试39/39、verification 226/226（本轮新增5项）、单模块5/5通过；compileall、全部JSON、
checkpoint长度和`git diff --check`均通过。

独立审阅确认分数与量纲正确，同时指出非中心 posterior 的单侧 support 不能替代镜像证明所需
半直径。已把在线 gate 修正为 `[h_X(a)+h_X(-a)]/2`，增加非对称集合测试；另补齐归档文件
比较和 `check_intermittent_metric.py` 传递依赖哈希。

## 主线总审视与唯一下一问题

本轮避免继续调 gain，把 Run160 的反证转成可由在线后验查询的控制相关阈值。仍未形成论文级
闭环方法。下一轮唯一问题：定义 `alpha` 的在线双侧支持/方向半直径查询及短-dropout fallback，证明 gate
通过时不破坏旧计划移位，未通过时仍有安全可执行动作。

