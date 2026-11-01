# Run241 — 有噪位置观测驱动的共享非零力矩恢复脉冲（2026-11-01）

**基准远端main：** `a61ed856bffe12058d4e8fc5cf9e15b7290c512b`。**本轮唯一瓶颈：** Run240的全部观测SMF速度包络尚未进入可执行控制。先在Run236两点初始隐藏速度纤维上构造一个对所有合法成功观测、扰动和噪声因果可执行的**非零**恢复控制，检验其是否严格改善有限时域最坏状态外包。不要将其称为一般SMF-MPC或终端RCI。

## 1. 具体策略、模型和全量词

冻结四状态Euler `(p,v,phi,omega)`、`h=1/50 s`、`J=1/50`、`T=981/100 N`，`r_k∈[-R,R]`且`R=3246383/1600000 m/s²`。初始两点 `(0,±hD,0,0)`，`D=1742383/800000`。首先共同施加`tau=0`达`n∈{5,10,15}`拍，收到任意合法成功位置观测`y=p_n+eta`、`|eta|≤1/50 m`。之后仅凭**当前可见的y**承诺15拍控制：

`tau_(n+j)=(2/3)y s_j` Nm，`s=[1,1,1,-1,-1,-1,-1,-1,-1,1,1,1,0,0,0]`，推力仍固定9.81N。控制不读取隐藏真实速度、扰动或未来观测。角状态系数由精确Euler递推得`phi_(n+j)=c_j y`、`omega_(n+j)=d_j y`，在第12个脉冲后精确返回`phi=omega=0`。整个15拍内所有输入满足`|tau|<0.08Nm`。

设Run240的初始到第n拍的关联生成元为`(p_i,v_i)`，`Y=sum_i |p_i|+1/50`，`alpha=hT sum_{j<15} c_j=0.141264`，`beta=h²T sum_{j<15}(14-j)c_j=0.0211896`。由`|sin(z)-z|≤|z|³/6`，得到全量词终端绝对速度/位置可靠外包：

`V_pulse≤sum_i |v_i-alpha*p_i|+alpha/50+15hR+E_v`；

`P_pulse≤sum_i |(1-beta)*p_i+15h*v_i|+beta/50+h²R*15*14/2+E_p`，

其中`E_v=hT*Y³*sum|c_j|³/6`，`E_p=h²T*Y³*sum(14-j)|c_j|³/6`。`p_i,v_i`来自同一个初始符号和扰动变量，不能分别取独立位置/速度盒。基线`tau=0`的终端最坏绝对支持在这个中心对称两点纤维上**精确**为`sum|v_i|+15hR`及`sum|p_i+15h v_i|+h²R*15*14/2`。所有分数用Python标准库`Fraction`精确运算，Taylor余项以可靠上界加入。

| 成功观测间隔 | 零力矩末端位置精确最坏值(m) | 本策略位置可靠上界(m) | 零力矩末端速度精确最坏值(m/s) | 本策略速度可靠上界(m/s) |
|---|---:|---:|---:|---:|
| 5拍 | 0.171627023 | 0.171786541 | 0.855155325 | 0.856218780 |
| 10拍 | 0.265258513 | 0.264723830 | 1.058054263 | 1.054489710 |
| 15拍 | 0.379179896 | 0.377521117 | 1.260953200 | 1.249894669 |

**严格正向结果：** 10、15拍两种成功观测模式下，针对全部连续合法观测和全部允许扰动/噪声，脉冲终端可靠上界**严格低于**零力矩基线的精确最坏绝对值；15拍位置至少改善0.0016587797m、速度至少改善0.0110585315m/s。全部5/10/15模式的脉冲过程每个中间时刻都由严格分数外包证明满足`|p|<5, |v|<3, |phi|<0.45, |omega|<2, |tau|≤0.08`。

**保留负面结果：** 5拍时本策略的**证书上界**比零力矩精确基线更差（位置约+0.00015952m、速度约+0.00106346m/s）；不能据此断言实际最坏性能必然恶化。观测噪声足以抵消此小反馈的可靠收益。策略在15拍末仅重置角状态，**位置速度不返回原信息状态**；故无递归闭合证明，也未接入一般SMF后验集合、MPC优化器、六状态耦合或20ms最坏时延。

## 2. 文献复核（已读去重91篇不变）

- **Liren Yang; Necmiye Ozay (2021)**，*Safety Control Synthesis for Systems with Missing Measurements*，*IFAC-PapersOnLine* 54(5):97–102，DOI https://doi.org/10.1016/j.ifacol.2021.08.481，作者PDF https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。本轮核对原文摘要及已有Run240的§3–4阅读记录。研究问题：有丢包自动机的安全综合；方法：字符串自动机与因果输入承诺。局限：成功包假设无噪完整状态，不可直接替代本项目有噪位置SMF；本轮只实现一次成功包后的预承诺输入，尚无product safety game的闭环闭合。待查：对每个后续成功/缺包模式，能否共同维持终端信息状态？
- **Joseph K. Scott; Davide M. Raimondo; Giuseppe R. Marseglia; Richard D. Braatz (2016)**，*Constrained zonotopes: A new tool for set-based estimation and fault detection*，*Automatica* 69:126–136，DOI https://doi.org/10.1016/j.automatica.2016.02.036，作者PDF https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf 。本轮复核摘要及既有Run239对集合交与映射的分节笔记。关键假设：线性集合估计和已知有界误差；可复用技术：关联生成元及测量条带交；局限：原文不提供本项目非线性脉冲的递归MPC保证。**未重读两篇全文，不新增已读计数。**

## 3. 工件、验证与课题评估

- 源码：`verification/check_four_state_observation_pulse.py`；11项测试：`verification/test_four_state_observation_pulse.py`；归档：`results/four_state_observation_pulse_20261101/checks.json`；工作流：`.github/workflows/run241-observation-pulse.yml`。
- 本地隔离Python标准库：`PYTHONPATH=verification python -m unittest -v verification.test_four_state_observation_pulse`，11项中**10通过、1项因隔离目录缺真实配置跳过**；`python -m py_compile verification/check_four_state_observation_pulse.py verification/test_four_state_observation_pulse.py`通过；生成JSON通过。独立浮点Euler极端轨迹测试仅是索引/实现sanity check，不用于数学证明。完整checkout配置、历史聚焦回归和归档一致性由GitHub Actions实际结果确认，不预先声称成功。
- **证据级别：** 精确有理数模型包含+严格Taylor外包（有限时域），并非严格最优控制；比较使用零力矩基线的精确最坏支持与脉冲的可靠上界。**可行性：** 共享非零控制与可证明微小收益存在；**创新性：** 有噪观测线性脉冲及Taylor外包属基础技术，尚不足独立成题；**难度：** 一般CZ后验与多模式递归可行性仍高。Gate A继续blocked。
- **下一轮唯一优先任务：** 将本轮一次性脉冲策略嵌入重复5/10/15成功/缺包信息状态转移，验证可否构造非空、含位置速度相关性的**递归闭合**信息状态终端域；如失败保存明确的反例或外包障碍。
