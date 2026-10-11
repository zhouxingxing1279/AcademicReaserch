# 研究短检查点（2026-10-11，Run154）

主线：传统 SMF/鲁棒输出反馈 MPC；学习暂停。本地 `main=1c49659`，Run153=`a95da0a`；15模态/17边，控制只读可见 `d=e−eta`。

Run154 精读 Houska 2026 §4.2--4.3、§6.3--6.5、Definitions5--7、Theorems1/3。对预先固定的因果策略，含真实 `(0,init)` 初始集的前向历史外包算子单调，其 Kleene 闭包是该策略下的最小 reachable envelope。若每层重选策略，层层可行不对应一张可执行控制器，也无一般跨策略最小闭包。凸化会生成新 `d` fibers，必须对其共享输入、执行器盒和逐边后继重新闭合。`init` 15态只承担首次 return 前瞬态安全；terminal family 可在45个 recurrent states 上闭合，但须覆盖全部首次 return image。当前仅建立项目特化合同，不是 RCI/递归可行性或创新证明。

下一唯一问题：冻结最小可审查类——竖直 affine-in-`d` correction 加 exact lifted convex hull——先证明新增 fibers 上输入可行与单步包含公式；通过后才实现从真实初始化开始的第一轮传播。
