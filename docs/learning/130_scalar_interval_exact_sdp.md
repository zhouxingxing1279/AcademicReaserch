# 130 标量推力区间上的精确二次 SDP 合同

## 1. 为什么 Run196 后不能直接写 endpoint LP

固定 active set 后，facet offset `q(s)=q_0+q_1 s` 给出仿射 vertex
`v(s)=Vq(s)`；四状态 LPV 动力学、vertex torque 与调度一致扰动支持也都至多仿射于
归一化推力 `s in [-1,1]`。因此每个 vertex/facet 的一步残差至多为二次函数，而不是
Run195 参数无关集合下的仿射函数。Run196 已精确展示两端满足但内部违反。

## 2. 单个二次条件的精确 LMI

令待认证安全余量为 `f(s)=a s^2+b s+c`。区间等于单个二次不等式
`s^2-1<=0`；`s=0` 是严格可行点。S-lemma 因而给出：

`f(s)>=0 for all |s|<=1`

当且仅当存在 `lambda>=0`，使 `f(s)+lambda(s^2-1)>=0` 对所有实数 `s` 成立。后一全局
二次非负等价于

`Q = [[c-lambda,b/2],[b/2,a+lambda]] >= 0`，

即 `f(s)=[1,s]Q[1,s]^T+lambda(1-s^2)`。`Q` 的元素对
`(a,b,c,lambda)` 仿射，因此这是凸的 `2 x 2` LMI。对有理候选，`lambda>=0`、两个对角元
非负及 determinant 非负可全部用 `Fraction` 精确核查。

## 3. 对 Run196 反例的回归

取 `p=(s+1)/2`。Run196 的后继幅度为 `g=9/8-s^2/8`，相对共同目标1的安全余量为
`f=1-g=(s^2-1)/8`。此时 `c=-1/8`，对任意 `lambda>=0` 都有
`Q_00=c-lambda<0`，故不可能存在 PSD 证书；这与内部点 `s=0` 的精确违反一致。边界正例
`1-s^2` 取 `lambda=1,Q=0`，`1+s` 取 `lambda=1/2` 与 rank-one Gram matrix，
检查器均精确通过。

## 4. 19-pair 综合器的冻结接口

对38个 facets、160个 vertices，需要6080条上述区间 LMI。configuration cone、每个 slice
的状态硬约束、affine vertex torque 上下界对 `s` 仍为仿射，故两个端点检查精确。

未来推力可任意跳变，因此 successor 必须进入全部未来 slices 的交。凸综合中引入共同 core
offset `r`，约束 `r<=q(-1)`、`r<=q(1)`，并把所有后继送入 `{x:Cx<=r}`。这对 affine
offset 是可靠的共同子集，但可能小于真实交，故整体综合仍是保守充分条件。令 slope 为零、
`r=q_0` 可恢复参数无关候选类，所以这个模板包含 Run195 的决策类，但不保证可行。

## 5. 证据等级和不能推出的结论

- `DERIVED`：单变量、单闭区间二次非负与 `2 x 2` LMI 的精确等价；
- `CONDITIONAL`：在冻结 affine LPV/support、固定 active sets 下的6080条 LMI 综合合同可靠；
- `OPEN`：该 SDP 是否数值/严格可行、返回候选能否理性化并通过独立全区间检查；
- `OPEN`：四状态结果如何嵌入六状态、间歇测量 output-feedback tube、终端移位与递归可行性。

下一轮唯一问题：安装或调用可复现 SDP 求解环境，求解固定 cone 的 affine-offset 候选；无论
solver 状态如何，若返回候选，必须逐条送入 Run196 的全区间二次最大值器，不能把浮点
`optimal` 当作不变性证明。
