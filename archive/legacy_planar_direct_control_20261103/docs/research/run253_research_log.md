**Run253完整checkout、PR/main CI及安全合并复核（2026-11-02 UTC）：** 研究PR #82 https://github.com/zhouxingxing1279/AcademicReaserch/pull/82 ，基准main `265a70c0bc9247d478b114e37c050aae808c794e`，合并前compare ahead=7/behind=0，7个预期文件，PR head `e6f5167128ad42bd2c6e31c8cc7a4b10baf0977a`，mergeable_state=clean。PR Actions https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41365844668 **completed/success**，读取完整checkout Python3.13.17 job日志确认Run249–253聚焦 **44/44通过、无跳过**，Run251/252和真实配置交叉核验、`py_compile`、精确JSON逐字比对及artifact上传成功。expected-head非强制squash合并至main `4a25e389f1ab4d7d2730dc308407b22bff21f6e3`，重新读取main SHA、PR merged和新增源码/证书/日志Blob核验落地。合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41365922605 **completed/success**，完整checkout再次**44/44通过、无跳过**，证书一致且artifact上传成功。此补记仅更新验证证据，不改变算法/数学证书；全仓库历史回归、整个SMF后验终端闭合、无限递归可行、六状态安全和20ms WCET仍未认证。Gate A仍blocked。

---

# Run253 — 强制位置恢复测量前的非零共享备份与双轨迹可区分性（2026-11-01）

## 基线、唯一问题和证据范围

起点远端main `265a70c0bc9247d478b114e37c050aae808c794e`（含背景模型选型PR #81及Run252）。复核 `docs/research/CURRENT_CHECKPOINT.md`、唯一论文阅读记录、Run249–252源码与Run252证书。Run249的55拍有限时域安全仍不是无限时域递归可行；Run252仅对一个真实可达的双速度纤维给出必要信息宽度。**Gate A继续blocked**。

唯一问题：Run252在第25拍位置包连续两次miss后，能否给出一个合法非零共享控制前缀，严格保证这两条真实轨迹至第30拍下一次强制success仍安全？该成功位置包能否区分两条极端轨迹？

## 严格数学增量（仅限Run251/252双轨迹）

冻结四状态离散Euler：`p+=h*v; v+=h*(-T*sin(phi)+r); phi+=h*omega; omega+=h/J*tau`，`h=J=1/50, T=981/100, |r|<=3246383/1600000, |tau|<=2/25`，位置测量噪声 `|n_p|<=1/50`。Run251已证明0–15拍固定零力矩下存在共同成功测量的两条合法路径，`p15=phi15=omega15=0`，速度差 `D15=42202979/80000000`。Run252使15–25拍残差分别为`+R,-R`，力矩可以为任意共同合法序列，姿态与角速依然相同，故角加速度及`-T sin(phi)`在两条路径差分中精确抵消。

对任何共享合法力矩15–29拍及任何25–29拍合法残差，取`j=k-15`，两条路径每个中间时刻的共同绝对外包：
`Phi(j)=h U j(j-1)/2`，
`V(j)=D15/2+j h R+h T sum_{i=0}^{j-1}Phi(i)`，
`P(j)=h sum_{i=0}^{j-1}V(i)`，
`Omega(j)=j U`。
只用`|sin(phi)|<=|phi|`，精确有理数对全部`0<=j<=15`检查安全；第30拍上界为
`|p|<=1383345243/8000000000≈0.172918155375m`、
`|v|<=32489569/32000000≈1.01529903125m/s`、
`|phi|<=21/125=0.168rad`、
`|omega|<=6/5=1.2rad/s`，均严格满足硬约束（5m、3m/s、0.45rad、2rad/s）。因此非零共享控制前缀 `(+0.04,-0.04,-0.04,+0.04,0)Nm` 是一个可执行的**有限5拍桥接例子**；甚至任意合法共同力矩也在本双轨迹的上述有限时域外包内安全。这**不是**整个SMF后验盒的充分安全证明。

两路径25拍位置差为 `Delta p25=35710213/200000000=0.178551065m`，速度差 `Delta v25=107130639/80000000=1.3391329875m/s`。后续5拍任意两个独立合法残差的差满足 `Delta r>=-2R`，因果共享力矩使姿态差始终为0，因此
`Delta p30>=Delta p25+5h Delta v25-2R h^2(0+1+2+3+4)=236985959/800000000=0.29623244875m`。
即使允许两条路径在30拍分别取任意合法位置噪声，成功测量读数的差仍至少 `0.29623244875-0.04=0.25623244875m>0`。因丢包自动机最多连续miss两次，`SSSMM`之后第30拍必须success；这**两条特定路径**的成功位置观测必然可区分，控制器可以在30拍以后分支。单个success后验位置投影直径至多`0.04m`，但不能据此声称速度后验宽度有统一收缩率。

**量词边界：** 只证明Run251固定0–15拍前缀和Run252指定15–25拍双扰动纤维的有限安全与强制success可区分性。未覆盖其余SMF一致状态、所有丢包历史、下一轮后继集合闭合、无限时域递归可行、稳定性、六状态安全或20ms WCET。绝不能把“有限5拍可执行备份”写成“终端RCI”。

## 文献重读与准确迁移边界

Liren Yang、Necmiye Ozay (2021), *Safety Control Synthesis for Systems with Missing Measurements*, ADHS 2021 / IFAC-PapersOnLine pp.97–102, DOI https://doi.org/10.1016/j.ifacol.2021.08.481 ，作者公开正文 https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。2026-11-01本轮重新核对§3式(3)–(7)及§4.2–4.4、Proposition 4/5：成功时`y=x`，失败时`y=empty`；string automaton编码失测上限与因果共享前缀，产品系统在额外紧性/连续性假设下综合不变核。本文**没有**位置-only有噪SMF，也不提供当前四状态的终端证书；本轮强制success可区分性是独立推导，不能归因于该文。既有文献重新分节阅读，统一去重数量不增加。

## 工件、测试与下一步

- `verification/check_forced_reobservation_bridge.py`：精确Fraction外包、两路径位置差下界、强制success与配置交叉核验。
- `verification/test_forced_reobservation_bridge.py`：9项测试（包含真实仓库配置与Run251/252的交叉项）。
- `results/forced_reobservation_bridge_20261101/checks.json`：精确有理数证书。
- `.github/workflows/run253-forced-reobservation-bridge.yml`：完整checkout的Run249–253聚焦回归、配置交叉核验、JSON逐字比对及上传。

隔离Linux/Python标准库运行 `cd /mnt/data/run253 && python -m unittest -v test_forced_reobservation_bridge`：**8通过、1因无完整仓库配置而显式跳过**；`python -m py_compile`和证书生成成功。PR及main CI须等待实际结果，不提前宣称。无新闭环控制器或新增统计仿真。

**可行性/创新性/难度：** 给出了非零共享备份的正向有限桥接证书和强制位置测量对特定极端双路径的可区分性，利于缩小信息状态终端搜索范围；但“有限桥接”不是独立硕士创新点。递归信息状态安全游戏仍为高难瓶颈。

**下一轮唯一优先任务：** 在第30拍两个互斥成功测量分支上，计算**覆盖全部SMF一致状态**的后验集合及可移位后继，检验至少一个非空输出反馈终端信息状态集合的闭合性；如果失败，明确将硕士课题限定为有条件有限时域安全过滤。
