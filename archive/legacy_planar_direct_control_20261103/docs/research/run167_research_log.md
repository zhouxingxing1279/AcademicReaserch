# Run167：测量范围支线的精确终止

日期：2026-10-12；从Run166本地`0e43865`、远端`eb0e6233424a462a929d225373bd1dba2f1d2648`
同tree `6070f696bf14a8cf21e7bca59b746eaff580b756`接续；远端`main=1c49659`。

## 文献与准入

精读Scott等2016 §2、§3.1 Proposition 1及证明、§5式(31)--(33)：精确测量更新是预测集与实际
测量逆像的generalized intersection；任何复杂度约减仍须外包真值。复核Alamo 2005摘要/已有片段
及Lu等2021的包含记录。本轮准入项目特定精确反例，不准入新SMF或MPC算法。

## 核心命题

当前初始化的14次miss精确到达`E14`，强制return满足`d_p^+=q+n_p`。精确
`h(q)=23312147/48000000≈0.485670`，已大于Run166阈值
`58684997/145000000≈0.404724`。取允许的`n_p=0`和达到支持的`q`顶点即为最小反例，所以完美
测量也无法保证该全局cap；删除该观测会破坏真值包含。

保留当前噪声`1/50`时，源支持必须降到至多`55784997/145000000≈0.384724`，即最多保留
`79.2152%`。证据等级：
`exact_noiseless_witness_rejecting_measurement_only_global_visible_cap_on_required_initialization_path`。

## 实现与验证

按TDD先新增4项Fraction测试并观察其因模块缺失失败，再实现检查器；检查器从现有return seed与配置
读取支持/噪声，锁定Minkowski支持、零噪声反例、必要源支持和声明边界。结果制品绑定代码、配置、
文献记录和本轮文档哈希。此反例改变研究方向，故不实现measurement gate或调小配置噪声。

## 方向总审视

当前传统主线仍只有冻结路径的必要条件链，没有terminal/recursive-feasibility闭环。连续三轮已把
center问题缩成三因素合同并排除measurement-only入口；继续局部fiber/法向枚举不会形成课题级贡献。
下一步必须转向可与四旋翼物理接口的future residual保证。

## 下一唯一问题

分解15-tick future residual的物理来源；同模型、同信息、同硬约束和同dropout语言下，审计是否能
证明`beta<=16254878/42598647`。若不能，给出物理合同不可达结论并停止该冻结模型支线。
