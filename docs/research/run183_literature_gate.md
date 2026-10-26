# Run183 文献准入卡：Houska 竖直强基线适配

日期：2026-10-26。实际续接 `research/run182-finite-cell-cover-gate` 的远端等价树；远端
Run182提交为 `1685b980`，远端 `main=1c49659`。

| 最近邻 | 本轮实际阅读 | 已解决内容 | 对本轮的约束 |
|---|---|---|---|
| Houska, *Intrinsic Separation Principles*, 2023/Automatica 2026，[全文](https://arxiv.org/pdf/2307.04146) | **全文定向精读 §4.2、§5.5、§6.1--6.7、式(24)--(31)、Theorem 3证明** | 固定线性 `A,B,C`、固定多面体 `W,V` 下，用 configuration-constrained information polytopes、extreme-set controls 与式(29)综合 invariant terminal ensemble；式(24)说明其终端含义。 | 当前 `W(T)` 与 packet-dependent measurement 不能无说明直接代入。information ensemble、极端集合控制及终端用法均不是创新。 |
| Villanueva--Müller--Houska, *Configuration-Constrained Tube MPC*, 2022，[全文](https://arxiv.org/pdf/2208.12554) | **阅读全文 pp.1--9：摘要、Introduction、§2.1--2.3、§3.1--3.4** | 固定 facet template、configuration cone、vertex maps 和 vertex controls；以可表示tube/policy类包含定义严格保守性比较。 | `Y/G/Lambda`几何是现成工具；本轮未选择模板，也未取得任何同预算优势。 |
| Dey--Bhasin, *Output Feedback MPC with Adaptive Tubes*, 2026, arXiv:2605.23661 | **本轮仅核查题名、摘要与问题陈述；未精读证明** | 摘要声明在线估计集合驱动tube几何、约束收紧、终端成分和递归可行性。 | 未读证明前不据此判断本项目首次性；本轮只把它保留为后续同条件比较线索。 |

## 严格差异、强基线和推翻条件

原项目竖直误差满足实际推力相关 residual；Houska 式(29)要求固定 `W`。因此本轮选择可靠但
保守的强基线适配：以真实竖直 tracking error `e_z=(e_pz,e_vz)` 为状态，把 residual 在完整
执行器推力区间上取最大包络；success边使用位置strip测量，miss边使用identity learning
operator；15 modes和17 edges原样保留，mode 4/9 的未知success/miss分叉复用同一当前控制。

最强同条件比较对象是这个固定包络、同传感信息、同硬状态/输入约束的edge-indexed Houska
ensemble，而不是Run180/181局部cells。若全域包络不能从冻结配置精确推出、miss被错误赋予
测量、或分叉后允许另选当前控制，则适配合同失败；若合同通过，也只准许下一步选择模板和求
式(29)图扩展，不得宣称terminal invariance。

## 准入判断

**通过“精确适配合同与可执行门槛”；不通过“本轮已经复现 invariant terminal ensemble”。**
该合同把下一步的未知量缩到 `Y/G/Lambda`、`Z/H/Omega`、每个极端信息集控制和逐边successor
inclusion。它直接推进强基线可实现性，但本身只是已有理论的项目化接口，不是论文创新。
