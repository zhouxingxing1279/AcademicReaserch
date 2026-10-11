# 研究短检查点（2026-10-12，Run165）

主线：传统SMF/鲁棒输出反馈MPC；学习暂停。远端`main=1c49659`、Run164=`dbd3a07`（tree=`ded2c20`）。

Run165全文重读Yang--Ozay缺测安全串，复核Hempel输出fiber与Houska多面体控制。Run164虽证明最坏fiber半宽仅`≈0.2175`，但绝对中心仍失败：可达极端观测`d_p=24272147/48000000`的整个fiber在`e_p+14he_v`方向已偏到正侧。允许乐观全状态因果反馈，14次miss的正端residual与最大负输入因`g_r=hU`精确相消；最终位置仍至少为`3889781459/3600000000=1+0.08049485`。故当前J14/global residual/correction box/15-tick合同被同观测fiber精确否定；不是一般RCI、其他合同或六自由度不可能性。

下一唯一问题：定量推导消除该中心反例所需的极端可见偏差、future residual与物理correction authority三因素最小合同修约，并只保留有可靠物理/估计来源的候选。
