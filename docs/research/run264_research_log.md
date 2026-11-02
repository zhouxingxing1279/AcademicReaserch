# Run264 — 第60–75拍共同备份策略的有限安全证书（2026-11-02）

## 1. 本轮问题与基准

基于远端 main `61c2e7fb1a7cc05343c0d2ff9ac3c626048429fa`，读取 `docs/research/CURRENT_CHECKPOINT.md`、Run260–263证书/代码、`configs/planar_baseline.json`和统一论文总账。背景任务最新PR #113只讨论Kamel等六旋翼级联MPC，未修改主任务控制器。本轮只解决一个有限前驱的可计算子问题：Run260第60拍两个外包（SMM/MMS）能否在不依赖未来测量数值的共同合法控制下，再安全推进15拍？这不是第60拍所有可能历史的终端信息集合综合。

## 2. 冻结合同、可核验结论

状态 `x=(p,v,phi,omega)`，定义的离散Euler真值 `p+=h v; v+=h(-T sin(phi)+r); phi+=h omega; omega+=h tau/J`。取 `h=J=1/50`、`T=981/100`、`|r|<=3246383/1600000`、`|tau|<=2/25`，硬界 `|p|<=5, |v|<=3, |phi|<=9/20, |omega|<=2`。本轮从Run260精确JSON读入第60拍两个可靠外包盒，不将其当作精确SMF后验，也不把Run263速度宽度界误用为绝对速度界。

使用共同备份控制 `T=9.81N, tau=0` 第60–74拍，利用 `sin(x)∈[x-x³/6, x-x³/6+x⁵/120]`（`0<=x<=0.45`）、奇对称、单调性和每步10^-10向外舍入，以Fraction包络传播。两类模式第60–75拍全部16个盒的四项硬界均严格满足：

| 起点历史 | 第75拍可靠速度区间(m/s) | 第60–75拍最小速度安全裕量(m/s) | 第75拍可靠位置区间(m) |
|---|---|---:|---|
| SMM | [-2.2047163143, 2.204276833] | 0.7952836857 | [-1.0917072485, 1.0913556638] |
| MMS | [-1.7298899592, 1.7297434655] | 1.2701100408 | [-0.6643635287, 0.6642756327] |

每个未来有噪位置/姿态成功读数或合法失测分支的非空后验都被无条件预测盒包含，因此无需枚举连续读数。将Run260第45–60拍15步桥与本轮第60–75拍15步桥拼接，得到同一固定历史条件下45–75拍共30步的共享开环安全前缀。**这是有限时域充分安全证书**；没有给出能回到同一个信息集合族的终端移位，也没有证明任意初始后验、无限递归可行性、稳定性或六状态物理安全。Run261已证明此零力矩控制不能无限重复，二者不矛盾。

## 3. 文献重读与方法边界

Quanwei Qiu, Fuwen Yang, Yong Zhu, Eman Mousavinejad, *Output feedback model predictive control based on set-membership state estimation*, *IET Control Theory & Applications* 14(4):558–567 (2020), DOI https://doi.org/10.1049/iet-cta.2019.0881 ，出版社开放全文 https://ietresearch.onlinelibrary.wiley.com/doi/full/10.1049/iet-cta.2019.0881 。2026-11-02实际重读§2 Assumptions 1–2、§3.1 Theorem 1、§3.2–3.4式(19),(34),(35)–(41)、§4式(45)–(57)、§5数值例。研究对象是LTV/LTI系统，椭球**状态**SMF和LMI/SDP输出反馈MPC，有界过程/量测噪声。Theorem 1依赖上一步状态已被估计椭球包含、且当前LMI可行；§4终端RPI构造明确引入**终端区域内真实状态已知的局部反馈假设**（原文“system state is assumed to be known inside ...”），不能直接当作本项目隐藏速度+间歇位置的可实现终端策略。§5为二阶系统、LPV系统和DC-DC转换器MATLAB/YALMIP/SeDuMi仿真，无四旋翼、无位置丢包、无20ms WCET。论文此前已登记（Run254），本轮只更新重读范围，去重总数不增加。

## 4. 工件与验证级别

新增 `verification/check_run264_epoch_backup.py`、`verification/test_run264_epoch_backup.py`、`results/run264_epoch_backup_20261102/checks.json`、`.github/workflows/run264-epoch-backup.yml`。独立Linux Python 3环境执行 `cd /mnt/data/run264_work && python -m unittest -v test_run264_epoch_backup`：首次9项中1项失败，因测试错误地要求**向外舍入后区间端点**与未舍入Euler端点严格相等；改成正确包含断言后**9/9通过**。源码编译和确定性JSON生成通过。完整GitHub checkout的真实Run260证书/配置交叉核验、Run260–264聚焦回归和PR/main CI由新增workflow核验；未经CI成功不得宣称已完成。证书不是MPC求解器、闭环仿真或终端信息状态RCI。Gate A=blocked。

## 5. 下一轮唯一优先任务

**停止延长零力矩开环桥**。以第60拍所有非空测量后验为输入，明确可重复的终端信息状态参数化（中心、关联生成元/条带、失测相位），构造观测纤维共享且允许测量反馈的15拍终端回返条件；首先用Run264终点外包检验能否回到候选族，若不能保留反例或给出必须的反馈权限，不得把有限桥当作递归可行性。
