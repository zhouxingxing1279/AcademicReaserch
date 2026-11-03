# Run217 — 跨块历史线性约束与控制相关支持上界（2026-10-31）

## 本轮唯一瓶颈及证据范围

Run216第193拍的两块乘积外包 (p,v)×(phi,omega) 对五拍负速度约束存在严格阻塞，最优合法 u0/u1 后裕度约 -0.0363203688。该结果是**外包集合安全证书不可行**，不是实际无人机不可生存。本轮只解决**如何可靠、低成本地把已知历史推力与已执行力矩转化为跨块四维约束，并用于关键支持方向**；未宣称恢复第193拍控制准入。

## 精确推导（原创推导，基础集合方法非原创）

冻结四状态离散Euler模型：
p_{i+1}=p_i+h v_i, v_{i+1}=v_i+h(-T_i phi_i+r_i),
phi_{i+1}=phi_i+h omega_i, omega_{i+1}=omega_i+(h/J)u_i。
假设 h=J=1/50、历史已施加力矩 u_i 与推力 T_i 已知，|r_i|<=47/25+(243/16000)T_i；在历史位置返包 a 时 y_a=p_a+e_a, |e_a|<=1/50。姿态子系统在本冻结模型中无额外未建模扰动；若存在该扰动，本式必须加大外包半径，不能照搬。

由反向精确动力学：
phi_i=phi_k-(k-i)h omega_k+C_i,
C_i=(h²/J) sum_{j=i}^{k-1}(j-i+1)u_j。

代入位置—速度恒等式，令 w_i=i-a+1，可得对当前四维状态 x_k=(p,v,phi,omega) 的**必要条件**：
|p_k-(k-a)h v_k-A phi_k+B omega_k-(y_a+D)|<=R，
A=h² sum w_i T_i，B=h³ sum w_i(k-i)T_i，
D=h² sum w_i T_i C_i，R=sigma_p+h² sum w_i rmax(T_i)。

这是一条同时耦合位置、速度、姿态、角速度的4D H-strip；它在假设成立时包含所有历史一致真实状态。实现使用反向加权力矩后缀递推，构造成本由 O(n²) 降为 O(n)。与Run215单独使用观测姿态、放松姿态误差不同，本条带用已执行力矩消除历史姿态，**不能用于存在未建模姿态动力学误差的模型**。

给定 Run216 的两个凸H多边形 P=P_pv×P_phiomega 及单条带 |c·x-d|<=R，对方向 q：
h_{P∩strip}(q) = min_{λ∈R} [h_P(q-λc)+λd+|λ|R]
（交集非空时的线性规划强对偶）。右端在λ上为分段线性凸函数；最优值可在0及两块顶点仿射函数的交点处取得。代码以Fraction枚举这些候选点，返回精确有理数支持。对多条带分别计算后取最小值仍为**可靠外支持**，但一般不是所有条带交集的精确支持；未实现完整CZ/4D LP。

## 本地已执行的验证与负面结果

- Python 3.13 / Linux，标准库 Fraction。命令：cd /mnt/data/run217 && python -m unittest -v test_cross_block_history_support && python -m py_compile *.py。**6/6测试通过**，含1条任意力矩无噪声恒等式、14组确定性无噪声历史、1条含测量误差和扰动的包含测试、合成双块耦合严格支持收紧及无关条带/缺失控制日志边界测试。
- 合成相关集合中，独立乘积支持为2，加入跨块条带后支持为1/5，改善9/5。这是**合成算例**，绝不是Run216第193拍恢复。
- 人工构造6个历史位置包、11/6顶点多边形：6条带构造10次中位数约5.28ms；6次单条带对偶合计10次中位数约19.39ms，串行约24.66ms，仍超过20ms周期。这是本机人工负载测量，不是实际第193拍实时性证明；上轮Run216全Backup约99ms，不应与本轮单行对偶混淆。
- GitHub分支上新增源码与测试的Git Blob SHA分别为 ede966c9c328ced7e713a1b377f609b11cbc2ebf / 017f4ff9fdef0ecc2a26b01f03eaa4b561455fd6，与本地通过测试的文件一致。
- **未执行完整仓库checkout集成**：本地容器无法解析github.com，仓库只能通过已连接GitHub接口读写；Run217的 run_tick193() 集成入口已提供，但尚未在真实完整checkout运行，故第193拍控制相关支持改善和是否越过0.0363203688门槛均**未知**。不将合成结果代替实测，不声称main合并前已运行CI。
- 证据工件：verification/check_cross_block_history_support.py、verification/test_cross_block_history_support.py、results/cross_block_history_support_20261031/checks.json。

## 论文阅读与定位

Scott, J. K.; Raimondo, D. M.; Marseglia, G. R.; Braatz, R. D. (2016), *Constrained zonotopes: A new tool for set-based estimation and fault detection*, Automatica 69, 126–136, DOI https://doi.org/10.1016/j.automatica.2016.02.036，作者公开稿 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf。本轮核对作者原稿摘要、书目信息及已有Run216定向阅读记录。其CZ保留约束的思想相关，但本轮实现的是4D H-strip及一条带对偶，不是该论文的CG形式CZ递推，亦不继承其未给出的闭环递归可行性保证。去重87篇不变，不新增全文已读记录。

## 硕士课题评价与唯一下一任务

可行性：精确跨块历史条带与标量对偶支持已实现并通过局部测试；历史信息和控制接口因果。创新性：H-strip、LP对偶与CZ为成熟方法，潜在创新需通过**同信息同预算下控制相关支持与闭环可行域**比较来证明。难度：跨条带联合求解、20ms实时预算、真正Tube MPC与终端不变性均未解决。**Gate A=blocked**，没有全时域安全/稳定性证明或六状态四旋翼验证。

**下一轮唯一优先任务：** 在完整仓库checkout运行 run_tick193()，记录第193拍真实历史的跨块支持收紧及单行裕度是否由负转非负；若仍不足，保留负面结果并优先优化多条带联合对偶与增量更新，不能仅凭单行结果宣称两层Backup恢复。
