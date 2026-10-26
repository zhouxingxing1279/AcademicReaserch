# 研究短检查点（2026-10-26，Run184）

主线：传统SMF/鲁棒输出反馈MPC；学习暂停。远端`main=1c49659`；Run183远端`893046dc`。

Run184构造box `Y/G/Lambda`与6参数`Z/H/Omega`，并按“source共享control→传播→edge测量”纠正Houska原式时序。15-mode/17-edge LP含498变量、2772约束。纯axis-aligned位置测量不能收缩velocity radius；在最短`0->1->2->3->4->0`环上，21行非负Farkas乘子将全部变量精确消去，得到`0<=-572143/800000`。证据等级：`exact_axis_aligned_box_information_ensemble_infeasibility_certificate`。只否定该box/meta-template，不否定相关多面体/CZ，也未证明MPC递归可行。

下一唯一问题：在相同15-mode、固定`W/V`、硬约束和extreme-control权限下，加入最小一对position--velocity耦合法向；先检查是否打破速度半径Farkas环，再求图不变LP的exact primal/dual证书。
