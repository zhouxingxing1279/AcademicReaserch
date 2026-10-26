# 研究短检查点（2026-10-27，Run187）

主线：传统SMF/鲁棒输出反馈MPC；学习暂停。远端`main=1c49659`；Run186远端`2047ee6`。

Run187纠正“连续measurement centers需枚举/min分支可能阻断固定预算”的前提。对Run186 configuration内`P(y)`，精确有`max p=y_0,min p=-y_3`；存在同一观测中心使位置误差不超过`a`当且仅当`(y_0+y_3)/2<=a`。故Houska sensor ensemble首行可取`Z_1=(e_0+e_3)/2`，一次覆盖全部中心。平移边界见证在`a=1/50`给出唯一中心`1/3`。证据等级：`exact_six_facet_sensor_ensemble_measurement_row`；未选择剩余`Z_2/H/Omega`，不是图不变、控制或递归可行性证明。

下一唯一问题：比较direct facet-offset bounds与center/radius/support bounds两种`Z_2`，构造有限固定configuration的exact `H/Omega`与extreme-set预算；在此闭合前不进入15-mode LP。
