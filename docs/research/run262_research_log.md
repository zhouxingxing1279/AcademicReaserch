# Run262 — 悬停点三拍力矩权限时滞与终端速度带必要宽度（2026-11-02）

## 1. 远端基准、唯一瓶颈、证据级别

读取远端 main `e9d53d4941f6e07c69c6aa4eb32ba8e96b3b215c`，`docs/research/CURRENT_CHECKPOINT.md`、Run259–261日志、`configs/planar_baseline.json`、Run259/260验证源码、统一论文总账及近期分支。Run260仅认证固定历史第45–60拍共享零力矩有限安全；Run261构造真实轨迹否定其无限重复。下一步的终端信息状态必须承认**真实控制权限和动力学响应延迟**，不能只收缩估计集合。此次不冒充构造第60拍全部测量纤维或信息RCI；只给出一个严格必要的终端集合几何筛选。

## 2. 冻结模型与全反馈也不能规避的三拍必要条件

沿用Run261四状态**定义的离散Euler真值**，不是六状态平面模型：
`x=(p,v,phi,omega)`，`p+=h v`，`v+=h(-T sin(phi)+r)`，`phi+=h omega`，`omega+=h tau/J`；
`h=J=1/50`，**固定** `T=981/100`，`|tau|<=U=2/25`，`|r|<=R=3246383/1600000`。冻结硬约束`|p|<=5,|v|<=3,|phi|<=9/20,|omega|<=2`。注意此模型**没有**可调T权限；六状态配置有T权限但不能借此将四状态结果扩张为六状态证明。

从真值原点`x0=(0,0,0,0)`，选择允许的恒定三拍`r0=r1=r2=+R`。无论任何可测量历史、任何因果甚至预知未来的合法力矩`tau0,tau1,tau2`，显式Euler顺序给出
`phi1=0`，`phi2=(h^2/J)tau0`，`v1=hR`，`v2=2hR`，
`v3=3hR-hT sin((h^2/J)tau0)`。
利用`sin(theta)<=|theta|`和`|tau0|<=U`，严格推出
`v3 >= 3hR - hT(h^2/J)U = 48570177/400000000 = 0.1214254425 m/s`。
对`r=-R`对称推出`v3 <= -0.1214254425`，故从原点出发的三拍鲁棒可达速度投影跨越至少`0.242850885m/s`；**这是必要下界，不是后验精确宽度**。在这些真实轨迹上`p3=3h^2R=9739149/4000000000<5`，且三拍姿态和角速度上界严格小于硬约束，因此不是因其他约束提前无效的扰动见证。

**严格但有限的推论：** 任何包含真值原点、并将其所有成员限制在`|v|<=0.12m/s`的鲁棒控制不变状态集合，不可能对上述四状态模型成立；即使每拍获得完整无噪真值也不行。这是针对**人为候选窄终端速度带**的必要排除，**不否定**仓库实际`|v|<=3m/s`的安全集合可生存，不否定更宽终端集合、反馈终端信息RCI、或Run260有限桥。也没有证明当前第60拍后验必然包含原点，不能把本必要条件直接判作第60拍RCI失败。

对设计的含义：扭矩在当前步改变`omega1`、下一步改变`phi2`、到第三次速度更新才改变`v3`；因此不能用零延迟的“虚拟横向加速度”控制权限构造物理`tau`终端集合。下一轮应把此三拍响应纳入第60拍真实后验的安全前驱。

## 3. 新论文核验及与本研究的关系

**Sabin Diaconescu, Florin Stoican, Bogdan D. Ciubotaru, Sorin Olaru**, *Elastic Tube Model Predictive Control With Scaled Zonotopic Sets*, *IEEE Control Systems Letters* 8 (2024), 1343–1348, DOI https://doi.org/10.1109/LCSYS.2024.3408047 。2026-11-02实际阅读作者开放版正文§II–V，重点式(8)–(15)、Lemma 2、Propositions 2–4、§V-A/B；可解析开放正文 https://www.researchgate.net/publication/381050260_Elastic_Tube_Model_Predictive_Control_With_Scaled_Zonotopic_Sets 。已核对IEEE期刊书目；不是逐式核对IEEE终版PDF。

实际对象是**已知A,B的LTI全状态Tube MPC** `x+=Ax+Bu+w`，控制`u=ubar+K(x-xbar)`，有界加性扰动W与状态/输入硬约束X/U；生成元可独立缩放的zonotope构造弹性管束，Proposition 3给出线性充分包含条件，Proposition 4提供LP的RPI构造。§V-A为2状态双积分器、单输入、N=12；§V-B为2ℓ状态弹簧阻尼质量链、两个端部力输入、N=25，使用MATLAB/YALMIP/MOSEK/CORA/MPT3。**没有四旋翼、SMF/CZ状态后验、传感器量测模型、丢包或实飞**；报告计算扩展性不能转写为本仓库20ms WCET。论文已有弹性zonotope Tube MPC技术，本课题创新不能只是“使用zonotope管束”。可借鉴其包含条件，但需新增有噪间歇位置的观测纤维、因果控制、物理`tau`权限与终端闭合。

## 4. 验证工件、执行、局限

新增 `verification/check_run262_actuation_delay.py`、`verification/test_run262_actuation_delay.py`、`results/run262_actuation_delay_20261102/checks.json` 与 `.github/workflows/run262-actuation-delay.yml`。独立Linux Python标准库执行：
`cd /mnt/data && python -m unittest -v test_run262_actuation_delay` → **8/8通过**；`python -m py_compile check_run262_actuation_delay.py test_run262_actuation_delay.py` →通过；`python check_run262_actuation_delay.py --output run262_checks.json` →成功，分数证书确定。独立环境未包含完整仓库，因此`--root`配置交叉核验、Run260/261聚焦回归、远端PR/main CI均须在完整checkout独立确认；workflow显式运行这些检查并逐字比较证书。没有MPC求解器、闭环仿真、SMF/CZ递推或安全终端集合实现。

可行性：本轮仅排除不合理窄终端模板，不能证明终端可行；创新性：时滞必要界是模型审计而非足够论文贡献；难度：物理控制权限与观测纤维联合前驱仍高。**Gate A=blocked**。

## 5. 下一轮唯一优先任务

以Run260第60拍SMM/MMS全部**非空有噪success观测纤维**为信息状态，建立至少一次15拍可移位、允许根据实际观测反馈的**共享因果安全前驱**；首先把三拍`tau→v`时滞写入前驱的状态传播，不得将第60拍单个零读数外包或三拍必要条件冒充所有后验的终端证明。
