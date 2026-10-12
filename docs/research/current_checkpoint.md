# 研究短检查点（2026-10-12，Run175）

主线：传统SMF/鲁棒输出反馈MPC；学习暂停。远端`main=1c49659`、Run174=`ec21e9a`。

Run175纠正Run174量词：五步最大推力轨迹仍精确证明“测量本身不重置物理速度”，但推力是控制器选择，不是对手扰动，故不能据此否定存在因果策略实现受控回返。检查器现明确`measurement_only_reset_implication_rejected=true`、`controlled_return_to_initial_box_impossible=false`、`control_exists_quantifier_not_tested=true`。周期tube综合必须采用`exists policy, forall disturbances/dropout paths`。

下一唯一问题：冻结基于可见posterior/模式的因果推力策略类，构造5步return predecessor，并对每个观测fiber用同一策略覆盖全部风、噪声和success/miss后继。
