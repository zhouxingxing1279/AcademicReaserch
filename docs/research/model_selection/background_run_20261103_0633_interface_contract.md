# 外环 MPC 模型迁移合同审计（2026-11-03 06:33 PST）

## 本轮唯一问题
Santos–Lagoa 的预稳定位置参考型 Tube MPC 能否在成熟 PX4 内环上按原模型直接使用？**结论：不能直接使用；需要版本固定的闭环辨识与可靠残差界。**

## 仓库读取与并发边界
GitHub commit search 返回最近 main 候选 `eb18e857090b0babe531c13c61aea944793af428`，本分支由该明确 SHA 建立；搜索排序不构成原子 HEAD 证明。读取 `docs/research/CURRENT_CHECKPOINT.md`、`docs/literature/PAPER_READING_LOG.md`、`docs/research/model_selection/MODEL_SELECTION_EVIDENCE.md`、`configs/planar_baseline.json`；检查 PR #188（open，基于相同 main，接口日志未合并）。main 上现有模型矩阵仍以平面六状态 wrench 级模型为首选，**与本任务的新外环权限不一致**，须待外环模型合同通过再更新唯一矩阵。旧四状态 Run246/260/261 不能迁移证明。

## 本轮实际证据与阅读等级
- **新增完整论文阅读 0、部分正文阅读 0、摘要/既有书目复核 3**（Santos–Lagoa 2022、Andriën et al. 2024、Xue et al. 2024；后两篇细节依据仓库既有总账，**不是本轮重新核验原始全文**）。因此未达到常规至少3篇原始论文正文核验目标，不能把此轮标为论文专题完成。
- Santos, D. A.; Lagoa, C. M. (2022), *Wayset-based guidance of multirotor aerial vehicles using robust tube-based model predictive control*, *ISA Transactions* 128:123–135, DOI https://doi.org/10.1016/j.isatra.2021.12.002 。本轮 DOI 跳转 Elsevier PII S0019057821006182 不可访问；**未读原始方程、终端定理、采样/时域**。既有仓库记录描述位置参考、预稳定低层控制器、闭环平移状态 [r,rdot] 和 Tube MPC；**此为待原文复核的历史记录，不能当本轮公式证据**。
- Andriën, A. R. P. et al. (2024), *Model Predictive Control for Quadcopters With Almost Global Trajectory Tracking Guarantees*, *IEEE TAC* 69(8):5216–5230, DOI https://doi.org/10.1109/TAC.2023.3349098 。既有记录称外环加速度参考、专门设计的非线性姿态内环；**不是 PX4 黑箱位置闭环**，定理不可直接转移。
- Xue, R. et al. (2024), *Output feedback stochastic MPC for tracking control of quadrotors with disturbances*, *IET Control Theory & Applications* 18(5):566–580, DOI https://doi.org/10.1049/cth2.12588 。既有正文记录：六维平移加三维风增广、加速度虚拟输入、姿态 ADRC/ESO 内环；每拍六维位置速度带噪量测、机会约束，**不处理本任务位置失测下的确定性硬安全**。
- **本轮新读一级接口证据**：PX4 Offboard 官方文档 https://docs.px4.io/main/en/flight_modes/offboard （2026-11-03，main 滚动版本）。`TrajectorySetpoint` 中 position 有效时进入位置闭环，velocity/acceleration 可作为前馈；position NaN、velocity 有效时为速度闭环；两者 NaN、acceleration 有效时为加速度参考。文档仅证实接口语义，不证实确定性跟踪误差、延迟、带宽、饱和。

## 模型与接口合同（**建议，非已验证实验结果**）
设外环状态 `x=[p_x,p_y,p_z,v_x,v_y,v_z]^T`，实际飞控执行的参考 `r_k` 为位置、速度或加速度三种互斥接口之一：
1. **位置参考首选候选**：`x_{k+1}=A_cl x_k+B_cl p_ref,k+w_cl,k`。必须通过锁定固件/参数/机体/采样率后的 SITL/HIL 或飞行数据辨识 `A_cl,B_cl`；`w_cl` 包括模型残差、外扰、内环参考误差、通信延迟和饱和后未实现命令，且需确定性有界证据。不可把 `p_ref` 当加速度输入。
2. **加速度参考备选**：`p+=p+h v+(h²/2)(a_ref+e_a),v+=v+h(a_ref+e_a)` 仅在零阶保持且真实加速度跟踪误差 `e_a` 有界时成立。不能从 PX4 支持该 setpoint 推出 `e_a=0`。如实际内环有显著滞后，需扩充低阶闭环动态或采用保守多步扰动界。
3. **速度参考备选**：辨识 `v_{k+1}=A_v v_k+B_v v_ref,k+w_v` 并保留位置积分；不能把速度指令直接当 `v_{k+1}=v_ref,k`。
4. **约束**：状态 `X`、参考/变化率 `U,\Delta U`、地理围栏、速度/加速度限制；对鲁棒误差集合 `Z` 使用 `\bar X=X\ominus Z`。倾角/推力可实现域必须由成熟飞控限幅及保守物理关系/辨识验证，不能借用旧 `(T,\tau)` 盒。
5. **异步量测**：区分原始 GNSS/VIO 位置更新与 PX4 EKF 已融合输出；SMF/CZ 预测步与到达测量条带交集仅在噪声/初始/过程界有效时保证真值包含；不能把相关 EKF 与 IMU 作为独立信息重复融合。

## 阶段门槛与后续
- 本轮未修改唯一论文总账/模型矩阵（避免以不充分原文证据覆盖旧并发内容），未开发控制器、验证脚本、运行 SITL/HIL 或证明递归可行。
- 首选候选仍是**位置参考型三维六状态闭环平移模型**，加速度参考为备选；只是选型假设，尚未锁定。
- **下一轮唯一优先问题**：取得 Santos–Lagoa 正文/合法作者稿并逐式核验 `A_cl,B_cl`、位置命令含义、采样/时域、扰动集、终端集合与证明前提；并以另外两篇直接四旋翼外环 MPC 原文对照 PX4 迁移条件。无法获取时继续检索作者稿，不以摘要代替公式。
