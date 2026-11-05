# 当前CZ/Tube算法的Gazebo接入验证（2026-11-04）

用户要求先验证当前算法。本轮开展经验SITL，不以此前“理论优先”的排期阻止接入，也不提前宣称物理模型映射通过。

固定PX4 v1.17.0、Gazebo Harmonic、X500；保留默认内环与EKF。原算法保持T=0.5、a=0.02、n=0.005、M=L=1和原输入/状态约束、增益、终端。通过MAVLink LOCAL_NED acceleration-only路径发送控制量，20Hz重复保持，外环2Hz按Gazebo时间采样。通过本地固定版本mavlink_receiver.cpp核对字段，不将加速度请求视为理想实际加速度。

模型副本增加Gazebo OdometryPublisher（3维、100Hz）；模型参数不变。真值位置采用Gazebo世界位姿，速度采用相邻位姿差分作为诊断参考，记录差分间隔；不将平滑的body-frame odometry twist直接当世界速度。ENU转NED。初始化用Gazebo参考状态设置初始先验（理想化初始化），之后滤波/控制只接收合成位置量测与执行过的命令。PX4自身EKF不施加丢包。

正常起飞至约3m并稳定，预流position setpoint切入Offboard；算法控制小幅0.2m北向调节。场景固定为fresh/无力、fresh/0.02N世界东向外力、max_gap/同外力。每组最多40个算法周期；外力从算法接入开始施加，4秒后清除。力通过Gazebo ApplyLinkWrench persistent topic施加至X500模型的canonical link。未控制的初期调试失败单列，保留原始日志。

记录：原始Gazebo位姿、PX4局部状态、模式、位置样本/时间戳、命令、估计包含、Tube、原约束、QP状态、计算耗时、采样和发送时序、ZOH一步残差。r_v/T和2r_p/T²分别作为两个等效加速度诊断；二者不一致反映残差不属于单一Bw，不因取最大值而假定合同成立。

包含或模型界失败继续记录（在物理约束范围内）；空后验、QP未决、模式退出、遥测中断或约束越界停止算法，清除外力并请求PX4正常降落。降落为实验监督器动作，不是当前算法已证安全回退。不强制解锁、不禁用飞前检查。所有进程只指向本地模拟器，保留独立Gazebo partition和实验目录。

本轮目标是确认可接入程度和首先失效的假设。任何试验失败不事后放大扰动界或替换控制律以追求通过；后续映射/重设计需单独标识。

接入调试修订：独立加载加装OdometryPublisher的模型出现一次起飞不响应（ULog显示飞控推力请求已达上限但机体未升高），尚不能确定物理插件原因；该调试失败保留。正式测试改为已验收的原始launch-px4.sh/X500，订阅SceneBroadcaster已有的/world/default/dynamic_pose/info，按x500_0筛选模型世界位姿，并记录实际差分间隔。算法与场景参数不变，保留--instrumented选项以复现旧加载方式。
