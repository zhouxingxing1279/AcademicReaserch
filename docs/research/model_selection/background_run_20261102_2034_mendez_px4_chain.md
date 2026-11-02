# 背景第26轮：Mendez等(2023)四旋翼风预报MPC与PX4归一化混控接口审计

日期：2026-11-02 UTC。任务：仅文献/模型/执行器接口证据，不开发主任务控制器、验证脚本或并行算法。基准main：`791dcb899f21b0ed214e900d3c425e159e83bacd`。本轮唯一问题：开源标准四旋翼分配器是否足以从上层虚拟输入推断**真实逐桨硬约束和共同可实现域**？

## 1. 已读原始论文、阅读范围与书目
Arthur P. Mendez, James F. Whidborne, Lejun Chen (2023), *Wind Preview-Based Model Predictive Control of Multi-Rotor UAVs Using LiDAR*, *Sensors* 23(7):3711, DOI https://doi.org/10.3390/s23073711，开放原文 https://pmc.ncbi.nlm.nih.gov/articles/PMC10098597/ （出版社 https://www.mdpi.com/1424-8220/23/7/3711）。**2026-11-02阅读全文HTML §1–4**，核验§2.1–2.4式(1)–(18)、Tables 1–3、§3.1–3.5 Tables 4–5及§4。HTML无稳定纸页码；没有逐页PDF排版审校，未独立重现优化、气动模型或仿真。真实论文且直接使用四旋翼MPC；仅有仿真，不能写成实飞。

## 2. 论文模型、输入、量测和优化
- 物理平台Draganflyer X-Pro，m=2.36kg，J=diag(0.1676,0.1686,0.2974)kg m²，臂长0.45m；6自由度Newton–Euler＋单桨气动/阻力非线性仿真，零风悬停线性化后外环**12状态**`(x,y,z,u_b,v_b,w_b,φ,θ,ψ,p,q,r)`，机体系速度不可误当惯性系。线性模型`xdot=A x+Bu u+Bw w`，离散采样0.1s；无明确实际电机转速动态/饱和最坏界。
- 上层MPC输入**4个虚拟需求**：高度、俯仰、横滚、偏航。内环4个PID给出collective、pitch、roll、yaw控制量；§2.2逐桨转速命令`Ω_i`是这些量的±组合，不能等同于物理推力分配已认证。MPC是增量LTI＋风预报，阶段输出跟踪/Δu二次成本，`MΔU≤γ`、Hildreth QP，N_p=N_c=10（1s，0.1s）；数值电机速率/饱和约束、终端集合/代价和单次求解最坏时间**未报告/无法从全文确认**。
- MPC输出`y=(x,y,z,u_b,v_b,w_b,p,q,r)`，KF实际测量`z=(x,y,z,u_b,v_b,w_b,φ,θ,ψ)`，估计三轴角速；论文没有每5拍位置机会、连续两次丢包的量测合同，也没有状态SMF/CZ。地面LiDAR测量风，真实LiDAR数据用于**仿真输入**，非真实飞行闭环。
- §3.3非线性阵风仿真：位置约±0.2m（有预报）对±0.6m（无预报），约66%改善；§3.5风预报时差/幅度敏感性为**仿真性能阈值**，非硬安全/递归可行证明。没有实飞、20ms WCET、状态集合真值包含或无限终端安全。

## 3. PX4独立开源源码核验（非论文配套）
固定PX4-Autopilot `216039a12bab5a86769128f7be3e5f63dc7b4952`：
- `src/modules/control_allocator/ControlAllocator.cpp` Blob `82bbb624fae229a54f74782b5480d961de199ab6`，主路径：`setControlSetpoint`→`allocate`→`updateSetpoint`→`handle_stopped_motors`→（若开启）`applySlewRateLimit(dt)`→`clipActuatorSetpoint`→`publish_actuator_controls`。非可逆电机归一化最小0最大1；`actuator_motors`是输出到驱动的**归一化推力命令**，不是实测牛顿推力。分配器状态含未分配力矩/推力和饱和标志。
- `src/lib/control_allocation/control_allocation/ControlAllocationSequentialDesaturation.cpp` Blob `4b28f44dacb9f4c7ffa26a5115aca0efda75a8b3`：顺序消饱和依MC_AIRMODE可能牺牲某些控制通道，**请求wrench≠必然实现wrench**。
- `src/lib/control_allocation/control_allocation/ControlAllocation.cpp` Blob `7278108a8cae320cc86c196d9f717e3966df5546`：归一化裁剪；可选速率限制`Δa_max=dt*(a_max-a_min)/CA_Ri_SLEW`。
- `src/modules/control_allocator/module.yaml` Blob `8571373930f4c4c966bee9ae2ee4e676ef9d526f`：`CA_R{i}_SLEW`默认0.0（**限速关闭**），非零表示完整归一化行程所需秒数。独立Python Fraction：`dt=1/50s`，若配置`S=1/10s`且`[0,1]`，则`Δa_max=1/5=0.2`；默认S=0不应用该限制。这是**源码/代数核验**，不是真实ESC物理响应认证。
- PX4文档 https://docs.px4.io/main/en/concept/control_allocation 、消息 https://docs.px4.io/main/en/msg_docs/ActuatorMotors 。未读具体PWM/DSHOT驱动/硬件数据、未验证真实RPM-推力关系；PX4也不是Mendez论文对应的飞控。

## 4. 与主任务及模型矩阵关系
截至基准main，主任务Run274已在冻结4状态Euler、T=9.81N、τ=0下认证60–90拍**完整可靠外包的有限安全**，但90–105拍全部后验门槛、终端信息RCI、无限递归可行、六状态物理安全、20ms WCET仍缺失，Gate A=blocked。**不将PX4归一化clip当作执行器物理保证，也不将Mendez风预报当作本仓库已有观测权限。**
条件性首选六状态平面`(p_x,p_z,v_x,v_z,φ,ω)`、`(T,τ)`不变；4状态有限数学基线，2状态姿态保底，12状态/分层作为文献对照。主任务建议的接口是：
`a_k = Allocation(u_k,geometry,mode,a_{k-1},dt)`，`f_k∈F(a_k,f_{k-1},ESC_uncertainty)`，`w_k=G f_k`，`w_k-u_k∈E_k`。必须针对同一SMF后验观测纤维检验共同命令、实际推力与硬盒，不能只检查归一化命令在[0,1]。SMF/CZ可用于维护`f_{k-1}`的集合并收紧可用wrench，但是否优于简单区间/参数固定边界仍待对照；“首次SMF+MPC”不能成立。

## 5. 检查、证据级别与下一轮
论文DOI/题名按唯一总账去重；4个PX4源码文件固定commit及Blob核验；算术`1/50 ÷ 1/10 = 1/5`、`1/0.1=10`通过。仅文档/源码静态检查，**没有运行PX4、SITL、飞行、主任务闭环测试、完整SMF/CZ、终端安全或执行器辨识**。若仓库文档检查/PR CI缺席，必须明确报告，不能宣称通过。
**下一轮唯一优先问题**：沿固定PX4版本继续审查归一化`actuator_motors`到具体PWM/DSHOT输出映射，并寻找标准单向四旋翼ESC RPM→实际推力的可用有界实验数据，判断能否给主任务建立确定性`E_k`外包；无数据则明确需要本机体标定，不凭默认参数造界。
