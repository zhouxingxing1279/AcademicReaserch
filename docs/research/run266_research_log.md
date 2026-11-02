# Run266 — 倾角与角速度条件化的三拍必要速度守卫（2026-11-02）

## 1. 基准与唯一瓶颈

基准远端main SHA 52b55cb067fab97e4476b437da50d8b45c7c9340；读取 CURRENT_CHECKPOINT、Run260/262/265日志及源码、真实 configs/planar_baseline.json、唯一论文阅读总账及模型选型证据。Run265仅给 phi=omega=0 切片的三拍绝对速度必要条件。本轮唯一问题：非零倾角/角速是否改变这一必要守卫？本轮构造了覆盖全部合法姿态/角速初始值的必要条件与非零倾角真实反例，但没有构造第60拍全部真实后验或终端信息RCI。

## 2. 数学证明与精确证书

仅针对冻结四状态“定义的离散Euler真值”，不是六状态整机：
p+=h*v; v+=h*(-T*sin(phi)+r); phi+=h*omega; omega+=h*tau/J。
h=J=1/50，T=981/100 N固定，|tau|<=U=2/25 Nm，|r|<=R=3246383/1600000 m/s²，|v|<=V=3 m/s，|phi|<=9/20，|omega|<=2。

Euler时序：phi1=phi0+h*omega0；phi2=phi0+2h*omega0+(h²/J)*tau0，后续tau1/tau2不能影响第三次速度更新。令a0=phi0、a1=phi0+h*omega0、a2=phi0+2h*omega0、delta=h²U/J=1/625。全部合法初始角/角速满足 |a2|+delta<1，sin在该区间单调递增。选择合法扰动r0=r1=r2=+R，对任意合法因果力矩：
v3 >= v0+3hR-hT[sin(a0)+sin(a1)+sin(a2+delta)]。
选择r0=r1=r2=-R，同理：
v3 <= v0-3hR-hT[sin(a0)+sin(a1)+sin(a2-delta)]。

所以任何三拍鲁棒可生存真实状态必须满足：
-V+3hR+hT[sin(a0)+sin(a1)+sin(a2-delta)] <= v0
<= V-3hR+hT[sin(a0)+sin(a1)+sin(a2+delta)]。

此为必要而非充分条件。验证脚本使用七次Maclaurin p7=x-x³/6+x⁵/120-x⁷/5040 与严格余项 |sin(x)-p7|<=|x|⁹/9!，用Fraction下界放宽必要下限、上界放宽必要上限，避免浮点误差错误剔除可行状态。

零姿态：v0必要带约[-2.878574557366,2.878574557366]m/s，较Run265 Lipschitz上界2.8785745575稍紧。phi0=-0.1rad、omega0=0时，v0必要上界约2.819811065108m/s，下界约-2.937334913041m/s。

**非零倾角真实反例**：x0=(p,v,phi,omega)=(0,2.85,-0.1,0)，r0=r1=r2=+R。对任意合法tau0:2，精确有理Taylor界给出 v1<=2.910167104<3、v2<=2.970334208<3，但v3>=3.03018893489>3；p3<=0.174610027<5、|phi1:3|<=0.1048<0.45、|omega1:3|<=0.24<2。因此第三拍**真实速度必然越界**，不是区间外包假阳性。该状态不在Run265的零姿态切片，说明必要筛选须保留速度与姿态关联。

量词：若某真实初始状态违反上述必要带，则对所有合法因果力矩策略存在合法三拍扰动导致速度越界。没有证明该见证属于Run260第60拍实际非空后验；也没有证明所有后验不可行、反馈终端RCI不存在或无限时域安全不可能。

## 3. 真实论文分节重读（唯一总账既有条目，去重数不增加）

Vu Tuan Hieu Le, Cristina Stoica, Didier Dumur, Teodoro Alamo, Eduardo F. Camacho (2011), *Robust Tube-Based Constrained Predictive Control via Zonotopic Set-Membership Estimation*, IEEE CDC-ECC 2011, pp.4580–4585, DOI https://doi.org/10.1109/CDC.2011.6161131 ，作者上传公开正文 https://www.researchgate.net/publication/254054580_Robust_Tube-Based_Constrained_Predictive_Control_via_Zonotopic_Set-Membership_Estimation 。2026-11-02实际核验pp.4580–4585：§III式(1)、§IV Algorithm 1/2、Property 4与式(2)–(22)、§V式(23)–(32)、Assumptions 1–3、§VI Table I；未逐页比对IEEE终版。

模型为离散LTI x+=Ax+Bu+Fw, y=cᵀx+σv，标量每拍量测、有界过程扰动与噪声、可控可观。方法以zonotope预测/每拍条带交集外包做状态SMF、离线LMI求收缩增益、在线名义Tube MPC及估计中心反馈；§V的硬约束和稳定性依赖初始误差管包含、收紧状态/输入约束、名义正不变终端集合和终端Lyapunov条件，不是无条件证明。§VI是2状态1输入数值例（N=13），不是四旋翼、没有失测自动机、真实力矩时滞或20ms最坏耗时。Table I给50个采样时刻累计计算时间0.0312s（不含LMI）与0.7488s（含LMI），不能解释成四旋翼单步实时性。

可复用Property 4的zonotope与条带外包、双层误差 S^e⊕S^co、X⊖S及U⊖KS^co收紧、Assumptions 1–3终端合同；不能直接移植其每拍测量/线性/无物理时滞假设。本论文已经有zonotope SMF+Tube MPC，因此组合本身不是创新。

## 4. 实际工件、测试与局限

新增 verification/check_run266_tilt_aware_velocity_guard.py、verification/test_run266_tilt_aware_velocity_guard.py、results/run266_tilt_aware_velocity_guard_20261102/checks.json、.github/workflows/run266-tilt-aware-velocity-guard.yml。隔离Linux Python 3.13.5标准库执行：
- PYTHONPATH=verification python -m unittest discover -s verification -p 'test_run266*.py' -v → 12/12通过；
- python -m py_compile verification/*.py → 通过；
- python verification/check_run266_tilt_aware_velocity_guard.py --output results/run266_tilt_aware_velocity_guard_20261102/checks.json → 生成确定性有理JSON。

本地容器DNS不能解析github.com，因此没有本地完整仓库回归；PR CI将核验真实配置、Run26x聚焦回归和归档JSON逐字比较，实际结果须独立读取。负面结果保留：新非零倾角状态在第三拍违约，说明零倾角守卫不足以筛选所有真实状态。

**Gate A=blocked**。没有新增MPC求解器、SMF/CZ递推、闭环控制、15拍终端回返、无限递归可行、鲁棒稳定、六状态安全或20ms WCET。条件性六状态平面物理首选与四状态数学基线暂不变。

## 5. 下一轮唯一优先任务

从Run260第60拍**全部非空有噪success/miss后验**建立带绝对v/phi/omega关联的可靠信息状态外包；先使用本轮必要守卫筛选，再尝试15拍共享因果终端回返。必要筛选绝不能冒充充分安全证书。
