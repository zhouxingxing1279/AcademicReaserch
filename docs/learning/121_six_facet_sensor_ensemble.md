# 121. 六 facet sensor ensemble：连续测量中心的精确消元

日期：2026-10-27。Run186只处理中心化位置strip与一个对称六边形；本章核查连续measurement
center是否迫使后续meta模型使用无限分支。

## 1. 传感器的正确量词

沿用Houska的测量模型`eta=Cx+v`、`v in [-a,a]`。信息集`X`与某个观测值相容，指存在同一个
`eta`使`eta-CX subset [-a,a]`，不是“每个状态各选一个测量中心”。对位置输出`C=[1,0]`，
所有可行中心构成

```math
I(X,a)=[max_{x in X} p-a, min_{x in X} p+a].
```

因此某个中心存在，当且仅当位置宽度不超过`2a`。

## 2. 六 facet 的精确 measurement row

Run186法向顺序是`+p,+v,-q,-p,-v,+q`，并在configuration cone内有
`P(y)=conv_i Lambda_i y`。逐个vertex map核查给出

```math
max_{x in P(y)} p=y_0, min_{x in P(y)} p=-y_3.
```

故

```math
I(y,a)=[y_0-a,-y_3+a] is nonempty
iff y_0+y_3<=2a
iff Z_1 y<=a,
```

其中`Z_1=(1/2)[1,0,0,1,0,0]`。这正是Houska §6.3要求放在`Z`首块的
measurement-compatible coordinate。未来测量中心无需枚举，也无需把Run186的三个`min`支持
分支显式塞进图LP；在ensemble层执行`P(z) intersect V`即可。若需要凸模型，Houska式(25)
已经给出对非凸`min`的安全外包。

## 3. 平移边界见证

取位置半径`1/50`、速度半径`1/10`、斜向半径`1/50`，整体平移
`(p,v)=(1/3,-1/2)`。对应offsets为

```math
(53/150,-2/5,-109/300,-47/150,3/5,121/300).
```

它精确位于Run186 configuration cone内。实际测量噪声半宽`a=1/50`时，兼容中心区间退化为
`[1/3,1/3]`，同时`Z_1 y=1/50`。这固定了halfwidth/diameter因子，也证明非零连续中心没有被
中心化假设遗漏。checker会拒绝configuration cone外的offsets，避免把形式宽度等式当作合法
六边形证据。

## 4. 方向纠正与证据边界

证据等级为`exact_six_facet_sensor_ensemble_measurement_row`。本轮纠正Run186检查点中的停止条件：
`min/disjunction`本身不会迫使固定预算表示失败，因为measurement centers已被单个线性meta
coordinate消去，而Houska已有凸外包。真正未决的是如何选择剩余`Z_2`，并为六维offset参数域
构造固定configuration的`H/Omega`与极端信息集。

这不是完整information ensemble、因果控制图、输入/终端约束或递归可行性证明。下一轮只比较
direct facet-offset bounds与center/radius/support bounds两类`Z_2`；要求给出有限
`H/Omega`、明确extreme-set预算，并在进入15-mode LP前用精确vertex replay排除错误模板。
