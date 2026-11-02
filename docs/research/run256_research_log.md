**Run256 PR/main CI及安全合并复核（2026-11-02 UTC）：** 研究PR #91 https://github.com/zhouxingxing1279/AcademicReaserch/pull/91 基于main `d807097e7b787bda8627e0d98d48a74b307c531d`；合并前compare ahead=7/behind=0、仅7个预期文件，PR mergeable_state=clean，expected head `7ac8ce169ec93d2884289ded8c42baed05d2db14`。PR CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41381714225 **completed/success**，读取完整checkout Python3.13 job日志确认Run249–256聚焦**70/70测试通过、无跳过**，Run249真实配置/step交叉核验、源码编译、精确JSON逐字比对及artifact上传均成功。使用expected-head非强制squash合并至main `02f7b10fd6b7359b8d608094f8e0a2c81b69229e`，重新读取main SHA、PR merged及6个源码/归档/文档Blob确认落地。合并后main push CI https://github.com/zhouxingxing1279/AcademicReaserch/actions/runs/41381772373 **completed/success**，再次读取Python3.13完整job日志确认**70/70通过、无跳过**、配置交叉核验、证书逐字比较和artifact上传成功。**全仓库历史回归未执行**；CI成功不等于数学证明自动正确，更不意味着真实后验无解或物理系统不安全。此补记只更新核验记录，不修改算法或证书。Gate A仍blocked。

---

# Run256 — 独立区间SMF的速度纤维不可收缩性（2026-11-02 UTC）

## 研究问题与证据级别

以远端main `d807097e7b787bda8627e0d98d48a74b307c531d` 为基准，已读取 `docs/research/CURRENT_CHECKPOINT.md`、`docs/literature/PAPER_READING_LOG.md`、Run249/255日志、`verification/check_four_state_shielded_smf_mpc.py`、`verification/check_run255_posterior_bridge.py`、`configs/planar_baseline.json` 及背景第9轮模型证据。Run255在特定 `SSSMMS` 零读数历史的**可靠独立区间外包** `S30` 上已得到未来39拍有限安全证书，但尚未得到可移位信息状态终端核。本轮只解决一个瓶颈：**在第35拍位置success/miss之后，现有独立区间SMF能否借助成功位置包压缩隐藏速度并复位到原先验宽度？**

**新结果为算法表示/认证方法的严格局限，不是物理系统的不可生存证明。** 不改变Run249的MPC或控制律，不声称新闭环、递归可行、稳定或六状态鲁棒安全。

## 模型、实际量测与精确后验分支

冻结四状态 `x=(p,v,phi,omega)`、固定 `T=981/100 N`、`h=J=1/50`、`|r|<=R=3246383/1600000 m/s²`、`|tau|<=2/25 Nm`；`p+=hv`、`v+=v+h(-T sin(phi)+r)`、`phi+=phi+h omega`、`omega+=omega+h/J tau`。硬约束 `|p|<=5, |v|<=3, |phi|<=0.45, |omega|<=2`。姿态/角速每拍带噪测量，位置每5拍一次机会、最多连续2包miss，成功位置噪声半宽0.02m。控制仅依赖已收到的观测，不使用隐藏速度。

继承Run254/255第30拍 `S30: p±0.02, v±1.346823505, phi±0.005, omega±0.01`，不是精确关联后验。应用Run255第30–34拍共享脉冲 `(+0.04,-0.04,-0.04,+0.04,0)Nm`，Run255 `step` 逐拍精确有理数外包得到第35拍**测量前**：
- `p35^-∈[-0.1630117728, 0.1629929378]`m；
- `v35^-∈[-1.5553337315, 1.554705901]`m/s，宽 `3.1100396325`m/s；
- `phi35^-∈[-0.006,0.006]`rad，`omega35^-∈[-0.01,0.01]`rad/s。

对第35拍零姿态/角速读数、两种合法位置包：
- **success且位置读数0**：`p35∈[-0.02,0.02]`，`phi35∈[-0.005,0.005]`，`omega35∈[-0.01,0.01]`；但 `v35=v35^-`。
- **miss**：`p35=p35^-`，`phi35∈[-0.005,0.005]`，`omega35∈[-0.01,0.01]`；仍 `v35=v35^-`。
- 这两个分支均非空；更一般地，对**任何**非空success位置读数 `y_p` 和任意非空角/角速条带，当前 `strip` 只与被直接观测坐标的区间相交，`v` 投影不变。上述零读数和端点读数由精确Fraction实例化，普遍性由代码更新定义直接给出，不是有限枚举替代全称证明。

## 严格表示层不可能性命题（本轮关键）

定义当前独立区间滤波器的后验速度宽度 `W_k = v_k^U-v_k^L`。只要区间步进合法（`|phi|<=0.45`）且不利用硬安全盒对速度作**无依据的裁剪**，每次预测的Run249/255有理数、单调正弦Taylor包络满足

```
W_(k+1)^- >= W_k + h*T*(sin_upper(phi_k)-sin_lower(phi_k)) + 2*h*R
           >= W_k + 2*h*R.
```

向外舍入只增大宽度；所有合法success/miss的非空直接坐标条带更新均有 `W_(k+1)=W_(k+1)^-`。因此对**任意因果合法力矩序列及任意非空观测历史**，在这个独立区间滤波算法内，`W_(30+n)>=W30+n*(3246383/40000000)`。即使将来的力矩选择依赖当前读数，此逐步不等式仍成立；若姿态区间先离开允许域，则认证已提前失败。

从 `W30=269364701/100000000=2.69364701` 出发：
- `n=40`：普遍下界 `5.94003001<=6`m/s，不足以仅靠该下界否定第70拍；
- `n=41`：普遍下界 `6.021189585>6`m/s，**第71拍任何非空独立区间后验都不可能被速度硬盒[-3,3]完整包含**。

这是该算法的终端集合认证不可能性：在这些规则下无法无限重复地用同一种独立区间表示证明 `S_k⊆X`，也不能直接把第35拍成功位置包当作“速度宽度复位”。**它不是对真实关联后验的下界、真实状态失控、所有SMF/CZ估计器、其他鲁棒控制策略或无限时域物理可生存性的反例。** 直接用“假设系统始终安全”来裁剪速度区间将循环论证；需要从实际测量历史的`p-v`相关约束推导收缩。

## 文献分节复核及迁移边界

Brenner S. Rego, Guilherme V. Raffo, Joseph K. Scott, Davide M. Raimondo, *Guaranteed methods based on constrained zonotopes for set-valued state estimation of nonlinear discrete-time systems*, **Automatica** 111:108614 (2020), DOI https://doi.org/10.1016/j.automatica.2019.108614 ，公开预印本 arXiv:1908.09950v3 https://arxiv.org/pdf/1908.09950 。2026-11-02实际重读预印本PDF pp.2–3 §2–3.1、pp.4–6 §4.1–4.2 Theorems 1–3、pp.8–10 §4.4–5（特别式(22)、Remark 10、Table 1）；不声称核对期刊终版逐式一致。该文模型是一般非线性离散 `x_k=f(x_(k-1),u_(k-1),w_(k-1))` 与**线性有界误差量测**，输入 `u` 为已知施加输入；研究**状态集合估计**而非参数SMF、无人机MPC或控制律。假设紧有界过程/量测集合和可认证的Jacobian/Taylor余项；Theorem 2/3提供CZ预测外包，§4.4式(22)提供线性量测的广义交集，Remark 10指出表示复杂度增长和需要保包含降阶。论文数值示例并非本仓库四旋翼、间歇包、执行器饱和或终端RCI；不能用其估计保证替代MPC递归可行性。它说明下一轮应优先保留 `p-v` 关联（CZ/H-rep或等价联合约束），而不是无限延长现有盒传播。

本论文已在唯一论文总账Run214、Run179等登记，本轮只做正文定向重读，不增加去重数；阅读日志中补记本轮确切范围与负面结果。

## 测试、工件和限制

隔离Linux/Python3.13环境，标准库 `fractions.Fraction`：
```bash
cd /mnt/data/run256_work
PYTHONPATH=. python -m unittest -v test_run256_interval_information_limit
python -m py_compile check_run256_interval_information_limit.py test_run256_interval_information_limit.py
python check_run256_interval_information_limit.py --output checks.json
```
**9/9本地测试通过、无跳过**；源码编译与精确JSON生成成功。隔离目录中Run255辅助模块由已读取远端源码的同方程副本构成；因此**本地不能冒充完整仓库交叉核验**。PR GitHub Actions将对Run249–256聚焦测试、真实Run249 `step` 和 `configs/planar_baseline.json` 交叉检查，并将归档JSON逐字比较；实际CI结果另行核验。

新增：`verification/check_run256_interval_information_limit.py`、`verification/test_run256_interval_information_limit.py`、`results/run256_interval_information_limit_20261102/checks.json`、`.github/workflows/run256-interval-information-limit.yml`。没有修改Run249控制器或先前证书。

**可行性/创新性/难度：** 排除“靠独立盒+位置成功测量就可构造无限终端核”的低成本模板，是严格方法筛选而非新控制理论；改用关联集合可能改善保守性，但CZ的约束/生成元增长和20ms求解预算是新的关键风险。Gate A仍blocked；无限递归可行、稳定、六状态安全和20ms WCET均未证明。

**下一轮唯一优先任务：** 对第30–35拍同一真实历史，构造保留 `p-v` 动力学关联的**最小可核验联合线性条带/H-rep或CZ原型**，对所有非空第35拍success/miss后验给出严格速度投影界，并与本轮独立盒 `3.1100396325m/s` 作同预算对照；只在确实缩小时再尝试终端前驱，不直接宣布无限安全。
