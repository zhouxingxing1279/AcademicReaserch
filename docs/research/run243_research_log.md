# Run243 — 两包速度SMF与阻尼脉冲固定模式Schur证书（2026-11-01）

**基准远端main：** 8a795a5575bf787313ba23ad299007ee4f7be420。**本轮瓶颈：** Run242证明原位置脉冲原样重复时局部不稳定。本轮检验能否仅由两次成功位置包恢复速度信息并构造因果阻尼控制；不把无扰局部稳定误作鲁棒安全。

## 1. 模型、因果性与精确证明

冻结四状态Euler (p,v,phi,omega)，h=1/50s、J=1/50、固定推力T=981/100N，横向残差r_j∈[-R,R]，R=47/25+(243/16000)T=3246383/1600000 m/s²，成功位置包y=p+eta，|eta|≤1/50m。严格限定初始phi=omega=0且角状态可由已知实际力矩历史精确预测；本轮不处理初始角度未知及带噪角传感器的通用情形。

两次成功位置包相隔N=15+n拍(n=5/10/15)。令已知角轨迹对应加速度a_j=-T sin(phi_j)。当前隐藏速度的可执行中心估计为

vhat_N = (y_N-y_0-h² sum_j (N-1-j)a_j)/(Nh)+h sum_j a_j。

Euler递推给出恒等式：

v_N-vhat_N = (h/N) sum_j (j+1)r_j + (eta_0-eta_N)/(Nh)。

因此所有合法独立残差与位置噪声下的**集员包含**为v_N∈[vhat_N-E_N,vhat_N+E_N]，其中E_N=hR(N+1)/2+2*(1/50)/(Nh)。20、25、30拍间隔的精确半宽分别为84174043/160000000≈0.526088m/s、48602979/80000000≈0.607537m/s、333913619/480000000≈0.695653m/s；在不引入其他先验约束时，该半宽可由合法极端序列达到。这一粗两包估计尚未与Run240的关联CZ历史后验求交。

成功位置包后使用u=(1/2)y+(1/2)vhat（Nm），饱和至±0.08Nm，提前承诺15拍力矩tau_j=u s_j，s=[+1×3,-1×6,+1×3,0×3]，随后零力矩等待n拍。控制仅使用已到达的测量与已知力矩历史；角度和角速度在脉冲结束严格归零。

无噪无扰时vhat=v，原点附近饱和不激活。精确Fraction给出单位力矩响应alpha=26487/125000=0.211896，beta=79461/2500000=0.0317844，宏周期Jacobian：

M_n = [[1-beta/2,(1-beta/2)nh+15h-beta/2],[-alpha/2,1-alpha/2-alpha nh/2]]。

n=5、10、15三种**分别固定**模式的det(M_n)=4549721/5000000=0.9099442<1；Jury判据1-det>0、1-tr+det>0、1+tr+det>0均由精确有理数严格验证。由于sin映射C¹，证明每个固定宏周期在无噪无扰下原点**局部渐近稳定**。尚无任意5/10/15切换的共同Lyapunov证书。原Run241只有位置增益、速度增益为零，det>1，是保留的严格负例。

单个无噪无扰宏周期若前一脉冲末|p|≤0.02m、|v|≤0.1m/s、phi=omega=0，则等待n≤15拍后|u|≤0.075Nm<0.08Nm；中间状态可靠外包为|p|≤0.089536m、|v|≤0.115893m/s、|phi|≤0.0135rad、|omega|≤0.225rad/s。**该盒并未证明自映射，且这些约束上界不包含实际残差/噪声。**

## 2. 可运行闭环、负面结果与证据级别

代码实现两包测量→速度重构→饱和力矩脉冲→Euler真值更新→下一包的75宏周期闭环。首次5拍被动测量用于初始化估计，不读取隐藏速度。初始p=0.01m、v=0.05m/s、phi=omega=0，按5/10/15重复切换；**无噪无扰单条浮点轨迹**最终p≈-0.00303257m、v≈0.00051073m/s，最大|tau|≈0.047333Nm，最大|p|≈0.081887m，速度重构误差<1e-12m/s。切换轨迹不等于切换稳定性证明。

**关键负面结果：** 最短两包速度半宽也达0.526m/s，显著超过上述局部无饱和盒的0.1m/s。对实际允许的残差/位置噪声，尚无法认证不饱和、鲁棒状态约束、递归闭合或稳定。饱和只强制力矩合法，不保证状态安全。六状态、推力调度、MPC优化与20ms最坏时延仍未证明。Gate A=blocked。

## 3. 真实文献复核与课题判断

**Johannes Köhler; Matthias A. Müller; Frank Allgöwer (2021)**，*Robust output feedback model predictive control using online estimation bounds*，arXiv:2105.03427，https://arxiv.org/pdf/2105.03427 。本轮实际阅读§II-A Assumption 1、§III开头对当前/未来估计误差和估计器偏差的要求、§IV-A/B的tube接口以及§V十状态四旋翼数值结果。论文通过在线误差界与homothetic Tube MPC保证满足其假设时的递归可行性；本轮两包速度区间仅满足部分估计包含条件，缺未来预测界和终端移位合同，不能套用其定理。局限为复杂在线集合估计计算成本高、假设不能直接转移到本项目。已在历史论文索引中，去重已读91篇不变；本轮为分节阅读，非全文逐式验证。

**D.Q. Mayne; S.V. Raković; R. Findeisen; F. Allgöwer (2006)**，*Robust output feedback model predictive control of constrained linear systems*，*Automatica* 42(7):1217–1222，DOI https://doi.org/10.1016/j.automatica.2006.03.005 。本轮核验书目及公开摘要，**未阅读全文**。论文以稳定观测器误差RPI、名义tube与约束收紧处理有界扰动线性系统；可复用的是估计误差与控制管束分离的证明合同，不是直接借用线性定理。历史已登记，不重复计数。

**可行性：** 理想量测下得到正向可执行阻尼基线；**创新性：** 两包差分SMF、PD脉冲与Jury均是基础技术，尚不足独立成题；**研究难度：** 全扰动/有噪姿态/任意失测的鲁棒信息状态递归闭合仍高。

## 4. 工件、验证与下一步

验证器verification/check_four_state_posterior_damping.py，13项测试verification/test_four_state_posterior_damping.py，归档results/four_state_posterior_damping_20261101/checks.json，工作流.github/workflows/run243-posterior-damping.yml，唯一论文日志docs/literature/PAPER_READING_LOG.md及docs/research/current_checkpoint.md。

本地Python标准库执行 PYTHONPATH=verification python -m unittest -v verification.test_four_state_posterior_damping：12通过、1项因隔离目录缺真实配置跳过；py_compile与精确证书JSON生成通过。完整checkout、聚焦回归、归档一致性及远端合并需由GitHub CI另行验证，不能预先声称成功。

**下一轮唯一优先任务：** 将两包速度区间与Run240关联CZ后验相交，在实际残差/噪声和任意5/10/15成功模式下检验阻尼控制的共享输入裕度与递归信息状态闭合；若失败，归档严格阻塞证书。

## 5. 完整checkout CI、PR合并及远端main核验（2026-11-01）

研究PR #55 https://github.com/zhouxingxing1279/AcademicReaserch/pull/55 基于main 8a795a5575bf787313ba23ad299007ee4f7be420，合并前ahead=1/behind=0、mergeable_state=clean、head=05ec02cd272df06f225bdf56e1971dbdec6ff6e2。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41315031734 completed/success；Python 3.13.17完整checkout Run224–243聚焦测试**167/167通过，无跳过**（21.872s），真实配置检查、源码编译、精确Fraction、JSON归档（浮点sanity允许1e-10跨平台容差）及artifact上传成功。通过非强制Squash合并至main b59bae34b6765d974df3bfa4047474dacb146f51，再次读取远端main并核对源码Blob b192948685c62136b589c8606cc07b5931d31856、测试Blob 7d80fb34cebfdc04467feb2411f537014ef49f8e、归档Blob 1309833a1389fe5d532a07ca71e7b01a031256e5 与本地实际字节一致。

合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41315122060 completed/success；完整checkout Python 3.13.17 **167/167通过，无跳过**（39.047s），归档校验与工件上传成功。**未执行全仓库历史回归**。本轮严格结论仍仅为已知角轨迹的两包速度包含与无扰固定模式局部Schur；没有鲁棒SMF+MPC递归可行性证明。


## 6. 量测时序量词审计（重要限定，2026-11-01）

**传感器合同纠正：** 配置每5拍有一次位置包机会，至多连续2次丢包，因此**连续实际成功包的最大间隔为15拍**。本轮固定宏周期使用的20/25/30拍，是**两次被本候选策略选中并使用的成功包之间的间隔**；要与原传感器合同相容，其间必有至少一次实际成功包被该策略主动忽略。即使中间存在成功包，也**不能保证**预设第20/25/30拍恰好成功。因此Run243的固定模式Schur证明只适用于满足这些选定包成功条件的**受限合法观测历史**，不是配置允许的所有丢包序列，更不能作为5/10/15最长实际成功间隔下的通用终端律。两包速度包含公式对任意指定正整数N仍成立，但在真实在线控制中应在**每次实际成功包**更新后验并对未知下一个包时刻提前准备因果控制。

此时序量词修正不改变已验证的Fraction代数或无扰仿真，却进一步收紧了可行性声明。**下一轮唯一优先任务不变：** 将Run240关联CZ后验与实际每5拍包机会/最多2次连续缺测的自动机联立，检查每一条success/miss边的共享力矩和终端回返。

