# 第127章：Run193 `S4` 同心模板不能形成 RCI

## 1. 适用范围

只考虑冻结的四状态横向—姿态离散模型、当前推力在力矩前可见、未来推力任意跳变、
`W(T)=47/25+T(9/20)^3/6`及Run193由HiGHS选择出的102-facet第四层多面体`S4`。
`S4`行选择仍是`NUMERIC_CHECK`；一旦行集合冻结，下述见证完全使用有理数。

候选类为

\[
S_\alpha=\alpha S_4,\qquad 0<\alpha\le 1,
\]

并给予最有利的调度可见vertex control：每个`S4`顶点和当前推力端点可分别选力矩。

## 2. 精确顶点

冻结`S4`包含精确顶点

\[
v=\left(
\frac{19040871601}{4000000000},
\frac{4786988769}{1600000000},
\frac{13488347}{39240000},
\frac{4169653}{3139200}
\right).
\]

逐行精确代入102条不等式得到最小slack为0；共有5条活跃法向，精确行消元秩为4，故这是
一个退化但由满秩活跃法向证实的顶点。`S_alpha`对应顶点为`alpha v`。

## 3. 低推力端点的力矩矛盾

在`T=981/200 N`下，要求`alpha v`的鲁棒后继仍在`alpha S4`。选择其中两条目标facet，
分别得到必要力矩下界和上界：

\[
\tau\ge
\frac{4546282867}{7848000}\alpha+
\frac{6254383}{196200},
\]

\[
\tau\le
\frac{564768769}{981000}\alpha-
\frac{6254383}{1569600}.
\]

两者之差为

\[
\tau_{\min}(\alpha)-\tau_{\max}(\alpha)=
\frac{5626543}{1569600}\alpha+
\frac{6254383}{174400}>0,
\qquad \forall\alpha>0.
\]

因此该顶点在低推力端点没有任何力矩可使后继留在同一同心模板。矛盾在加入
`|tau|<=2/25`之前已经成立，所以放宽或忽略当前力矩限幅也不能挽救这一固定形状。

## 4. 证据等级与不能推出的结论

- `COUNTEREXAMPLE`：不存在正尺度`alpha`使冻结的同心`alpha*S4`配合调度可见vertex torque
  成为RCI。
- `OPEN`：独立变化offset的configuration-constrained polytope、不同法向、非同心集合、
  PWA/gain-scheduled/PD-RCI控制器。
- 不能推出一般RCI不存在、四旋翼物理不可行、六状态安全、terminal invariance或递归可行性。

该结果停止“仅缩放Run193形状”的路线。下一步必须进入真正的offset/controller联合综合，
而不是继续增加有限predecessor层数。
