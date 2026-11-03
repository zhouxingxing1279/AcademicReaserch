#!/usr/bin/env python3
"""Run256: a representation-specific limit of independent-box SMF.

This proves a *certificate limitation*, not a physical no-go theorem.
Only measured coordinates are intersected with their own noise strips.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

from check_run255_posterior_bridge import (
    H, J, T, R, U, LIMIT, NOISE, PULSE, posterior30, bridge, step, safe,
)


def width(box, key):
    lo, hi = box[key]
    return hi - lo


def observe(box, readings):
    """Direct-coordinate box measurement update; None denotes empty branch."""
    out = dict(box)
    for key, value in readings.items():
        if key not in NOISE or key == 'v':
            raise ValueError('Only directly observed coordinates can be updated')
        lo, hi = out[key]
        lo, hi = max(lo, value - NOISE[key]), min(hi, value + NOISE[key])
        if lo > hi:
            return None
        out[key] = (lo, hi)
    return out


def serial(box):
    return {key: [str(z) for z in box[key]] for key in ('p', 'v', 'phi', 'omega')}


def width_floor(n):
    """Exact universal lower bound for the Run249/255 box recursion."""
    if n < 0:
        raise ValueError('nonnegative tick offset required')
    return width(posterior30(), 'v') + n * 2 * H * R


def verify(root=None):
    s30 = posterior30()
    p35 = bridge(s30, 5)[5]
    assert safe(p35)
    assert p35['v'] == (-F(3110667463, 2000000000), F(1554705901, 1000000000))
    readings = {'phi': F(0), 'omega': F(0)}
    miss35 = observe(p35, readings)
    success35 = observe(p35, {**readings, 'p': F(0)})
    assert miss35 is not None and success35 is not None
    assert miss35['v'] == success35['v'] == p35['v']
    assert width(success35, 'p') < width(miss35, 'p')
    assert width(success35, 'v') > width(s30, 'v')

    # Nonempty edge-position readings also leave v unchanged in box SMF.
    for y in (p35['p'][0] - NOISE['p'], F(0), p35['p'][1] + NOISE['p']):
        post = observe(p35, {**readings, 'p': y})
        assert post is not None and post['v'] == p35['v']

    increment = 2 * H * R
    assert increment == F(3246383, 40000000)
    assert width(s30, 'v') == F(269364701, 100000000)
    assert width(p35, 'v') == F(6220079265, 2000000000)
    assert width(p35, 'v') >= width_floor(5)
    assert width_floor(40) == F(594003001, 100000000)
    assert width_floor(41) == F(1204237917, 200000000)
    assert width_floor(40) <= 2 * LIMIT['v'] < width_floor(41)

    # For any legal torque, the independent interval step has v-width
    # at least old width + 2*h*R; direct-coordinate updates cannot shrink v.
    for torque in (-U, -F(1, 25), F(0), F(1, 25), U):
        nxt = step(success35, torque)
        assert width(nxt, 'v') >= width(success35, 'v') + increment
        after = observe(nxt, {'phi': F(0), 'omega': torque})
        assert after is not None and width(after, 'v') == width(nxt, 'v')

    if root is not None:
        cfg = json.loads((Path(root) / 'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert F(str(cfg['domain']['input_upper'][1])) == U
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        import sys
        sys.path.insert(0, str(Path(root) / 'verification'))
        import check_four_state_shielded_smf_mpc as prior
        assert prior.step(s30, PULSE[0]) == bridge(s30, 1)[1]
        assert prior.step(bridge(s30, 4)[4], PULSE[4]) == p35

    return {
        'run': 256,
        'evidence': 'EXACT_RATIONAL_REPRESENTATION_SPECIFIC_BOX_SMF_WIDTH_NO_GO',
        'history': 'Run254 SSSMMS all-zero readings through tick 30',
        'start_tick': 30,
        'start_posterior_box': serial(s30),
        'tick35_unconditioned_prediction': serial(p35),
        'tick35_miss_zero_attitude_posterior': serial(miss35),
        'tick35_success_zero_readings_posterior': serial(success35),
        'tick35_success_and_miss_velocity_identical': True,
        'per_step_velocity_width_floor_increment': str(increment),
        'tick70_universal_velocity_width_floor': str(width_floor(40)),
        'tick71_universal_velocity_width_floor': str(width_floor(41)),
        'velocity_hard_box_total_width': str(2 * LIMIT['v']),
        'first_tick_width_floor_exceeds_hard_box': 71,
        'quantifiers': 'any causal legal torque; any nonempty direct-coordinate measurement updates; while the box step remains defined and no safety-box clipping is used',
        'scope': 'Run249/255 independent-box recursion, fixed thrust and disturbance bound; NOT the exact correlated posterior, CZ or the physical plant',
        'physical_unsafety_proved': False,
        'terminal_information_invariance_proved': False,
        'gate_A': 'blocked',
    }


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    content = json.dumps(verify(args.root), sort_keys=True, indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content)
    else:
        print(content, end='')


if __name__ == '__main__':
    main()
