# Run235 — 四状态有限生成元鲁棒终端集合与严格闭合证书（2026-11-01）

**远端基准 main：** db23aaa410a67fc929100146e12a51d8b3ebf820。**唯一瓶颈：** Run234证明非空的无限zonotope RCI尚无有限维成员资格表示。本轮不改变冻结模型、不宣称输出反馈闭合，而是构造一个**有限生成元、严格鲁棒正不变**的外包集合。

## 1. 冻结模型与信息权限

沿用Run234和configs/planar_baseline.json：横向四状态 x=(p,v,phi,omega)，Euler步长h=0.02s，固定推力T=9.81N，完整真实状态反馈 tau=-Kx，K=(-0.123,-0.494,2.341,0.933)，允许逐拍独立且控制后选择的 |r|<=1.88+(243/16000)T。闭环严格写为 x+=Ax+Bd，B=(0,0.02,0,0)^T，d=r+T(phi-sin(phi))。只要 |phi|<=0.45rad，利用全实数Taylor余项可取 |d|<=D=1742383/800000 m/s²。原非线性系统被这一线性加性扰动系统外包，**没有**把sin(phi)=phi当作恒等式。

## 2. 有限RCI构造及证明

令 U=B[-D,D]，n=800，P_n=⊕_{j=0}^{n-1}A^j U。用精确有理数计算

- rho=||A^n||_infty<0.044224501<1；
- eps=D||A^n B||_infty<0.0002561563；
- W=eps[-1,1]^4，Q=(1-rho)^(-1)⊕_{j=0}^{n-1}A^j W；
- **F=P_n⊕Q**，是包含原点的紧致、非空、有限4000生成元zonotope（800个P生成元、4×800个Q生成元）。

关键精确包含：A^n U⊆W、A^n W⊆rho W。因为 W 是对称凸盒，

A Q⊕W ⊆ (1-rho)^(-1)[⊕_{j=1}^{n-1}A^jW ⊕ rho W ⊕ (1-rho)W] = Q。

同时 A P_n⊕U=P_n⊕A^nU⊆P_n⊕W，所以 **A F⊕U⊆F**。这是真正的一步无限时域后继闭合，不是只认证n拍安全。且 F 的所有状态满足姿态界，非线性余项嵌入对F每个状态有效，故原冻结非线性四状态系统在固定推力、全状态反馈下亦严格RCI。

使用生成元支撑函数的**精确有理数**求和并向上取整，得到以下安全上界：

| 量 | Run235上界 | 硬约束 |
|---|---:|---:|
| |p| | 4.36189355m | 5m |
| |v| | 2.55727183m/s | 3m/s |
| |phi| | 0.37147212rad | 0.45rad |
| |omega| | 0.77413543rad/s | 2rad/s |
| |tau| | 0.06690522Nm | 0.08Nm |

因此全体F上的力矩不饱和，闭环反馈可实现。有限集合成员资格可写成4×4000生成元矩阵G的线性可行性问题：存在 xi∈[-1,1]^4000使 x=Gxi。代码提供精确Fraction生成元迭代器，并逐项复核5个支撑值；**尚未运行在线LP或测20ms延迟**。有限外包F不等于Run234的最小无限和S；证明保证S⊆F及F自身不变，不能把F误称为最小RCI。

## 3. 文献证据级别

复核Raković、Kerrigan、Kouramas、Mayne（2005），*Invariant approximations of the minimal robust positively invariant set*，IEEE TAC 50(3):406–410，DOI https://doi.org/10.1109/TAC.2005.843854 的书目、公开摘要及仓库历史阅读记录；**本轮未取得全文，不宣称逐条核对原论文定理，也不新增已读计数**。有限和、稳定线性系统的RPI外逼近属于经典思想；上述带盒尾项的具体闭合推导由本项目逐项给出，不能据此宣称原创集合理论。

## 4. 可复现工件与测试

- 源码：verification/check_four_state_finite_rpi.py
- 测试：verification/test_four_state_finite_rpi.py（9项）
- 归档：results/four_state_finite_rpi_20261101/checks.json
- CI：.github/workflows/run235-finite-rpi.yml（Run224–235聚焦回归）

复现指令：

    PYTHONPATH=verification python -m unittest -v verification.test_four_state_finite_rpi
    python -m py_compile verification/check_four_state_finite_rpi.py verification/test_four_state_finite_rpi.py
    python verification/check_four_state_finite_rpi.py --root . --output /tmp/run235_certificate.json

本地Python 3.13环境先在无checkout镜像执行9项，8通过1项真实配置检查跳过；后将GitHub公开配置中的相关字段建立**等价最小配置镜像**，执行9/9通过、JSON与归档逐字一致，耗时约25秒（包含生成元枚举）。首次测试命令因执行目录未设置为仓库根目录发生ModuleNotFoundError，已修正并重测，保留此失败记录。真实完整checkout的回归必须由GitHub Actions再次验证，不能用最小镜像代替。n=400构造因硬约束无法认证，已作为负面回归保留。无全仓库历史回归或最坏在线耗时认证。

## 5. 硕士课题判断与唯一后续任务

**Gate A仍blocked。** 四状态固定推力全状态RCI由Run234的隐式存在性推进到有限生成元可计算表示；理论可行性提高，创新性仍低（经典mRPI外逼近），工程难度在4000生成元LP、间歇位置量测下的隐藏状态纤维、共享因果控制与MPC终端移位。该有限F不能直接作为部分观测SMF后验集合的安全终端：tau=-Kx读取真实隐藏状态，当前观测并不允许此操作；“后验集合包含于F”也不能让控制器使用不同的tau(x)。

**下一轮唯一优先任务：** 对当前冻结四状态F和Run221的间歇量测模式，构造**共享观测控制**的必要/充分接口：从同一SMF后验纤维中两个不同隐藏状态计算所需力矩差，先严格判断是否存在单一合法控制可保持后继包含F；若不成立，给出反例并转向估计误差联合RPI或更保守的可实现输出反馈终端，不直接宣称MPC递归可行。
