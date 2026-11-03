# Run220 — 双共享扰动历史约束的有理数支持上界（2026-10-31）

**基准main：** `157b8375d2469048f8b6ecf91a661d8644018665`。**唯一瓶颈：** Run219一条共享扰动半空间将第193拍关键支持收紧0.01158303778，但有限五步速度安全行仍为负；需检验第二条独立历史约束是否提供额外收益。

## 本轮可验证算法增量

给定已核验的联合外包 P=(P_pv × P_phiomega) 与两条因果共享扰动必要半空间 c_i^T x≤b_i，对任意非负有理数乘子λ_i，有

h_{P∩H1∩H2}(q) ≤ h_P(q−λ1 c1−λ2 c2)+λ1 b1+λ2 b2.

证明：对每个满足半空间的x，q^Tx=(q−Σλ_i c_i)^Tx+Σλ_i c_i^Tx≤h_P(q−Σλ_i c_i)+Σλ_i b_i。此结论不要求浮点LP精确求解。新代码仅用SciPy HiGHS建议乘子，使用Fraction有理数化并**重新精确计算右端**；所以返回值是可靠支持上界，但不保证达到真实最优值。对于该上界产生的控制裕度，得到的是**下界**：若仍为负，不能判定实际联合约束的安全行必然阻塞；若为正，只排除这一行的阻塞，不等于全部Backup可行。

候选历史权重固定为7组三包组合（含Run219原组合），使用已执行推力、力矩和决策前位置包，均转化为两个必要半空间；对Run219第一条排除半空间与其余12个候选方向分别进行双乘子优化，记录最佳支持上界、乘子、第二约束编号、失败次数与真值包含。初始本地环境未能执行真实第193拍；随后通过GitHub Actions完整checkout执行，实测结果及证据限制见文末补充验证。

## 实测测试与边界

本地 Linux/Python 3环境，SciPy HiGHS + Fraction；命令：`cd /mnt/data/run220 && python -m unittest -v test_two_shared_rows`；4项聚焦测试通过，1项真实仓库集成因缺少完整checkout显式跳过；`python -m py_compile check_two_shared_rows.py test_two_shared_rows.py`通过。合成二维方盒q=(1,0)与两条约束x+y≤0、x−y≤0：单条最优支持仍为1，联合两条有理数乘子(1/2,1/2)给出精确上界0，证实实现可识别仅由联合约束产生的收益。另测非最优乘子499/1000、501/1000的精确上界1/500及负乘子拒绝。

**验证更新：** 本地容器github.com DNS解析失败；GitHub Actions已在完整checkout完成聚焦与第193拍集成测试（见文末）。仍未执行全仓库回归、20ms在线控制预算或闭环准入恢复验证。

## 文献与课题状态

Scott、Raimondo、Marseglia、Braatz (2016), *Constrained zonotopes*, Automatica 69:126–136, DOI https://doi.org/10.1016/j.automatica.2016.02.036：本轮核对公开摘要及既有集合运算笔记；不将双乘子证书归于该文定理。Köhler、Müller、Allgöwer (2021), *Robust output feedback MPC using online estimation bounds*, arXiv https://arxiv.org/abs/2105.03427：核对摘要中在线可靠估计界、homothetic tube与四旋翼示例；非全文重读。统一论文日志去重87篇不变。

**Gate A=blocked。** 双约束算法有明确可验证接口，但第193拍真实增益、完整SMF后验、终端受控不变集、递归可行性、稳定性和六状态四旋翼鲁棒安全证明均未完成。创新性取决于实际控制准入/实时预算收益；目前不足以支持创新性成立。

**下一轮唯一优先任务：** 在完整仓库中执行`RUN_TICK193_AUDIT=1 PYTHONPATH=verification python -m unittest -v verification.test_two_shared_rows`，读取真实双约束支持上界及耗时；若收益不足，停止无目标叠加条带，转向有终端安全保证的最小可行闭环基线。


## GitHub Actions完整checkout补充验证（2026-10-31 14:08 UTC）

已在GitHub Actions Ubuntu/Python 3.13.17、SciPy 1.17.0的**完整仓库checkout**执行真实第193拍：聚焦4项测试通过，opt-in实际历史集成1项通过；工作流run [41208687506](https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41208687506) 全部成功。执行`RUN_TICK193_AUDIT=1 PYTHONPATH=verification python -m unittest -v verification.test_two_shared_rows`；另直接调用`audit_tick193()`打印JSON。

**实测负面结果：** 以Run219第一条共享扰动半空间为基准，扫描另外6组三包权重的正反两个半空间（共12个候选第二行），SciPy无失败，但在最终Fraction重新核验后，**没有任何一组提供可认证的额外支持上界改善**：`extra_certified_gain_exact=0`；新支持上界与Run219一条半空间的精确支持相同。对应五拍速度安全裕度的**可认证下界**仍约`-0.02473733102`。这不证明所有两条约束组合无效，也不证明真实联合历史后验没有改善；只否定本轮固定候选集、乘子建议/有理数化算法在该方向的新增收益。负下界是**不确定**而非不可行证书。

完整重放+12个候选LP+精确核验的独立脚本wall time约`4.9238s`（GitHub hosted runner；**非纯在线支持求解耗时**），不能据此直接比较20ms周期。当前证据仍不足以主张恢复第193拍控制准入。下一轮不再盲目添加同类三包行，转向能明确提供递归可行性的最小终端安全基线或先分析全历史约束的紧性。
