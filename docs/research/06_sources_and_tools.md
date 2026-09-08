# 06 文献、工具依据与查新边界

检索截止：2026-09-08。本文区分来源中的已有工作、本方案的推断与尚待验证的候选贡献。链接指向原论文、出版社、作者机构或官方代码；摘要级证据不能证明论文“没有做过”某一机制。

## 1. 最接近工作及实际影响

| 来源 | 已核查内容与阅读层级 | 对本方向的约束与下一步 |
|---|---|---|
| [Köhler, Müller, Allgöwer：Robust output feedback model predictive control using online estimation bounds，2021 预印本](https://arxiv.org/abs/2105.03427)；[原文 PDF](https://arxiv.org/pdf/2105.03427) | 核查原文方法与数值例：在线估计界、集员/MHE 思路、非线性输出反馈 MPC，包含四旋翼例子 | “SMF＋MPC＋四旋翼”已经存在；学习目标须提供独立于控制架构拼接的贡献。其可检测性和可稳定性条件不能自动转移到本网络 |
| [KNODE-MPC，2021 预印本](https://arxiv.org/abs/2109.04821) | 原始摘要/论文页面：知识驱动神经 ODE、四旋翼 MPC 与实验 | “物理模型＋残差网络＋MPC”不是创新。需要同等模型容量与物理基线 |
| [Ren 等：KNODEOB-MPC，2026，DOI 10.1002/rnc.70444](https://onlinelibrary.wiley.com/doi/10.1002/rnc.70444) | 出版社摘要：知识驱动神经 ODE、在线观测器、多扰动四旋翼跟踪 | “再加观测器”也已有直接近邻。未逐页核查全部证明，不能据摘要断言其没有某项保证 |
| [Pan 等：Zonotopic set-membership state estimation for nonlinear systems based on deep Koopman operator，Neurocomputing 618，129004，2025](https://scholar.xjtlu.edu.cn/en/publications/zonotopic-set-membership-state-estimation-for-nonlinear-systems-b/)；[DOI](https://doi.org/10.1016/j.neucom.2024.129004) | 作者机构记录与摘要；全文尚需获取 | 深度学习与 zonotope 集员状态估计已有直接结合；本方案保留物理状态不构成单独创新，必须比较后验训练机制 |
| [Kayalibay 等：Filter-Aware Model-Predictive Control，L4DC 2023](https://proceedings.mlr.press/v211/kayalibay23a.html)；[原文 PDF](https://proceedings.mlr.press/v211/kayalibay23a/kayalibay23a.pdf) | 原文核查：将估计误差/滤波表现纳入预测控制，使用学习的预期误差信息 | 考虑估计质量本身不新；本方案候选差别是学习动力学时递推带测量修正的状态外包络，并重新认证物理误差 |
| [Shen, Chou：Parallel Differentiable Reachability for Learning and Planning with Certified Neural Dynamics and Controllers，2026](https://arxiv.org/abs/2605.25346)；[核查版本 v1](https://arxiv.org/html/2605.25346v1)；[作者代码](https://github.com/trustworthyrobotics/DiffReach-Robotics) | 核查原文框架/初始不确定集与训练目标：可微可达性、神经模型与控制器训练、机器人规划；作者代码引用标为 RSS 2026 | 最强重叠风险。不能声称其不处理状态不确定性。待验证差别仅是递归、测量条件化后验集合目标与间歇测量模式；C/D 对比不可省 |
| [Deole, Mesbahi，arXiv:2501.09192](https://arxiv.org/abs/2501.09192) | 原始论文页面：集合值估计/测量相关轨迹规划方向；细节需逐节再读 | 测量影响集合和规划也不是空白；复查是否已有优化后验几何量的同构目标 |
| [Perception-Aware Model Predictive Control for Quadrotors，2018](https://arxiv.org/abs/1804.04811) | 原始摘要/页面：四旋翼中同时考虑动作与感知 | 不把“感知与控制联合设计”作为新贡献；本研究不优化相机朝向 |
| [Neural-Fly，2022](https://arxiv.org/abs/2205.06908)；[作者训练代码](https://github.com/aerorobotics/neural-fly) | 作者来源：学习与适应气动效应、四旋翼扰动控制 | 后续工程比较线索；代码/数据的适用性和许可需按实际选用版本核查，未在本交付复现 |
| [Robust Learning-Based Output-Feedback MPC，arXiv:2110.00542](https://arxiv.org/abs/2110.00542) | 原始论文页面：学习型输出反馈 MPC 的既有研究 | 不能因题目含 learning 就认定其训练神经动力学；需区分迭代学习终端安全集与模型学习 |
| [Outlier-robust set-membership filtering，DOI 10.1109/JAS.2021.1003826](https://www.ieee-jas.com/article/doi/10.1109/JAS.2021.1003826) | 出版社页面：异常观测与集员滤波相关机制 | 异常点处理已有路线；本方案首轮只考虑缺失，不将异常鲁棒性捆绑成贡献 |

上表是有针对性的最近邻核查，不是穷尽性系统综述。对仅查到摘要的文章，投稿前必须获取全文、定位公式与实验，再更新差异表。本文对机制差别的判断均为**研究推断**；没有建立优先权或首创性证明。

## 2. 三个具体候选贡献与否证条件

| 候选 | 可实现对象 | 最接近已有内容 | 必须得到的证据 | 否证/收缩条件 |
|---|---|---|---|---|
| CAND-1 主线：测量模式感知的后验集合训练 | 02 的 T1，固定物理状态、小型网络、25 步测量展开 | DiffReach 的集合传播训练；Filter-Aware MPC 的估计质量意识 | 同预算 D 对 C、B 的收益；每网络重新认证仍有效；紧集合表示仍有同向收益 | 收益仅由无效界或 box 缺陷产生；已有文献含同构机制 |
| CAND-2 扩展：模型—丢测合同的可行区域比较 | 模式自动机、03 的增广误差族与终端验证 | 在线估计界输出反馈 MPC | 明确计算域内，得到经验证的充分丢测容忍条件或可行初始集扩大 | 找不到非空终端族；只能得到有限经验成功率 |
| CAND-3 次线：认证后的模型选择准则 | 联合报告预测误差、真实残差界、后验宽度、控制可行率 | 可达性友好学习与认证工具 | 解释点预测最优模型为何不一定后验最优；可重复的边界实验 | 差异由预算/调参不公平造成；只换指标名称 |

优先执行 CAND-1；CAND-2 不应阻塞早期否证，CAND-3 可以支持负结果论文，但单独发表价值仍需文献与数据判断。暂不承诺任何期刊层次。

## 3. 可复查检索协议

本轮使用及后续复查的查询族：

- `quadrotor set-membership output-feedback MPC neural dynamics`
- `measurement update aware learning posterior set reachability`
- `filter-aware model predictive control`
- `deep Koopman zonotopic set-membership state estimation`
- `differentiable reachability neural dynamics intermittent observations`
- `KNODE MPC online observer quadrotor`

每次 G0/G3/G4 查新同时检查近邻文章的参考文献、作者代码和后续论文。记录：检索日期、版本、状态/测量假设、训练变量、集合表示、目标函数、认证对象、定理前提、实验平台。只看标题相似度不足以判断重复。

尚未解决的查新任务：Pan 2025 全文；KNODEOB 2026 逐页方法与证明；DiffReach 会议最终版与 v1 差异；Deole/Mesbahi 的测量条件化目标是否与 T1 等价。任一发现同构目标，先调整主张，再继续训练。

## 4. 工具选择的官方依据

| 工具/官方入口 | 本研究的具体职责 | 当前完成程度 |
|---|---|---|
| [PyTorch 随机性说明](https://docs.pytorch.org/docs/stable/notes/randomness.html) | 小型 MLP、可微区间展开、种子与数值精度记录 | 尚未训练；固定种子不意味着跨平台逐位一致 |
| [CasADi 文档](https://web.casadi.org/docs/) | M1/M2 表达、AD、IPOPT 原型与导数交叉检查 | 尚未实现 MPC |
| [acados 文档](https://docs.acados.org/) | 后期 OCP 求解与代码生成加速 | 尚未移植，不承诺 20 ms 达标 |
| [auto_LiRPA 官方仓库](https://github.com/Verified-Intelligence/auto_LiRPA) | 网络输出松弛界，辅助残差函数包络 | 未运行；需核查运算支持和舍入误差 |
| [CORA 官方项目](https://tumcps.github.io/CORA/) | 连续/离散系统可达性、集合和独立认证参考 | 可选 MATLAB 路线，未安装/执行 |
| [SciPy linprog](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html) | 普通 zonotope 支持函数的独立 LP 数值检查 | 本次已执行；不是严格舍入 LP 证书 |
| [CVXPY 半正定约束](https://www.cvxpy.org/tutorial/constraints/index.html) | 模式相关 Lyapunov/LMI 候选的离线综合 | 待实现；数值可行解需再认证 |
| [PX4 官方仿真](https://docs.px4.io/main/en/simulation/) | 后期 SITL、传感器链路与执行接口核对 | 未运行 PX4，不声称实飞性能 |

只锁定本次真正执行的轻量环境：Python 3.12.13、NumPy 2.3.5、SciPy 1.17.0，见 verification。完整训练/MPC 依赖在 G1 安装兼容版本后冻结 lockfile，保存 OS、BLAS、GPU、编译器与 solver 配置；这里没有把滚动网页的“latest”写成可复现版本。

## 5. ARS 使用说明

使用用户指定的 [academic-research-skills 仓库](https://github.com/imbad0202/academic-research-skills) 中 deep-research 的来源核验、研究设计与反方审查思想，并阅读其 bibliography/devils_advocate 角色材料。未照搬用户过去的研究结论；也没有完整执行该仓库全部流水线、所有钩子、跨模型 API 或投稿操作。

本次保存的是针对该课题编写的方案与核查脚本，没有把第三方 skill 源码复制进本仓库。AI 辅助推导与文献筛选不能替代作者对关键全文和证明的复核。执行记录见 07。
