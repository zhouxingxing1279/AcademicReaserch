# 当前研究检查点 — Run234（2026-10-31）

**基准main：** `107d08ac91e71948d65f535b19c9fe06caf3cb5b`。本轮建立首个**非空、严格无限时域四状态RCI存在性证书**，仅针对固定推力9.81 N、冻结Euler横向模型、完整全状态反馈 `tau=-Kx`，`K=(-.123,-.494,2.341,.933)`，对所有逐拍独立有界横向残差成立。并非Run233的饱和LQR策略。

**证书：** `S=⊕_{j>=0} A_cl^j B[-D,D]`，`D=1742383/800000`；精确Fraction计算800步支撑与几何尾项，`||A_cl^800||∞<0.044224501`；可靠状态幅值上界(4.406855m,2.538442m/s,0.361233rad,0.742976rad/s)，力矩幅值<0.064424 Nm，均严格低于硬约束。用 `|phi-sin(phi)|<=|phi|^3/6` 证明真实非线性闭环每拍被线性扰动集合包含，故S严格不变。详见 [Run234研究日志](run234_research_log.md)及 `verification/check_four_state_rpi_zonotope.py`。

**证据级别：** 数学证明（固定模型和全状态反馈）；不是SMF后验共享控制、MPC递归可行、六状态安全或渐近点稳定性证明。S为隐式无限zonotope，尚无可在线使用的有限终端成员资格约束。**Gate A仍blocked，但四状态固定推力全状态终端RCI存在性子问题已证明可行。**

**本地测试：** Python标准库Fraction，8项中7通过1项因隔离镜像缺真实配置跳过；已修正一次测试预期分数约分问题并重测。完整checkout GitHub Actions须实际成功后才能归档，未执行全仓库历史回归或20ms在线时限认证。

**文献：** 复核Raković等(2005)，DOI https://doi.org/10.1109/TAC.2005.843854 既有mRPI记录；非新增全文阅读，唯一日志去重仍91篇。

**下一轮唯一优先任务：** 将隐式S转成可验证鲁棒后继闭合的有限终端集合表示，进一步研究间歇位置量测SMF后验集合上的同一因果控制律。

---

## 历史Run233检查点（保留）
# 当前研究检查点 — Run233（2026-10-31）


**Run233验证补记（2026-11-01 UTC）：** PR #35 https://github.com/zhouxingxing1279/AcademicReaserch/pull/35 已安全Squash合并，代码main SHA 52d4d02cce7d9f60fb11a25880cec714c12992f4；PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41268160006 与合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41268193922 均success。完整checkout Python 3.13.17，Run224–233聚焦测试69/69通过、无跳过；真实配置、编译、JSON归档核对及工件上传成功。已重新读取远端main及源码、测试Blob确认落地。**未执行全仓库历史回归，数值反馈种子仍非RCI/SMF+MPC安全证明。**


**基准main：** 8cee19a9a937f7037cf4ba1b28f2ede8ed82b98b。主方向：无人机MPC+SMF鲁棒输出反馈闭环；子课题允许证据驱动收敛。

**本轮实测增量：** 新增冻结四状态Euler的全状态饱和LQR反馈数值种子（固定T=9.81N，tau=clip(-Kx,±0.08)）。原点7种确定性/固定种子残差序列各1000拍未观察到违约；128组小初始扰动的1000拍随机残差实验0/128违约；相同持续正向极端残差下无反馈基线第74拍越界。**全部是有限轨迹数值证据，不是非空RCI、输出反馈MPC或安全证明。** 详见 [Run233研究日志](run233_research_log.md)。

**文献：** 新增Decardi-Nelson & Liu (2020) arXiv:2009.13581分节原文阅读§2.1、§3.1–3.4；统一论文日志去重90→91篇，未核实期刊DOI。

**测试：** 本地Python 3.13.5共8项测试7通过1项缺完整checkout跳过，源码编译及JSON输出成功；GitHub Actions完整仓库结果待实际运行后补记。尚未执行全仓库历史回归或20ms最坏耗时认证。

**Gate A=blocked：** 四状态非空终端RCI、SMF输出反馈Tube MPC递归可行性、稳定性和六状态安全均未证明。下一轮唯一优先任务：从数值反馈轨迹提取相关四维小单元，以严格区间外包认证闭合终端策略图，不能将数值无违约误作鲁棒安全。

