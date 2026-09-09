# AcademicReaserch

## 当前研究：间歇位置测量下的神经动力学建模与集员输出反馈 MPC

本仓库从零建立一条可证伪的研究路线：在物理状态上学习未建模加速度，研究测量更新与丢测模式是否改变模型训练的最优选择，并验证这种变化是否减少集合外包络冗余、改善控制可行性。

**当前已有详细方案与可运行的 G1 数值原型（模拟器、测量调度、box SMF、线性 zonotope 对照）。17 项新增性质测试通过；尚未实现神经训练与 MPC。** 不预设论文级别，不将有限仿真覆盖率称作确定性安全保证。

最新结果：平面 box 基线在 9 次 pilot 中均于 1.36 秒因外包络超域停止。已保留全部失败记录，下一步先补齐非线性 zonotope 基线。详见 [08 G1 实现与发现](docs/research/08_g1_implementation_and_findings.md)。

### 文档导航（建议按顺序阅读）

| 文件 | 解决的问题 |
|---|---|
| [00 研究总纲与验收](docs/research/00_research_contract.md) | 研究问题、创新边界、交付物、继续/终止条件 |
| [01 模型与误差界](docs/research/01_model_and_bounds.md) | 坐标、单位、连续/离散方程、Jacobian、网络、残差包络 |
| [02 集员滤波与训练算法](docs/research/02_filter_and_training.md) | 区间与 zonotope 递推、测量修正、A/B/C/D 训练、伪代码 |
| [03 输出反馈 MPC 与证明义务](docs/research/03_mpc_and_proof_obligations.md) | 误差耦合、约束收紧、可行性、安全候选验证、待证定理 |
| [04 验证协议](docs/research/04_validation_protocol.md) | 工具、数据划分、实验矩阵、统计、时延与失败分类 |
| [05 后续执行路线](docs/research/05_execution_roadmap.md) | 模块接口、阶段任务、时间预算、模块验收与论文推进 |
| [06 文献与工具依据](docs/research/06_sources_and_tools.md) | 最近邻文献、证据等级、工具能力边界与复现依据 |
| [07 本次交付核查](docs/research/07_delivery_audit.md) | 实际执行了什么、没有执行什么、审查结论 |

默认物理参数、归一化、传感器时序和实验种子见 [planar_baseline.json](configs/planar_baseline.json)。其中控制增益与终端证书留空，表示后续需要求解的对象。

### 现在可以运行什么

```bash
python -m venv .venv
# Linux/macOS
source .venv/bin/activate
# Windows PowerShell 使用 .venv\Scripts\Activate.ps1
python -m pip install -r verification/requirements.txt
python verification/run_checks.py --output /tmp/academic_checks.json
```

输出路径可按系统修改。详见 [verification/README.md](verification/README.md)。脚本只核查基础代数和数值实现关系，不能据此宣称完成 SMF、神经训练、MPC 闭环或实机验证。

### G1 原型运行

```bash
python -m unittest discover -s tests -v
python scripts/run_g1.py --output results/my_g1_run
```

依赖沿用上面的 NumPy/SciPy。输出目录须为空；结果带源码、配置和数据哈希。已归档的 [实际结果](results/g1_20260909/summary.json) 与 [科研图](results/g1_20260909/g1_findings.svg) 均为数值 pilot，不是训练或控制性能。

### 后续工作的第一条指令

先按 [08 的后续清单](docs/research/08_g1_implementation_and_findings.md) 实现带余项的非线性 zonotope，并重放同一输入/观测。当前 box 未通过长时可用性门，因此暂不进入神经训练和 MPC。每次提交记录命令、哈希、失败样本与尚未满足的证明假设。

方案版本：2026-09-08；G1 实现更新：2026-09-09。AI 辅助文献分析与推导，作者需复核理论及实验；没有代替作者实施人类阅读确认。仓库原有项目名保留。
