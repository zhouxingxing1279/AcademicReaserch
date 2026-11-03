**Run275 PR CI与main安全合并独立复核（2026-11-02 UTC）：** PR #146 https://github.com/zhouxingxing1279/AcademicReaserch/pull/146 以main dbb5e67379ea2dd625b562d9e0ae099ecfecc6d9 为基准；合并前compare ahead=7/behind=0，严格7份预期文件、零删除，mergeable=true，expected head 739544d8af024359a9efcdf94e4e4843174e715b。GitHub Actions https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41525788580 **completed/success**；独立读取Python3.13.17完整checkout job日志确认源码编译、Run275聚焦8/8测试通过、Fraction归档JSON逐字比较及冻结配置交叉核验成功。以expected-head非强制squash合并至main d0c894a5b87af18d020387b47a1a88f1ec05107a；再次读取main SHA、PR merged与源码/测试/JSON/日志/总账/检查点Blob均确认落地。**合并后main push CI未独立确认，全仓库历史回归未执行**。仅观测条件化速度充分门槛，不是完整SMF后验、MPC或信息终端RCI；Gate A=blocked。

---

# Run275 — 两次成功位置测量的第90拍速度后验充分准入条件（2026-11-02）

## 基准与唯一问题
远端main基准SHA：dbb5e67379ea2dd625b562d9e0ae099ecfecc6d9。已读取CURRENT_CHECKPOINT、唯一PAPER_READING_LOG、Run260/272/274日志、configs/planar_baseline.json与背景任务PR #145。Run274已认证冻结四状态模型的第60–90拍零力矩30拍有限安全，且给出第90拍速度绝对上界的第三15拍充分准入门槛 G=187678479/80000000=2.3459809875 m/s。**本轮唯一问题：怎样根据真实成功位置读数为44种合法丢包模式计算后验速度充分准入条件？** 不假设所有读数都通过。

## 数学模型和证明
冻结四状态离散Euler x=(p,v,phi,omega)，动力学 p[k+1]=p[k]+h*v[k]，v[k+1]=v[k]+h*(-T*sin(phi[k])+r[k])，phi[k+1]=phi[k]+h*omega[k]，omega[k+1]=omega[k]+h*tau[k]/J。h=J=1/50，T=981/100，|r|<=R=3246383/1600000。共同控制tau=0；第60拍可靠姿态外包 |phi60|<=1/125、|omega60|<=1/100。因此对60<=k<90，依据全局 |sin(phi)|<=|phi|，有 |a[k]|<=A[k]=R+T*(1/125+(k-60)*h/100)。

第60拍位置成功，65/70/75/80/85/90每5拍机会、禁止连续MMM。成功读数 y_k=p_k+n_k，|n_k|<=eps=1/50。令a<b为第90拍之前最后两次成功位置测量的拍号（包含第60拍），n=b-a，j=90-b。所有44个模式均满足n属于{5,10,15}、j属于{0,5,10}。

Euler递推精确消元（a[k]在下式表示横向加速度而非拍号）：
- v_b=(p_b-p_a)/(n*h)+(h/n)*sum_{k=a}^{b-1}(k-a+1)*a[k]。
- v90=v_b+h*sum_{k=b}^{89}a[k]。
- B(a,b)=2*eps/(n*h)+(h/n)*sum_{k=a}^{b-1}(k-a+1)*A[k]+h*sum_{k=b}^{89}A[k]。
- 对每条与读数一致的真实轨迹，|v90|<=|y_b-y_a|/(n*h)+B(a,b)。
- D(a,b)=n*h*(G-B(a,b))。若 |y_b-y_a|<=D(a,b)，则所有一致真值满足|v90|<=G。

这是**严格观测条件化速度投影充分证书**；没有计算完整SMF/CZ后验，D不是必要条件，也不证明终端信息RCI。角度量测虽有噪，证明仅依赖第60拍已认证的可靠角度盒。

## 全44模式Fraction结果与负面见证
精确枚举44种禁止MMM的6机会字符串。九类(n,j)计数：(5,0)=13，(5,5)=7，(5,10)=4，(10,0)=7，(10,5)=4，(10,10)=2，(15,0)=4，(15,5)=2，(15,10)=1。注意D还依赖a、b的绝对拍号，不能只靠(n,j)确定。44个D均正，最小138634543/1000000000=0.138634543m，最大2241376601/4000000000=0.56034415025m。

**仅外包成员反例，非Run260真实后验反例：** 第60拍取SMM可靠无条件外包内状态(p,v,phi,omega)=(0,1.5,0,0)，以后30拍tau=0、r=+R。真值第90拍v=21739149/8000000=2.717393625m/s>G，p=1002435321/800000000=1.25304415125m，整个30拍满足四状态硬盒。合法模式MMSMMS（75、90成功）、两次零噪声读数差=287130639/400000000=0.7178265975m，大于该模式D=0.56034415025m，因此门槛拒绝。此第60拍状态仅认证在SMM外包盒内；**没有证明它属于Run260此前固定零读数的精确后验**，不得升级为实际历史反例。外包不足以自动认证所有后验满足G。

## 真实文献阅读
Alex Reis de Souza, Denis Efimov, Tarek Raïssi (2022), Robust output feedback model predictive control of time-delayed systems using interval observers, International Journal of Robust and Nonlinear Control 32(3):1180–1193，DOI https://doi.org/10.1002/rnc.5874 。2026-11-02分节阅读作者上传全文 https://www.researchgate.net/publication/355700252_Robust_output_feedback_MPC_of_time-delayed_systems_using_interval_observers §2–6、印刷pp.1182–1192；重点Assumptions 1–3、Theorems 1–4、Algorithm 1、QP(23)–(24)与§6实验。网页公式部分字符乱码，未逐式核验全部LMI。论文是**已知固定时滞、每拍有噪输出的通用线性系统**，采用IO状态区间更新、IP预测、QP与终端反馈；Theorem 4依赖初始可行、合作性、终端输入约束及扰动包络嵌套等条件。数值案例2状态、h=10、N=20、100次仿真，作者报告平均求解0.0042±0.0021s、最大样本0.1358s；非四旋翼实飞、非20ms WCET。可复用的是估计包含、预测硬约束与终端回返的分工，不能直接继承该定理。

## 工件、测试、证据等级
新增verification/check_run275_two_packet_velocity_gate.py、verification/test_run275_two_packet_velocity_gate.py、results/run275_two_packet_velocity_gate_20261102/checks.json、.github/workflows/run275-two-packet-velocity-gate.yml。本地Linux Python3执行：
- cd /mnt/data/run275 && python -m unittest -v test_run275_two_packet_velocity_gate.py：8/8通过。
- python -m py_compile check_run275_two_packet_velocity_gate.py test_run275_two_packet_velocity_gate.py：通过。
- python check_run275_two_packet_velocity_gate.py --output checks.json：生成Fraction证书。

测试涵盖Euler恒等式、44模式、正门槛、3组精确逐拍扰动轨迹与所有模式有噪读数包含、外包负面见证、JSON一致性。容器无法解析github.com，PR完整checkout与CI必须实际运行后另行复核；本地测试不是数学证明。可行性：充分门槛低成本可计算；创新性：Euler消元不是新算法；难度：真实全观测纤维与终端信息RCI仍中高。没有新MPC求解器、完整SMF/CZ递推、终端信息不变集、无限递归可行/稳定、六状态物理安全或20ms WCET。**Gate A=blocked。**

## 下一轮唯一优先任务
从Run260第60拍真实可行历史与Run274完整可靠外包出发，对44个模式全部非空有噪读数后验核验D准入是否普遍成立；失败时给出真正属于Run260精确后验的成员见证，并尝试观测条件化非零力矩安全反馈。不要把外包成员反例当成实际后验反例。
