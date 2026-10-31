# Run215：第193拍历史一致联合条带与位置支持审计（2026-10-31）

**基准 main：** `8ef0cceccf9b2fc64883346cc3b6e324d711b151`（Run214）。**唯一瓶颈：** Run214第193拍的危险独立盒角点是否与已有位置、姿态观测和已施加控制相容？能否以可复核的历史联合约束排除，而非只继续收紧速度区间？

## 1. 研究方法、模型与可验证结论

沿用Run206/214冻结的四状态离散Euler模型 `(p,v,phi,omega)`，`h=J=1/50`，`v+=v+h(-T phi+r)`，`p+=p+h v`，`phi+=phi+h omega`，`omega+=omega+h u/J`。已知当前以前的实际推力与已施加力矩；位置返包误差 `±1/50 m`，姿态误差 `±1/200 rad`，余项 `|r_i|<=47/25+(243/16000)T_i`。全部安全相关计算使用Python `Fraction`。

- **联合位置—速度条带：** 对任何过去成功返包 `a<k`，精确Euler恒等式 `p_k-(k-a)h v_k = p_a-h² Σ_{i=a}^{k-1}(i-a+1)a_i`，其中 `a_i=-T_i phi_i+r_i`。利用历史观测及误差上界构造线性条带。仅含过去可见信息，且因独立放松噪声/余项是可靠**外包**。
- **联合姿态—角速度条带：** `phi_k-h omega_k=phi_{k-1}-(h²/J)u_{k-1}`，利用过去姿态观测和实际记录力矩构造严格条带；禁止读取未来控制/真值构造在线证书。
- **三包位置支持：** 对 `a<b<c<=k`，选择 `c_a+c_b+c_c=1`、`(b-a)c_b+(c-a)c_c=k-a`，从 `p_k=Σ c_j p_j+h²Σ_i [(k-1-i)_+-c_b(b-1-i)_+-c_c(c-1-i)_+]a_i` 得到精确有理数位置支持外包。Run215用 `(105,165,180)` 三包与 `c_c=7/3`，不是网格采样证明，也没有宣称这是全历史最优支持。
- 以上集合是独立状态盒与联合半空间的**多面体外包**，数学上可转为CZ，但本轮**尚未实现CG形式、完整CZ递推或降阶**。Scott等（2016）Theorem 1只提供表示等价，不能把该实现称为完整CZ观测器。

## 2. 第193拍实际可达历史的结果

| 指标 | 数值或结论 |
|---|---|
| Run214独立盒位置下界 | `1.296554197827568 m` |
| 本轮三包历史一致位置下界 | **`1.322291105702568 m`** |
| 严格改善 | **`205895263/8000000000 = 0.025736907875 m`** |
| 离线真值位置（仅用于核验） | `1.624466665869235 m` |
| 旧危险盒角点是否满足新位置下界 | **否，严格排除** |
| 六条单独位置—速度条带是否排除旧角点 | 否（负面结果） |
| 单独姿态—角速度条带是否排除旧角点 | 否（负面结果） |
| 新位置盒输入Run208/210原两层Backup | **仍拒绝** |

因此，Run214五拍速度越界的**独立盒角点确实不符合该历史的严格位置必要条件**，无需借助浮点LP作数学证明。但这不说明所有不安全联合状态均被排除，也不说明当前真实后验具有非空的两层控制准入。Run214第193拍拒绝尚未恢复。

附加数值诊断：在SciPy HiGHS中，对150..192拍的线性状态、姿态/角速度测量及位置返包约束求解，旧联合角点得到数值不可行；这**不是精确Farkas证书**，不能替代上述精确三包位置不等式。

## 3. 测试、复现与证据边界

- 新增 `verification/check_joint_history_strips.py` 与 `verification/test_joint_history_strips.py`；修改Run214 `replay_to_193(return_controls=False)`，仅可选返回历史实际施加力矩，默认返回值和控制行为保持不变。
- 新增**8/8**聚焦测试通过：精确Euler条带、真实状态包含、伪角点排除、三包位置支持、因果性、Run214第193拍复现与Backup仍拒绝。语法编译通过。
- 本地环境：Python 3.13.5，Linux x86_64。执行 `PYTHONPATH=/mnt/data/run215/mirror_shims:/mnt/data/run215/verification:/mnt/data/run215 python -m unittest -v test_joint_history_strips` 和 `python -m py_compile verification/check_joint_history_strips.py verification/test_joint_history_strips.py`。由于执行容器无法访问GitHub，使用**从Run206/208/210/214源码逐式构建的本地镜像**，其第193拍原位置/速度盒与真值和Run214已提交结果一致；**并非真实完整checkout的回归**。新增源码/测试Git Blob SHA为 `963f65ec77404b060de26d8fe36a1de37a4a87e7` / `54d99de67c91afbd279047674db25d48d477f4bd`。
- 在完整仓库的复现指令：`PYTHONPATH=verification python -m unittest -v verification.test_joint_history_strips`；`PYTHONPATH=verification python verification/check_joint_history_strips.py`。**完整仓库回归及GitHub CI尚未执行**，不能虚报。
- 在本地镜像100次重算中，三包位置支持约`1.80 ms/次`，三包支持加六条联合条带约`8.27 ms/次`；机器相关，且未计入原Backup求解，**不能宣称满足20ms在线预算**。Run214二十组三包速度支持约0.75s，工作负载不同，不计算不公平加速比。

## 4. 文献阅读与硕士课题评估

Scott, Raimondo, Marseglia, Braatz (2016), *Constrained zonotopes: A new tool for set-based estimation and fault detection*, *Automatica* 69:126–136, DOI https://doi.org/10.1016/j.automatica.2016.02.036，作者全文 https://web.mit.edu/braatzgroup/Scott_Automatica_2016.pdf。本轮定向精读Definition 3、Propositions 1–2、Theorem 1、Section 4和Section 5，阅读范围/限制已写入唯一论文日志。去重文献总数保持87篇。

**可行性：** 小规模有理数历史约束已可实现，验证证据增加。**创新性：** 单纯CZ、三包消元、半空间相交均为已有数学工具；潜在贡献必须是失测/调度不确定性下控制相关保守性、在线压缩与因果安全保证的联合分析。**难度：** 计算预算、联合支持优化、完整MPC和终端不变性仍高。**Gate A=blocked**，不得将单角点排除或局部Backup当作递归可行性、稳定性证明。

**下一轮唯一优先任务：** 将本轮联合半空间外包以真正的有界复杂度CZ/线性约束优化接口直接用于第193拍两层Backup的支持函数计算（而不是先重置为独立盒），在同等信息与计算预算下判断能否恢复非空首拍力矩区间，并给出可靠的数值/对偶验证。
