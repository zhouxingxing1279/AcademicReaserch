# Run160：`J14` 完整15步周期的策略无关输入权限反证

日期：2026-10-11；分支 `research/run160-full-cycle-authority-obstruction`。

## 仓库接续与文献门槛

从本地 Run159 `97c1af1` 接续；其 tree `6bc5cb34` 与远端 Run159 `9d3e928` 一致，远端
`main=1c49659`。只读取短检查点、第95章及相关 exact generator checker。重读 Yang--Ozay
2021、Rungger--Tabuada 2017、Goulart--Kerrigan 2007 的相关正文；Rutledge--Yong--Ozay
2020 仅核查摘要/引言并明确标注，不引用其定理。

## 核心结果与方向纠正

Run159 未排除 mode-0 起更早反馈。本轮从 `J14` return seed 起，允许每拍任意 causal bounded
control，并进一步放宽为 full-state feedback。对一对镜像初态/扰动轨迹，输入差始终不超过
`2U`，故 `k` miss 后的位置半直径至少为

`H_k^0 - k(k-1)h²U/2`。

第12个 miss 下界为 `398207933/400000000≈0.995520`；第13个 miss 首次升至
`934206607/900000000=1+34206607/900000000≈1.038007`。所以当前 fixed global residual、
`J14` seed 与 correction 盒下，任何 causal policy 都不能保证15-tick return 的中间状态安全。
这不是局部 gain 失败，而是输入权限不足的完整周期必要反证。

证据等级：`exact_policy_independent_full_cycle_position_diameter_obstruction`。它不否定不同 seed、
scheduled/tighter residual、更大 correction authority 或完整六自由度合同。

## 实现与验证

按 TDD 先观察核心测试与 artifact CLI 因缺少实现而失败，再实现 exact-rational checker。最终
基础测试39/39、verification 221/221（本轮新增3项）通过；8份历史 artifact 仅更新统一文献表
哈希，移除该字段后内容8/8不变。Python compileall、全部 JSON、checkpoint 长度与
`git diff --check` 均通过。提交 SHA 见 git 历史。

独立审阅未发现证明或算术问题；指出 artifact 未绑定 `J14` seed 的四个传递依赖，以及单模块
测试导入依赖 discovery 路径。已把 correlated seed、mode radius/nestedness、joint predecessor
checker 纳入 `source_sha256`，并显式 bootstrap `verification/` 路径；随后同时验证 discovery 与
`python -m unittest verification.test_vertical_full_cycle_input_authority -v`。

## 主线总审视与唯一下一问题

当前研究已从局部模板否证升级到一条完整 dropout contract 的输入权限必要条件，但仍未形成论文级
闭环方法。停止继续为当前 `J14->15` constituent 调 gain。下一轮唯一问题：推导 `k=14` 安全所需
的 seed contraction、global residual reduction 与 correction authority 三者的精确 trade-off，
并核查其中哪一项能由可靠在线集合信息在同扰动保证下实现。
