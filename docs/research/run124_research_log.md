# Run 124：控制方向压缩可通过，但非零重定心卡在终端 mRPI

文献准入见 [run124_literature_gate.md](run124_literature_gate.md)。本轮不提出新控制算法，只回答 Run 123 留下的唯一问题。

## 1. 固定复杂度 outer template

令 Run 123 的 602 潜变量后验为 $C$，非零 nominal 初值平移为 $d_0$。对阶段 $i=0,\ldots,29$ 和每个状态/输入方向 $p_j\in\{\pm e_1,\ldots,\pm e_4,\pm K\}$，定义

\[
q_{i,j}=(F^i)^Tp_j,
\qquad
\beta_{i,j}=U_C(q_{i,j})-q_{i,j}^Td_0,
\]

以及固定 300 行模板

\[
T(d_0)=\{e:H e\le \beta\}.
\]

其中 $U_C(q)$ 不是 HiGHS 的原始 primal 值：浮点 LP 只提议非负对偶乘子，代码随后把输入数据和乘子转成精确二进制有理数，并以

\[
U_C(q)=\lambda^Tb+\lVert q^TG-\lambda^TA\rVert_1
\]

构造弱对偶上界；随后连同 $q^Td_0$ 的减法也在精确有理数中完成，最后才向正无穷方向舍入为 binary64 cap。因此由支持半空间定义严格得到 $C-d_0\subseteq T(d_0)$，且 $h_T(q_{i,j})\le\beta_{i,j}$。该模板把 602 维 latent LP 表示压成 4 个状态变量、固定 300 条不等式；它在保护方向上的保守量由认证 cap 决定，不再把浮点 primal 当成精确支持。它不是一般 CZ 降阶创新，而是共享 control-normal support ledger 的 H-representation 实例。

## 2. 全部阶段余量上的非零重定心 LP

先选择一个数值上接近新测量条带中心的 posterior member 方向

\[
\hat d=(0.01400001,0.01400000,0.01194394,0.01400000),
\]

其后验不等式/box 违反量为零，位置相对条带中心的浮点残差为 `1.16e-8`；该残差单独归档，不把近似等式误写为精确成立。

再令 $d_0=\alpha\hat d$，并优化 nominal 修正 $a_i$ 与状态修正

\[
d_{i+1}=A d_i+B a_i,\qquad d_{30}=0.
\]

LP 同时加入 30 阶段的 240 条状态余量和 60 条输入余量；误差模板的平移项按 $F^i d_0$ 计入。结果：

- 最大尺度 `alpha = 0.12264367365259067`，`||d0||inf = 0.0017170128554372824`；
- 认证 cap 与原始 HiGHS primal 的有符号差范围为 `[-4.66e-8, 3.09e-9]`；负值说明该 primal 在 solver tolerance 下不能充当上界，不是否定弱对偶证书；
- 平移后 binary64 cap 超过精确有理数认证值的 outward gap 范围为 `[6.51e-19, 3.13e-16]`；
- 使用认证 cap 后，300 条阶段 LP 余量最大超额为 `0`；直接重算的最大超额为 `1.04e-17`；
- nominal 动力学残差 `1.91e-17`，终端 nominal 修正为零；
- 输入修正范围 `[-0.0175811, 0.0197652]`。

因此“非零重定心必然被所有状态/输入余量拒绝”是错误的；阶段 LP 确有非平凡解。

## 3. 终端阻塞：阶段通过不等于递归可行

Run 123 的终端论证依赖：新后验按旧 nominal 后继对齐，故其有限冲激前缀属于 Run 121 的固定 mRPI $S$，而旧 nominal 终点为零。若重定心只做保持物理集合不变的精确坐标平移，则 nominal 修正必须满足

\[
a_i=-K d_i,\qquad d_{i+1}=F d_i,\qquad d_{30}=F^{30}d_0.
\]

本模型

\[
\det F=0.6999615978\ne0.
\]

所以同时保持精确平移并满足冻结 OCP 的 $d_{30}=0$ 时，严格推出 $d_0=0$。上节 LP 能取非零值，是因为它允许一般 $a_i$，从而改变了物理终端集合；此时原有 $E_{30}\subseteq S$ 不再由 Run 123 自动继承。仅检查状态/输入硬界或 nominal 终端为零都不能替代这项集合包含。

最小反例是标量 $S=C=[-1,1]$：任意 $d>0$ 都使 $C-d=[-1-d,1-d]\not\subseteq S$。即使有限阶段硬约束更宽、所有阶段余量仍为正，也不能据此推出固定终端集包含。

## 4. 结论和证据等级

- **已证明：** 由精确有理数弱对偶上界构造的 300 行模板 outer-contains $C-d_0$，并给出所有列入方向的安全上界；若要求保持物理集合的平移协变和零 nominal 终端，由 $F$ 可逆可知非零重定心不可能。
- **数值观察：** 放松“保持物理集合不变”后，全部 300 条阶段余量允许上述非零重定心与终端 nominal 归零。
- **未决：** 该新终端误差集合是否包含于 Run 121 的 mRPI；当前没有可执行包含证书，故整体准入为 `false`。
- **方向纠正：** 不继续扩大阶段方向集或调小重定心幅度。下一步只研究一个终端接口：构造可计算的 $E_N(d_0,a)\subseteq S$ 证书，或改用允许非零 nominal 终点、对实际终端集合认证的 terminal set。若两者都只能退化到 $d_0=0$，停止重定心主张，将 300 行模板仅保留为压缩基线。

## 5. 复现

```bash
python -m unittest verification.test_run124_recenter_compression -v
python verification/check_run124_recenter_compression.py
python -m unittest discover -s verification -p 'test_*.py' -v
python verification/check_run120_terminal_rpi_support.py
```

结果：`results/controller_direction_closure_20260928/run124_recenter_compression.json`。
