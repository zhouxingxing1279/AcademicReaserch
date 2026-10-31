# Run218 — 第193拍跨块历史条带的支持饱和反例（2026-10-31）

## 本轮唯一问题

Run217构造6条4D历史一致必要条带并实现单条带精确对偶，但没有执行第193拍集成。本轮检验：这些条带是否能消除Run216第193拍五步负速度硬约束的严格阻塞（约−0.0363203688）。

## 严格数学结论与证据级别

设Run216当前可靠外包 `P=P_pv × P_phiomega`，第193拍五步负速度支持方向为 `q=(0,-1,2943/2000,2943/50000)`；历史条带 `S_i={x:|c_i^T x-d_i|<=R_i}`，i∈{105,120,135,150,165,180}。若存在 `x*∈argmax_{x∈P} q^T x` 且 `x*∈∩_i S_i`，则由集合包含的双向不等式立即得到

`h_{P∩(∩S_i)}(q) = h_P(q)`。

本轮用 `Fraction` 在11顶点位置—速度多边形和6顶点姿态—角速度多边形的支持极点上找到联合 `x*`，并逐条严格核验 `R_i-|c_i^T x*-d_i|>=0`。六条带的裕度近似为 `[2.7528856067,2.2111642466,1.1394906777,0.3976671303,0.0297030541,0.0395714992]`，均为严格正数。`x*≈(1.3222911057,-2.4955466060,0.2427028632,-0.3818210442)`。**因此这6条带即使被联合精确求解，也不能收紧该关键方向的支持函数，增益精确为0。** 原单行最有利控制裕度保持约 `−0.0363203688`。这是特定外包与特定方向的数学证明，不是完整后验、物理不可生存性或全时域安全结论。

这比“逐条对偶未改善”更强：已经找到同时满足所有6条带的乘积支持极大点，因此针对这6条带再做多约束4D LP也不会改善这一行。**不应继续在完全相同6条带上盲目优化联合求解器。**

## 实际验证及负面结果

- 通过GitHub连接读取远端 `main=39acef9f3792502f1584cd8145a1c79a203027ae`、Run217检查点/日志/源码、Run216、Run214/215/210/208/206依赖。容器DNS不能访问github.com，因此不能完整git clone；通过已核对源码逐式构造本地兼容镜像（`/mnt/data/run218/audit.py`），执行真实参数的192步确定性历史重放。镜像复现Run216原临界行裕度 `−0.03632036879978493`、11/6顶点数、真值及6包位置。
- `python -m unittest -v test_cross_block_saturation`：4项快速测试通过；第5项完整仓库集成测试因缺少完整checkout被明确跳过。`python -m py_compile check_cross_block_saturation.py test_cross_block_saturation.py`通过。
- `python run_mirror_integration.py`：使用兼容镜像给仓库集成入口注入依赖，真实第193拍条带饱和证书通过，6条带支持增益**精确为0**；没有伪称完整仓库测试。
- 兼容镜像重放及证书总耗时约2.89秒，包含192步历史重放，不能作为单周期在线耗时；尚无20ms实时证明。完整仓库历史回归、GitHub CI未执行。
- 结果保存在 `results/cross_block_saturation_20261031/checks.json`；源码和测试为 `verification/check_cross_block_saturation.py`、`verification/test_cross_block_saturation.py`。可在完整仓库执行 `RUN_TICK193_AUDIT=1 PYTHONPATH=verification python -m unittest -v verification.test_cross_block_saturation`，本轮未执行该完整仓库命令。

## 文献阅读（均为已有87篇中的定向核对，不新增已读计数）

1. Scott, Raimondo, Marseglia, Braatz (2016), *Constrained zonotopes: A new tool for set-based estimation and fault detection*, *Automatica* 69:126–136, DOI https://doi.org/10.1016/j.automatica.2016.02.036，作者稿 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf。本轮复核原文第2节集合表示、Definition 3与第3节开头。CZ能够精确执行某些集合运算，但并不意味着额外历史条带必然收紧每个控制相关方向；本轮给出一个明确的零增益见证。
2. Köhler, Müller, Allgöwer (2021), *Robust output feedback model predictive control using online estimation bounds*, arXiv https://arxiv.org/abs/2105.03427，作者公开稿 https://www.ist.uni-stuttgart.de/dokumente/public/Output.pdf。本轮核对摘要、第I节贡献和第II节Assumption 1；其输出反馈Tube MPC的约束与递归可行性保证依赖额外稳定性、估计界及终端条件，本仓库仍未满足。不是全文重读。

## 硕士课题评估及下一轮唯一任务

- **可行性：** 历史一致必要约束与严格支持证书可实现；本轮证伪“只增加现有6条跨块条带即可解除第193拍阻塞”的具体假设。
- **创新性：** 不能把LP对偶、H条带或CZ本身当原创。可能的论文贡献需来自具有控制相关增益的历史相关性保留及同信息同预算比较；本轮负面证据有助于收敛范围。
- **难度：** 全历史噪声/扰动相关性、集合复杂度和20ms实时预算仍高。Gate A=blocked；尚无真正Tube MPC、终端受控不变集、递归可行性、稳定性或六状态安全证明。
- **下一轮唯一优先任务：** 审计该临界极大点是否满足更强的**共享扰动和多位置测量联合历史可行性**（而非重复现有六条独立必要条带），给出可检查的可行/不可行证书；只有在确认能排除它后才值得实现昂贵的全维CZ/LP优化。
