# Run237 — 两状态后验纤维的共享力矩严格不可行证书（2026-11-01）

**基准远端main：** `a51a657de081c7b49884569fd02b87326c93126d`。唯一瓶颈：Run236只证明全状态K不具观测可实现性，未判定是否有其他共享力矩使所有真实后继仍落入Run235有限终端RPI F。本轮直接检验 `exists tau forall x in {x+,x-} forall r in [-R,R]: f(x,tau,r) in F`。

## 1. 精确有理数支持超平面反例

沿用Run235冻结四状态Euler、固定推力T=981/100 N、h=1/50 s、J=1/50、D=1742383/800000、R=3246383/1600000、F=P_800+Q（4000生成元），以及Run236不可区分的两个初态 x±=(0,±hD,0,0)。两者位于F、初始先验且共享成功位置包下的(p,phi,omega)=(0,0,0)观测。扰动对手分别取合法r=±R。

令支持方向 l=(13939/100000,55667/100000,-252917/100000,-1)，通过800步Fraction矩阵幂递推，直接求F的精确支持 h_F(l)=D sum(j=0..799)|l A^j B|+scale sum(j=0..799) sum(i=1..4)|l A^j e_i|，其中scale=D||A^800 B||∞/(1-||A^800||∞)。严格计算 h_F(l) < 0.028770186。正状态正扰动、tau=0的实际Euler后继 y+=(h²D,h(D+R),0,0)，其 l·y+=0.04695929430606，故精确差值 > 181/10000=0.0181。

因 h/J=1，施加共享力矩tau时正分支支持投影为 l·y+ - tau。若后继属于F，必要tau>0.0181 Nm。负状态负扰动后继关于原点对称，F也中心对称，取支持方向-l得必要tau< -0.0181 Nm。**同一个观测不能同时选择满足两条件的力矩**；因此该两状态后验纤维没有任何共享实数力矩能使所有后继落在原F内，甚至放宽执行器力矩界也不成立。

这是对**指定后验纤维+原终端F**的严格一步反例，证据比Run236的“全状态律不可实现”更强，但**不**证明一般SMF输出反馈终端核为空，不排除改造F、信息状态终端集、联合估计误差RPI或带历史的策略。

## 2. 文献

定向阅读Qiu, Yang, Zhu, Mousavinejad (2020), *Output feedback model predictive control based on set-membership state estimation*, IET Control Theory & Applications 14(4):558–567, DOI https://doi.org/10.1049/iet-cta.2019.0881 ，出版社公开正文§2、§3.1–3.4、§4（公式部分网页以图片呈现，未逐式核验）。该文用椭球SMF的预测/量测更新与LMI/SDP MPC及终端不变约束构建输出反馈；需要初始可行和适当集合外包。其线性/椭球假设不能直接覆盖本冻结非线性间歇量测系统。已在统一日志历史条目出现，去重已读仍91篇；本轮补充实际阅读范围与局限。

## 3. 验证及工件

新增 verification/check_four_state_shared_successor.py、verification/test_four_state_shared_successor.py（8项测试）、results/four_state_shared_successor_20261101/checks.json、.github/workflows/run237-shared-successor.yml。隔离Linux Python 3环境使用与远端Run235公开常数完全一致的最小模块镜像，运行：
```
PYTHONPATH=verification python -m unittest discover -s verification -p 'test_four_state_shared_successor.py' -v
PYTHONPATH=verification python verification/check_four_state_shared_successor.py --output results/checks.json
```
结果7通过、1项真实配置检查因本地缺完整checkout跳过，JSON精确摘要生成成功；GitHub Actions负责完整checkout/配置/旧新聚焦测试/归档比对。**CI实际完成前不宣称94+8项全通过**。未执行全仓库历史回归、在线20ms最坏时延或四状态SMF-MPC仿真。

## 4. 课题评估及唯一下一任务

Gate A=blocked。全状态F的RCI证明仍成立；该F对上述部分观测信息状态不能作为共享力矩不变终端。可行性：需转向估计误差/信息状态联合终端设计；创新性：负面证书本身不足支撑硕士论文；难度：高但目标更清楚。

**下一轮唯一优先任务：** 在保留已证明全状态F为对照的同时，构造一个包含估计误差/观测历史的可实现输出反馈终端集合与备份律，首先对同一两状态纤维给出一步严格可行见证（可使用更大且满足硬约束的终端集合），再讨论递归闭合。
