# 当前研究检查点 — Run212（2026-10-30）

**唯一主方向：** 四旋翼/无人机 MPC＋SMF 闭环；子课题随证据收敛，不预设无限时域保证。

**本轮可验证增量：** 在Run210 `positive_high` 第192拍真实可达历史，利用第150、165、180拍位置返包及150..190每拍姿态观测，建立精确有理数三包历史一致速度外包。旧独立SMF盒速度下端 `-2.4931037251954926 m/s` 被排除；新严格下端 `-2.419767402278826 m/s`，精确收紧 `7040287/96000000 m/s`。因此Run211旧盒的该速度端点及包含它的联合角点与这段测量历史不相容。**这不是精确CZ后验，也未证明控制可准入或长期安全。**

**实现/验证：** `verification/check_three_packet_velocity_support.py`、`verification/test_three_packet_velocity_support.py`、`results/three_packet_velocity_support_20261030/checks.json`、[Run212日志](run212_research_log.md)。Python 3.13.5标准库Fraction；4/4测试、语法编译、191拍可达重放通过；在与远端算法核对的本地镜像执行，尚无完整仓库历史回归与GitHub CI。精确Fraction结果由脚本重生，JSON保留精确改善分数及近似展示值。

**文献：** Scott等(2016) *Automatica* 69:126–136，DOI 10.1016/j.automatica.2016.02.036，本轮复核Definitions 2–3、Proposition 1、Section 5片段；统一阅读日志去重87篇不变。

**未闭合：** 四状态完整鲁棒Tube MPC、终端RCI、递归可行性/稳定性、六状态四旋翼安全保证。Gate A = **blocked**。

**下一轮唯一优先任务：** 将三包历史一致速度界接入原Run208/210因果backup准入，对第192拍及整段闭环进行同策略、同信息的复核；检查能否真正扩大可接受首力矩集合，并记录仍阻塞的坐标与耗时。