# 研究短检查点（2026-10-02，Run 144）

主线为传统 SMF/输出反馈 Tube MPC，学习暂停。基于 Run143 tree `3893f40`；远端
`main=1c49659`。合同固定15模态/17边、actual-input时序、共享原语及只按可见
`d=e-eta`共享输入。

Run144精读 Houska 2023 information ensemble、Hempel 2011 fiber量词及
Kumar--Kothyari 2026 zonotope-LP OFCI。联合信息集和多面体综合已有近邻；本轮不作创新声明。

候选 `S_j=E_eta,vertical^j x {|e_pz|<=1,|e_vz|<=11/4}`，不独立限制`d`。精确证明
modes 4、9、14 的一步 predecessor 均包含
`C_j={eta in E_j,|d_pz|<=1/5,|d_vz|<=1/4,e=eta+d}`。`C_j`为四维正体积；统一
`deltaT=0`同时服务mode4/9的success/miss。全nominal thrust区间的共享residual上界为
`411370817/128000000`。五条关键边eta包含通过；最紧mode14 next tracking余量为位置
`14847853/48000000`、速度`22053067447/57600000000`。证据仅为三个关键一步内证书，
不是RCI、固定点、全六状态或递归可行性。

下一唯一问题：对15模态执行一次joint descending predecessor sweep，报告各模态保留的
observation projection/正体积内集或空集证书；全模态一步非空后才启动固定点迭代。
