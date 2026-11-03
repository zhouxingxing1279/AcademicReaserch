# Run230 — 四状态终端核的25拍位置边界必要条件（2026-10-31）

**基准main：** d3f221144d73142dc2da2b9f31e21c2c30fb46e4。**唯一瓶颈：** Run229的两拍分叉图虽有三条认证边，却没有闭合终端RCI；先利用姿态/角速度控制权限导出全控制量词下可严格排除的终端状态，避免盲目细分错误区域。

## 动力学与严格排除证书

冻结Run224/228四状态Euler模型 \((p,v,\phi,\omega)\)，\(h=1/50\) s，\(p^+=p+hv\)，\(v^+=v+h[-T\sin\phi+r]\)，\(\phi^+=\phi+h\omega\)，\(\omega^+=\omega+h\tau/I\)，\(I=1/50\)，\(T\in[981/200,2943/200]\)，\(|\tau|\le2/25\)，\(|p|\le5\)，\(|\phi|\le9/20\)。逐拍残差合同为 \(|r|\le R(T)=47/25+(243/16000)T\)。

从 \(x_0=(p_0,0,0,0)\) 出发，允许控制器完整观察状态、逐拍因果选择任意合法 \(T_k,\tau_k\)。对手在每拍控制之后选择 \(r_k=+R(T_k)\)。在任何尚未违约的轨迹上，
\[
\phi_k\le b_k=h^2(\tau_{\max}/I)k(k-1)/2.
\]
对于 \(k=0,\ldots,24\)，有 \(b_k\le b_{24}=276/625=0.4416<0.45\)。因此由正弦单调性和严格Taylor上界 \(s_5(b)=b-b^3/6+b^5/120\ge\sin b\)，
\[
v_{k+1}-v_k\ge h\left[R_0+\min_{T\in[T_{\min},T_{\max}]}T(R_T-s_5(b_k))\right]=h a_k.
\]
右侧对推力为仿射函数，其最小值在某个端点，且与控制器是否采用状态反馈无关。定义 \(L_{v,0}=L_{p,0}=0\)，\(L_{v,k+1}=L_{v,k}+ha_k\)，\(L_{p,k+1}=L_{p,k}+hL_{v,k}\)。对所有合法因果控制与该合法对抗残差，\(p_k\ge p_0+L_{p,k}\)，或更早已经违反安全约束。

使用Python Fraction精确计算：
\[
L_{p,25}=\frac{98296135986106564467}{762939453125000000000}
\approx0.12883871136\ {\rm m}.
\]
故当 \(p_0>5-L_{p,25}\approx4.87116128864\) 时，最迟25拍严格违反 \(p\le5\)。例如 \(p_0=4.9\) 时 \(p_{25}\ge5.02883871136>5\)。通过 \(r_k=-R(T_k)\) 和符号镜像，\(p_0<-4.87116128864\) 也严格排除。**这是针对 \(v_0=\phi_0=\omega_0=0\) 切片的有限时域、所有因果控制排除证书；不是整个四状态RCI为空，也不是SMF/MPC安全证明。** 该对抗扰动是模型允许的逐拍独立极值，不代表实际风场必然如此。

Run229若尝试用固定零力矩和仅追加位置/速度外包盒构成循环，必须首先满足这一位置边界必要条件；新的证书将用于候选终端图的严格剪枝。没有构造出非空闭合终端循环。

## 论文阅读

新增分节原文阅读：Zexiang Liu、Liren Yang、Necmiye Ozay (2020), *Scalable Computation of Controlled Invariant Sets for Discrete-Time Linear Systems with Input Delays*, American Control Conference (ACC 2020), pp. 4722–4728，DOI https://doi.org/10.23919/ACC45564.2020.9147731，arXiv https://arxiv.org/abs/2003.04953，作者全文 https://web.eecs.umich.edu/~necmiye/pubs/LiuYO_acc20.pdf 。核对§I、§II-A/B、§III及Theorem 1，尤其控制先于不可测扰动的量词、有限步前驱外近似及输入延迟的预测状态变换。其结果是**线性纯输入延迟系统**的最大RCI构造；本项目是非线性姿态积分链与控制依赖残差，不能直接引用其Theorem 1证明本项目不变性。统一论文日志原去重89篇，本轮新增分节阅读1篇为90篇；非全文精读。

## 验证与复现

新增：verification/check_four_state_position_guard.py；verification/test_four_state_position_guard.py；results/position_guard_20261031/summary.json；.github/workflows/run230-position-guard.yml。本地Python标准库Fraction测试：6项中5通过、1项因无完整仓库配置跳过；py_compile与完整25行有理数JSON生成通过。仓库复现命令：

- PYTHONPATH=verification python -m unittest -v verification.test_four_state_position_guard
- PYTHONPATH=verification python verification/check_four_state_position_guard.py --root . --output /tmp/run230_checks.json

GitHub Actions将执行Run224–230共46项聚焦测试、真实配置检查及有理数归档断言；**只有CI成功后才能宣称完整checkout测试通过**。未执行全仓库历史回归、闭环性能比较或20ms最坏耗时验证。

**Gate A=blocked。** 可行性：增加了四状态终端集合的严格必要剪枝；创新性：低，属模型特定安全必要条件，不是新RCI算法；难度：闭合非空RCI、SMF信息状态与MPC递归可行仍高。二维姿态Run221限定保证未改变。

**下一轮唯一优先任务：** 在排除位置边界静止切片后，使用控制标记、位置—速度—姿态关联的细分单元，寻找**真正非空且所有扰动后继闭合的四状态循环终端图**；若仍无法构造，给出有量词正确性的严格阻塞并据此收缩课题范围。

## 完整checkout验证及main合并记录（2026-10-31/11-01 UTC）

研究PR #29 https://github.com/zhouxingxing1279/AcademicReaserch/pull/29 已通过非强制Squash合并，代码main SHA `3ad53240ed9b57149cf9aa8459cea20dbca72832`。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41255007550 与代码合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41255049647 均为success。GitHub Actions Python 3.13.17完整checkout中Run224–230共**46/46聚焦测试通过，无跳过**，真实配置、语法编译、25拍有理数证书断言及JSON artifact上传成功（artifact ID 13061824630）。已重新读取远端main SHA及源码/测试Blob，与本地已测版本逐字一致。**不是全仓库历史回归；无四状态终端RCI、输出反馈SMF＋MPC递归可行、稳定性、六状态安全或20ms最坏耗时证明。**
