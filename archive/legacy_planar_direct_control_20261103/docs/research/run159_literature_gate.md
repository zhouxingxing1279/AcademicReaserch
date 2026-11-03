# Run159 文献准入卡：`J14 -> 15` 完整 return 的位置下界

## 最近邻正文核查

1. **Goulart--Kerrigan 2007**：重读 finite-horizon affine output-feedback robust constraints、
   invariant estimation-error approximation及无限时保证条件。一般仿射输出反馈综合已有成熟框架。
2. **Yang--Ozay 2021**：重读 Sections 4.1--4.4、Algorithm 1、Propositions 2--5。缺测语言上的
   safety 必须覆盖整条 string 的每个中间状态，不能只检查重新测量时刻。
3. **Houska 2023/2026**：重读 Sections 6.4--6.5、Theorem 3。information-set feedback 与
   extreme controls 已覆盖一般方法，本轮只能声称项目参数下的路径级证书。

## 严格差异、最强基线与证明义务

最强同条件基线是 Run158 的 rescued mode-9 shared-branch witness。其只认证下一拍；本轮检查
miss 后继续到 mode 11 的硬位置约束，并允许 age 8、9 各自使用任意满足同一 correction 盒的
centered affine-in-`d` policy。证明义务是给出与具体 gain 无关的支持函数下界。

## 推动作用与可证伪条件

若下界不超过1，则应继续联合综合完整 return；若严格超过1，则 `(0,15)` 的 `15->15`
constituent 不安全，直接阻断目标凸包。下界必须保留独立 residual、正确输入到位置的时延系数，
并以 exact rational arithmetic 复核。

## 判断

**通过路径级 exact obstruction；不通过一般 output-feedback 不可行、RCI、终端或递归可行性
声明。** 该反证改变 target-family 可构造性，避免继续做无意义凸包，具有本轮研究价值。
