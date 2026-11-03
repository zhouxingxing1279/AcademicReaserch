# Run164：`J14` 可见纤维方向半宽纠错

日期：2026-10-12；从Run163本地`56a89e9`、远端`d99f456`同tree `a4f30a8`接续；远端
`main=1c49659`。

## 文献与准入

全文定向重读Scott等2016 Sections 2.2、3.1--3.2；复核Goulart--Kerrigan 2007相关
information-set反馈章节；Alamo等2005仅核查正式摘要、问题设定与可访问正文片段。最近邻已覆盖
CZ等式切片和按实际测量形成consistent set，故不声明新集合算法。准入仅通过“既有门槛量词纠错”。

## 命题与证明

成功测量可见 `d=e-eta`；`J14`中 `d_v=(103/100)d_p`，独立观测矩阵为一行 `D`。对控制方向
`F=e_p+14h e_v`，证明最坏观测fiber半直径等于
`max{Fz: |z|∞<=1, Dz=0}`。原始/对偶精确证书给出lambda=`29/15`、共同目标
`16315003/75000000≈0.21753337`；相较整体无条件半宽
`3889781459/3600000000≈1.08049485`，已低于单位必要门槛。

因此Run161“无条件J14方向半宽必须缩小7.4498%”只对所有观测共用同一原点/计划的固定合同成立，
不是按实际 `d` 条件化重规划的必要条件。Run160镜像代数本身不删，但其对一般measurement-
conditioned策略的外推撤回。证据等级：
`exact_primal_dual_visible_fiber_width_and_quantifier_correction`。

## 实现与验证边界

新增精确Fraction检查器和四项回归测试，验证原始可行性、对偶等值、无条件/条件化门槛反转及声明
边界。该结果不证明15-tick完整路径安全、终端闭合、旧计划移位、递归可行或六自由度保证。

复现命令：`python verification/check_vertical_visible_fiber_width.py --output <new-file>`；基础测试
`python -m unittest discover -s tests -v`为39/39，通过；全量理论验证
`python -m unittest discover -s verification -p 'test_*.py'`为230/230，通过。首次全量运行的10项
失败均由本文献索引变更触发历史制品哈希不匹配；只刷新对应SHA-256后数值载荷未变并全量通过。

## 下一唯一问题

以观测参数 `d_p` 表示每个 `J14(d_p)` fiber，构造并验证一张因果的15-tick竖直安全/终端包含
证书；必须同时覆盖绝对中心偏移、位置/速度/输入约束及success/miss后继。若失败，给出某个可达
`d_p` fiber的精确反例，而不能再用整体J14宽度替代。
