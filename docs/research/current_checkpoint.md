# 研究短检查点（2026-10-02，Run 143）

主线为传统 SMF/输出反馈 Tube MPC，学习暂停。基于 Run142 tree `d0056a3`；远端
`main=1c49659`。Run140 合同固定15模态/17边、shared primitive、actual-input 时序及只按
可见`d=hat x-z`共享输入。

Run143 精读 Baras--Patel 1998 信息状态递归、Hempel等2011 OFCI fiber量词、Kjellqvist
2024有限逆像信息状态。joint information state已有一般理论；本轮只作合同语义纠正。

已精确证明：初始化后的14条miss边不能把mode14条件`q=eta_pz+h eta_vz`半宽从
`23312147/48000000`压到product门槛`57902137/162000000`。但success创新项在
`eta_v+`与`d_v+`中精确抵消；构造见证使`d_v+`超过product限幅，而
`e_v+=eta_v++d_v+=9237859/4500000<11/4`，同时`eta+`落入Run136 mode0 box。因此旧门槛
不是joint target必要条件，只对`E_eta x D`成立。证据等级为exact counterexample，不是
joint RCI证书。全仓201/201通过。

下一唯一问题：在竖直`(eta,e)`坐标定义最小mode-indexed convex joint candidate，对固定
`d=e-eta` fiber综合shared-input predecessor；先检验`14->0`及mode4/9分叉的一步非空性。
