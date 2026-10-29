# 研究短检查点（2026-10-29，Run199）

唯一主线仍为间歇测量与推力调度不确定性下的鲁棒输出反馈Tube MPC；当前只推进Gate A。接续远端Run198=`42be3a2`、tree=`4baee10`（纠正Run198旧检查点在同步后仍写`399e00a`的问题），`main=1c49659`。Run199本地内容提交=`8d87a1c`，远端等树提交=`68c2004`，tree=`1badee5`。

冻结合同不变：四状态横向—姿态降阶基准，当前推力可见、未来推力可全区间任意跳变；19-pair fixed-normal configuration采用仿射offset/vertex torque和共同后继core。锁定`clarabel==0.11.1`求解6514变量、39870行、225744非零元、6080个SOC的充分模型；默认与关闭equilibration均返回`PrimalInfeasible`。主39870维浮点对偶ray独立复核：`b^Tz=-0.9999999666`、`||A^Tz||inf=3.69e-9`、最差dual-cone margin=`0.0758`；另一scaling亦通过`1e-7`审计。证据仅为`NUMERIC_CHECK`：不能推出精确不可行、一般PD-RCI不可行、物理权限不足、六状态安全失败或递归不可行。Gate A仍blocked。

下一唯一问题：将高余量浮点ray稀疏化/有理化，并用精确有理或区间算术认证`A^Tz=0`、`z in K*`、`b^Tz<0`；此前不更换configuration family。
