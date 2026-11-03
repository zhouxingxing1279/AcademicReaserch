# 117. Houska 竖直 information-ensemble 基线适配合同

日期：2026-10-26。Run182停止手工cell枚举后，本章先回答一个更早的可执行性问题：Houska
式(29)需要固定线性系统和固定扰动/测量误差集合，当前实际推力相关四旋翼合同怎样可靠落入
该接口？

## 1. 固定包络竖直模型

取真实竖直tracking error `e_z=(e_pz,e_vz)`，采样周期 `h=1/50`：

```math
e_z^+=\begin{bmatrix}1&1/50\\0&1\end{bmatrix}e_z
 +\begin{bmatrix}0\\1/50\end{bmatrix}\delta T+w,
\qquad C=\begin{bmatrix}1&0\end{bmatrix}.
```

竖直连续 residual 半宽为

```math
\bar r_z(T)=\frac{1043}{500}+\frac{81}{800}T.
```

由于实际推力 `T in [981/200,2943/200]` 且系数为正，全域最大值精确为

```math
\bar r_z=\frac{572143}{160000},\qquad
\bar w_v=h\bar r_z=\frac{572143}{8000000}.
```

这一步把decision-dependent `W(T)`外包成固定 `W`，因此满足Houska问题接口，但明确损失
scheduled residual相关性。它是强基线的保守化，不是候选新方法。

## 2. 信息和硬约束

success边对位置作噪声半宽 `1/50` 的strip求交；miss边不获得位置信息，learning operator为
identity。15-mode图保留14条miss和3条success边。mode 4、9各有两个未知后继，因此同一个
source extreme information set的当前control必须同时满足两边；mode14只允许success返回。

由真实状态盒与nominal probe盒的逐坐标最小余量，得到对所有nominal states都安全的对称误差盒

```math
|e_{pz}|\le1,\qquad |e_{vz}|\le\frac{11}{4}.
```

名义/实际推力区间的两侧余量相等，故

```math
|\delta T|\le\frac{572143}{160000}.
```

注意数值恰与连续 residual 全域半宽相等只是当前冻结配置的巧合；检查器分别从两条来源推导并
要求二者相等，不能据此把扰动与输入混为同一对象。

## 3. 式(29)的图扩展义务

下一步需为每个source mode建立一个information ensemble parameter，选择信息集模板
`Y,G,Lambda`和meta-template `Z,H,Omega`，并对17条边分别施加successor inclusion。每个source
extreme information polytope只配一个当前控制；该控制在mode 4/9的全部外出边间共享。状态
约束施加在所有extreme information-set vertices上，输入约束施加在全部extreme controls上。

本轮没有选择模板，也没有求解极端集合控制。已证明的仅是：上述模型、固定 `W/V`、图、信息
时序和硬约束可从仓库配置以精确有理数无歧义重建。证据等级为
`exact_houska_vertical_adapter_contract`。未证明invariant ensemble、递归可行性、同预算优势或
六状态非线性四旋翼保证。

下一唯一问题：先用二维axis-aligned box information template构造其完整configuration cone与
vertex maps，再选择最小meta-template并把式(29)扩成15-source/17-edge线性可行性问题；必须
在mode 4/9复用控制并输出可独立重放的原始/对偶证书。
