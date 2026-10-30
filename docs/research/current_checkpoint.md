# 研究短检查点（2026-10-30，Run204）

唯一总方向：四旋翼/无人机 MPC＋SMF 闭环与可完成硕士课题。Run200标量SMF–MPC闭环；Run201四状态缺测信息下界；Run202四状态条件化CZ/返包速度界；Run203三拍硬约束准入与永久零力矩72 tick违约；**Run204证明15-mode五边合法成功环上，任何固定原点对称直积盒形式的模式相关物理状态终端族都不可能对所有边一步鲁棒受控不变**。理由：每边位置积分器强制 P_next≥P_i+h V_i，环求和强制全部V_i=0，而合法非零残差立即产生 v_next>0。精确有理证据为 EXACT_RATIONAL_CLASS_SPECIFIC_NO_GO；不排除平移/相关/条件化信息集合或一般RCI。

Run204还实现四状态区间SMF+非零饱和反馈的150 tick闭环数值探针：3个合法推力/残差场景×零力矩、SMF中点反馈、真值全状态反馈共9条轨迹，浮点容差下SMF覆盖1350/1350；非零SMF反馈在高推力正残差tick114违反角速度约束、切换推力正残差tick125违反姿态角约束。它不是MPC，亦无鲁棒安全/递归可行性保证。17/17新增测试在本地关键配置镜像通过，未运行完整仓库回归/CI。

工件：verification/check_mode_indexed_box_terminal_obstruction.py、verification/test_mode_indexed_box_terminal_obstruction.py、verification/check_four_state_feedback_smf_probe.py、verification/test_four_state_feedback_smf_probe.py、results/mode_indexed_box_terminal_obstruction_20261030/checks.json、results/four_state_feedback_smf_probe_20261030/summary.json、docs/research/run204_research_log.md；docs/literature/PAPER_READING_LOG.md复核Athanasopoulos、Lorenzetti与Pavone、Ping等已有论文，84篇总数不变。

**Gate A仍blocked。下一唯一任务：** 构建观测条件化的移动中心/相关SMF信息状态下可实施的有限时域backup或安全过滤器，统一合法测量边和未来任意推力，并对完整四状态闭环进行保守安全准入与失败见证。
