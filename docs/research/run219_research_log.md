# Run219 — 共享扰动历史排除第193拍旧支持极大点（2026-10-31）

**基准 main：** `3467cced8d3ad2421d65d51c9d9435fabbbbd163`（Run218）。**唯一瓶颈：** Run218证明六条分别放松扰动的4D位置历史条带对关键支持方向增益严格为0，但没有检查不同测量包是否能由**同一段扰动序列**同时解释。

## 研究问题与严格证书

冻结四状态Euler模型 `x=(p,v,phi,omega)`，`h=J=1/50`，`v+=v+h(-T*phi+r)`，`|r_j|<=47/25+(243/16000)T_j`；历史施加力矩与推力已知，位置测量误差 `|e_a|<=1/50`。利用确定性的姿态反向递推，令

`d_a(x_k)=y_a-[p_k-(k-a)h*v_k-h²*sum_{j=a}^{k-1}(j-a+1)*T_j*phi_j(x_k)]`。

由于同一个 `r_j` 同时影响多个位置包，任意有理数权重 `lambda_a` 必须满足

`|sum_a lambda_a*d_a(x_k)| <= sigma_p*sum_a|lambda_a| + h²*sum_j rad(T_j)*|sum_{a<=j}lambda_a*(j-a+1)|`。

与对每条包分别放松扰动后相交不同，**先合并共享扰动系数再取绝对值**，保留了包间相关性。这是完整历史后验的可靠必要半空间，不是精确CZ后验，也不是新的文献定理。

选取实际因果位置包 `a=(135,165,180)` 和 `lambda=(1,-6,5)`，对Run218的关键支持方向 `q=(0,-1,2943/2000,2943/50000)` 的**全部两个乘积顶点极大点**得到相同的精确证书：

- 约束左端：`10787547317/8000000000`；
- 共享扰动与测量误差右端：`2140829889/1600000000`；
- **严格排除裕度：`5212367/500000000 = 0.010424734 > 0`**。

由于权重和为0，证书与极大面上位置 `p` 的变化无关；其他关键状态分量在该面固定，故**整个原支持极大面**均被排除，而非只排除一个任意角点。离线真值满足新半空间。另用第135拍姿态观测及已施加力矩反推，旧极大点的姿态观测残差 `4/625=0.0064`，超过 `1/200=0.005`，提供独立必要条件排除证据（此观测在第193拍决策前已经可用）。

## 控制相关支持改善与负面结果

对原11顶点 `(p,v)` 与6顶点 `(phi,omega)` 乘积外包加入上述**一条**有效共享扰动半空间，使用精确Fraction枚举原乘积顶点及边与半空间的交点，得到关键支持上界的严格改善：

`h_P(q)-h_{P∩H}(q) = 5212367/450000000 ≈ 0.01158303778`。

因此完整历史后验的关键支持至多为新外包支持；该方向至少可以收紧上述数值。**但一条半空间仍不足以解除原五拍速度下界阻塞：** 先前最佳控制裕度约 `-0.03632036880`，新外包对应的单行裕度仍约 `-0.02473733102 < 0`。这只是**当前外包的有限备份证书仍被阻塞**，不是完整历史可行域不可生存的证明；更不能声称递归可行。

## 实际代码、验证与证据边界

- 新增 `verification/check_shared_disturbance_support.py`：共享残差权重合并、因果历史反推、精确半空间、四维乘积边裁剪与第193拍完整仓库集成入口；`verification/test_shared_disturbance_support.py`：4项聚焦测试、1项需完整checkout的显式跳过测试。
- 在Python 3.13.5/Linux标准库Fraction环境执行 `cd /mnt/data/run219 && python -m unittest -v test_shared_disturbance_support`：**4通过、1跳过**；`python -m py_compile check_shared_disturbance_support.py test_shared_disturbance_support.py`：通过。
- 本地源码兼容独立镜像执行 `PYTHONPATH=/mnt/data/run219 python /mnt/data/run219/run_mirror_integration.py`：真实参数192拍确定性重放通过；复现Run214的速度下界、Run216的11/6顶点和Run218的两个旧极大点，核验精确共享扰动排除裕度、支持改善和真值包含。镜像并非完整GitHub checkout。
- 镜像192拍重放约3.02秒；单条共享半空间裁剪约12.38ms（一次测量，**不含**历史构造、MPC优化及其他约束），**未证实20ms完整在线控制预算**。容器无法解析github.com，完整仓库回归和GitHub CI未执行。结果归档 `results/shared_disturbance_support_20261031/checks.json`。
- 在完整仓库可运行 `RUN_TICK193_AUDIT=1 PYTHONPATH=verification python -m unittest -v verification.test_shared_disturbance_support`；**本轮未在完整checkout执行**。所有算术证书使用Fraction，近似值只用于展示。

## 文献与课题评估

本轮复核既有Scott、Raimondo、Marseglia、Braatz（2016），*Constrained zonotopes: A new tool for set-based estimation and fault detection*，*Automatica* 69:126–136，DOI https://doi.org/10.1016/j.automatica.2016.02.036，作者原稿 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。核对摘要、CZ集合运算及状态估计问题定位；本轮**不是全文重读**，也不将本轮共享扰动权重证书归为论文原有定理。统一论文日志维持87篇去重。

**可行性：** 可以用小规模精确线性证书排除虚假支持极大面；**创新性：** 线性组合、支持函数、CZ本身不是原创，后续须证明控制准入或复杂度的实质收益；**难度：** 保留多包共享扰动的在线规模控制、完整Tube MPC及终端安全集仍高。**Gate A=blocked**：无终端受控不变集、递归可行性、稳定性及六状态四旋翼安全证明。

**下一轮唯一优先任务：** 在相同第193拍历史上，选择并联合验证少量**独立的共享扰动组合约束**，检验能否继续缩小剩余约 `0.02473733` 的五拍速度阻塞，并记录总在线计算预算；若不能，保留负面结果并转向可计算的终端安全基线。
