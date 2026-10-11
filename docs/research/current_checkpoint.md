# 研究短检查点（2026-10-11，Run160）

主线：传统 SMF/鲁棒输出反馈 MPC；学习暂停。远端 `main=1c49659`、Run159=`9d3e928`。

Run160 重读 Yang--Ozay 2021 dropout-string safety、Rungger--Tabuada 2017 RCI近似与 Goulart--Kerrigan 2007 robust output feedback；Rutledge--Yong--Ozay 2020仅核查摘要/引言。把Run159“更早介入”问题放宽为从`J14` mode0起每拍任意causal full-state bounded control。镜像初态/扰动轨迹及`|u_t^+-u_t^-|<=2U`给出`k` miss后位置半直径下界 `H_k^0-k(k-1)h²U/2`。第12 miss下界`398207933/400000000≈0.995520`，第13 miss首次为`934206607/900000000=1+34206607/900000000`，故当前fixed global residual、`J14` seed与correction盒下，任何因果策略都无法安全完成15-tick return。证据是完整路径必要反证，不是一般output-feedback/RCI/递归可行性结论。

下一唯一问题：推导`k=14`安全所需的seed收缩、residual降低与correction authority精确trade-off，并核查哪项可由可靠在线集合信息在同扰动保证下实现。
