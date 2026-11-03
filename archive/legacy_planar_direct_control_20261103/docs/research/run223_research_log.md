# Run223 — 四状态终端集合的双侧倾角必要条件（2026-10-31）

**基准 main：** f72155bf15c782ca32d51d0cd873524060d1372e。**唯一瓶颈：** Run222证明小角度姿态终端管无法支撑四状态鲁棒不变性；本轮先筛除其他过窄倾角终端候选，不宣称构造出可生存核。

## 冻结模型与精确证明

沿用 configs/planar_baseline.json、Run208/210横向残差合同和Run222模型：h=1/50，T∈[981/200,2943/200]，|vx|≤3，|phi|≤9/20，|omega|≤2；vx^+=vx+h[-T sin(phi)+r_x]，允许每拍独立选择 |r_x|≤47/25+(243/16000)T。

对0≤r≤9/20，交错Taylor展开给出 sin(r)≤s5(r)=r-r³/6+r⁵/120。由于sin在[-0.45,0.45]上单调，若一个候选终端集合C的所有状态满足phi≤r，对手可逐拍选择r_x=+R(T)，则无论因果控制器选择何种合法推力/力矩：

vx^+-vx ≥ h·min_{T∈[Tmin,Tmax]} [47/25+(243/16000-s5(r))T] = h·δ(r)。

若δ(r)>0，任意从vx≥-3出发的策略在 n=floor(6/(hδ))+1 拍内严格违反vx≤3，或此前已经离开C。因此非空鲁棒受控不变C不可能完全位于phi≤r。对称地，以r_x=-R(T)可证明C不可能完全位于phi≥-r。**这是针对任意形状C、任意因果控制策略的必要条件，不是某种特定盒模板失败。**

r=717/5000=0.1434时，严格有理数δ=14439858027668066783/25000000000000000000000>0，故任何非空RCI集合必须同时满足 sup_C(phi)>0.1434 和 inf_C(phi)<-0.1434。r=7/50=0.14时，δ=125267818583/2500000000000>0，最多5988拍越过速度上界。r=0.1434的保守越界上限为519396拍。对于r=3/20=0.15，此漂移下界为负，**不能据此断言可行或不可行**。

此外若一条轨迹确实要从phi≥0.1434转到phi≤-0.1434，由phi^+=phi+h omega及|omega|≤2，至少需要ceil(2·0.1434/(0.02·2))=8拍。这只是运动学下界，不是控制器必须在8拍内切换或能够实现切换的证据。

**重要限制：** 证明依赖Run208/210允许逐拍独立极端残差的冻结不确定性合同，不证明真实气动可长期实现该残差。两侧姿态投影是必要非充分条件；未证明四状态可生存核非空、MPC递归可行、稳定或六状态安全。

## 文献核对与阅读状态

- Kolmanovsky, I.; Gilbert, E. G. (1998), Theory and computation of disturbance invariant sets for discrete-time linear systems, Mathematical Problems in Engineering 4(4):317–367, DOI https://doi.org/10.1155/S1024123X98000866 。本轮核对出版商公开摘要和书目信息（**非正文精读**）：研究有界扰动离散LTI系统最大不变集、Pontryagin差和计算算法。本文是线性框架，不自动证明本仓库非线性推力调度模型的终端核存在。
- Blanchini, F. (1999), Set invariance in control, Automatica 35(11):1747–1767, DOI https://doi.org/10.1016/S0005-1098(99)00113-2 。本轮复核DBLP书目；**未读正文**，不新增已读数。作为后续不变核理论候选。

双侧漂移证明为本仓库针对冻结模型自行推导，不归于上述论文。唯一论文阅读日志维持87篇历史去重记录。

## 复现、测试和证据等级

本地Python 3标准库Fraction执行：5项聚焦测试中4通过、1项完整仓库配置检查因缺checkout跳过；源码py_compile通过；生成结果与结果文件一致。命令：

PYTHONPATH=verification python -m unittest -v verification.test_two_sided_terminal_necessity

python -m py_compile verification/check_two_sided_terminal_necessity.py verification/test_two_sided_terminal_necessity.py

python verification/check_two_sided_terminal_necessity.py --root . --output /tmp/run223_checks.json

diff -u results/two_sided_terminal_20261031/checks.json /tmp/run223_checks.json

完整checkout的配置与结果逐字比对由新增GitHub Actions工作流负责；在工作流成功前不宣称CI通过。有限数值sin sanity test不替代Taylor余项数学论证。

## 课题收敛与唯一下一轮任务

**Gate A=blocked。** 可行性：证明所有终端候选必须允许双侧较大倾角，但尚无充分RCI证书；创新性：这属于设计前必要条件审计，不是新SMF/MPC方法；难度：需要结合姿态加速度、位置约束和全扰动的因果量词。**下一轮唯一任务：** 以允许|phi|>0.1434的四状态候选集合为起点，计算至少一轮具有正确控制—扰动量词的鲁棒前驱并给出非空内核的可核验见证或进一步严格阻塞，不再无目标调整估计条带。
