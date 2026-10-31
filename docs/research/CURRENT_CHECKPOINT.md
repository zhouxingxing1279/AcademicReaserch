# 当前研究检查点 — Run217（2026-10-31）

**主方向：** 四旋翼/无人机MPC＋SMF闭环；仅按可验证结果收敛课题，不预先锁死子方向。

**本轮瓶颈：** Run216第193拍五拍负速度约束在(p,v)×(phi,omega)乘积H外包下严格阻塞（最有利控制后约-0.0363203688）。本轮构造跨(p,v,phi,omega)的历史一致4D H-strip，并使用单条带精确Fraction标量对偶，直接改善控制相关方向的可靠支持上界。它是必要条件外包，**不是完整CZ后验**。

**严格数学增量：** 通过已执行力矩与冻结Euler姿态动力学反推历史phi_i，导出 |p_k-(k-a)h v_k-A phi_k+B omega_k-(y_a+D)|<=R。每条带的支持上界由min_lambda[h_(Ppv×Pao)(q-lambda*c)+lambda*d+|lambda|R]计算；单条带交集非空时精确，多条带逐个取最小仅为外支持。O(n)力矩加权后缀计算已实现。

**本地验证：** Linux/Python3.13标准库，6/6单元测试、py_compile通过；14条附加确定性历史的无噪声恒等式验证；合成相关集合支持2→1/5（不是实际第193拍）。人工6包/11+6顶点负载下构造6条带中位约5.28ms，6次对偶中位约19.39ms，串行约24.66ms，**尚不满足20ms周期**。源码/测试Git Blob SHA为 ede966c9c328ced7e713a1b377f609b11cbc2ebf / 017f4ff9fdef0ecc2a26b01f03eaa4b561455fd6。

**集成边界：** 本地容器无法通过网络克隆GitHub完整仓库，run_tick193()仅作为真实仓库入口，**尚未执行**；第193拍真实支持改善、是否消除单行阻塞及控制可行性均未知。完整回归及GitHub CI未执行，不得虚报。

**工件：** verification/check_cross_block_history_support.py、verification/test_cross_block_history_support.py、results/cross_block_history_support_20261031/checks.json、docs/research/run217_research_log.md。docs/literature/PAPER_READING_LOG.md维持87篇去重记录，Scott等（2016）本轮只核对原稿摘要、书目和既有分节记录。

**Gate A=blocked：** 尚无完整历史一致4D CZ、真正MPC优化、终端受控不变集、递归可行性/稳定性或六状态安全证明。数学局部证据不能升级为全时域鲁棒安全。

**下一轮唯一优先任务：** 在完整仓库checkout运行第193拍跨块支持集成，比较精确改善量与0.0363203688阻塞门槛并记录时间；未消除阻塞则改进多条带联合支持/增量计算，优先保持可复现负面结果。
