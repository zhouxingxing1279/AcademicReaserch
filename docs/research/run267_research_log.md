**Run267 合并后独立复核（2026-11-02 UTC）：** PR #123 https://github.com/zhouxingxing1279/AcademicReaserch/pull/123 在main `c730828f42c75bba95d730f8af5e75a4c28a62ac` 上7提交ahead、0 behind、仅7个预期文件，mergeable_state=clean。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41463272428 **completed/success**；Python3.13完整checkout聚焦回归 **70/70通过**，源码编译、真实配置、Run260/264归档交叉核验与Fraction JSON逐字比较成功。expected-head `3ae16fe17809150e0952ad3d335814f0b1d04665` 非强制squash合并至main `ea7a5c0075f46d0199306c3af00d5ceffdbff0dd`，重新读取main SHA、PR merged及关键文件Blob核验落地；本地与远端代码/测试/证书blob SHA一致。**合并后main push CI未独立确认、全仓库历史回归未执行。** 必要筛选全盒通过不等于充分安全，Gate A仍blocked。

---

# Run267 — Run260/264 可靠外包的三拍必要守卫筛选与终端非闭合边界（2026-11-02）

## 1. 本轮基准、唯一瓶颈及证据等级

远端main基准：`c730828f42c75bba95d730f8af5e75a4c28a62ac`（2026-11-02 UTC）；读取CURRENT_CHECKPOINT、Run260/263/264/266日志、源代码与归档证书、`configs/planar_baseline.json`、唯一论文总账及模型选型矩阵。背景任务PR #122已在此基准上落地，不覆盖其文件。

唯一问题：Run266三拍必要速度守卫能否排除Run260第60拍任意非空有噪后验的状态？先用已有可靠无条件外包给出**保守、可核验的全盒筛选**，而不是把宽度界冒充绝对状态后验、或把必要条件当充分终端RCI。

## 2. 冻结模型与严格推导

仅四状态定义的离散Euler真值：`p+=h*v, v+=h*(-T*sin(phi)+r), phi+=h*omega, omega+=h*tau/J`，`h=J=1/50, T=981/100, |tau|<=2/25, |r|<=3246383/1600000`，`|v|<=3`。控制先于扰动与未来观测选择。Run266已证明任意三拍鲁棒可生存真值必须满足

`L(phi,omega) <= v <= U(phi,omega)`，其中
`L=-3+3hR+hT[sin(phi)+sin(phi+h*omega)+sin(phi+2h*omega-delta)]`，
`U=3-3hR+hT[sin(phi)+sin(phi+h*omega)+sin(phi+2h*omega+delta)]`，
`delta=h²*tau_max/J=1/625`。

对可靠盒`B=[v-,v+]×[phi-,phi+]×[omega-,omega+]`，所有正弦自变量位于(-1,1)，故`L`、`U`对phi和omega均单调递增。要证明**盒中每一点均满足上述必要守卫**，必须使用`v- >= max_B L`、`v+ <= min_B U`。Run267以`phi+,omega+`求`L`的**严格上界**，以`phi-,omega-`求`U`的**严格下界**，而非使用Run266用于安全剔除的反方向放宽界；七次Maclaurin加`|x|^9/9!`余项全用Fraction运算。这一方向区别是关键：**通过必要条件的证书，不能使用仅适于排除的松弛必要界**。

## 3. 证书结果（外包全盒筛选，不是可行性证明）

| 起点固定历史 | 时刻 | 全盒必要守卫最小严格裕量(m/s) |
| --- | ---: | ---: |
| SMM | 60 | 1.3053923640 |
| MMS | 60 | 1.7802187191 |
| SMM | 75 | 0.6672660434 |
| MMS | 75 | 1.1420923985 |

四个盒均严格通过必要守卫；第60拍的所有合法success/miss、任意有噪且非空后验是Run260对应无条件盒的子集，故**Run266必要守卫无法在这两个固定历史的第60拍后验中筛出违约真值**。该结论不需要未来读数为零，也不表示后验精确形状已知。第75拍来自Run264同样的无条件零力矩外包；它们的速度投影均比第60拍相应外包更宽，故**外包不满足零力矩15拍自包含检查**。注意外包不包含不等于真实可达集不包含，不能据此证明零力矩真实策略失效；Run261关于固定零力矩不能无限重复的独立结果仍保留。

**本轮负面发现**：Run266单真值必要守卫虽能排除倾角反例，却不能排除Run260/264现有盒内的任何状态；继续只收紧该守卫或反复延长零力矩桥，不能解决终端信息状态RCI。必须把后验的绝对速度—倾角—角速关联、未来观测纤维和可实现反馈回返纳入下一步。

## 4. 论文正文复核（既有论文，去重总数不增加）

Xubin Ping, Ning Sun (2015), *Dynamic Output Feedback Robust Model Predictive Control via Zonotopic Set-Membership Estimation for Constrained Quasi-LPV Systems*, *Journal of Applied Mathematics* 2015, Article 875850, DOI https://doi.org/10.1155/2015/875850；出版社开放全文 https://onlinelibrary.wiley.com/doi/full/10.1155/2015/875850 。2026-11-02实际核验§3假设A1–A3、§4.1式(15)–(26)、§4.2式(27)–(32)、§4.3式(33)–(35)、§4.4 Algorithm 8/Theorem 9、§5 CSTR数值例；网页数学公式部分渲染为空，不能冒称逐符号核对所有LMI。

论文为当前调度参数已知、未来多胞体不确定的离散quasi-LPV系统；动态输出反馈`u=C_c x_c+D_c y`，zonotope估计误差外包、固定阶数`N_z`的降阶、下一拍可行性辅助LMI门控；若门控失败则沿用旧控制器参数。Theorem 9在初始主优化可行及文中模型/约束假设下给出输入输出约束与趋于邻域的结论。§5为2状态CSTR数值例，非四旋翼、无丢包自动机、无推力/力矩三拍时滞，也无20ms最坏计算保证。**SMF+MPC、可行性门控、回退旧控制器均非本课题新机制**；其可行性继承证明不能不经修改用于本项目非线性Euler/间歇位置量测的信息终端。

## 5. 实际工件、测试与限制

新增：
- `verification/check_run267_terminal_guard_clearance.py`（严格全盒必要守卫，读取Run260/264归档与真实配置交叉核验）
- `verification/test_run267_terminal_guard_clearance.py`（6个隔离单元测试）
- `results/run267_terminal_guard_clearance_20261102/checks.json`（四盒Fraction精确证书）
- `.github/workflows/run267-terminal-guard-clearance.yml`（完整checkout的聚焦回归、配置与归档JSON逐字比较）

本地Linux Python 3执行`PYTHONPATH=. python -m unittest discover -p 'test_run267*.py' -v`：**6/6通过**；`python -m py_compile *.py`：通过；`python check_run267_terminal_guard_clearance.py --output checks.json`：生成确定性JSON。因本地容器DNS无法解析github.com，未在本地完整checkout中执行旧版Run26x回归或读取真实配置；以PR CI实际结果为准，不能先报成功。

**证据等级**：这是对既有可靠外包的必要条件筛选（严格有理数数值证书），不是SMF/CZ后验构造、MPC求解、共享因果控制律、终端RCI、无限递归可行、鲁棒稳定、六状态安全或20ms WCET。**Gate A=blocked**。条件性六状态平面物理首选、四状态有限安全数学基线均不变。

## 6. 下一轮唯一优先任务

在第60拍SMM/MMS两类**全部非空有噪观测后验**上，构造可计算的`(v,phi,omega)`关联集合（保留测量纤维与success/miss分支），以可实现力矩的15拍因果策略检验**回到同一信息终端族**；若找不到，记录精确阻碍/反例，不再以必要守卫通过冒充安全闭合。
