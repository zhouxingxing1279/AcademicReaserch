# 123 物理有界六-offset ensemble：有界但退化为单一极端集合

## 1. 物理域与支配 offsets

Run183冻结的竖直tracking-error安全盒为

\[
\mathcal X=[-1,1]\times[-11/4,11/4].
\]

沿Run186法向顺序 `(+p,+v,-q,-p,-v,+q)`、\(q=p-v/10\)，该盒的紧支持为

\[
y_{\mathcal X}=(1,11/4,51/40,1,11/4,51/40).
\]

六个vertex maps在此参数上只产生盒的四个角，configuration最大margin为0，因此
\(P(y_{\mathcal X})=\mathcal X\)。

## 2. 为什么多个参数极点不等于多个极端信息集

考虑不额外调参的物理有界参数域

\[
Q_{\mathcal X}=\{y\in\mathcal G:P(y)\subseteq\mathcal X\}.
\]

对任意 \(y\in Q_{\mathcal X}\)，configured facets是紧支持，故支持函数单调性给出

\[
y_i=h_{P(y)}(Y_i)\le h_{\mathcal X}(Y_i)=(y_{\mathcal X})_i.
\]

于是 \(P(y)\subseteq P(y_{\mathcal X})=\mathcal X\)。Houska information ensemble包含所有这些
多面体的任意紧子集；其极端集合是包含关系下的最大成员。因此

\[
\partial\mathbb P(Q_{\mathcal X})=\{\mathcal X\}.
\]

参数域虽然有界且可有多个几何极点，真正extreme information set却只有一个。给这个单元素配置
control会退化为固定最坏盒控制，无法利用在线SMF收缩。

## 3. 证据边界与方向纠正

证据等级为 `exact_physical_bound_meta_ensemble_singleton_extreme_set`。它只否定“configuration cone
+物理包含”这一meta域，不否定加入measurement/history条件的direct-offset域、CZ ensemble或一般
输出反馈控制器。尚未构造variable `H/Omega`、图不变性、输入/终端约束或递归可行性。

下一步必须从可辨识information变量出发增加线性约束，使最大多面体互不包含；先在一个source
mode上精确得到至少两个真实extreme sets并检验measurement closure，再决定是否扩展全图。
