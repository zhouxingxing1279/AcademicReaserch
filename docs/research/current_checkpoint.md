# 研究短检查点（2026-10-27，Run186）

主线：传统SMF/鲁棒输出反馈MPC；学习暂停。远端`main=1c49659`；Run185远端`302600a5`。

Run186恢复`+/-p,+/-v,+/-(p-(1/10)v)`，精确构造6个vertex maps与24行configuration cone。位置strip交集的紧支持为`h_p=min(a,r_q+kappa*r_v)`、`h_v=min(r_v,(a+r_q)/kappa)`、`h_q=min(r_q,a+kappa*r_v)`。可靠见证`(r_p,r_v,r_q)=(1,11/4,1)`、`a=1/50`中，raw success offsets离开所选configuration；canonical `h_q=59/200`，严格收缩`141/200`并落在cone边界。因此active velocity facets能消除Run185的局部unchanged-q前提。证据等级：`exact_six_facet_measurement_support_map`；不是graph/meta ensemble、控制或递归可行性证明。Badalamenti等2025已覆盖一般facet refinement，手工加法向不构成创新。

下一唯一问题：把canonical support分支提升为覆盖连续measurement centers的六facet`Z/H/Omega`，在control-before-packet时序下构造15-mode/17-edge LP并输出exact primal或Farkas证书；若有限extreme meta-polytopes不能覆盖min/disjunction，则停止该模板。
