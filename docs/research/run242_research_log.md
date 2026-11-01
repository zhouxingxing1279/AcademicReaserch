# Run242 — 重复Run241观测脉冲的严格局部不稳定性审计（2026-11-01）

**基准远端main：** 475cbf3598286ce4d57068dd876191ad88329684。**唯一瓶颈：** Run241只认证一次成功观测后的15拍有限安全及微小收益；直接重复是否能成为递归输出反馈终端备份，必须先检查必要的无噪无扰局部稳定性。

## 1. 数学结果（独立项目证明）

冻结四状态Euler x=(p,v,phi,omega)，h=1/50s，J=1/50，T=981/100N。Run241脉冲为tau_j=(2/3)y s_j，s=[+1×3,-1×6,+1×3,0×3]。每宏周期先用零力矩n∈{5,10,15}拍，收到成功位置包；在**允许的特例**测量噪声=0、外扰=0下，y=p_n。执行15拍脉冲后phi、omega严格归零；下周期从零姿态开始。其余中途收到的包被本候选固定策略忽略，因此该测试仅针对“原样重复固定宏周期”，不是任意可切换因果策略。

以Run241的精确Euler角响应c_j计算alpha=hTΣc_j=8829/62500=0.141264，beta=h²TΣ(14-j)c_j=26487/1250000=0.0211896。令L=15h=0.3，n拍无力矩段为位置速度剪切矩阵P_n=[[1,nh],[0,1]]。脉冲非线性映射在悬停原点的Jacobian为B=[[1-beta,L],[-alpha,1]]，完整宏周期为M_n=B P_n：

M_n=[[1-beta,(1-beta)nh+L],[-alpha,1-alpha nh]]。

严格Fraction验证对三个n均有det(M_n)=1-beta+L alpha=1276487/1250000=1.0211896>1，且tr(M_n)^2-4det(M_n)<0。两特征值为复共轭，模长平方均为det(M_n)>1，模长约1.01054。实际非线性sin映射C¹且原点为固定点，离散非线性系统间接法据此给出该固定宏周期悬停平衡点**局部不稳定**；这不是有限采样数值猜测。相同的局部不稳定证据覆盖n=5/10/15三个固定宏周期。无扰/无噪是合法特例，因此原样重复Run241脉冲**不能被认证为局部渐近稳定的终端备份律**。

**严格边界：** 局部不稳定不等于“所有有界RCI不存在”；不能推出某个非吸引的有界安全集合不存在，也不能否定加入速度后验、重新设计脉冲或模式切换的输出反馈控制。现有策略没有完成SMF更新→MPC优化→施加控制→再观测的递归闭环，Gate A仍blocked。

## 2. 文献阅读与可复用技术

- **Yang, Liren; Ozay, Necmiye (2021)**, *Safety Control Synthesis for Systems with Missing Measurements*, IFAC-PapersOnLine 54(5):97–102, DOI https://doi.org/10.1016/j.ifacol.2021.08.481 ，作者原文 https://web.eecs.umich.edu/~necmiye/pubs/YangO_adhs21.pdf 。本轮实际核对§3 Problem Statement、Assumption 1和§4.1–4.2因果承诺/字符串自动机；核心结论是有限丢包语言下通过product safety game处理无限时域安全。其成功包无噪且为完整状态，不能直接替代本项目有噪位置SMF；原样重复固定宏周期只是因果策略的一个严格受限子类。
- **Köhler, Johannes; Müller, Matthias A.; Allgöwer, Frank (2021)**, *Robust output feedback model predictive control using online estimation bounds*, arXiv:2105.03427，https://arxiv.org/abs/2105.03427 。本轮实际阅读公开全文的Introduction、§III-C set-membership、§IV输出反馈MPC概述。研究问题为非线性系统有噪输出下的约束保证；方法为在线验证估计误差界与homothetic tube MPC，定理依赖检测性、稳定估计与预测误差界等假设；包含10状态四旋翼案例。局限：论文未直接提供本仓库15拍丢包、冻结非线性残差的现成证书；未来可复用估计误差有效性+预测偏差两类界作为递归MPC合同。该文仓库已有登记，**去重已读91篇不变**。

## 3. 可复核工件与测试

- 源码 verification/check_four_state_repeated_pulse.py；9项测试 verification/test_four_state_repeated_pulse.py；归档 results/four_state_repeated_pulse_20261101/checks.json；CI .github/workflows/run242-repeated-pulse.yml。
- 本地Python3标准库运行 PYTHONPATH=. python -m unittest -v test_four_state_repeated_pulse：8项通过、1项因本地缺完整仓库配置跳过；py_compile与JSON生成成功；独立浮点Euler有限差分仅用于核对实现索引，**不参与严格证明**。完整checkout配置/历史聚焦回归由PR CI再确认，未完成前不声称成功。
- **课题评估：** 正向可行性（一次性有限安全）不变；否定“原脉冲原样重复可稳定悬停”的直接路线；创新性仍待基于后验速度与模式的可证闭环策略，理论难度高。没有六状态安全、20ms最坏时延或MPC递归可行证据。

**下一轮唯一优先任务：** 设计一个利用SMF后验速度中心/区间的因果**阻尼型**恢复律，在无扰/无噪固定宏周期首先取得Schur稳定的精确Jacobian及合法输入裕度，再扩展到全部观测与5/10/15丢包模式的集合包含/递归终端证书。
