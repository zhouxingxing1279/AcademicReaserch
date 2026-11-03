# 模型选型与文献研究导航

当前问题：以 12 状态六自由度刚体模型作为仿真物理对象，成熟飞控负责姿态/角速度/分配/电机；比较位置、速度、加速度三种外环 MPC 高层接口。六状态三维平移模型只是待验证的外环预测候选，不是物理 plant。研究间歇/异步位置测量下的 SMF/CZ 与 Tube MPC 接口。

## 核心文件
- [模型证据矩阵](MODEL_SELECTION_EVIDENCE.md)：先读顶部当前决策摘要；下方旧矩阵和逐轮研究日志均已明确标为历史证据，不再提供当前优先级。
- [PX4 外环接口证据](PX4_INTERFACE_EVIDENCE.md)：整合 #188/#186/#190，明确 NaN mask、NED、三类 setpoint 与闭环辨识合同。
- [外环 MPC 与 SMF/CZ 文献证据](OUTER_LOOP_MPC_LITERATURE.md)：整合 #184/#162/#170，区分 12 状态物理 plant、外环预测状态与优化器输入权限。
- [唯一论文总账](../../literature/PAPER_READING_LOG.md)：按 DOI/题名去重的唯一登记处。
- [当前模型合同](../MODEL_CONTRACT.md)：被控对象、候选输入、测量和扰动合同。
- [当前检查点](../CURRENT_CHECKPOINT.md)：下一唯一研究问题。

## 近期关键审计
- [执行器预测与接口边界审计](background_run_20261103_actuator_prediction_interface_audit.md)
- [Hu 10-state 论文复核](background_run_20261103_hu_primary_followup.md)
- [Hu / Mo Chen 模型交叉核验](background_run_20261103_mo_chen_tac_model_crosscheck.md)
- [SMF/Zonotope 四旋翼文献审计](background_run_20261103_1510_smf_zonotope_quadrotor_audit.md)
- [Patel 混合 ZSMKF-MPC 审计](background_run_20261103_1747_patel_ch7_hybrid_zsmkf_mpc_audit.md)

证据规则：直接四旋翼外环 MPC 优先；全状态/电机级论文只作对照；区分自定义内环与现成飞控；SMF 后验、未来 Tube 和物理扰动集合分别定义；文献、仿真、实飞和形式化证明分开陈述。
