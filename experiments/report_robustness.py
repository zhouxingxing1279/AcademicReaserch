"""Generate the disturbance-first report from retained evidence."""
import json
from pathlib import Path
from experiments.robustness import OUT


def main():
    r = json.loads((OUT/'results.json').read_text(encoding='utf-8'))
    audit = json.loads((OUT/'replay_audit.json').read_text(encoding='utf-8'))
    cases = r['summaries']
    legal = [s for s in cases if s['in_contract']]
    text = [
        '# 抗扰性能验证结果（2026-11-04）', '',
        '本轮按用户明确的抗扰目标评价约束满足、可行性和扰动承受范围。'
        '跟踪RMSE不作为主判据。事前方案见[抗扰预登记](ROBUSTNESS_PLAN.md)。'
        '本轮保留原CZ/pair估计器、统一Tube、控制增益和约束，未修改控制算法。', '',
        '## 结论与证据边界', '',
        f'- 完成{len(cases)}条计划轨迹（含提前停止），实际保存{sum(s["axis_steps"] for s in cases)}个分轴步。'
        f'其中{len(legal)}条合同内轨迹全部完成，'
        f'{sum(s["all_checks_pass"] for s in legal)}条通过全部数值检查。',
        '- 当前结果支持指定数学合同内的鲁棒基线；尚未证明CZ相对于pair提高可认证抗扰上限。'
        '两者使用相同E、Tube和收紧预算，因此本构造的解析边界本来就相同。',
        '- 固定设计a=0.02在实际扰动0.04时已出现真值包含失败，即使名义QP与原硬约束检查仍通过。'
        '不能把“QP有解”或“有限仿真未越界”当作合同外鲁棒保证。',
        '- 0.08及以上的部分CZ场景出现空后验；这是额外量测约束发现模型/数据不一致，'
        '不能仅凭pair继续运行就断言pair更抗扰。空后验停止也不是经证明的安全回退。', '',
        '## 1. 当前统一Tube的解析扰动预算边界', '',
        '固定T=0.5、噪声半径0.005、初始误差盒(0.005,0.01)、状态限幅(3,2)、输入限幅4。'
        '按当前误差界E的所有分段仿射候选计算：', '',
        r'\[\delta=a+4E_p+3E_v,\quad s_p=\delta/4,\quad s_v=\delta,\quad m_u=3a+16E_p+12E_v.\]', '',
        '要求s_p<3、s_v<2、m_u<4，并检查初始盒准入。'
        'Fraction逐一求解所有候选线性不等式，得到下面严格正预算的上界（不含端点）。'
        '这是每个a重新设计E/Tube时的构造边界，不能用于扩大固定a=0.02控制器的保证。'
        '非空终端不等于任意初值QP可行；这个边界也不是系统最优抗扰极限。', '',
        '| M | L | 严格上界（精确分数） | 数值 | 活跃约束 |',
        '|---|---|---|---|---|',
    ]
    for b in r['budgets']:
        text.append(f'| {b["M"]} | {b["L"]} | {b["strict_upper_fraction"]} | {b["strict_upper"]:.8f} | {b["active_constraint"]} |')
    text += ['', '默认M=L=1时，a<82/1775≈0.04619718；16组的最先耗尽项均为输入预算。'
             '无失测、无延迟时上界约0.37333；M=L=3时仅约0.005783，显示观测条件与扰动承受预算之间的权衡。', '',
             '### 名义初值可行性网格', '',
             '每个扰动设计界分别用21×17个二维名义初值检查时域12的线性约束可行性，'
             '使用LP并独立检查约束残差。不是连续可行域体积，也不是三轴独立统计样本。', '',
             '| 扰动设计界a | 可行点/357 | 不可行点 | 未决 |', '|---|---|---|---|']
    for g in r['feasible_grid']:
        if g['status'] == 'evaluated':
            text.append(f'| {g["a"]} | {g["feasible"]} | {g["infeasible"]} | {g["unresolved"]} |')
        else:
            text.append(f'| {g["a"]} | 无正预算 | — | — |')
    text += ['', '## 2. 固定控制器的合同内验证', '',
             '设计界a=0.02；M=L=1。136条合同内轨迹包括36条边界噪声/确定性压力轨迹和'
             '50个随机种子×2种估计器。每条三轴轨迹60拍，扰动在第20拍开始。'
             '逐步检查真值包含、统一估计界、Tube、状态与输入约束、名义移位和代价下降，失败计数全部为0。', '',
             '| 全过程指标（含初始状态） | 合同内最小裕度 |', '|---|---|',
             f'| 位置约束裕度 | {min(s["min_p_margin"] for s in legal):.8f} |',
             f'| 速度约束裕度 | {min(s["min_v_margin"] for s in legal):.8f} |',
             f'| 输入约束裕度 | {min(s["min_input_margin"] for s in legal):.8f} |', '',
             '这些初值没有逼近约束边界，因此较大实测裕度不证明所有可行初值都同样宽裕。'
             'a=0.03、0.04的重新设计只执行了预算和初值可行性扫描，没有运行对应重新设计闭环。', '',
             '## 3. 合同外压力测试：完成、停止与保证失效分别统计', '',
             '每行9条压力轨迹：3种交付表×3种扰动形状。0.5和1倍为合同内，其他为合同外。'
             '“完成”只表示运行到末拍，不代表包含、Tube或安全保证成立。'
             '包含/Tube失效列按轨迹计数，可与其他列重叠；提前停止后的表现未知。', '',
             '| 实际扰动倍数 | 估计器 | 完成/9 | 空后验停止 | 硬约束停止 | 有包含失败 | 有Tube失败 |',
             '|---|---|---|---|---|---|---|']
    for factor in [.5, 1, 2, 4, 8, 16, 32]:
        for mode in ['cz', 'pair']:
            ss = [s for s in cases if s['profile'] != 'random' and s['factor'] == factor and s['mode'] == mode]
            counts = [sum(s['status'] == label for s in ss) for label in
                      ['completed', 'estimator_contract_error', 'hard_constraint_violation']]
            counts += [sum(s['counts'][label] > 0 for s in ss) for label in ['containment', 'tube']]
            text.append(f'| {factor:g} | {mode} | '+ ' | '.join(str(v) for v in counts)+' |')
    text += ['', '所有提前停止均保留在结果中。本轮没有QP不可行或求解未决记录；'
             '这与名义状态独立传播有关，不代表实际轨迹安全。32倍实际扰动a=0.64时，'
             '6条轨迹因输入约束违反停止；这是抽象系统中计算命令的越界，不是执行器实测。', '',
             '| 硬约束停止场景 | 估计器 | 首次步k | 最小输入裕度 |', '|---|---|---|---|']
    for s in cases:
        if s['status'] == 'hard_constraint_violation':
            text.append(f'| {s["delivery"]}/{s["profile"]} | {s["mode"]} | {s["failure_step"]} | {s["min_input_margin"]:.6f} |')
    text += ['', '## 4. 50组合同内随机成对比较', '',
             '统计单位是一条完整三轴轨迹；每个种子共用初值、外生噪声、扰动及交付表。'
             '指标为扰动施加后的峰值；保留测量噪声影响，没有减去零扰动对照，不能解释为严格的扰动诱导增益。'
             '区间为5000次轨迹级配对bootstrap的描述性95%区间，不构成总体等效性证明。', '',
             '| 指标 | CZ均值 | pair均值 | CZ−pair均值 | 95%区间 |', '|---|---|---|---|---|']
    names = dict(peak_p_after_onset='峰值位置偏移', peak_v_after_onset='峰值速度', peak_u_after_onset='峰值输入')
    for key, s in r['paired_statistics'].items():
        lo, hi = s['interval95']
        text.append(f'| {names[key]} | {s["cz_mean"]:.8f} | {s["pair_mean"]:.8f} | '
                    f'{s["mean_cz_minus_pair"]:.8g} | [{lo:.8g}, {hi:.8g}] |')
    text += ['', '峰值位置差异仅为浮点舍入量级，速度差异区间跨0；CZ的峰值输入略高。'
             '这些结果没有提供CZ额外抗扰优势的证据，也不能否定其他设计中保留相关性的价值。', '',
             '合同内12条pulse轨迹在脉冲结束时已经处于事前规定的|p|≤0.05、|v|≤0.1邻域，'
             '且保持至结束，因此恢复时间均为0。该指标在这批场景中没有区分力；本轮不事后缩小阈值制造差异。'
             '后续可事前定义更接近约束边界的初值、不同恢复邻域及独立零扰动对照。', '',
             '## 5. 复核与局限', '',
             '- 32项活动测试通过，包括新增的精确预算表达式/浮点实现交叉检查、外生刺激合法性、恢复时间定义和异常停止保留。',
             '- 原328端点有限记忆证书、64实例/8976联合顶点启动门证书均复核通过，未改写原结果。',
             f'- 保存数据重放{audit["cases"]}条轨迹、{audit["axis_steps"]}分轴步；'
             f'最大重放残差{audit["maximum_replay_residual"]}，'
             f'{audit["estimator_failure_stops_reproduced"]}次空后验停止逐一复现。'
             '检查源码与刺激哈希、初值、量测重建、估计选点、控制律、真实/名义传播和五类包含/约束标志。',
             '- 重放复用同一估计器库，没有重新求解MPC最优序列或独立重证移位结论；不是外部审稿、向外舍入认证或物理验证。',
             '- 脚本生成时曾有换行转义语法错误，在实验前修复。首次结果汇总漏计初始时刻的状态裕度；'
             '修正后完整复跑，模型、刺激、阈值和控制器未改变。最终报告的裕度包含初始状态。',
             '- 仅对照CZ与pair，两者共享鲁棒Tube架构。尚未与非鲁棒MPC或其他鲁棒控制方法比较，'
             '因此不能把当前结果提升为“SMF+MPC相对普通MPC的抗扰提升已经验证”。', '',
             '## 6. 下一研究验收', '',
             '下一阶段以相同输入/状态约束下扩大可认证扰动范围、鲁棒初始可行域、失测/延迟容忍域为主目标。'
             '优先研究信息模式误差管与可移位收紧；只有全边包含、初始化和终端义务通过后，'
             '才能与本轮统一Tube抗扰边界公平比较。跟踪精度作为辅助指标。', '',
             '## 7. 复现与文件', '',
             '```powershell', './.venv/Scripts/python.exe -m unittest discover -s tests -v',
             './.venv/Scripts/python.exe -m experiments.robustness',
             './.venv/Scripts/python.exe -m experiments.validate_robustness',
             './.venv/Scripts/python.exe -m experiments.report_robustness', '```', '',
             '- [全部结果、环境和源码哈希](../../../experiments/results/robustness/results.json)',
             '- [固定外生刺激](../../../experiments/results/robustness/stimuli.json)',
             '- [逐步轨迹及失效标志](../../../experiments/results/robustness/trajectories.csv)',
             '- [重放审计](../../../experiments/results/robustness/replay_audit.json)',
             '- [测试日志](../../../experiments/results/robustness/tests.log)', '',
             '实验设计过程使用本机experimental-design技能组织事前计划、同刺激配对和轨迹级统计。'
             '其附带书目在线核验入口不可用，本报告不将该书目作为控制理论或实验结果的证据。', '']
    target = Path('docs/research/proposal/ROBUSTNESS_RESULTS.md')
    target.write_text('\n'.join(text), encoding='utf-8')
    print(str(target))


if __name__ == '__main__':
    main()
