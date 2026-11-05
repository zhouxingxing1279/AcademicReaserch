# WSL PX4 / Gazebo 科研验证环境

安装日期：2026-11-04。本环境用于后续算法验证，当前验收仅覆盖基础仿真链路，不表示已验证本项目的 MPC / CZ-SMF 控制器。

同日后续已实际接入当前CZ/Tube MPC并运行4次正式场景；结论为接入成功、现有算法未通过。见[算法SITL验证结果](CZ_SITL_RESULTS.md)，与本页的基础起降验收分开统计。

## 已安装版本

| 组件 | 本机配置 |
| --- | --- |
| WSL 发行版 | `Ubuntu`，WSL2，Ubuntu 24.04.4 LTS |
| PX4 | `v1.17.0`，提交 `d6f12ad1c4f70ad3230afd7d86e971421e02fef4` |
| 仿真器 | Gazebo Harmonic，Gazebo Sim `8.15.0` |
| 默认模型 | X500 四旋翼；另有 RC Cessna 固定翼和 standard VTOL |
| 图形 | WSLg，D3D12 / AMD Radeon 780M；启动脚本显式选择 `GALLIUM_DRIVER=d3d12` |
| Python | Python 3.12.3，独立虚拟环境，包含 pymavlink 和 pyulog |
| 编译 | `px4_sitl_default`，Ninja，最多 4 个并行任务 |

Linux 安装目录为 `/home/alfred/px4-research`，源码在其 `PX4-Autopilot` 子目录。源码与构建产物位于 WSL Linux 文件系统中。已有 ROS 2 Jazzy 保留；ROS 2 / PX4 DDS 通信尚未验收。

## 一条命令启动

在 Windows PowerShell 中执行：

```powershell
wsl -d Ubuntu -- bash /home/alfred/px4-research/bin/launch-px4.sh
```

默认打开 X500 的 Gazebo 窗口和 PX4 控制台。其他模式：

```powershell
# 无图形模式，适合批量科研实验
wsl -d Ubuntu -- bash /home/alfred/px4-research/bin/launch-px4.sh x500 headless

# 固定翼
wsl -d Ubuntu -- bash /home/alfred/px4-research/bin/launch-px4.sh rc_cessna gui

# 垂直起降飞机
wsl -d Ubuntu -- bash /home/alfred/px4-research/bin/launch-px4.sh standard_vtol gui
```

退出时在 `pxh>` 中输入 `shutdown`，必要时用 Ctrl+C 结束启动命令。当前单机入口应一次运行一个实例。模型切换会触发 PX4 自动配置；正式实验请另行记录自己的参数配置。

仓库保留了 [Linux 启动脚本](../../scripts/simulation/launch-px4.sh)、[PowerShell 入口](../../scripts/simulation/Start-PX4.ps1) 和 [验收脚本](../../scripts/simulation/smoke-test.py)。WSL `bin` 目录中有对应脚本副本。

## 自动起降验收

在没有其他 PX4 仿真实例运行时执行：

```powershell
wsl -d Ubuntu -- /home/alfred/px4-research/.venv/bin/python /home/alfred/px4-research/bin/smoke-test.py --flight
```

脚本启动本地 X500，接收 PX4 心跳和局部位置，发送地面站心跳，再请求正常解锁、起飞、降落，检查降落后自动上锁，最后关闭其仿真进程。不会强制解锁或关闭飞前检查。

2026-11-04 验证结果：

- X500：MAVLink 心跳、局部位置估计、起飞、降落、自动上锁通过；最高观测相对高度 **4.759 m**，起飞目标 5 m，测试在超过 4 m 后短暂停留再降落。
- Gazebo GUI：现场确认显示 `x500_0`；渲染日志确认 D3D12 / Radeon 780M，观察时实时速度约 97%，该值不是性能基准。
- RC Cessna：启动、MAVLink 心跳和局部位置通过；尚未执行固定翼飞行任务。
- VTOL：启动、MAVLink 心跳和局部位置通过；未进行转换飞行试验。

验收结果副本在 [validation](validation/)；完整输出在 WSL `/home/alfred/px4-research/logs/`。PX4 ULog 位于 `/home/alfred/px4-research/PX4-Autopilot/build/px4_sitl_default/rootfs/log/`，日志内部使用 UTC 时间。

## 后续实验接口与复现记录

- WSL 内 MAVLink 伴随计算接口：`udpin:127.0.0.1:14540`；地面站默认目的端口为 14550。
- 已有 uXRCE-DDS 客户端使用 `127.0.0.1:8888`；本次未安装/验收 Micro XRCE-DDS Agent、px4_msgs 或 QGroundControl。
- Python 环境：`/home/alfred/px4-research/.venv`。
- `manifest/` 保存 PX4 提交、递归子模块提交、APT 包版本、Python 依赖锁定清单、系统版本、图形信息以及系统安装脚本。
- Python 包安装在独立 venv 中；构建时先 `source /home/alfred/px4-research/.venv/bin/activate`。
- 初始飞前提示（例如尚未连接 GCS）需等待估计器初始化并连接地面站/发送心跳；默认 GUI 启动本身不会提供 GCS 心跳。验收脚本会发送心跳。
- `gz_frame_id` SDF 扩展警告、仿真 LED 设备提示在本次通过的验收中也会出现。
- WSL 启动的 localhost 代理提示不妨碍本地仿真；本次下载所用临时转发已关闭，离线仿真无需该转发。

官方参考：[PX4 v1.17.0](https://github.com/PX4/PX4-Autopilot/releases/tag/v1.17.0)、[该版本 Ubuntu 依赖脚本](https://github.com/PX4/PX4-Autopilot/blob/v1.17.0/Tools/setup/ubuntu.sh)、[Gazebo 飞行器模型](https://docs.px4.io/main/en/sim_gazebo_gz/vehicles.html)。
