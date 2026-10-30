# 研究短检查点（2026-10-30，Run202）

主目标：无人机 MPC + SMF 可复现闭环与可完成硕士课题。承接 Run201 四状态位置缺测必要信息下界，Run202 在同一冻结降阶模型上实现了**精确有理 CZ 测量一致递推**（每 tick 姿态/角速率观测、位置最长15 tick返包）和独立区间可靠外包；CZ投影支持使用浮点 LP，仅为数值诊断。

**新增严格条件结论：** 对固定可见推力、零观测历史及合法返包，消去初始未知速度可得 `|v_n|<=2σp/(nh)+h(n+1)(Tσφ+d(T))/2`。在15 tick返包时，低/高推力速度可靠半宽从返包前区间 `0.69371/0.75312 m/s` 降为 `0.44998/0.48166 m/s`，分别收紧35.1%/36.0%；返包前速度必要半宽 `0.68635/0.73105m/s`，不得套用于返包后。不是终端 RCI 或四旋翼闭环保证。

**工件：** `verification/check_four_state_conditional_smf.py`、`verification/test_four_state_conditional_smf.py`、`results/four_state_conditional_smf_20261030/checks.json`、`docs/research/run202_research_log.md`；本地 Python 3.13.5 + SciPy 1.17.0，最小配置字段镜像7/7测试通过，尚未在完整远端仓库回归。

**文献：** Scott et al. (2016) Definition 2/3、Section 3.1；Lorenzetti & Pavone (2020) Section II/IV；均为已有84篇内的定向重读，非新增篇数，记入 `docs/literature/PAPER_READING_LOG.md`。精确 CZ 运算不主张创新。

**Gate A：blocked。** 无四状态可行 backup/terminal/递归可行性证明，无六状态安全保证。下一唯一任务：将返包速度界映射到 15-mode SMF—MPC 的因果成功/缺包分支及未来推力全区间下的控制准入与终端集合，测试是否可行。
