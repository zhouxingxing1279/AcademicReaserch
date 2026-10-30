#!/usr/bin/env python3
"""Exact four-state lateral-attitude dropout support audit, not an MPC controller.

For x=(px,vx,phi,omega), the frozen linear reduced dynamics are
  px+ = px + h vx
  vx+ = vx - h T phi + h r_x, |r_x| <= 47/25 + 243*T/16000
  phi+ = phi + h omega
  omega+ = omega + (h/J) tau.
No lateral position/velocity observation occurs during the audited gap.
The two adversarial paths share every attitude/omega observation and input.
"""
import argparse
import json
from fractions import Fraction as F
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def contract(root=ROOT):
    c = json.loads((root / 'configs/planar_baseline.json').read_text(), parse_float=F)
    graph = c['mpc']['ancillary_rci_contract']['disturbance_graph']
    assert graph['physical_residual_halfwidth']['r_x'] == '47/25 + (243/16000) * actual_thrust'
    assert c['state_order'] == ['px', 'pz', 'vx', 'vz', 'phi', 'omega']
    assert c['sensing']['always_observed_indices'] == [4, 5]
    assert c['sensing']['position_indices'] == [0, 1]
    assert c['initial_set']['center'][0] == 0 and c['initial_set']['center'][2] == 0
    h = c['plant']['dt_s']
    j = c['plant']['inertia_kg_m2']
    tmin, tmax = c['domain']['input_lower'][0], c['domain']['input_upper'][0]
    p0, v0, ph0, om0 = (c['initial_set']['halfwidth'][i] for i in (0, 2, 4, 5))
    period = c['sensing']['position_period_ticks']
    misses = c['sensing']['max_consecutive_missed_packets']
    assert h > 0 and j > 0 and tmin > 0 and tmax >= tmin
    assert period == 5 and misses == 2
    assert c['sensing']['observed_noise_halfwidth']['px'] >= p0
    return dict(h=h, j=j, tmin=tmin, tmax=tmax, p0=p0, v0=v0,
                ph0=ph0, om0=om0, period=period, misses=misses,
                p_limit=c['domain']['state_upper'][0])


def radius(t):
    return F(47, 25) + F(243, 16000) * t


def step(x, t, tau, r, h, j):
    p, v, phi, omega = x
    return (p + h*v, v - h*t*phi + h*r,
            phi + h*omega, omega + h*tau/j)


def floor(schedule, c):
    """Exact unavoidable p radius for independent initial px,vx and r_x."""
    n = len(schedule)
    return (c['p0'] + n*c['h']*c['v0'] + c['h']**2 *
            sum((n-1-i)*radius(t) for i, t in enumerate(schedule)))


def pair_witness(schedule, c):
    """Two histories indistinguishable by always-on attitude sensors."""
    plus = (c['p0'], c['v0'], F(0), F(0))
    minus = (-c['p0'], -c['v0'], F(0), F(0))
    for t in schedule:
        plus = step(plus, t, F(0), radius(t), c['h'], c['j'])
        minus = step(minus, t, F(0), -radius(t), c['h'], c['j'])
        assert plus[2:] == minus[2:]  # identical phi/omega observations
    return plus, minus


def full_prior_position_radius(schedule, c):
    """Exact p support of full initial box + independent process intervals,
    for a *fixed* input schedule with no measurement updates (zonotope)."""
    generators = [tuple(width if k == i else F(0) for k in range(4))
                  for i, width in enumerate((c['p0'], c['v0'], c['ph0'], c['om0']))]
    for t in schedule:
        generators = [step(g, t, F(0), F(0), c['h'], c['j']) for g in generators]
        generators.append((F(0), c['h']*radius(t), F(0), F(0)))
    return sum(abs(g[0]) for g in generators)


def run(root=ROOT):
    c = contract(root)
    gaps = [c['period']*k for k in range(1, c['misses']+2)]
    rows = []
    for n in gaps:
        low = [c['tmin']]*n
        high = [c['tmax']]*n
        alternate = [c['tmin'] if i % 2 == 0 else c['tmax'] for i in range(n)]
        for name, seq in [('low', low), ('high', high), ('alternating', alternate)]:
            lower = floor(seq, c)
            plus, minus = pair_witness(seq, c)
            upper = full_prior_position_radius(seq, c)
            assert (plus[0]-minus[0])/2 == lower
            assert lower <= upper
            rows.append(dict(gap_ticks=n, thrust_schedule=name,
                             indistinguishable_position_halfwidth=str(lower),
                             no_measurement_prior_position_halfwidth=str(upper),
                             position_bound=str(c['p_limit']),
                             does_not_by_itself_violate_global_position_bound=lower <= c['p_limit']))
    for n in gaps:
        selected = [r for r in rows if r['gap_ticks'] == n]
        assert F(selected[0]['indistinguishable_position_halfwidth']) <= F(selected[2]['indistinguishable_position_halfwidth']) <= F(selected[1]['indistinguishable_position_halfwidth'])
    return dict(status='PASS', evidence='EXACT_FRACTION_FOUR_STATE_REDUCED_CONTRACT',
                model='frozen 4-state lateral-attitude linear proxy',
                sensing='position/velocity unavailable for gap; phi and omega observable every tick',
                proof_scope='pair indistinguishability and exact fixed-input zonotope support; no feedback/terminal/RCI certificate',
                quantifiers='for any causal controls based on identical available histories, adversary can choose opposite independent lateral residuals; low-thrust row is universal lower floor',
                initial_position_halfwidth=str(c['p0']),
                initial_velocity_halfwidth=str(c['v0']),
                time_step_s=str(c['h']),
                residual_at_min_thrust=str(radius(c['tmin'])),
                residual_at_max_thrust=str(radius(c['tmax'])),
                results=rows, gate_A='blocked',
                limitations=['Initial posterior must contain the two displayed extreme states; not guaranteed after arbitrary tick-0 measurement',
                             'A nonzero future position/velocity observation can separate the witness paths',
                             'Full prior support assumes fixed input schedule and omits attitude measurement conditioning',
                             'No controller synthesis, robust terminal set, recursive feasibility, or six-state safety proof'])


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', type=Path, default=ROOT)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    data = json.dumps(run(args.root), indent=2, ensure_ascii=False) + '\n'
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(data)
    else:
        print(data, end='')


if __name__ == '__main__':
    main()
