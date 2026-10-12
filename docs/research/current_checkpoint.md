# 研究短检查点（2026-10-12，Run170）

主线：传统SMF/鲁棒输出反馈MPC；学习暂停。远端`main=1c49659`、Run168=`9862e36`（tree=`f7b15d49`）。

Run170审计纠正Run169：J14端点只在独立逐边`rho_x,rho_z`的线性残差外包内一致；checker没有从初始集出发的非线性plant轨迹、控制/测量/风历史重放。故有理数超限仍精确否定当前抽象外包达到`D*`，但不能推出真实benchmark局部气动路线不可能。Rego等非线性CZ factorable外包是下一直接基线；Robbins等2026仅核查摘要，首次性未知。

下一唯一问题：写出单步`(state,wind,aerodynamic factors,residual)`共享primitive的factorable CZ合同，以包含证明和可行性查询判断Run169极端组合是否仍被联合物理外包容许。
