# Run255 — 完整Run254区间后验上的共享非零控制有限桥接（2026-11-02 UTC）

## 基线与唯一瓶颈
起点远端main `b60b4ae67ac7da7fcd08ba54b0d65d80ae8dacec`，已读取`CURRENT_CHECKPOINT.md`、唯一`PAPER_READING_LOG.md`、Run249/253/254日志与Run249/254源码及Run254精确归档。Run254仅用两条真实轨迹证明第30拍成功位置包后隐藏速度仍不可区分；下一步需要覆盖该**完整一致后验**而非仅两条见证轨迹。本轮选择Run254特定合法零读数历史，构造其可靠**区间外包**上的共享非零备份及全部未来测量分支的有限安全证书。没有宣称覆盖其他第30拍读数历史或得到无限终端不变核。

## 精确模型、量词与正向证书
冻结四状态Euler `x=(p,v,phi,omega)`，`h=J=1/50`、`T=981/100`、`|r|<=3246383/1600000`、`|tau|<=2/25`；`p+=h v`、`v+=h(-T sin(phi)+r)`、`phi+=h omega`、`omega+=h/J tau`。硬盒`|p|<=5, |v|<=3, |phi|<=0.45, |omega|<=2`。角/角速每拍有噪读数，位置每5拍一次、最多连续miss两包；本轮冻结的历史为`SSSMMS`（5/10/15/30拍成功，20/25拍失测），所有可用读数取0。

按Run249的有理数、sin Taylor可靠包络和1e-10向外网格舍入重算Run254第30拍区间后验：
`S30^box: p∈[-0.02,0.02], v∈[-1.346823505,1.346823505], phi∈[-0.005,0.005], omega∈[-0.01,0.01]`。
这**包含全部与该历史一致的真实状态**，但不是精确关联后验。选择因果共享、合法的第30–34拍力矩`(+0.04,-0.04,-0.04,+0.04,0) Nm`，其后恒为0；它不使用隐藏速度、未来扰动或未来success/miss。对`S30^box`整体、全部逐拍独立`|r|<=R`做可靠区间传播，逐拍精确断言**30–69拍全部硬约束安全（39个未来控制步，0.78s）**。第69拍可靠外包：
`p∈[-1.6938481349,1.6934023754]`m，
`v∈[-2.9970839345,2.996456104]`m/s，
`phi∈[-0.0128,0.0128]`rad，
`omega∈[-0.01,0.01]`rad/s。
第70拍外包速度`[-3.0401750135,3.039547183]`m/s越界，**仅说明本区间证书无法延长至第70拍**；不能推出真实后验在70拍必然不安全、此策略的物理最大时域或其他反馈不可行。

任意后续合法成功位置读数（噪声半宽0.02）、角度/角速读数与失测分支，其非空SMF后验都是未条件化预测外包的子集；因为固定共享输入不依赖未来观测且区间预测单调，以上30–69拍安全对**所有后续合法扰动、噪声和success/miss分支**成立。这是针对**一个既定第30拍观测历史的全部可靠外包状态**的充分有限安全结果，不是所有历史上的终端集合闭合或无限时域递归可行。

## 论文重读与迁移边界
Liren Yang, Necmiye Ozay (2021), *Safety Control Synthesis for Systems with Missing Measurements*, IFAC-PapersOnLine / ADHS 2021, pp.97–102, DOI https://doi.org/10.1016/j.ifacol.2021.08.481 ，作者全文 https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。2026-11-02实际复核PDF pp.2–5 §3、§4.2–4.5，尤其Propositions 4–5、式(8)–(17)。其安全博弈将**完整无噪状态测量**的丢失模式编码成string automaton，并用共享因果控制序列与产品系统不变核证明无限时域安全；§4.5讨论部分状态始终完美可测且该部分动力学不受未测状态影响的特例。本仓库角度/角速**有噪**，位置**有噪且间歇**，隐藏速度未测，因此不能直接套用其完整状态/完美部分状态定理。可复用自动机与共享前缀量词，必须另建SMF信息状态转移。既有已读论文重读，唯一去重数量保持102，不增加条目。

## 运行、可复核工件与限制
本地Linux Python 3.13.5，标准库Fraction：
```bash
cd /mnt/data/run255_work
python -m unittest -v test_run255_posterior_bridge
python -m py_compile check_run255_posterior_bridge.py test_run255_posterior_bridge.py
python check_run255_posterior_bridge.py --output checks.json
```
8/8本地测试通过、无跳过；精确JSON生成成功。GitHub完整checkout工作流额外执行Run249–255聚焦回归、与Run249原始`step`及Run254原始`outer_history`交叉核验、真实配置、证书逐字比对；其状态以实际CI为准，不能把本地独立计算冒充完整checkout。

源码`verification/check_run255_posterior_bridge.py`，测试`verification/test_run255_posterior_bridge.py`，归档`results/run255_posterior_bridge_20261101/checks.json`，工作流`.github/workflows/run255-posterior-bridge.yml`。本轮不修改Run249控制器，不新增仿真性能比较。数学级别：特定历史的全可靠区间后验**有限**安全证书；不是真实后验精确直径、一般信息状态RCI、无限递归可行、鲁棒稳定、六状态安全或20ms WCET。Gate A仍blocked。

**可行性/创新性/难度：** 相较Run253只覆盖两条见证路径，本轮将有限共享控制证书提升至Run254同一历史的**全部可靠区间后验**；是正向验证增量，但有限固定策略不是独立理论创新。区间在第70拍过宽、未建立后验分支的可移位闭合，继续直接扩大时域收益有限。

**下一轮唯一优先任务：** 在第35拍success/miss的**所有非空后验分支**上定义可计算的信息状态前驱，并尝试找出一个统一有界、可移位的非空终端信息状态族；若不可得，应明确收敛为有条件有限时域SMF+MPC安全过滤硕士题目。
