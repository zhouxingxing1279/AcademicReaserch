# 背景第12轮：逐拍区间观测器在位置失测模式下的结构性障碍（2026-11-02 05:36 UTC）

## 远端基准、任务边界
- 研究起点：远端 main `0ee5d493afb463e3bf97da7b958185e1df2c500a`；已读取 `docs/research/CURRENT_CHECKPOINT.md`、`docs/literature/PAPER_READING_LOG.md`、`docs/research/model_selection/MODEL_SELECTION_EVIDENCE.md`、Run258日志和背景第11轮日志；检索近期研究分支及Run258 PR #97/#98。
- 主任务Run258在固定第30拍历史下严格认证第40拍success速度投影宽度上界0.857482532595 m/s；MM分支3.5256474675 m/s；第45拍强制success尚未递推。该结果是历史两点运动学外包，非完整CZ/信息终端核。主任务负责后验递推和控制代码；本轮只增加文献和模型必要条件，不修改验证脚本、MPC或检查点。

## 实际阅读论文（新增去重文献一篇）
- **真实题名**：*Robust Output Feedback MPC: An Interval-Observer Approach*
- **作者**：Alex Reis de Souza, Denis Efimov, Tarek Raïssi, Xubin Ping。
- **发表**：59th IEEE Conference on Decision and Control (CDC 2020), pp.2529–2534；DOI https://doi.org/10.1109/CDC42340.2020.9304070 ；原始公开作者上传全文 https://www.researchgate.net/publication/343994166_Robust_Output_Feedback_MPC_An_Interval-Observer_Approach ；DBLP https://dblp.org/rec/conf/cdc/SouzaERP20.html 。**注意**：与 de Souza、Efimov、Raïssi 2022 *IEEE TAC* 的LPV论文 DOI 10.1109/TAC.2021.3099449 是不同文献，不混用定理或作者。
- **实际阅读/状态**：2026-11-02，作者上传的可解析公开全文§II–V（问题式(1)、Assumptions 1–5、Theorems 1–3、Propositions 1–2、式(5)–(16)和数值例）；按原文版面约pp.2–6，未下载/逐页核对IEEE出版PDF。论文Theorem 3原文明确省略证明，不能把本轮分节阅读说成独立复现其证明。
- **实际系统与量测**：一般离散LTI `x+=Ax+Bu+w, y=Cx+v`，过程/量测噪声及初始状态均区间有界；固定已知C，每个采样步都有输出注入。§V为连续搅拌釜反应器CSTR**两状态**`(C_s,T)`，**单输入**冷却流温度`T_C`，**单输出**反应器温度`T`（C=[0,1]），采样0.25 min，N=10；没有四旋翼姿态/位置/速度、推力力矩或位置丢包自动机。
- **硬约束与算法**：示例`X=[-0.4,0.4]×[-25,25]`、`U=[-15,15]`、`W=[-0.02,0.02]×[-0.4,0.4]`、`V=[-0.1,0.1]`；采用**状态**区间观测器IO(5)与区间预测器IP(7)，中心轨迹二次型MPC(13)–(15)，区间预测包含硬约束及中心终端集；不是参数SMF、CZ、四旋翼Tube MPC或实飞实验。
- **关键定理/假设**：Theorem 1要求`A-LC`逐元素非负且Schur，给每拍有界区间状态包含；Theorem 2通过LMI设计可靠IP；Proposition 1的IO/IP嵌套需额外条件(11)，并非无条件；Assumption 5要求终端反馈对所有指定扰动保持不变且输入可行；Theorem 3在Assumptions 1–5、(11)、常值扰动界等条件下声称递归可行、终端中心ISS及约束满足，原文省略证明。不能只移植`z_center∈X_f`就声称真实状态安全。
- **结论/局限**：文章对CSTR数值例报告较传统Tube MPC低保守性、名义MPC相近复杂度；不是本仓库20ms WCET证据。固定C、逐拍输出、LTI、非负Schur观测误差矩阵和终端不变性条件不满足时不能直接引用其保证。可复用的是“在线IO可靠后验→未来IP→硬约束包含→终端控制不变性”的接口清单；本仓库必须用失测自动机条件化的多拍后验替代逐拍固定C。

## 独立解析：miss时不能使用论文逐拍Schur观测器条件
以下是**本轮独立推导**，非论文定理；只对仓库无阻力、固定悬停T=mg、Euler线性化的名义运动学成立，不能自动推广至非线性残差/气动耦合。
- 四状态顺序`(p_x,v_x,phi,omega)`，`h=1/50`，`g=981/100`：
  `A4=[[1,h,0,0],[0,1,-h*g,0],[0,0,1,h],[0,0,0,1]]`，
  `C_miss4=[[0,0,1,0],[0,0,0,1]]`。
  对**任意**L∈R^(4×2)，`A4-L*C_miss4`的前两列不变，前2×2不变块`[[1,h],[0,1]]`，其特征值1重数至少2，故不可能Schur。即使允许每拍重新选择L，**单独一个miss步**仍不能满足论文Theorem 1的逐拍非负Schur充分条件。
- 六状态顺序`(p_x,p_z,v_x,v_z,phi,omega)`，名义Euler悬停线性化`A6=I`，另有`A[px,vx]=h`, `A[pz,vz]=h`, `A[vx,phi]=-h*g`, `A[phi,omega]=h`；miss只测`(phi,omega)`。对任意L∈R^(6×2)，`A6-L*C_miss6`保留四维`(p_x,p_z,v_x,v_z)`不变子空间的单位特征值（代数重数至少4）。这与实际T/τ的双输入权限、推力/高度耦合需要单独认证并不矛盾。
- success时测位置及姿态/角速：四状态`C_s4`测`(p_x,phi,omega)`；六状态`C_s6`测`(p_x,p_z,phi,omega)`。理想无噪名义系统的`rank([C_s;C_s A^n])`在`n=5,10,15`时分别等于4/6，位置对初始速度的系数`n*h=0.1,0.2,0.3`。这是**跨时刻线性可观测性**，不是有噪/有扰条件下的精确速度恢复、收缩速率或终端安全证明。
- 可复核交互式命令：Python 3.13.5、SymPy 1.14.0；`h=Rational(1,50);g=Rational(981,100)`，分别构造上述A/C及任意符号L；`factor((A-L*Cmiss).charpoly().as_expr())`含`(lambda-1)**2`（4状态）或`(lambda-1)**4`（6状态）；`Matrix.vstack(Cs,Cs*A**n).rank()`对n=5,10,15分别为4/6。全部断言通过。本轮未运行控制回归，也未生成新的验证脚本。
- **精确解释**：这是“不能直接移植固定C逐拍Schur观测器定理”的结构性障碍，**不是**证明切换观测器的多拍乘积不稳定、真实SMF/CZ不可收缩或四旋翼无安全控制。Run258的success延迟锚点正是多拍恢复的正向证据。

## 模型选择、创新边界与下一轮唯一问题
- 2状态姿态：低风险局部备选，无位置/高度安全；4状态：有限安全闭环基线，固定T非零phi存在垂向漂移；**6状态平面T/τ：条件性物理首选**，需覆盖垂向推力与横向高相对阶控制；10/12状态：不因维数高而优先；分层：必须证明虚拟输入到物理T/τ的内环误差与饱和合同。
- 可行性：成功包的跨时刻位置—速度关联有严格有限证据，但miss不满足逐拍Schur模板；创新空间在**有噪间歇量测＋可递推关联SMF/CZ＋共享物理输入的终端信息安全**，不是“首次将区间观测器和MPC结合”。硕士难度中高至高；Gate A仍blocked。
- **唯一下一轮问题**：在主任务Run258→后续第45拍强制success的全部非空分支上，核对能否构造可移位的15拍失测自动机条件化可靠误差管束；必须给出可检查的测量模式、噪声/扰动界、集合复杂度和共享输入合同，不能沿用本文每拍固定C的Schur假设。
