# 122 六 facet meta 坐标门槛：五参数不闭合，六参数不省预算

## 1. 坐标比较

沿用 facet 顺序 `(+p,+v,-q,-p,-v,+q)`，其中 \(q=p-\kappa v\)、\(\kappa=1/10\)。定义

\[
\begin{aligned}
c_p&=(y_0-y_3)/2,&r_p&=(y_0+y_3)/2,\\
c_v&=(y_1-y_4)/2,&r_v&=(y_1+y_4)/2,\\
c_q&=(y_5-y_2)/2,&r_q&=(y_2+y_5)/2.
\end{aligned}
\]

六个 paired coordinates 与六个 offsets 可逆。若只保留
\((c_p,c_v,r_p,r_v,r_q)\)，则隐含 \(\delta:=c_q-c_p+\kappa c_v=0\)。这不是一般
六 facet configuration 的换坐标，而是一个五维切片。

## 2. 实际测量产生的精确反例

取中心对称 source \(y=(3/200,3/200,3/200,3/200,3/200,3/200)\)，故 \(\delta=0\)。
使用项目合同的位置测量噪声半宽 \(a=1/50\)，选择测量中心 \(\eta=-23/4000\)，测量 strip 为
\([-103/4000,57/4000]\)。精确求交并在原六法向上取紧支持，得到

\[
y^+=(57/4000,3/200,3/200,3/200,3/200,3/200).
\]

该 posterior 六个 facets 均活跃，configuration cone 最大 margin 为 \(-3/4000<0\)，但
\(\delta^+=3/8000\ne0\)。因此五参数 center/radius family 对一次合法 measurement update
不闭合。此结论不否定六 offsets、CZ 或其他非中心对称集合表示。

## 3. 补回 skew 后的预算结论

补回 \(c_q\)（或等价的 \(\delta\)）后，paired coordinates 与 direct offsets 是可逆线性映射。
若 \(\mathcal Q_y=\{y:A_y y\le b\}\)，令 \(w=S y\)，则同一集合为
\(\mathcal Q_w=\{w:A_yS^{-1}w\le b\}\)。两者极点一一对应；同一参数多面体的
`H/Omega` extreme candidates 数量不因换坐标而减少。预算优势必须来自另一个受限或有损
参数域，并重新证明覆盖、measurement closure 和图不变性。

## 4. 证据边界与下一步

证据等级：`exact_six_facet_meta_coordinate_nonclosure_certificate`。本章没有选择有界 meta
polytope，没有构造完整 `H/Omega`，也没有证明15-mode/17-edge information ensemble、输入
约束、终端不变性、递归可行性或六自由度保证。下一步只以direct offsets选择受物理bounds限制的
有界参数多面体并精确枚举extreme information sets；预算不可接受时再转向固定复杂度CZ外包。
