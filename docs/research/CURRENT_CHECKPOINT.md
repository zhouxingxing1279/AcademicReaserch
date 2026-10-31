# 当前研究检查点 — Run213（2026-10-31）

**唯一主方向：** 四旋翼/无人机 MPC＋SMF 闭环；子课题随证据收敛，不预设无限时域保证。

**最新可验证增量：** Run212三包历史一致速度界（下界严格改善 `7040287/96000000 m/s`）已经实际接入Run208两层因果backup与Run210 8拍姿态必要guard。冻结四状态 `positive_high` 的真实可达第192拍，原独立盒两层backup为空；历史速度交集后两层backup和综合首力矩准入恢复为 **[-2/25,2/25] N·m**。同策略反事实重放成功准入拍数由191增至**192**，但第193拍仍拒绝。已执行状态保持在后验与硬约束内。**这是严格有限步局部证书，不是递归可行性或无限时域安全证明。**

**实现/证据：** `verification/check_history_tightened_backup.py`、`verification/test_history_tightened_backup.py`、`results/history_tightened_backup_20261031/checks.json`、[Run213日志](run213_research_log.md)。Python 3.13.5精确Fraction；5/5新增测试、语法编译、191拍历史重放、9个独立后继backup检查及220拍预算对照通过。测试在核对过的本地依赖镜像中完成；尚无完整仓库checkout回归或GitHub CI。远端新文件Git Blob SHA可与本地实测版本对照。

**文献：** Scott等（2016），DOI 10.1016/j.automatica.2016.02.036；Köhler等（2021），arXiv:2105.03427。本轮仅核对公开摘要及已有定向阅读笔记，统一去重87篇不变。

**未闭合：** 持续历史一致CZ/SMF、四状态完整鲁棒Tube MPC、终端RCI、递归可行性/稳定性、六状态四旋翼安全保证。Gate A = **blocked**。

**下一轮唯一优先任务：** 诊断第193拍再次拒绝的阻塞坐标和历史不一致角点，设计小窗口滚动CZ/等价历史线性约束估计，保持因果性并与原控制器同预算对照。
