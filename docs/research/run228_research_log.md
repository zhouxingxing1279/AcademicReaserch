# Run228 — 小倾角桥的速度分叉必要条件与有限单元策略图审计（2026-10-31）

**基准远端 main：** `2d25c3736bc987edf2b4b3d53e0dc155e9263810`。本轮唯一瓶颈：Run227要求四状态终端集合穿过 \(|\phi|\le0.02\) 的桥，但尚无桥上后继闭合的可计算证书。

## 冻结模型及新证据

沿用Run224四状态离散Euler：\(x=(p,v,\phi,\omega)\)，\(p^+=p+hv\)，\(v^+=v+h(-T\sin\phi+r)\)，\(\phi^+=\phi+h\omega\)，\(\omega^+=\omega+h\tau/J\)；\(h=1/50\)，\(T\in[981/200,2943/200]\)，\(|\tau|\le2/25\)，\(J=1/50\)，\(|r|\le R(T)=47/25+(243/16000)T\)，每拍独立对抗残差。安全盒 \(|p|\le5, |v|\le3,|\phi|\le0.45,|\omega|\le2\)。这是**全状态反馈**冻结模型，不是输出反馈SMF。

构造三个闭区间单元的候选并集：中央桥 \(|p|\le1, |v|\le b,|\phi|\le0.02,|\omega|\le0.1\)，正模式 \(|p|\le4,0\le v\le3,0.15\le\phi\le0.25,|\omega|\le1\)，负模式为符号镜像。比较 \(b=0.03\) 与 \(b=0.05\)。两种并集均非空且满足安全盒，但**不预设RCI**。

**严格新反例（仅 \(b=0.03\) 候选）：** 中央状态 \(x_0=(0,0,0,0)\) 属于候选。对任意合法 \(T,\tau\)，第一拍 \(\phi^+=0\)，选择合法对抗 \(r=+R(T)\)，则 \(v^+=hR(T)\ge hR(T_{\min})=6254383/160000000=0.03908989375>0.03\)。其后继不能属于任何正负模式（两者排除 \(\phi=0\)），也不属于中央桥。因此该**具体三单元候选**不可能RCI，严格速度缺口 \(1454383/160000000=0.00908989375\)。这是所有连续合法控制的反例，不是菜单扫描结论；不能推广为所有四状态RCI均为空。

**一般必要条件（有前提）：** 若候选包含该中心状态，且其 \(\phi=0\) 截面只允许 \(|v|\le b\)，并且其他单元均排除 \(\phi=0\)，则RCI必须满足 \(b\ge hR(T_{\min})\)。这不是任意桥集合的全局宽度下界，因为其可不包含中心状态。

**可计算算法：** 新增标准库 `Fraction` 的四维区间后继外包、闭盒并集精确覆盖判定（按全部端点与开区间中点的笛卡尔网格检查）、每单元固定输入菜单 \(3T\times3\tau=9\) 的策略图扫描。两种候选的三个单元均未找到经认证的固定输入（0/9）。**这是不完备筛选**：未覆盖的外包点可能不可达，输入菜单也不连续，不能把0/9写成控制不存在的数学证明。\(b=0.05\) 中心反例不成立，RCI状态仍未知。

## 文献与证据级别

本轮直接复核Yinan Li、Jun Liu的2018年正式期刊版 *Invariance Control Synthesis for Switched Nonlinear Systems: An Interval Analysis Approach*, *IEEE Transactions on Automatic Control* 63(7):2206–2211，DOI https://doi.org/10.1109/TAC.2017.2760106，原文 https://www.math.uwaterloo.ca/~j49liu/papers/2018/li2018invariance.pdf 。核对§II–III、Definition 1、Propositions 2–3、Algorithm 2、Assumption 1及Theorem 1附近的有限终止与鲁棒裕度条件。与Run227的2016 arXiv:1608.08683属同一研究工作的不同版本，不重复增加已读论文数，仍89篇。该文是**有限切换模式、无当前对抗扰动量词**的理论；本轮区间图与严格扰动证书均为自行推导，不能直接援引其不变性结论。

## 测试与局限

本地隔离环境执行 `PYTHONPATH=verification python -m unittest -v verification.test_four_state_bridge_graph`：8项中7通过、1项因没有完整checkout的真实配置跳过；`python -m py_compile ...`通过；`PYTHONPATH=verification python verification/check_four_state_bridge_graph.py --output results/terminal_bridge_graph_20261031/checks.json`成功生成确定性完整审计JSON。新增GitHub Actions工作流用于完整checkout配置验证、Run224–228聚焦回归、精确摘要断言及完整JSON artifact。CI未实际完成前不可宣称CI成功。

**Gate A=blocked。** 本轮只有特定三单元候选的严格排除和一个保守区间策略图验证器；无非空四状态RCI、输出反馈SMF＋MPC递归可行、稳定性、六状态安全或20ms最坏时间证明。可行性：桥区需要容纳扰动速度分叉并考虑位置—速度耦合；创新性：主要为方法性验证工件，尚无论文级新颖性；难度：高。

**下一轮唯一优先任务：** 将桥的速度宽度扩大到至少0.03908989375，并引入位置—速度关联的邻接桥单元，在连续输入候选或自适应细分下尝试获得**至少一条经严格区间外包认证的非空单元后继边**；若无则记录导致失败的维度和外包松弛，不盲目宣称终端核为空。

## Run228 GitHub 合并与完整checkout验证补记（2026-10-31）

PR #25 https://github.com/zhouxingxing1279/AcademicReaserch/pull/25 通过非强制Squash安全合并，首个main落地SHA `57f749a884588247b846d251103a2c745f444b6b`；已重新读取main与新增源码/测试Blob确认落地。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41246301443 和合并后main CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41246344516 均为success，Python 3.13.17，完整checkout Run224–228共34/34项聚焦测试通过、真实配置、源码编译、精确摘要断言及JSON artifact上传成功。**未执行全仓库历史回归；未证明四状态RCI、输出反馈MPC递归可行、六状态安全或20ms最坏执行时间。** 本补记及归档摘要为文档/结果补充，不单独触发聚焦CI。
