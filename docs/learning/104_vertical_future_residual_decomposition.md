# 104. 竖直 future residual 的精确分解与姿态单项路线否证

## 结论

冻结benchmark的竖直物理余项半宽为

\[
D=c+\alpha T_{\max}=\frac{1043}{500}+\frac{81}{800}\frac{2943}{200}
=\frac{572143}{160000}=3.57589375.
\]

其中`c=2.086`是当前全状态/风域上的气动核心外包，`alpha T_max=1.48989375`是姿态--推力
线性化项。benchmark真值语义是定义好的离散Euler映射，而不是连续真值的数值近似；配置中的
外部过程半宽全为零。因此当前合同没有另一个隐藏的积分余项或外部增量可供重新分摊。

Run166要求`beta<=16254878/42598647`，对应绝对半宽

\[
D_\star=\beta D=\frac{89401829}{65520000}\approx1.36449678.
\]

即便把姿态--推力项完全消去，仍有`c=2.086>D_star`，严格超出
`47272891/65520000≈0.72150322`；可达到的最好比例只有

\[
\frac{c}{D}=\frac{333760}{572143}\approx0.583351>0.381582.
\]

所以更精确的姿态测量、精确余弦传播或单独消去该线性化项，都不可能达到Run166门槛。

## 尚未否定的唯一物理路线

在姿态项取零这一最乐观条件下，气动核心仍须满足

\[
c_{\mathrm{local}}\le D_\star,
\quad \frac{c_{\mathrm{local}}}{c}\le
\frac{89401829}{136674720}\approx0.654121,
\]

即至少降低34.5879%；若未来姿态项为正，要求更严格。这个局部界必须量化15个未来tick上的
全部信息一致状态、风与控制序列，而非只量化当前SMF后验。Hu等的nonlinear tube基线正要求在
整个当前预测tube上外包余项；还需证明压缩、重定心和旧计划移位后仍保持该域。

## 证据等级与边界

- **已证明（精确有理数、配置锚定）**：姿态项单独缩小不能达到Run166阈值。
- **条件性必要条件**：任何可行局部气动合同至少满足上述65.4121%比例，且覆盖完整未来语言。
- **未决**：该局部域能否初始化、跨时刻闭合并给出终端/递归可行性。
- **不声称**：当前冻结模型完全不可行、一般输出反馈MPC不可能，或六自由度非线性四旋翼保证。

复现：

```bash
python -m unittest verification/test_vertical_future_residual_decomposition.py
python verification/check_vertical_future_residual_decomposition.py \
  --output results/theory_vertical_future_residual_decomposition_20261012/exact_checks.json
```
