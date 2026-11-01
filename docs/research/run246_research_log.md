## Run246完整checkout CI与main安全合并核验（2026-11-01）

研究PR #62 https://github.com/zhouxingxing1279/AcademicReaserch/pull/62 基于main `e4e832a3fbfb02281c1b179d8bb6e2338e57406e`；合并前compare ahead=7/behind=0，mergeable_state=clean，head=`b1d047f48d2c1783b06d86a3054e68a8476935f5`。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41330175901 **completed/success**；Python 3.13.17完整checkout Run224–246聚焦**200/200通过、无跳过**，真实配置、精确Fraction证书、归档JSON对比与artifact上传成功。PR非强制squash合并到main `83675ca663e7df210db7a51de4d873768f609715`，重新读取main SHA、PR merged状态及验证源码/JSON Blob核验落地。合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41330291108 **completed/success**，Python 3.13.16完整checkout再次**200/200通过、无跳过**（28.491s），证书对比与artifact上传成功。此补记仅更新文档，不修改算法、测试或数学证书；全仓库历史回归、递归可行、六状态安全与20ms最坏时延仍未认证。

---

# Run246 — Run245终点存在真实可达但不可恢复的状态：精确13拍可生存性反例（2026-11-01）

**远端main基准：** `e4e832a3fbfb02281c1b179d8bb6e2338e57406e`。读取Run245日志、检查点、真实配置、源码、归档证书、工作流及唯一论文阅读记录。Run245已经认证全初始盒在30拍内安全，但没有终端可生存性；本轮优先回答“30拍末端能否作为可重复安全备份的起点”，不并行设计多个未经证明的控制器。

## 1. 精确反例与量词

沿用Run245的冻结四状态显式Euler模型，`x=(p,v,phi,omega)`，`h=J=1/50`，`T=981/100N`，`|tau|<=2/25Nm`，`|r|<=3246383/1600000m/s²`，`|v|<=3m/s`。初始选取**配置初始盒真实角点**：

```text
(p0,v0,phi0,omega0)=(-1/50,-1/10,-1/200,-1/100)
r_k = -3246383/1600000 (所有k)
tau_0:11 = +2/25, tau_12:23 = -2/25, tau_24:29 = 0
```

这是一条合法的真实plant轨迹（不是独立区间外包伪造的角点）。通过精确角度/角速度递推与`sin`交错Taylor有理数外包，认证0–30拍全部硬约束；第30拍：

- `phi30=1097/5000=0.2194rad`、`omega30=-1/100=-0.01rad/s`，两者精确；
- `v30∈[-2.034914078,-2.034904500]m/s`，真实值在该区间；`p30≈-0.554486m`，可靠外包；
- `v30`上界使用每拍真实已知角度的`sin`**下界**得到，保守方向已核对。

从第30拍起，允许控制器选择**任意**满足`|tau_k|<=0.08Nm`的力矩，包括全状态反馈、知道未来的非因果策略（因此结论更强于SMF因果限制）；扰动只需保持一个合法序列`r=-R`。由于Euler的先更新角速度、下拍才影响角度的顺序，对所有`j=0,...,12`：

```text
phi_(30+j) >= phi30 + h*j*omega30 - h*(h/J)*U*j*(j-1)/2 = phi_min(j)
phi_(30+j) <= phi30 + h*j*omega30 + h*(h/J)*U*j*(j-1)/2
0 < phi_min(j) <= phi_(30+j) < 0.45
sin(phi_(30+j)) >= phi_min(j)-phi_min(j)^3/6
```

因此无论未来如何选力矩，利用有理数求和：

```text
v43 <= v30_upper - h*SUM_{j=0}^{12}[R+T*(phi_min(j)-phi_min(j)^3/6)]
    = -472862755273957527852863/156250000000000000000000
    ≈ -3.026321634 m/s < -3 m/s.
```

**严格越界裕度** `4112755273957527852863/156250000000000000000000≈0.026321634m/s`。第30拍状态的13拍安全必要速度下界是 `v30>=-2.008582866m/s`，而真实`v30<=-2.034904500`，严格不满足。

结论：**Run245的30拍可达终点集合包含至少一个不属于冻结模型鲁棒可生存核的真实状态**。该状态即使后续获取完整真值、使用任意可用力矩也无法在恒定合法负扰动下避免最迟第43拍的速度硬约束越界。因而Run245的有限安全管**不能直接作为可递归终端合同**。并不意味着所有30拍终点不可生存，也不意味着一般SMF＋Tube MPC不可能。

## 2. 文献阅读与证据级别

新增分节阅读 **Shahab Kaynama, Ian M. Mitchell, Meeko M. K. Oishi, Guy A. Dumont**, *Scalable Safety-Preserving Robust Control Synthesis for Continuous-Time Linear Systems*，2013 arXiv:1312.3399（2015 *IEEE Transactions on Automatic Control* 60(11):3065–3070，DOI https://doi.org/10.1109/TAC.2015.2411872）。实际阅读公开预印本§1、§2 Definition 1–2、§5.3、§6（12状态四旋翼例子），链接 https://arxiv.org/abs/1312.3399 。其discriminating kernel与鲁棒安全控制的定义提醒必须检查终端**可生存性**，而非只检查有限时域状态约束；该论文连续时间LTI、全状态反馈、椭球内近似，**没有**证明本项目离散非线性、有噪SMF和丢包自动机的终端合同。唯一论文日志新增1篇分节已读，历史91篇→92篇；Blanchini(1999)仅书目核验，不冒充已读。

## 3. 可复现工件、测试和局限

- `verification/check_four_state_terminal_nonviability.py`：复用Run245已验证配置/正弦有理数包络，单条真实角点的精确姿态与速度外包，所有未来力矩的角度极值及速度上界。
- `verification/test_four_state_terminal_nonviability.py`：10项回归，含Euler时序、0–30拍可达安全、全部未来角度区间、必要速度门槛、越界、数值sanity和证据范围。
- `results/four_state_terminal_nonviability_20261101/checks.json`：精确分数证书。
- `.github/workflows/run246-terminal-nonviability.yml`：Python 3.13完整checkout，Run224–246聚焦回归、真实配置、归档JSON对比和工件上传。

隔离Python标准库：`PYTHONPATH=/mnt/data python -m unittest -v test_four_state_terminal_nonviability_compact`，8通过、2项因隔离环境无仓库配置/归档跳过；`python -m py_compile`通过，`run246_compact.json`成功生成。仓库实际文件名移除`_compact`，完整checkout CI以PR运行结果为准，未执行全仓库历史回归。浮点全制动仿真只是sanity，不用于证明。**本轮没有构造后验反馈或MPC优化器。**

**Gate A仍blocked**：一般四状态SMF＋Tube MPC递归可行、六状态耦合安全、推力调度及20ms最坏时延均未认证。可行性：证明Run245原终端候选必须排除真实非可生存分支；创新性：该必要条件本身不是成熟硕士创新点；研究难度：必须在控制前驱中联合处理双向残差、执行器权限和因果观测。

## 4. 下一轮唯一优先任务

**在30拍终点之前建立双向扰动的可生存前驱筛选（viability guard），以真实5拍success/miss自动机和SMF后验为信息状态，寻找一个非空且不包含本轮反例的鲁棒安全后继集合。** 先用严格证书验证至少一个可执行的共享因果控制分支；若不可行，保留负面结果，不宣称递归闭合。
