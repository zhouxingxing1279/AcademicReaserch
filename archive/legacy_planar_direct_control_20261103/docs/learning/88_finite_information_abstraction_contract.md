# 88. 有限信息抽象的充分性合同

## 1. 目标与对象

令 `h_k` 为控制器在时刻 `k` 可获得的完整历史（测量、packet outcome、历史输入），令
`I(h_k)` 为与该历史相容的联合 `(eta,e)` 信息集。Baras--Patel 的精确信息状态递推以
`I(h_k)`（更一般地为函数值信息状态）为充分统计量；本节只讨论如何安全地把它保守压缩
为可实现状态

`a_k = (sigma_k, d_k, z_k, bar_u_k)`，

其中 `sigma_k` 是有限离散索引，`d=e-eta` 可见。该压缩不要求精确等价，但必须保证任何
由压缩控制器认证的安全性也适用于全部真实历史。

## 2. 五项充分条件

对每个抽象状态 `a` 给出联合集合 `K(a)` 和因果控制 `delta u=kappa(a)`。若满足：

1. **初始化覆盖**：所有允许初始历史均有 `I(h_0) subset K(alpha(h_0))`；
2. **历史一致性**：`alpha` 只依赖控制器可见历史，不能使用隐藏 `eta`、未来 packet outcome
   或未来扰动；
3. **逐边模拟**：对任意 `I(h) subset K(a)`、同一当前 `kappa(a)`、任意允许共享物理原语
   及下一 packet 边 `ell`，真实 posterior update 满足
   `I(h+) subset K(A(a,ell,y+))`；测量求交必须发生在正确时序，不能把共享原语复制成
   独立笛卡尔积；
4. **硬约束**：`z+e` 对 `K(a)` 的全部成员满足状态/余项源域，且
   `bar_u+kappa(a)` 满足执行器盒；
5. **终端闭合**：候选抽象集合族在上述 successor map 下自映射，并含初始化像。

则由归纳法，所有真实闭环信息集均被对应 `K(a_k)` 覆盖，因而集合上的状态/输入约束成立。
这只是终端安全/不变性的接口；要得到 MPC 递归可行性，还需名义计划移位、终端名义控制和
收紧一致性证明。

## 3. 当前 15-mode 合同的审计

当前 mode graph 的 `0,...,14` 已表示自上次 success 后的 miss age。三条 success 边
`4->0`、`9->0`、`14->0` 都把 age 重置为 0。因此：

- 若 `return-age` 仍指“当前连续 miss 数”，它与 `mode` 重复，不能区分三种 mode-0
  return history；
- 若它指“上一周期长度”，应明确扩展为 `last_return in {5,10,15}`，并给出 success/miss
  更新规则；这只是一个有限 automaton memory，不等于完整信息状态；
- Run148 已在相同目标 mode 0、相同 success 前可见 offset `(0,0)` 下构造来自 4/9/14
  的三种不同相关 return seed。它证明现有 `(mode,current-age,visible-center)` 标签不唯一
  决定 intrinsic shape；但不证明不存在共同安全外包，因为三者可取凸包。

所以有限索引的正确验证对象不是“同标签历史是否有相同形状”，而是它们的联合外包是否在
硬约束和共享输入下逐边闭合。只有证明上述五项条件，有限模板 fixed point 才有终端意义。

## 4. 证据等级与停止点

本节给出的是 **sufficient simulation contract for a conservative finite information
abstraction**，是一般信息状态理论在当前合同上的直接特化，不是新算法或 RCI 存在证明。
当前仓库只满足 mode automaton、控制时序和若干初始化 return seed；尚未给出覆盖所有历史
的 `alpha/K/A`，因此不应启动宣称终端证书的有限周期求解器。

若下一步无法为 `last_return` 扩展证明逐边共同外包，或共同外包立即违反状态/输入硬约束，
应停止有限周期模板支线，转向 Houska 型完整 information ensemble/极端信息集基线。
