# Run158 文献准入卡：救援后 mode-9 共享分叉

## 最近邻正文核查

1. **Goulart--Kerrigan 2007**：精读问题设定、finite-horizon affine output-feedback 凸化、
   robust constraints 与 invariant error approximation。已有方法可保证仿射输出反馈的有限时域
   约束；无限时保证仍需误差不变集、终端和移位条件。
2. **Hempel--Kominek--Werner 2011**：重读 Section III-A--C、Definition 2、Theorem 1 与
   式(3)--(14)。量词是对同一 admissible output/fiber 先选一个输入，再覆盖全部隐藏状态、
   扰动与模型顶点。
3. **Houska 2023/2026**：重读 Section 6.5、Theorem 3 证明。information-set feedback 与
   extreme controls 已是一般近邻，一步实例不具算法首次性。

## 差异、基线和证明义务

Run157 已使 `J_14` 在 edge `8->9` 后恢复速度安全。本轮最强同条件基线是该 exact rescued
mode-9 set。当前决策必须在 packet outcome 未知时固定同一 `deltaT=K_v d_v`，然后同时检查
`9->10 miss` 与 `9->0 success`。两支真实 `e` 动力学相同，但 estimator update 和测量噪声
不同；因此必须保留共享物理 residual，分别核查 estimator envelope，并 robustly 满足输入盒。

## 推动作用与可证伪条件

若不存在共享 gain，则 Run157 的局部救援不能穿过第一个真实分叉；若存在，只解除一步状态/
输入阻塞，仍必须构造按 target `last_return` 分组的 recurrent container。任一 branch 的
`|e_p|>1`、`|e_v|>11/4`、estimator edge 不包含或输入 support 超盒即推翻候选见证。

## 判断

**通过 exact shared-branch safety witness；不通过 target inclusion、gain 最优性、RCI、终端
或递归可行性声明。**
