# Run220 — 双共享扰动历史约束的有理数支持上界（2026-10-31）

**基准main：** `157b8375d2469048f8b6ecf91a661d8644018665`。**唯一瓶颈：** Run219一条共享扰动半空间将第193拍关键支持收紧0.01158303778，但有限五步速度安全行仍为负；需检验第二条独立历史约束是否提供额外收益。

## 本轮可验证算法增量

给定已核验的联合外包 P=(P_pv × P_phiomega) 与两条因果共享扰动必要半空间 c_i^T x≤b_i，对任意非负有理数乘子λ_i，有

h_{P∩H1∩H2}(q) ≤ h_P(q−λ1 c1−λ2 c2)+λ1 b1+λ2 b2.

证明：对每个满足半空间的x，q^Tx=(q−Σλ_i c_i)^Tx+Σλ_i c_i^Tx≤h_P(q−Σλ_i c_i)+Σλ_i b_i。此结论不要求浮点LP精确求解。新代码仅用SciPy HiGHS建议乘子，使用Fraction有理数化并**重新精确计算右端**；所以返回值是可靠支持上界，但不保证达到真实最优值。对于该上界产生的控制裕度，得到的是**下界**：若仍为负，不能判定实际联合约束的安全行必然阻塞；若为正，只排除这一行的阻塞，不等于全部Backup可行。

候选历史权重固定为7组三包组合（含Run219原组合），使用已执行推力、力矩和决策前位置包，均转化为两个必要半空间；对Run219第一条排除半空间与其余12个候选方向分别进行双乘子优化，记录最佳支持上界、乘子、第二约束编号、失败次数与真值包含。**本轮未在真实第193拍完整checkout执行**，因此实际额外收益未知，绝不把合成测试写成真实控制恢复。

## 实测测试与边界

本地 Linux/Python 3环境，SciPy HiGHS + Fraction；命令：`cd /mnt/data/run220 && python -m unittest -v test_two_shared_rows`；4项聚焦测试通过，1项真实仓库集成因缺少完整checkout显式跳过；`python -m py_compile check_two_shared_rows.py test_two_shared_rows.py`通过。合成二维方盒q=(1,0)与两条约束x+y≤0、x−y≤0：单条最优支持仍为1，联合两条有理数乘子(1/2,1/2)给出精确上界0，证实实现可识别仅由联合约束产生的收益。另测非最优乘子499/1000、501/1000的精确上界1/500及负乘子拒绝。

**未完成：** 容器github.com DNS解析失败，未获得完整checkout；没有真实tick193联合支持数值、总20ms计算耗时、完整回归、CI或闭环准入恢复证据。只有已验证的通用算法和合成单测，不能据此宣称Run219负裕度已消除。

## 文献与课题状态

Scott、Raimondo、Marseglia、Braatz (2016), *Constrained zonotopes*, Automatica 69:126–136, DOI https://doi.org/10.1016/j.automatica.2016.02.036：本轮核对公开摘要及既有集合运算笔记；不将双乘子证书归于该文定理。Köhler、Müller、Allgöwer (2021), *Robust output feedback MPC using online estimation bounds*, arXiv https://arxiv.org/abs/2105.03427：核对摘要中在线可靠估计界、homothetic tube与四旋翼示例；非全文重读。统一论文日志去重87篇不变。

**Gate A=blocked。** 双约束算法有明确可验证接口，但第193拍真实增益、完整SMF后验、终端受控不变集、递归可行性、稳定性和六状态四旋翼鲁棒安全证明均未完成。创新性取决于实际控制准入/实时预算收益；目前不足以支持创新性成立。

**下一轮唯一优先任务：** 在完整仓库中执行`RUN_TICK193_AUDIT=1 PYTHONPATH=verification python -m unittest -v verification.test_two_shared_rows`，读取真实双约束支持上界及耗时；若收益不足，停止无目标叠加条带，转向有终端安全保证的最小可行闭环基线。
