# Run165：极端可见fiber的完整路径反例

日期：2026-10-12；从Run164本地`08a6945`、远端`dbd3a07`同tree `ded2c20`接续；远端
`main=1c49659`。

## 文献与准入

全文重读Yang--Ozay 2021 Sections 3--4、Definition 3、Propositions 2--5；重读Hempel等2011
Section III-A--C/Theorem 1及Houska等的polyhedral RCI/tube章节既有全文记录；复核Scott等CZ切片。
一般缺测安全游戏、output-fiber共享控制和等式切片均已有，本轮仅准入当前冻结合同的精确反例。

## 核心命题

Run164只证明同一fiber的方向宽度小。取可达极端观测
`d_p=24272147/48000000`，该fiber的`e_p+14h e_v`区间整体位于1之上，下/上端分别为
`3745601423/3600000000`和`3889781459/3600000000`。

允许任意乐观全状态因果反馈后，每拍输入仍受`|delta T|<=U`。14次miss的全部正端residual平移
与最大负输入平移因`g_r=hU`精确相消，所以环境选极端fiber上端点时最终位置至少为
`3889781459/3600000000`，严格超限`289781459/3600000000≈0.08049485`。这是真正的同观测
fiber中心反例，不再混合可区分观测。

证据等级：`reachable_extreme_visible_fiber_full_state_fifteen_tick_obstruction`。它否定当前冻结四状态
合同的15-tick安全保证，不是一般RCI、递归可行或六自由度不可能性。

## 实现与验证

新增Fraction检查器和五项测试，分别锁定极端观测可达性、fiber区间、residual/input精确抵消、
声明边界及哈希绑定复现。浮点轨迹或控制器优化不会提升该策略无关反例的证据等级，故不实现MPC
求解器。基础测试`39/39`、理论验证`235/235`通过；Python编译、JSON复现与`git diff --check`
也纳入最终检查。

## 下一唯一问题

停止当前15-tick合同下的gain/terminal综合。建立同条件三因素的**中心范围**修约门槛：定量求出
极端可见偏差上界、future residual或物理correction authority至少需改变多少，才能消除式(101.2)
反例；随后只对有明确物理/估计来源且可可靠初始化的合同进入完整闭环综合。
