# Run204：15-mode 固定中心盒终端族的精确排除与因果 SMF 反馈闭环探针

日期：2026-10-30。起点 main=b89b376c11b43b547f0f855e3432970e1ec901fc（Run203）。唯一问题：能否将三拍局部准入升级为每个合法模式边的一步受控不变条件？先检验最简单的“每模式一个固定原点对称直积盒”，再运行非零因果反馈闭环，避免把局部安全误写为递归安全。

## 冻结合同

configs/planar_baseline.json 的四状态横向—姿态模型 \((p,v,\phi,\omega)\)，\(h=1/50\)s、\(J=1/50\)kg m²：
\[
p^+=p+h v,\quad v^+=v-hT\phi+hr,\quad
\phi^+=\phi+h\omega,\quad \omega^+=\omega+h\tau/J.
\]
\(T\in[4.905,14.715]\)N，\(|r|\le47/25+(243/16000)T\)，\(|\tau|\le0.08\)N m，原始硬约束 \((|p|,|v|,|\phi|,|\omega|)\le(5,3,0.45,2)\)。当前推力可见、未来任意跳变，位置每5 tick有成功/缺包，最多连续丢两包；姿态和角速度每tick观测。控制先于后继边；不是六状态四旋翼结论。

## 结果A：精确有理的类特定排除定理

令每个模式对应**物理状态**固定原点直积盒
\[
B_i=[-P_i,P_i]\times[-V_i,V_i]\times[-\Phi_i,\Phi_i]\times[-\Omega_i,\Omega_i],
\]
其中半宽均有限、非负。若要求对每条合法边 \(i\to j\) 在任意合法扰动下由同一个因果控制实现一步包含，则五边合法环
0→1(miss)→2(miss)→3(miss)→4(miss)→0(success)
已给出矛盾。

对每条边取盒内角点 \(p=P_i,v=V_i,\phi=\omega=0\)。因为 \(p^+=p+h v\) 不依赖当前力矩、推力或扰动，必要条件为 \(P_j\ge P_i+hV_i\)。沿五边求和得到 \(0\ge h(V_0+\cdots+V_4)\)，故所有 \(V_i=0\)。但每个盒含零状态，取 \(T=T_{\min},r=d(T_{\min})>0\)，则 \(v^+=h d(T_{\min})=6254383/160000000>0\)，与后继 \(V_j=0\) 矛盾。此论证甚至允许完整状态反馈，因此也排除使用更少信息的输出反馈在这一盒族上成功。

**严格范围：** 排除固定中心、独立坐标、按模式索引的物理状态盒；不排除平移/相关/斜面集合、依测量值移动的后验集合、一般RCI或SMF–MPC。测量成功不能瞬间重置真实物理位置。示例候选盒 \(P=1,V=1/2,\Phi=1/10,\Omega=1/5\) 在 \(x=(1,1/2,0,0)\) 时，即便非零反馈力矩 \(\tau=1/25\)N m，\(T=T_{\min},r=0\)，也有 \(p^+=101/100>1\)；这只违反**候选盒**，不违反原始 \(|p|\le5\)。

力矩相对阶由精确脉冲证明：首次影响 \(\omega_{k+1},\phi_{k+2},v_{k+3},p_{k+4}\)。当前力矩无法在一拍内修复位置—速度角点。

## 结果B：四状态因果SMF + 非零反馈探针（非MPC）

verification/check_four_state_feedback_smf_probe.py 实现：真实状态推进→有界扰动区间SMF预测→每tick姿态/角速率测量更新→位置在5、10 tick缺包、15 tick成功并重复→利用两次成功位置包的加速度消元式收紧速度→取后验中点反馈。控制律
\[
\tau=\operatorname{sat}_{[-0.08,0.08]}(0.8\hat p+1.08\hat v-2.95\hat\phi-0.4\hat\omega).
\]
增益为近似名义LQR启发式，**不是MPC、鲁棒最优控制或安全过滤器**。比较永久零力矩、SMF中点反馈及不可实际实施的真实全状态反馈（信息上界基线）。150 tick、零初态、合法零测量噪声，残差取幅值上界，推力高端点常值或端点切换。

| 扰动/推力模式 | 零力矩首次原始硬约束违例 | SMF中点非零反馈首次违例 | 真值全状态反馈首次违例 |
|---|---|---|---|
| 高推力、最大正扰动 | tick72：速度 | tick114：角速度 | 150 tick内未观察到 |
| 高推力、每15 tick反转扰动 | 150 tick内未观察到 | 150 tick内未观察到 | tick88：角速度 |
| 每10 tick切换推力、最大正扰动 | tick74：速度 | tick125：姿态角 | 150 tick内未观察到 |

9条轨迹×150 tick，浮点容差下SMF包含真实状态1350/1350次；SMF反馈每条135/150 tick使用非零力矩且满足输入幅值约束。**数值探针不构成普遍安全证书**：浮点区间没有向外舍入、只检查3个确定性模式、测量噪声为零；全状态反馈在交变扰动下也失败，不能将个别成功轨迹当作鲁棒控制证明。

## 文献复核（原84篇内，不重复计数）

1. Athanasopoulos、Smpoukis、Jungers (2017)，Invariance in Constrained Switching，arXiv https://arxiv.org/abs/1702.00598；相关期刊版本 Invariant Sets Analysis for Constrained Switching Systems，DOI https://doi.org/10.1109/LCSYS.2017.2714840。本轮复核摘要、图约束不变多集合的定位；不把文献的算法/定理直接移植至带因果控制和观测更新的系统。
2. Lorenzetti、Pavone (2020)，A Simple and Efficient Tube-based Robust Output Feedback Model Predictive Control Scheme，ECC，DOI https://doi.org/10.23919/ECC51009.2020.9143979。复核输出反馈管束与终端不变条件的角色；本轮反证不能替代正向终端证明。
3. Ping、Yao、Ding、Li (2022)，Tube-Based Output Feedback Robust MPC for LPV Systems With Scaled Terminal Constraint Sets，IEEE Transactions on Cybernetics 52(8):7563–7576，DOI https://doi.org/10.1109/TCYB.2020.3041334。本轮仅核对正式摘要，未重读全文定理；其LPV输出反馈、离线误差集合和scaled terminal是直接比较基线。

## 可复现性、证据与课题收敛

运行：
- PYTHONPATH=verification python -m unittest verification.test_mode_indexed_box_terminal_obstruction -v
- PYTHONPATH=verification python -m unittest verification.test_four_state_feedback_smf_probe -v
- python verification/check_mode_indexed_box_terminal_obstruction.py --output results/mode_indexed_box_terminal_obstruction_20261030/checks.json
- python verification/check_four_state_feedback_smf_probe.py --output /tmp/run204_feedback_full.json

本地Python 3.13、仓库关键配置字段镜像：**17/17新增测试通过**，两个生成器运行成功。未获取完整仓库checkout，未执行历史全量回归或GitHub CI；远端应重新运行。归档精确有理证明和数值探针紧凑摘要。A是**类特定精确反证**，B是**数值确定性闭环探针**；两者均不证明一般SMF–MPC不可行。

**Gate A仍blocked。下一唯一任务：** 在移动中心、保留相关性的SMF信息状态上构建有限时域因果backup/安全过滤器；对位置包成功/缺包和未来推力任意跳变作统一准入，先寻找至少一条真实可实施的全时域安全闭环，再讨论终端/递归证书。
