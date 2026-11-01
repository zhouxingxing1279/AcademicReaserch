# Run234 — 首个四状态非线性鲁棒受控不变集合的精确有理数证书（2026-10-31）

**基准远端 main：** `107d08ac91e71948d65f535b19c9fe06caf3cb5b`（Run233）。**本轮唯一瓶颈：** Run224–233只有有限步安全与全状态LQR数值轨迹，尚无非空四状态终端RCI。改用固定推力下的无限zonotope与可计算尾项，直接验证非空集合的无限时域后继闭合，不将有限轨迹误作证明。

## 1. 冻结模型与新增反馈

采用仓库 `configs/planar_baseline.json` 的定义离散Euler横向四状态，`x=(p,v,phi,omega)`：

```text
p+     = p + h*v
v+     = v + h*(-T*sin(phi)+r)
phi+   = phi + h*omega
omega+ = omega + h*tau/J
h=1/50 s, J=1/50 kg m^2
|r| <= 47/25 + (243/16000)*T
|p|<=5, |v|<=3, |phi|<=9/20, |omega|<=2
T in [4.905,14.715] N, |tau|<=2/25 Nm
```

**本轮新反馈**固定 `T=981/100=9.81 N`，`tau=-Kx`，`K=(-123/1000,-247/500,2341/1000,933/1000)`。它不同于Run233的饱和LQR数值种子；该增益仅为寻得可认证裕度的理性数候选，不声称最优。由 `h/J=1` 得闭环线性化矩阵：

```text
A = [[1, 1/50,        0,      0],
     [0,    1, -981/5000,    0],
     [0,    0,        1,   1/50],
     [123/1000,247/500,-2341/1000,67/1000]]
B = [0,1/50,0,0]^T
```

原始非线性闭环可**精确重写**为 `x+=A*x+B*d`，其中 `d=r+T*(phi-sin(phi))`。在物理姿态约束 `|phi|<=9/20` 内，利用全实数成立的Taylor余项不等式 `|phi-sin(phi)|<=|phi|^3/6`，有 `|d|<=D`，`D=R(9.81)+9.81*(9/20)^3/6=1742383/800000=2.17797875 m/s²`。这一外包覆盖每一拍、每一个允许残差，**不假定随机扰动或小角度等式**。

## 2. 非空RCI集合及有限精确证明

定义无限Minkowski和（无限zonotope）

`S = ⊕_{j=0}^∞ A^j B[-D,D]`。

使用Python标准库 `fractions.Fraction` 精确计算 `A^j B`（`0<=j<800`）、`A^800`及相关支撑函数。验证：

- `rho=||A^800||_infinity <=0.044224501<1`，故A为Schur，级数收敛，S非空、紧致、中心对称、包含原点；
- 令 `s_i=sum_{j=0}^{799}|(A^j B)_i|`，`q=sum_{j=0}^{799}||A^j B||_infinity`。对每个坐标，严格尾项 `sum_{j=800}^∞ |(A^j B)_i| <= ||row_i(A^800)||_1*q/(1-rho)`；
- 力矩的尾项同理用 `||K*A^800||_1*q/(1-rho)` 上界。所有不等式在内部均以**精确有理数**判断，JSON中的十进制数字仅为**向上取整**的展示上界。

最终严格得到 `|x_i|` 上界（单位依次m、m/s、rad、rad/s）：

| 项目 | 向上取整的可靠上界 | 硬约束 |
|---|---:|---:|
| `|p|` | 4.406855 | 5 |
| `|v|` | 2.538442 | 3 |
| `|phi|` | 0.361233 | 0.45 |
| `|omega|` | 0.742976 | 2 |
| `|tau|=|Kx|` | 0.064424 Nm | 0.08 Nm |

于是 `S subset int(X)` 且 `|Kx|<tau_max` 对所有 `x in S` 成立，力矩**不饱和**。对任意 `x in S` 与任意当拍允许的 `r`，上述非线性余项满足 `d in [-D,D]`，故 `A*S+B*d subset S`。由数学归纳，固定推力+全状态反馈使真实非线性冻结四状态系统对所有允许逐拍扰动**无限时域鲁棒受控不变**。这是明确非空的RCI存在性证书，不是有限样本结论。

**严格适用范围：** 固定T=9.81 N、完整真实四状态可观测、冻结Euler横向动力学与给定残差界。S为隐式无限zonotope，尚未给出MPC可直接施加的有限维成员资格约束；没有间歇位置量测SMF共享控制、Tube MPC递归可行性、六状态耦合、点稳定性或20ms在线耗时保证。不能用这一证明替代这些缺口。Gate A整体仍blocked，但**四状态全状态固定推力终端RCI存在性子问题已从unknown变为proved under frozen contract**。

## 3. 论文与方法出处

定向核对Raković、Kerrigan、Kouramas、Mayne（2005），*Invariant approximations of the minimal robust positively invariant set*，`IEEE Transactions on Automatic Control` 50(3):406–410，DOI https://doi.org/10.1109/TAC.2005.843854 。本轮核对DBLP书目与公开摘要，并复核仓库既有阅读记录；**不是新增全文阅读**，不重复增加91篇去重已读计数。其mRPI与有限和加尾项是相关理论背景；本轮非线性嵌入、具体K和800步精确尾项证书均为本项目独立计算，**不将论文线性定理直接称作本非线性结论**。参照Mayne等（2006），*Robust output feedback model predictive control of constrained linear systems*，DOI https://doi.org/10.1016/j.automatica.2006.03.005（此前Run221已分节阅读），强调输出反馈需另证估计误差和控制管束。

## 4. 实现、测试与复现

新增 `verification/check_four_state_rpi_zonotope.py`（全Fraction、无外部依赖）、`verification/test_four_state_rpi_zonotope.py`（8项测试）、`results/four_state_rpi_20261031/checks.json` 与 `.github/workflows/run234-exact-rpi.yml`。测试指令：

```bash
PYTHONPATH=verification python -m unittest -v verification.test_four_state_rpi_zonotope
python -m py_compile verification/check_four_state_rpi_zonotope.py verification/test_four_state_rpi_zonotope.py
python verification/check_four_state_rpi_zonotope.py --root . --output /tmp/run234_certificate.json
```

隔离本地Python环境执行8项：**7通过，1因无完整仓库配置而跳过**；原先`test_rounding_is_outward`预期分数未约分导致一次失败，已修正并重新运行通过，负面过程保留。实际完整checkout的配置、历史Run224–234聚焦回归与JSON归档一致性由PR CI验证；在CI成功之前不声称其已通过。未执行全仓库历史回归。

## 5. 硕士课题收敛与下一轮唯一任务

可行性由“无四状态终端正证”提升为“固定推力、全状态反馈的非空RCI已严格证明”；创新性：该mRPI构造本身是经典技术，尚不构成独立创新，真正研究问题仍在SMF条件化误差集合与共享控制的输出反馈闭合；难度仍高，但终端存在性障碍显著缩小。

**下一轮唯一优先任务：** 将隐式S转成可计算成员资格/支撑约束的有限外近似终端表示，严格验证其鲁棒后继闭合，并明确间歇位置量测下`SMF后验集合 subset terminal`时可使用的同一因果控制律；若有限表示外近似不保持不变，保留失败证据而不偷换为证明。
