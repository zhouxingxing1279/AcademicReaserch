**Run257 PR/main CI及安全合并复核（2026-11-02 UTC）：** 研究PR #94 https://github.com/zhouxingxing1279/AcademicReaserch/pull/94 基于main `4bbe6ab7e579ae1f48f4c1dd58afaa7f6d07b5c9`，合并前compare ahead=9/behind=0，严格仅7个预期文件，PR mergeable_state=clean，expected head `09021e7f50bd1280fbe31e6f759301e3773f0f4a`。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41386737723 **completed/success**；读取完整Python3.13 job日志确认Run249–257聚焦**78/78通过、无跳过**，源码编译、真实Run255/256与配置交叉核验、精确JSON逐字比较和artifact上传成功。使用expected-head非强制squash合并至main `d6a7cb3ac235959880962fd57cf3d675a6750b01`，重新读取main SHA、PR merged及7个文件Blob核验落地。合并后main push CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41386789339 **completed/success**；完整Python3.13 job日志再次**78/78通过、无跳过**、配置交叉核验与JSON逐字比较成功。**全仓库历史回归未执行**，CI通过不代表关联后验已完整实现、无限时域终端核或稳定性得到证明。本补记仅记录验证状态，不改变算法、论文数量或数学证书；**Gate A仍blocked**。

---

# Run257 — 两次位置条带保留 p-v 关联的严格速度投影界（2026-11-02 UTC）

## 本轮瓶颈与基准

起点远端 main `4bbe6ab7e579ae1f48f4c1dd58afaa7f6d07b5c9`；阅读 `docs/research/CURRENT_CHECKPOINT.md`、Run249/255/256日志与验证源码、`docs/literature/PAPER_READING_LOG.md`、`configs/planar_baseline.json` 约束及背景第10轮结论。Run256证明**独立盒表示**的位置成功包不能收缩速度宽度，并非证明关联后验不收缩。本轮只研究第30–35拍关联信息的一个可复核、低复杂度内核，不改Run249控制器，不并行开发六状态算法。

四状态Euler基准 `x=(p,v,phi,omega)`，`h=0.02`、固定`T=9.81`、`J=0.02`、`|r|<=3246383/1600000 m/s²`、位置噪声`±0.02m`。继承Run254特定`SSSMMS`零读数历史第30拍可靠外包 `p30∈[-0.02,0.02]`、`v30∈±1.346823505`、`phi30∈±0.005`、`omega30∈±0.01`；执行Run255共享力矩`(+0.04,-0.04,-0.04,+0.04,0)Nm`。第35拍未观测速度独立盒为`[-1.5553337315,1.554705901]`，宽`3.1100396325m/s`。

## 关联H-rep条带与全称保证

定义真实水平加速度 `a_i=-T sin(phi_i)+r_i`。使用Run255逐拍可靠姿态区间和精确有理数Taylor正弦包络，逐拍得到 `a_i∈[a_i^L,a_i^U]`。由**真实离散Euler运动学**逐项消元：

```
p35 = p30 + 5h*v30 + h²*sum_(i=0)^4 (4-i)*a_i
v35 = v30 + h*sum_(i=0)^4 a_i
v35 = (p35-p30)/(5h) + h*sum_(i=0)^4 (i+1)/5*a_i .
```

对于第35拍**任何非空success位置读数**`y`，其条带`p35∈[y-0.02,y+0.02]`与第30拍`p30∈[-0.02,0.02]`给出可靠速度投影；再与第35拍独立盒速度区间相交。因使用的是包含真实状态的必要线性条带与向外加速度界，结论对该历史下**所有合法真实状态、扰动、成功位置读数**成立，未假定真实速度可见。每一固定success读数的后验速度投影宽度满足统一上界

```
width(v35|y,success) <= 0.8 + h*sum_(i=0)^4 ((i+1)/5)*(a_i^U-a_i^L)
                       = 1.0499925305899253448... m/s.
```

对读数`y=0`，所得认证速度区间约`[-0.52521600592954,0.52477652466039]`m/s，宽`1.04999253058993`，相较独立盒宽`3.1100396325`约缩小**66.24%**。精确分数存入JSON，非浮点求解器近似。零读数success分支并非空：构造`p30=v30=phi30=omega30=0`、逐拍`r_i=0`与合法脉冲，姿态/角速第35拍回零，精确正弦包络证明`p35`约`-9.42e-6m`，落在零读数±0.02m内；中间姿态/角速读数可取真实值，不要求脉冲中途每拍读数为零。

对于第35拍**miss**，本轮没有新的位置条带，保守速度外包仍为`3.1100396325m/s`；不能将success的收缩外推给miss或所有后续观测图。以上是低维联合运动学/H-rep投影的**可靠外界**，不是精确真实后验、CZ-CG实现、同预算复杂度比较、终端RCI或MPC安全性充分证书。尚未量测20ms最坏运行时间。

## 论文定向复核（去重不增加）

Brenner S. Rego, Guilherme V. Raffo, Joseph K. Scott, Davide M. Raimondo, *Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems*, *Automatica* 111:108614 (2020), DOI https://doi.org/10.1016/j.automatica.2019.108614，作者公开预印本 arXiv:1908.09950v3 https://arxiv.org/pdf/1908.09950 。本轮实际阅读预印本PDF pp.2–3 §2–3.1（状态预测/量测更新、CG-rep式(7)与广义交集式(10)）、pp.7–8 §4.4–4.5（式(22)、Remark 10）、pp.10–12 §5.2四旋翼案例与Tables 5–6。论文研究**状态估计**而非参数估计；模型一般非线性离散、已知施加输入、紧有界过程/量测噪声。其§5.2确有**12状态四旋翼Euler仿真**，输入`U1`总推力与`U2/U3/U4`转子差动推力/力矩通道，位置/姿态/角速带噪观测、速度不直接测量；但其控制器在该实验**使用真实状态**（脚注10），并非真正的SMF闭环输出反馈MPC，也没有位置丢包。该仿真中CZMV/ZMV平均半径比74.41%，表6计算耗时104.7ms起（CZMV 3约束），**超过论文10ms采样周期**，不能据此声称实时可用。既有Run256日志曾把该论文示例概括为“非四旋翼”，本轮纠正这一文献事实；不新增去重篇数。论文的CZ交集可保留相关性，但复杂度增长需保包含降阶，不提供本仓库终端安全定理。

## 测试与研究边界

隔离Linux Python标准库、Fraction：相同动力学的独立原型8/8本地测试、`py_compile`与JSON精确生成通过；完整仓库的Run249–257聚焦回归、真实Run255源码与配置交叉核验、归档JSON逐字比较由PR Actions运行并另行核验。源码`verification/check_run257_correlated_position_velocity.py`、测试`verification/test_run257_correlated_position_velocity.py`、证书`results/run257_correlated_position_velocity_20261102/checks.json`、工作流`.github/workflows/run257-correlated-position-velocity.yml`。

**可行性/创新性/难度：** 证明保留最小`p-v`关联即可显著收缩某次成功测量后的可靠速度投影，支持转向关联H-rep/CZ，但这只是标准集合估计思想在仓库具体历史上的可复核实例，不宣称方法创新；在连续miss与完整观测树上的有效性、计算复杂度和终端安全仍是高难度未决问题。Gate A **blocked**，没有无限时域递归可行性、稳定性、六状态安全或20ms WCET证书。

**下一轮唯一优先问题：** 在同一Run254/255信息状态下，将这条五拍联合约束构造成**可递推的H-rep/CZ后验**（包含success与miss并保持`p-v`关联），检查第40拍下一次合法位置观测后的联合投影及复杂度，再决定是否进入终端安全前驱计算。
