# 研究短检查点（2026-10-03，Run 147）

主线为传统 SMF/输出反馈 Tube MPC，学习暂停。基于远端 Run146 `160952c` / tree
`5f039e1`；远端 `main=1c49659`。合同固定15模态/17边、共享原语、初始化
`mode=0,d=e-eta=0`，控制只读取可见 `d`。

Run147精读 Houska 2023 information ensemble 的控制不变性、极端集合和多面体 tube，
重读 Hempel 2011 noisy-output fiber 量词，并复核2026 zonotope-LP近邻；不作创新声明。

排重发现 Run146 下一问题已被 Run143否定：14条miss后固定`d=0`仍必须保留完整`E_14`，
不能先压缩`q|d`。本轮改为构造强制`14->0 success`的完整相关return image。精确证书含
106列共享原语生成元，affine-hull rank为3，且恒满足`d_v=(9/2)d_p`。完整`eta`投影落入
mode-0竖直盒，完整真实误差支持为
`(23312147/48000000,152955031/72000000)`，满足`|e_p|<=1,|e_v|<=11/4`；尽管`d_v`
超过Run146 product target约`0.641398`。这只是必达seed，不是RCI或全六状态保证。

当前回归：`verification/`188/188、`tests/`39/39。下一唯一问题：为5/10/15 tick三种
success return构造相关seed，并判断是否存在满足真实约束且容纳三者的单一mode-0模板；
通过后才准入controlled predecessor综合。
