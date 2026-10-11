# Run159：`J14 -> 15` 三步位置支持反证

日期：2026-10-11；分支 `research/run159-affine-return-obstruction`。

## 仓库与文献核查

从干净的 Run158 本地提交 `57c3ed7` 接续；其 tree `f72d29ca` 与远端 Run158 一致，远端
`main=1c49659`。只读取短检查点、Run156--158 相关推导/checker。定向重读 Goulart--Kerrigan
2007、Yang--Ozay 2021 与 Houska 的相关章节；准入项目特定 exact path certificate，不作算法
创新声明。

## 方向纠正与精确结果

检查点要求合并 `(0,10)`、`(0,15)` 各三条 return histories，但 Run158 尚未构造两个 rescued
`(0,15)` final success images。先补路径发现：`10->15` 可继续安全 success；`15->15` 沿
Run158 gain 在 mode 11 位置超限。进一步消除 gain 偶然性：从 `J14` age-8 exact set 出发，
三条 miss 的零输入 mode-11 位置支持为 `3714127151/3600000000`。age 8、9 两次 bounded
affine correction 最多削减 `3h^2U`，故任何该类策略仍满足

`h_ep >= 369867929/360000000 = 1 + 9867929/360000000`。

因此 `15->15` constituent 在当前候选类中精确不可行，不能构造安全 `(0,15)` target hull。
证据是 `exact_three_miss_position_support_lower_bound`，不否定更早控制、不同 seed/residual 或
一般 output feedback。

## 实现与验证

按 TDD 先写3项测试并观察缺失模块/CLI失败，再实现 exact checker 与 hash-bound artifact。
最终基础测试39/39、verification 218/218（其中本轮3项）通过；7份历史 artifact 仅因统一
文献表哈希变化由原 checker 重建，数值与结论不变。Python compileall、全部 JSON 解析、
checkpoint 长度与 `git diff --check` 均通过。提交 SHA 见 git 历史。

## 唯一下一问题

把 affine correction 从 `J14` return seed（mode 0）开始介入，联合综合完整15步 dropout cycle，
检查能否在不破坏早期状态/输入约束的前提下把 age-8 source 缩到本轮必要阈值以内。
