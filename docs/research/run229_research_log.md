# Run229 — 中央桥双侧速度分叉的严格两拍区间策略图（2026-10-31）

**本轮基准远端main：** `20bf13cdfb1de57ffddacae58ecda5b11ded69cb`。承接Run228的0/9固定菜单认证结果，唯一瓶颈是取得可复核的非空鲁棒后继边，并明确区间图不能自动等同终端RCI。

## 模型、构造及数学保证

沿用Run224/228冻结四状态全状态Euler系统 `(p,v,phi,omega)`，`h=1/50`、`Tmin=981/200` N、`tau=0`，每拍独立 `|r|<=47/25+(243/16000)T`。所有状态/输入/正弦Taylor界与Run228完全一致。这里是**全状态、固定输入、有限时域**验证，不是SMF或MPC闭环。

选取严格内域种子闭盒：
`|p|<=1/1000, |v|<=1/200, |phi|<=1/1000, |omega|<=1/100`。
使用Run228的 `Fraction` 外向区间后继 `S1=Outer(seed,Tmin,0)`，在速度零点拆成 `B1- = S1∩{v<=0}`、`B1+ = S1∩{v>=0}`，再计算 `B2±=Outer(B1±,Tmin,0)`。每个节点严格位于安全盒内，且有三个经逐轴端点/中点并集覆盖算法认证的后继关系：

1. `Outer(seed)⊆B1-∪B1+`；
2. `Outer(B1-)⊆B2-`；
3. `Outer(B1+)⊆B2+`。

控制 `T=981/200, tau=0` 在每个源单元上固定，故认证量词强于 `forall x exists u forall r` 的单元版本：`exists u forall x in cell forall r`。两拍内的全部可能轨迹均在安全盒内。**图是两层无环DAG，没有终端自环或闭合强连通分量；不能据此宣称无限时域RCI、递归可行性或稳定性。**

精确第一拍速度外包 `[-17675197493460000327/400000000000000000000, +17675197493460000327/400000000000000000000]` m/s，幅值约0.044188。中心点在正/负合法扰动下分别达到 `±6254383/160000000≈±0.039089894` m/s；因此仅保留单个速度符号的下一单元不可能覆盖真实后继。第二拍正/负速度分支的**位置**区间端点不同，显示位置—速度耦合（这是集合外包关联，而非CZ后验）。每条边由构造外包而成立，主要贡献是**验证器的正向回归基线**，不是论文级新方法或非空终端核。

## 文献核验与课题关联

直接重新核对Yinan Li、Jun Liu（2018），*Invariance Control Synthesis for Switched Nonlinear Systems: An Interval Analysis Approach*，*IEEE TAC* 63(7):2206–2211，DOI https://doi.org/10.1109/TAC.2017.2760106，作者公开正式版 https://www.math.uwaterloo.ca/~j49liu/papers/2018/li2018invariance.pdf 。本轮核对Definition 1、Proposition 2（`Omega⊆Pre(Omega)`的无限时域闭合条件）、Assumption 1与Theorem 1的鲁棒裕度条件。论文面向有限切换模式，不直接处理本项目连续推力、控制依赖对抗扰动或部分观测。**与Run227/228同一论文，不重复计数；统一去重已读仍89篇。** 需要后续检查：将有限DAG闭合为循环RCI所需的自适应细分、连续输入搜索与扰动后验信息结构。

## 验证、复现及负面结果

本地Python 3.13隔离镜像（Run228核心常数及外包的独立同公式实现）执行：
`PYTHONPATH=/mnt/data/run229 python -m unittest -v test_four_state_bridge_branching`：6项中5通过、1项因缺完整checkout真实配置跳过；`python -m py_compile`通过；`python check_four_state_bridge_branching.py --output checks.json`成功，三条边及精确有理数均核验。仓库正式复现命令：
`PYTHONPATH=verification python -m unittest -v verification.test_four_state_bridge_branching`；
`PYTHONPATH=verification python verification/check_four_state_bridge_branching.py --root . --output /tmp/run229_checks.json`。
新增GitHub Actions在完整checkout运行Run224–229聚焦回归、真实配置与精确摘要断言，上传完整JSON工件。**PR CI未成功之前不可宣称完整checkout通过。** 无全仓库历史回归、在线周期最坏耗时、SMF集合包含率或MPC控制性能实验。

**Gate A=blocked。** 可行性：两拍全状态有限图正向认证已建立，终端RCI依旧未知；创新性：低，属于验证工具正向对照；研究难度：四状态终端循环与部分观测提升仍高。Run221二维姿态SMF＋MPC的限定证明不受本轮改变。

**下一轮唯一优先任务：** 从本轮有理数DAG出发，寻找并严格认证一个**包含全部扰动分叉的非空闭合循环单元集合**（允许不同控制/细分），或者给出导致无法闭合的可核验必要条件；在此之前不把两拍图接入MPC终端条件。
