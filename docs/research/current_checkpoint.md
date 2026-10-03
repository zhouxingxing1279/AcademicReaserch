# 研究短检查点（2026-10-03，Run 149）

主线为传统 SMF/输出反馈 Tube MPC，学习暂停。远端 `main=1c49659`；Run148 基线
`390f035`，语义修正 `0f65ef3`。合同为15模态/17边、共享原语，控制只读可见
`d=e-eta`。

Run148已纠正：`C0=conv(J4 union J9 union J14)`只是先行 correction 全零时的 rank-3
reachable baseline；连续 perspective selector 允许分数混合，`C0`零中心不是一般必要
target。

Run149重读 Houska 2023、Hempel 2011、Wehbeh等2026。精确证明：固定绝对余项集时，
correction对miss/success只产生`Delta eta=0, Delta e=Delta d=(0,h Delta deltaT)`中心平移；
scheduled `r_z(T)`则使一步共享联合生成元在`T=4.905->14.715 N`间增加
`79461/4000000`，同时改变形状。Run136 global列等于上端点并覆盖全区间。

证据仅为竖直一步exact interface split，不是RCI/六状态/MPC保证。下一唯一问题：用固定
Run136 envelope，以`C0+c_0`对mode 4/9分叉和14->0 return做带可见中心的exact
shared-input containment；失败只否定fixed-shape translation类。
