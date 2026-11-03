# Run245 — 保留非零倾角的共享因果控制：30拍严格有限安全证书（2026-11-01）

**远端main基准：** `a4ae3a7f6bf8587d0f328160a44cda3be6b8b0eb`。已读取Run243/244日志、检查点、配置、验证器与历史文献索引。本轮瓶颈：Run244排除每15拍强制姿态复位脉冲的持续扰动权限；检查保留非零倾角是否至少能在实际初始不确定性及全部合法丢包路径上实现可验证的横向抵抗权限。

## 1. 模型、控制与精确证据

固定推力 `T=981/100 N`，冻结四状态显式Euler `x=(p,v,phi,omega)`：
`p+=h*v; v+=h*(-T*sin(phi)+r); phi+=h*omega; omega+=h/J*tau`，`h=J=1/50`，每拍独立 `r∈[-3246383/1600000,+3246383/1600000] m/s²`。初始盒严格采用真实配置水平/姿态四维投影：`|p0|<=0.02m, |v0|<=0.1m/s, |phi0|<=0.005rad, |omega0|<=0.01rad/s`。此模型不包含竖直耦合。

控制是**全部后验fiber共享、无未来包预知的开环可执行见证**：前12拍 `tau=+0.08 Nm`，后12拍 `tau=-0.08 Nm`，后6拍 `tau=0`。控制器可见信息仅为时钟与自身历史，不读取隐藏状态，也不根据未来success/miss选择输入。12+12拍后名义姿态为 `phi=0.2304rad,omega=0`，但实际初始角误差未被虚构为零；严格角度区间为 `phi24∈[0.2206,0.2402]`、`omega24∈[-0.01,0.01]`。

对 `|phi|<=0.45` 使用单调性及交错Taylor有理数包络：
`x-x³/6 <= sin(x) <= x-x³/6+x⁵/120`（`x>=0`，负值用奇对称），每拍对 `p,v,phi,omega` 作向外包含传播。**全部0至30拍**状态/输入硬约束严格成立；全时域可靠绝对上界：

| 状态 | 可靠上界 | 配置硬约束 |
|---|---:|---:|
| `|p|` | 0.577744215 m | 5 m |
| `|v|` | 2.126530612 m/s | 3 m/s |
| `|phi|` | 0.2414 rad | 0.45 rad |
| `|omega|` | 0.97 rad/s | 2 rad/s |
| `|tau|` | 0.08 Nm | 0.08 Nm |

第24至30拍，任一初始角度/角速度实现均满足 `T*sin(phi)-R > 0.106057198 m/s²`（精确有理数下界），所以**即使持续正向极端扰动`r=+R`，横向加速度也为负**。这是Run244脉冲复位策略缺乏的持续非零倾角权限，证明为条件化的有限时域事实，不是对任意切换残差的无限安全性。

**必须保留的负面结果：** 与30拍零力矩外包相比，新策略正速度上界下降至少0.764009721m/s，但在合法`r=-R`下最坏绝对速度外包反而从1.363892472增至2.126530612m/s。因此不能把对`+R`的抵抗能力误称为双向鲁棒性能提升；更不能在此固定倾角上永久保持。初始`omega`不确定导致零力矩保持阶段仍有角度漂移。

## 2. 量测自动机与SMF接口

真实传感器每5拍一次位置包机会，至多连续两次缺包，30拍共有6次机会；枚举全部**44条**合法有限success/miss字串（不是只看all-success）。上述共享力矩序列对所有字串完全相同，因此逐条安全性由**同一**扰动/初始盒全时域外包蕴含，而非44条采样轨迹的统计结论。

实现有界区间SMF：预测 `X^-_{k+1}⊇f(X_k,u_k,W)`；每拍角度/角速度噪声条带交；位置包成功则交 `p∈[y-0.02,y+0.02]`，缺包不交。对任何真实且满足传感器噪声合同的轨迹，交集保持真值包含（归纳）；**不**宣称任意不相容观测后验非空，也**不**宣称已实现Run240关联CZ的高精度后验或基于后验的MPC优化。单条`SMMSSS`数值SMF重放仅为sanity，不作为严格证明。

## 3. 文献核验（既有已读去重91篇，不新增全文已读）

- **Liren Yang; Necmiye Ozay (2021)**，*Safety Control Synthesis for Systems with Missing Measurements*，*IFAC-PapersOnLine* 54(5):97–102，DOI https://doi.org/10.1016/j.ifacol.2021.08.481 ，作者PDF https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。本轮实际阅读§3 Assumption 1、§4.1–4.2 string automaton与因果开放环承诺、§4.4 Proposition 4–5。论文对缺测语言用product安全游戏综合，成功包为无噪全状态；本轮只借鉴因果量词，不套用其完整状态结论。待查：将有噪位置后验嵌入product前驱，并实现全部success/miss后继的统一可行控制。
- **Johannes Köhler; Matthias A. Müller; Frank Allgöwer (2021)**，*Robust output feedback model predictive control using online estimation bounds*，arXiv:2105.03427，https://arxiv.org/abs/2105.03427 ，作者PDF https://www.ist.uni-stuttgart.de/dokumente/public/Output.pdf 。本轮核对引言、§II-A Assumption 1及§III/IV接口摘要：在线当前/未来估计误差及估计器偏差界用于homothetic Tube MPC递归可行。此处只有有限时域安全外包和保守SMF更新，不能宣称满足论文的终端/递归条件。待查：如何由角度不确定的共同输入构造可重复估计-控制管束。

## 4. 验证、工件与证据等级

源码：`verification/check_four_state_tilt_authority.py`；12项测试：`verification/test_four_state_tilt_authority.py`；精确归档：`results/four_state_tilt_authority_20261101/checks.json`；工作流：`.github/workflows/run245-tilt-authority.yml`。

隔离环境Python标准库执行：
`PYTHONPATH=verification python -m unittest -v verification.test_four_state_tilt_authority`，**11通过、1项因无完整仓库配置跳过**；`python verification/check_four_state_tilt_authority.py --output ...`成功。完整checkout须由GitHub Actions执行配置一致性、Run224–245聚焦回归、归档证书对照；尚未完成全仓库历史回归、20ms最坏时延测试。

**证据等级：** 严格数学外包证明（冻结模型、给定初始盒、30拍、所有有界残差与合法包字串）；单条SMF数值重放（非证明）。**Gate A仍blocked**：无后验驱动的反馈优化、信息状态RCI、递归可行、六状态安全、任意推力调度、20ms时限。可行性：有限控制权限正向见证；创新性：基础bang-bang和区间SMF并非新方法；研究难度：双向扰动下的姿态—速度反馈和信息状态终端闭合仍高。

## 5. 下一轮唯一优先任务

**针对30拍末端关联状态集合，设计使用真实5拍success/miss信息的双向姿态/速度反馈（允许非零倾角），检验是否存在在全部`r∈[-R,R]`和所有合法观测分支下均可重复闭合的共享因果终端策略。** 首先严格处理`r=-R`造成的速度下界恶化；失败时归档反例，禁止把本轮开环安全见证包装成MPC。

## Run245完整checkout CI与安全合并核验（2026-11-01）

研究PR #60 https://github.com/zhouxingxing1279/AcademicReaserch/pull/60 基于main `a4ae3a7f6bf8587d0f328160a44cda3be6b8b0eb`，合并前compare ahead=7/behind=0、mergeable_state=clean、head=`a039c58c54e2a263f75802085770ade03dbc1c21`。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41324536887 **completed/success**；Python 3.13.17完整checkout执行Run224–245共**190/190项聚焦测试通过、无跳过**，真实配置核验、精确Fraction外包、归档JSON比对、artifact上传成功。PR通过非强制squash合并到main `8984d21d796fc6d57edc13cace9addfd5a720664`；再次读取远端main SHA、PR merged状态及源码/测试/JSON Blob确认落地。合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41324650743 **completed/success**，Python 3.13.17完整checkout再次**190/190通过、无跳过**（38.727s），归档证书比对和artifact上传成功。此补记不改变数学证书或算法，未单独触发CI；全仓库历史回归、SMF-MPC递归可行、六状态安全与20ms最坏时延仍未认证。

