# 研究短检查点（2026-10-11，Run161）

主线：传统SMF/鲁棒输出反馈MPC；学习暂停。远端`main=1c49659`、Run160=`c11faa0`（tree=`04163b0b`）。

Run161精读Lu--Cannon--Koksal-Rivet 2021的fixed-complexity set update、tube与递归可行性；重读Köhler 2021、Dey--Bhasin online-bound compatibility；Robbins 2026仍仅有正式摘要。对Run160的`k=14`必要下界分离seed方向半直径`alpha`、future residual`beta`与correction authority`gamma`，得到`alpha*(3889781459/3600000000)+(beta-gamma)*(52065013/400000000)<=1`。当前`g_r=hU`使baseline residual与最乐观输入削减相消。单因素至少需seed半直径缩小7.4498%，或residual缩小61.8418%，或authority增加61.8418%。非中心后验的`alpha`必须由正反两个support计算；只有该realized state width可由当前SMF直接改变。状态估计不能缩小未来扰动，也不能增加物理权限。证据为必要权衡，非充分可行性/RCI结论。

下一唯一问题：定义seed双侧support/方向半直径gate与短-dropout fallback，并证明两支均保持旧计划移位可行。
