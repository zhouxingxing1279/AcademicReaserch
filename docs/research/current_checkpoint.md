# 研究短检查点（2026-10-30，Run203）

唯一总方向：四旋翼/无人机 MPC＋SMF 闭环与可完成硕士课题。Run200建立标量闭环基线；Run201给出四状态缺测信息下界；Run202建立四状态精确CZ递推和返包后速度可靠界。Run203将Run202精确有理后验**区间外包**接入15-mode位置包成功/缺失分支，建立未来两拍推力全区间任意跳变下的三拍硬约束准入审计。当前推力可见、选择一个tau0、后两拍tau=0；生成元和端点推力最大化均为有理数。10种合法历史分支（5/10成功或缺包、15只能成功）全部在3拍内满足原始硬约束，5个力矩网格点亦通过；这不是MPC、RCI或终端证明。

重要信息收益：10 tick高推力时，第3拍速度外包在成功包下为0.57028m/s，缺包下为0.66621m/s。假设的0.65m/s诊断阈值因此改变判定，但不是实际硬约束或终端集。**反例：** 恒定高推力、最大正横向扰动、永久零力矩，在第72拍达到v=3.02901705m/s，违反|v|<=3；因此局部安全不能递推为长期安全。

工件：`verification/check_mode_indexed_backup_admission.py`、`verification/test_mode_indexed_backup_admission.py`、`results/mode_indexed_backup_admission_20261030/checks.json`、`docs/research/run203_research_log.md`。Python 3.13.5标准库，远端字段镜像，9/9新增测试通过；完整仓库回归/CI未运行。文献重读Lorenzetti & Pavone (2020) Section IV-C/D/E 与 Athanasopoulos et al. (2017) 图约束切换概念，更新 `docs/literature/PAPER_READING_LOG.md`，仍为原84篇，不虚增。

**Gate A仍blocked。下一唯一任务：** 构造模式相关的非零因果反馈及一拍controlled invariant候选，检验成功/缺包与任意未来推力；若不可行，保存最小反例并评估收敛至有限时域安全过滤器方案。
