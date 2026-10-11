# 研究短检查点（2026-10-11，Run159）

主线：传统 SMF/鲁棒输出反馈 MPC；学习暂停。远端 `main=1c49659`、Run158=`400a505`；控制只读可见 `d=e−eta`。

Run159 重读 Goulart--Kerrigan 2007 robust affine output-feedback constraints、Yang--Ozay 2021 dropout-string safety 与 Houska information-set feedback。纠正 Run158 下一步：`(0,15)` 的 rescued returns 尚未走到 final success，不能直接合并。对 `J14` 经8 miss后的 age-8 exact set，三条后续 miss 的零输入 mode-11 位置support为 `3714127151/3600000000`；age8/9两次 bounded centered affine correction 最多削减 `3h²U`，故任意该类策略仍有 `h_ep>=369867929/360000000=1+9867929/360000000`，严格违反 `|e_p|<=1`。因此当前 fixed-global-residual、correction盒和seed下 `15->15` constituent不可行，安全 `(0,15)` target hull不能构造。证据仅为 exact path-level affine-class obstruction，不是一般output-feedback不可行、RCI或递归可行性。

下一唯一问题：从 `J14` return seed（mode0）即开始联合综合整个15步周期，判断更早 affine correction 能否在不破坏硬约束下把 age-8 source 缩至本轮必要阈值。
