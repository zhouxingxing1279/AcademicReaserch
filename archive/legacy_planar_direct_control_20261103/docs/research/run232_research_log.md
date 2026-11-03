# Run232 — 中央桥14拍全控制量词速度分叉排除（2026-10-31）

**远端main基准：** 0f05bf4273be2f00b5731e3a371a1500f7177236。**本轮唯一瓶颈：** Run228把中央桥扩大至 |v|≤0.05 m/s 后，原先的单拍反例不再成立；Run229虽认证两拍分叉DAG，但仍无闭合终端循环。本轮用任意连续因果控制下的严格多拍对抗证书，检验三模式桥是否值得继续扩展，避免把有限控制菜单未认证当成数学反证。

## 冻结模型与命题

沿用 verification/check_four_state_bridge_graph.py 的冻结Euler四状态模型 (p,v,phi,omega)：h=1/50 s，p+=p+h*v，v+=v+h*(-T*sin(phi)+r)，phi+=phi+h*omega，omega+=omega+h*tau/I；I=1/50，T∈[981/200,2943/200]，|tau|≤2/25，|r|≤R(T)=47/25+(243/16000)T。保留全部硬约束。

考察Run228三模式候选：中央桥包含原点、|phi|≤0.02、|v|≤b；正/负倾角模式分别要求 phi≥0.15 和 phi≤-0.15。结论也适用于所有其他单元均排除 |phi|<0.15 的更一般并集。

**严格命题（仅针对该候选族）：** 从 x0=(0,0,0,0) 出发，对任意全状态因果控制序列 T_k,tau_k，合法对抗扰动策略 r_k=+R(T_k)（在每次控制选择后）使

v_14 ≥ 7744536014241741013/19073486328125000000 = 0.406036729783477... m/s，

而对所有控制都有 |phi_14|≤91/625=0.1456<0.15 rad。因此只要 b<0.406036729783477...，第14拍要么已提前离开候选终端集合，要么仍处于小倾角区域而速度超过中央桥上界；该包含原点的三模式候选严格**不是鲁棒受控不变集**。负向扰动 r_k=-R(T_k) 得到对称的负速度界。此为真正可实现的对抗扰动策略，而非不可达区间外包点。

**推导：** 从 phi0=omega0=0、|tau|≤tau_max 可得 |phi_k|≤alpha_k=h²(tau_max/I)k(k-1)/2。对k≤14有 alpha_k≤0.1456<0.45，正弦严格Taylor上界 s5(alpha)=alpha-alpha³/6+alpha⁵/120。选择正向极端残差后，逐拍对任意合法T成立

v_(k+1)-v_k ≥ h*[R0 + min(Tmin*(RT-s5(alpha_k)), Tmax*(RT-s5(alpha_k)))]。

因为关于T仿射，最小值在端点。Python Fraction精确累加14拍得到上述分数；前14拍加速度下界均为正。镜像扰动和控制对称性给出负向结论。对抗残差属于冻结模型允许的不确定性，**不意味着真实飞行会持续遇到极端气动扰动**。

**严格失败时刻：** b=0.03时第1拍；b=0.05时第2拍；b=0.40时第13拍。b=0.41在本14拍证书下**不确定**，不是可行性或RCI证明。证明只排除小倾角由一个限速桥覆盖的候选，不排除更多小倾角单元、位置—速度相关非凸集合或一般四状态RCI。

## 文献与适用边界

2026-10-31定向重读Yinan Li、Jun Liu (2018), *Invariance Control Synthesis for Switched Nonlinear Systems: An Interval Analysis Approach*, IEEE Transactions on Automatic Control 63(7):2206–2211, DOI https://doi.org/10.1109/TAC.2017.2760106，作者原文 https://www.math.uwaterloo.ca/~j49liu/papers/2018/li2018invariance.pdf ，§II–III Definition 1、Propositions 2–3、Definition 3、Theorem 1前提。该文用有限模式、区间前驱与分区控制合成不变内近似；其有限终止/完备性需要正鲁棒裕度，且并未覆盖本项目连续推力及控制后选择的独立残差。**本轮证书独立推导**。已读去重数维持90篇，未把复核冒充新读。

## 实现、测试与科研判断

新增验证器 verification/check_four_state_bridge_multistep_obstruction.py、8项测试 verification/test_four_state_bridge_multistep_obstruction.py、完整checkout CI工作流 .github/workflows/run232-bridge-multistep-obstruction.yml、精确结果 results/bridge_multistep_obstruction_20261031/certificate.json。复现命令：

    PYTHONPATH=verification python -m unittest -v verification.test_four_state_bridge_multistep_obstruction
    PYTHONPATH=verification python verification/check_four_state_bridge_multistep_obstruction.py --root . --output /tmp/run232_summary.json
    python -m py_compile verification/check_four_state_bridge_multistep_obstruction.py verification/test_four_state_bridge_multistep_obstruction.py

本地Python 3.13.5隔离公式镜像：7项通过、1项完整checkout配置测试跳过；精确Fraction断言、语法编译与JSON生成通过。完整仓库CI必须实际运行后再记录结果；不预先宣称成功。尚未执行全仓库历史回归、20ms最坏执行时间认证或新增四状态滚动闭环仿真。

**Gate A=blocked。** 仅二维姿态SMF+MPC在Run221限定假设下有递归可行性；四状态非空终端RCI、输出反馈Tube MPC递归可行、稳定性和六状态安全仍未证明。可行性：特定单桥方案被严格排除，但一般方案未知；创新性：单项剪枝不足以构成硕士贡献；难度：高。不能把该反例推广为全局不可控。

**下一轮唯一优先任务：** 用本轮b≥0.4060367...的必要条件筛除过窄单桥，允许多个小倾角位置—速度相关单元，寻找一个经严格区间覆盖认证的非空闭合控制循环；若仍不能闭合，评估缩小课题保证对象。


## GitHub Actions与main合并落地核验（2026-11-01 UTC）

研究PR #33 https://github.com/zhouxingxing1279/AcademicReaserch/pull/33 以非强制Squash安全合并；合并前确认head为 718d70d1728e9dfefc2c01233223a46ad5eda88a、main基准 0f05bf4273be2f00b5731e3a371a1500f7177236、ahead=8、behind=0、mergeable=true。合并生成main SHA 8236ccebd8eeb99fb82fcb09f8c9aa8cfb3f91f6，重新读取远端main及新增源码、测试、检查点、论文日志与结果文件的Git Blob，均确认落地。

完整checkout PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41264059008 和代码合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41264106302 均为**success**；Python 3.13.17执行Run224–232聚焦测试 **61/61通过，无跳过**，真实配置合同、源码编译、Fraction精确证书、归档certificate.json比对及Actions工件上传均成功。**没有执行全仓库历史回归**；没有四状态终端RCI、完整输出反馈SMF+MPC递归可行性、稳定性、六状态安全或20ms最坏耗时证明。本节为事后文档记录，不改变数学/代码。
