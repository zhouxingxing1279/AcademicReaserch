**Run272 PR CI与安全合并独立复核（2026-11-02 UTC）：** 研究PR #139 https://github.com/zhouxingxing1279/AcademicReaserch/pull/139 以main `e77fd13e31dd72b834eae1704cbc2245a7a8d5ac`为基准，合并前compare ahead=7/behind=0，严格7个预期文件、无删除，PR mergeable=true，expected head `d604785090a0389b3d3bc04a40b899572c3147f8`。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41507301427 **completed/success**；读取Python3.13.17完整checkout job日志确认Run270/271/272聚焦回归**24/24通过**、源码编译、真实冻结配置及Run271证书交叉核验、Run272 Fraction JSON逐字比较通过。expected-head非强制squash合并至main `e4cad987b4383df43d21310941466a4ac41c4469`，再次读取main SHA、PR merged及6个关键文件Blob确认落地；本地代码、测试、JSON的Git Blob SHA与远端一致。**合并后main push CI尚未独立确认，全仓库历史回归未执行。** 本轮仅证明特定Run260后验纤维的重复混叠与双真值15拍安全前缀，不是全后验终端信息RCI、MPC或无限递归安全；**Gate A=blocked**。

---

# Run272 — 第60–75拍双失测后的重复观测混叠：安全前缀不等于信息终端回返（2026-11-02）

## 1. 最新远端基准与唯一问题
基于远端 main `e77fd13e31dd72b834eae1704cbc2245a7a8d5ac` 创建独立分支。读取 `CURRENT_CHECKPOINT.md`、唯一 `PAPER_READING_LOG.md`、背景模型矩阵、Run260/268/270/271日志、Run270/271验证源码及真实 `configs/planar_baseline.json`。背景任务第24轮未解决执行器最终命令认证，六状态平面物理首选仍是条件性的。本轮仅解决：**Run271已证明的第60拍真实双真值，在下一次最坏合法连续失测(65/70 miss,75 success)后，能否仍产生相同读数且隐藏速度差更大？** 不将此问题等同完整信息RCI。

## 2. 冻结模型、精确构造和量词
使用Run260定义的四状态Euler真值 `x=(p,v,phi,omega)`，`h=J=1/50,T=981/100,R=3246383/1600000,|r|<=R,|tau|<=0.08`；硬盒 `|p|<=5,|v|<=3,|phi|<=0.45,|omega|<=2`；位置成功读数 `y=p+n,|n|<=1/50`，每5拍位置机会、最多连续两次miss，每拍角度/角速有噪观测。Run271在Run260真实MMS→MMS历史中证明第60拍共享零读数双真值：
`x60±=(±68174043/4000000000, ±22724681/80000000,0,0)`。
从这两个**真实后验成员**出发，施加共同合法 `tau=0`，第60–74拍给正轨迹 `r=-R`、负轨迹 `r=+R`；65/70 miss、75 success且读数 `y75=0`。所有角度/角速真实值及读数均相同。Euler精确求和得到
`p75±=±68174043/4000000000`，`v75±=∓3246383/10000000`。
两条位置分别配 `n75±=∓68174043/4000000000`，合法且成功读数相同；因此该**特定非空完整观测纤维**的任何可靠SMF后验，第75拍速度投影直径至少 `3246383/5000000=0.6492766 m/s`，大于第60拍见证的 `0.568117025m/s`。这**不证明整个第75拍后验直径恰为该值**。

对任意同观测纤维的共同力矩（直到首次可区分观测）和任意两条合法未来扰动，角状态相同使其横向加速度差中的 `-T sin(phi)` 项抵消。第60拍差 `Δp0=42h²R,Δv0=14hR`；任意未来 `q<=15` 拍有
`Δp_q>=Δp0+qhΔv0-h²R q(q-1)`。
故第65拍、70拍的最小位置差均为 `74666809/1000000000=0.074666809m>2eps=0.04m`，若这些拍**成功**，这对真值无法共享同一位置读数；但合法65/70双miss后，第75拍对抗扰动可使位置差重新为 `68174043/2000000000=0.0340870215m<0.04m`，仍混叠。这个差异证明丢包模式和测量纤维必须纳入信息状态，而不能仅用“15拍必有成功包”代替。

**有限安全充分证书（仅双真值）：** 对上述两条第60拍初始真值，施加共同 `tau=0`，对**全部**后续 `|r_k|<=R`，第60–75拍都有 `|v|<=35710213/40000000=0.892755325m/s`、`|p|<=749914473/4000000000=0.18747861825m`、`phi=omega=0`，严格满足四状态硬盒；具体混叠轨迹逐拍也经Fraction检查。此结果只是两个初始真值的15拍共享鲁棒安全前缀，**不是完整Run260第60拍后验外包的安全前缀、终端回返、无限递归可行或稳定性证明**。

## 3. 文献研读与不可直接迁移的保证
新读 Minghong She、Wenbin Wu (2023), *Efficient Output Feedback MPC for NCS With Data Dropout and Bounded Disturbance via Adaptive Event-Triggered Control*, *IEEE Access* 11:118161–118169, DOI https://doi.org/10.1109/ACCESS.2023.3324923；公开作者接受稿 https://www.researchgate.net/publication/374963972_Efficient_Output_Feedback_MPC_for_NCS_with_Data_Dropout_and_Bounded_Disturbance_via_Adaptive_Event-triggered_Control 。2026-11-02实际分节阅读接受稿正文pp.1–7 §II–V，重点式(1)–(8)、Lemma 1–4、OP1–OP4及两个仿真案例；参考文献未逐项阅读、未复现LMI。论文是一般多面体不确定线性系统，不是四旋翼；采用**Bernoulli随机丢包**、保持上一输出、LMI观测器、椭球误差界、离线反馈增益及在线有限维补偿优化。其关键二次估计误差/性能不等式含期望算子，且实验为CSTR与三状态一般系统仿真；**不能把随机意义的结果当作本项目“最多2次丢包、所有扰动、每拍硬约束”的路径级安全保证**。可迁移：丢包观测器与MPC接口分离、离线增益和在线补偿、把丢包机制显式编码；不可直接移植其LMI证书或声称已解决本项目终端信息RCI。首次登记唯一总账，按DOI去重。

## 4. 工件、执行结果和失败边界
新增 `verification/check_run272_recurrent_aliasing.py`、`verification/test_run272_recurrent_aliasing.py`、`results/run272_recurrent_aliasing_20261102/checks.json`、`.github/workflows/run272-recurrent-aliasing.yml`。本地Linux Python 3执行 `cd verification && python -m unittest -v test_run272_recurrent_aliasing.py`（隔离等价目录）：**8/8通过**；`python -m py_compile`通过；精确Fraction证书生成且与GitHub远端文件blob SHA逐字一致。容器DNS不能连接github.com，本地无法运行完整checkout；CI将检查真实配置、Run271归档交叉核验、Run270/271/272聚焦回归及JSON逐字一致。**PR CI与合并状态必须在实际执行后另行核验**，不预设成功。若CI失败，保留失败记录且不合并。

可行性：有限双真值证书低计算成本，完整信息状态安全综合仍中高；创新性：这是本项目观测纤维的严格反例性证据，**不声称首先发现丢包混叠**；研究难度：全后验共享反馈回返是主要瓶颈。主方向可调整为有严格有限时域安全保证的MPC+SMF，但尚不做无证据收口。**Gate A=blocked**。没有新MPC求解器、CZ递推、全后验终端不变核、六状态物理安全或20ms WCET。

## 5. 下一轮唯一优先任务
针对Run260第60拍**完整可靠后验外包**而非两条见证轨迹，构造可计算的15拍因果共享控制安全前驱/回返检验；先比较65/70成功与双miss分支的条件化后验是否均进入同一个可移位终端信息族。若不能给充分证书，应记录失败并明确有限时域安全课题的收敛条件。
