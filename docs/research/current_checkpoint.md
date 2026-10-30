# 研究短检查点（2026-10-30，Run201）

主目标：四旋翼 MPC + SMF 的可复现闭环与可完成的硕士课题。承接 Run200 main=`25aa83bfe2e0` 的**标量**间歇 SMF-MPC 闭环，本轮转入原四状态横向—姿态冻结合同的**必要**观测信息边界；不把标量递归可行性证明迁移为四旋翼安全结论。

**新增可验证结论：** 在合法的15 tick位置丢测历史上，若初始后验包含配置中的两条对称极端状态，持续姿态/角速率观测无法辨别独立横向扰动的对称轨迹。对任意仅使用共同可见历史的因果推力/力矩控制，横向位置后验的必要半宽至少为 `211342043/1600000000 ≈ 0.13208878m`（低推力给出的统一下界）；固定高推力时为 `221354129/1600000000 ≈ 0.13834633m`。该结果不构成全局位置约束违例、终端/RCI不存在性或四旋翼闭环证明。

**工件：** `verification/check_lateral_dropout_support_floor.py`、`verification/test_lateral_dropout_support_floor.py`、`results/lateral_dropout_support_floor_20261030/checks.json`、`docs/research/run201_research_log.md`。本地 Python 3.13.5 在核对的配置字段镜像上7/7测试通过，9组精确分数审计；未运行整个远端仓库回归或 CI。

**文献：** `docs/literature/PAPER_READING_LOG.md` 增加 Lorenzetti & Pavone（2020）原文 Section II/IV 定向重读，原84篇去重计数不变。其耦合误差 RPI 与终端闭合是强基线，不能作为本项目创新。

**Gate A：blocked。** Run199 的19-pair affine-offset/common-core SOCP 浮点不可行 ray 仍不是精确类普遍不可行证明；尚无原四状态的充分 terminal/backup 控制证书。下一唯一问题：实现四状态条件化 SMF（含每 tick 姿态观测）可靠外包并与15 tick必要半宽及终端收紧进行兼容性检查。
