# 110. 受控回返前驱的排重与证明对象纠正

Run175把正确量词恢复为`exists causal policy, forall disturbances/dropout paths`，但“冻结策略类并构造
观测fiber前驱”本身并不是新的仓库缺口。Run142已经对二维竖直product-fiber类实现精确前驱：同一
可见`d`上的隐藏状态及所有出边共享一个输入，再对未知量鲁棒化并消去输入。Run160进一步允许两条
镜像轨迹使用不同的任意因果full-state反馈，仍以输入幅值给出J14十五步位置直径下界；因此它是原
output-feedback问题的乐观放宽。

本轮精读Ghaemi--Del Vecchio的Problem 1--2、Theorems 1与4。其information state由初始集合、
已施加输入和测量历史共同定义；控制映射以当前information state为自变量。开环安全量词明确为
`exists u, forall disturbances`，闭环策略还须对全部允许测量历史成立。这支持Run175纠错，但也说明
不能把旧J14/product-fiber结论直接搬到配置初始posterior。

严格区分三个对象：

1. Run142：固定Run136估计zonotope与product结构的线性二维前驱；
2. Run160：固定J14 seed、固定残差合同和修正输入盒的十五步不可能性；
3. 当前未决：配置初始posterior经真实非线性plant、五步测量时序及物理推力输入的return set。

前两者均未回答第三者。故本轮停止重复实现通用前驱。下一证明对象应从配置初始posterior直接定义
五步非线性information-state Bellman/predecessor算子；第一阶段只核查竖直不变切片，同时保留
真实推力、风和测量噪声的共享primitive。若该切片已不可行，才可形成受控回返反证；若可行，再扩展
到横向—姿态联合合同。该排重不构成新算法或递归可行性证明。
