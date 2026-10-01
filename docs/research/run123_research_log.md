# Run 123：两时刻因果更新与旧计划移位基线

基线：`main` 1c49659c；`research/run122-reproduce-run119` 90acb9a。文献阅读和准入见 [run123_literature_gate.md](run123_literature_gate.md)。Dey–Bhasin 2026 已覆盖一般 adaptive output-feedback tube 的递归可行结构，所以本轮没有新颖性声明。

## 时序与条件性命题

Run 122 的当前误差后验记为 $C_t=\{G_t\xi:\xi\in[-1,1]^{601},A_t\xi\le b_t\}$。执行旧计划首个 nominal 输入并采用固定反馈后，一步误差预测为

\[
P_{t+1|t}=F C_t\oplus W,
\]

其中 $W=D_0G[-1,1]$。代码把 601 个旧潜变量完整推进，并显式加入一个新扰动潜变量；继承两条旧测量行后，再以位置测量残差 0.014、半径 0.02 的条带求交，得到 602 潜变量、三条独立测量行的新后验 $C_{t+1}\subseteq P_{t+1|t}$。这里 $C_{t+1}$ 的坐标原点严格取旧 nominal 后继 $z_{1|t}$，其位置为 0.001，因此对应绝对位置测量为 0.015；未进行任意重定心。

对相同 $F,W$，集合传播的单调性给出

\[
F^iC_{t+1}\oplus\sum_{j=0}^{i-1}F^jW
\subseteq
F^{i+1}C_t\oplus\sum_{j=0}^{i}F^jW.
\]

因此移位输入 $v_{i|t+1}=v_{i+1|t}$（$i=0,\ldots,28$）继承旧约束。旧名义终点为零，追加 $v_{29|t+1}=0$ 后仍为零；新后验及其有限时域传播只使用 mRPI 脉冲序列的有限前缀，故被 Run 121 已用有理数尾界认证的固定 $S$ 包含，最后一拍由 $S$ 的状态/输入余量覆盖。这是冻结四状态、固定 $F,W,K$ 和对齐中心条件下的直接集合推论。

## 可执行核查

`verification/check_run123_two_time_shift.py` 复用 Run 122 的 OCP 与严格 HiGHS 设置，重新解旧计划，再构造新后验和移位候选。结果保存于 `results/controller_direction_closure_20260928/run123_two_time_shift.json`：

- 旧/新潜变量维数为 601/602，新测量行秩为 3，LP 判定后验非空；
- 在 30 个阶段、每阶段 8 个状态方向和 2 个输入方向共 300 个查询上，新 tube 相对旧 tube 下一阶段的最大支持超额为 `1.11e-16`；
- 移位候选追加输入为 0，终端无穷范数 `9.48e-18`，最小鲁棒余量 `-6.94e-18`，均为浮点零量级；
- 直接脚本入口和模块入口均有回归测试。首次直接执行暴露仓库根目录未进入 `sys.path`，补测试后修复。

命令：

- `python -m unittest verification.test_run123_two_time_shift -v`
- `python verification/check_run123_two_time_shift.py`
- `python verification/check_run120_terminal_rpi_support.py`

## 证据等级与剩余缺口

条件性证明：精确测量求交、对齐旧 nominal 后继、固定模型/反馈/扰动和 Run 121 RPI 条件下，一次移位候选保持可行。数值证据：具体 602 潜变量后验、300 个控制方向支持及浮点 OCP 余量。尚未证明：任意重定心、在线压缩误差、连续多拍归纳、缺测/扰动合同切换、稳定性、非线性六自由度四旋翼安全及同预算严格优势。

下一唯一问题：在本轮 602 潜变量后验上同时施加**非零重定心与固定复杂度压缩**，用全部移位候选控制方向余量作准入证书；若不存在非平凡可准入方案，给出最小反例并停止该机制。
