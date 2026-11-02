#!/usr/bin/env python3
"""Run257: certified two-position p-v correlation strip (not a full CZ filter)."""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path
from check_run255_posterior_bridge import (
    H, J, T, R, NOISE, PULSE, posterior30, bridge, sin_bounds,
)

def acceleration_bounds(rows):
    out = []
    for box in rows[:-1]:
        low, high = box['phi']
        slo = sin_bounds(low)[0]
        shi = sin_bounds(high)[1]
        out.append((-T * shi - R, -T * slo + R))
    return out

def uniform_width(rows):
    acc = acceleration_bounds(rows)
    n = len(acc)
    p0 = posterior30()['p']
    return ((p0[1] - p0[0] + 2 * NOISE['p']) / (n * H)
            + H * sum(F(i+1, n) * (a[1]-a[0]) for i, a in enumerate(acc)))

def success_velocity(y, rows):
    """Every true trajectory satisfies the exact kinematic elimination:
    v35=(p35-p30)/(5h)+h*sum((i+1)/5*a_i), a_i=-T*sin(phi_i)+r_i.
    p30 and p35 measurement strips yield a sound velocity outer interval.
    """
    acc = acceleration_bounds(rows)
    n = len(acc)
    p0 = posterior30()['p']
    lower = ((y - NOISE['p'] - p0[1]) / (n*H)
             + H*sum(F(i+1, n)*a[0] for i,a in enumerate(acc)))
    upper = ((y + NOISE['p'] - p0[0]) / (n*H)
             + H*sum(F(i+1, n)*a[1] for i,a in enumerate(acc)))
    box = rows[-1]['v']
    return max(lower, box[0]), min(upper, box[1])

def zero_success_witness():
    """p30=v30=phi30=omega30=0, r=0, legal shared torque PULSE.
    Bound the irrational sine by exact rational Taylor intervals.
    Intermediate attitude readings may equal actual nonzero states.
    """
    p_lo = p_hi = v_lo = v_hi = phi = omega = F(0)
    for tau in PULSE:
        slo, shi = sin_bounds(phi)
        p_lo, p_hi, v_lo, v_hi, phi, omega = (
            p_lo+H*v_lo, p_hi+H*v_hi,
            v_lo-H*T*shi, v_hi-H*T*slo,
            phi+H*omega, omega+H/J*tau,
        )
    assert phi == omega == 0
    assert -NOISE['p'] <= p_lo <= p_hi <= NOISE['p']
    return p_lo, p_hi

def verify(root=None):
    s30 = posterior30()
    rows = bridge(s30, 5)
    box = rows[-1]['v']
    assert box == (-F(3110667463,2000000000), F(1554705901,1000000000))
    zero = success_velocity(F(0), rows)
    width = uniform_width(rows)
    assert zero[0] < 0 < zero[1]
    assert zero[1] - zero[0] == width
    assert width < (box[1] - box[0]) / 2
    witness = zero_success_witness()
    for y in (rows[-1]['p'][0]-NOISE['p'], F(0),
              rows[-1]['p'][1]+NOISE['p']):
        lo, hi = success_velocity(y, rows)
        assert box[0] <= lo <= hi <= box[1]
        assert hi-lo <= width
    if root is not None:
        root = Path(root)
        cfg = json.loads((root/'configs/planar_baseline.json').read_text())
        assert cfg['plant']['truth_semantics'] == 'defined_discrete_euler'
        assert F(str(cfg['plant']['dt_s'])) == H
        assert F(str(cfg['plant']['gravity_m_s2'])) == T
        assert F(str(cfg['plant']['inertia_kg_m2'])) == J
        assert cfg['sensing']['position_period_ticks'] == 5
        assert cfg['sensing']['max_consecutive_missed_packets'] == 2
        from check_run256_interval_information_limit import observe
        assert observe(rows[-1], {'p':F(0),'phi':F(0),'omega':F(0)})['v'] == box
    return {
        'run':257,
        'evidence':'EXACT_RATIONAL_TWO_POSITION_CORRELATED_H_REP_VELOCITY_OUTER_BOUND',
        'history':'Run254 SSSMMS zero readings through tick30; Run255 pulse ticks30..34',
        'tick35_independent_box_velocity':[str(x) for x in box],
        'tick35_independent_box_velocity_width':str(box[1]-box[0]),
        'tick35_success_zero_position_correlated_velocity':[str(x) for x in zero],
        'tick35_success_zero_position_velocity_width':str(zero[1]-zero[0]),
        'uniform_upper_width_all_nonempty_success_readings':str(width),
        'tick35_miss_velocity_width_unimproved':str(box[1]-box[0]),
        'zero_success_witness_position35_interval':[str(x) for x in witness],
        'scope':'sound two-position kinematic projection with acceleration enclosures, not exact full posterior/CZ; arbitrary nonempty success readings have uniform width bound; miss has no new position strip',
        'terminal_information_invariance_proved':False,
        'recursive_feasibility_proved':False,
        'gate_A':'blocked',
    }

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--root', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    content = json.dumps(verify(args.root), sort_keys=True, indent=2,
                         ensure_ascii=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(content)
    else:
        print(content, end='')

if __name__ == '__main__':
    main()
