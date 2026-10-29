# 研究短检查点（2026-10-29，Run197）

唯一主线仍为间歇测量与推力调度不确定性下的鲁棒输出反馈Tube MPC；只推进Gate A。起点远端Run196=`d98ddcd`，`main=1c49659`。

冻结合同不变：当前推力可见、未来推力可在全区间任意跳变。Pólik--Terlaky 的S-lemma给出本轮关键收口：归一化`|s|<=1`上二次`f=a s^2+b s+c>=0`，精确等价于存在`lambda>=0`使`Q=[[c-lambda,b/2],[b/2,a+lambda]]>=0`（`DERIVED`）。纯有理checker通过`1-s^2`与`1+s`边界证书，并拒绝Run196残差`(s^2-1)/8`。固定cone的38 facets×160 vertices需6080条该LMI；affine configuration/state/torque条件仍可精确查端点。共同后继core可靠但保守；未求解SDP，19-pair可行性、六状态安全和递归可行性仍`OPEN`，Gate A blocked。

下一唯一问题：在可复现SDP环境求解固定cone affine-offset候选，并逐条用全区间精确二次检查器独立复核。
