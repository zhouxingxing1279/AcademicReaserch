# 研究短检查点（2026-10-02，Run 142）

主线为传统 SMF/输出反馈 Tube MPC，学习暂停。基于 Run141 tree `cf2234c`；远端 `main=1c49659`。Run140 合同固定15模态/17边、shared primitive与只观察`(d,mode,z,bar u)`的因果输入。

Run142 精读 Hempel 2011 OFCI验证/输入计算、Rungger--Tabuada 2017 predecessor/RCI近似及Houska等2024多面体综述；迭代、投影和非轴对齐参数化均非创新。

已精确否定候选类`S_j=E_eta^j x D_j`：mode14强制success下隐藏`q=eta_pz+h eta_vz`与测量噪声造成`d_vz+`半宽`72816441/32000000`，严格超过任意满足真值源域的mode0 `D_0`最大半宽`61142137/36000000`，超量`166210873/288000000`。推力只能平移区间；沿必经miss路径，满足初始化的非空product-fiber RCI不存在。该结论不否定joint `(eta,d)` information set。全仓197/197通过。

下一唯一问题：构造竖直四维joint information set，判断mode14条件纤维能否把`q` support压到`57902137/162000000`以下；随后才做shared-input predecessor。
