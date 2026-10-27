# Run189 研究日志：物理有界 direct-offset meta domain

日期：2026-10-27。

## 仓库与文献

远端`main=1c49659`；最新成果为Run188 `b5253cbb`，tree `6a786415`，本轮无Run189远端分支。
基线项目39/39、研究验证320/320。按检查点只审计“物理bounds是否足以给出有用有界meta域”。

重读Houska §3.1--3.2、§6.2--6.7，Villanueva--Müller--Houska §3.4--3.5，以及Badalamenti
等2025 §3.5--3.6、§4.1。最新DC nonlinear CCTMPC仅核对摘要/问题概述。文献明确要求区分参数
多面体极点与包含极大意义下的extreme information sets。

## 精确命题

物理盒`[-1,1]x[-11/4,11/4]`的六方向支持为
`(1,11/4,51/40,1,11/4,51/40)`，其configured polytope精确等于物理盒。任何物理允许的
`P(y)`均包含于该盒，故物理包含域诱导ensemble的极端边界是单元素。该域虽有界，却退化为固定
worst-case box，不能利用在线集合差异。

## 实现、验证与边界

TDD先写5项测试；checker缺失时2项FAIL、3项ERROR，随后实现精确支持、vertex/configuration
检查、singleton边界证书和哈希绑定。聚焦5/5、阶段性项目39/39、研究验证325/325。

独立只读复审额外核查12个facet--incident-map恒等式，确认configuration边界退化时各offset仍为
紧支持；同时确认singleton结论来自普遍物理包含而非样本。无Critical、Important或Minor问题。

证据等级为`exact_physical_bound_meta_ensemble_singleton_extreme_set`；未构造variable
`H/Omega`、mode graph、控制或递归可行性。下一唯一问题是增加由可辨识information变量驱动的
约束，在一个source mode上产生至少两个互不包含且measurement-closed的真实extreme sets。
