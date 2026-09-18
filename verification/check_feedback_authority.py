#!/usr/bin/env python3
"""Exact authority obstruction and known-input transport; no controller certificate."""
import argparse
import hashlib
import json
from fractions import Fraction as Q
from pathlib import Path
import numpy as np
from check_transport_template import Transport
from check_cz_template import Template, GRID

ROOT = Path(__file__).resolve().parents[1]


def authority_certificate():
    cfg = json.loads((ROOT/'configs/planar_baseline.json').read_text())
    h = Q(str(cfg['plant']['dt_s']))
    inertia = Q(str(cfg['plant']['inertia_kg_m2']))
    tau = Q(str(cfg['domain']['input_upper'][1]))
    phi_max = Q(str(cfg['domain']['state_upper'][4]))
    p_max = Q(str(cfg['domain']['state_upper'][0]))
    t = Transport()
    assert h == t.dt and phi_max == Q('.45') and p_max == 5
    angular_accel = tau/inertia
    p = v = Q(0)
    first = None
    samples = []
    at = {}
    for k in range(357):
        at[k] = p
        if first is None and p > p_max:
            first = k
        if k in (0, 24, 208, 209, 356):
            samples.append({'tick': k, 'position_lower': str(p), 'velocity_lower': str(v)})
        angle_upper = min(phi_max, angular_accel*h*h*k*(k-1)/2)
        p, v = p+h*v, v+h*(t.dx-t.g*angle_upper)
    n = 356
    coeff = h*h*n*(n-1)/2
    critical = (p_max-at[n]+coeff*t.dx)/coeff
    assert first == 209 and at[208] <= p_max < at[209]
    return {'status': 'old_box_not_robustly_viable_from_center_for_any_policy',
            'disturbance': str(t.dx), 'angular_acceleration_limit': str(angular_accel),
            'first_position_failure': first, 'p208': str(at[208]), 'p209': str(at[209]),
            'necessary_D_at_356': str(critical), 'samples': samples,
            'quantifiers': 'fixed +Dx defeats every policy that respects the other constraints; perfect information does not help',
            'scope': 'independent global affine box, not physical nonlinear impossibility'}


class InputTransport(Transport):
    """Freeze an actually known thrust; tau=0 in this verification pilot.

    q includes signed affine offsets and therefore is not a noise radius alone.
    Future feedback-dependent inputs require a joint model, not this class alone.
    """
    def __init__(self, thrust):
        if not isinstance(thrust, Q):
            raise TypeError('thrust must be an exact Fraction')
        if not Q('4.905') <= thrust <= Q('14.715'):
            raise ValueError('thrust outside the certified source domain')
        super().__init__()
        self.thrust = thrust
        self.dx = Q('1.880')+thrust*Q('.45')**3/6
        self.dz = Q('2.086')+thrust*Q('.45')**2/2
        self.f[2, 4] = -self.dt*thrust
        self.w[2, 0], self.w[3, 1] = self.dt*self.dx, self.dt*self.dz
        self.offset = np.array([Q(0)]*6, dtype=object)
        self.offset[3] = self.dt*(thrust-self.g)
        for row in (2, 8):
            col, _ = self.terms[row][1]
            self.terms[row][1] = (col, self.dt*thrust)
        for j in range(1, 16):
            for sign in (1, -1):
                row = self.strip(0, j, sign)
                col, _ = self.terms[row][1]
                self.terms[row][1] = (col, j*self.dt**2*thrust)
        self.q = [sum(abs(v) for v in row @ self.w)+row @ self.offset for row in self.h]


def uniform_bounds():
    t = InputTransport(Q('14.715'))
    ax = t.dx+t.thrust*t.noise[4]
    az = t.dz
    cases = []
    for gap in (5,10,15):
        for age in range(15):
            vals = []
            for a in (ax, az):
                reset = Q('.04')/(gap*t.dt)+t.dt*a*(gap+1)/2
                vals.append((reset+age*t.dt*a+Q(65,GRID),
                             Q('.02')+age*t.dt*reset+t.dt**2*a*age*(age-1)/2+Q(100,GRID)))
            cases.append(vals)
    return {'max_acceleration': [str(ax),str(az)],
            'max_velocity_halfwidth': [str(max(c[i][0] for c in cases)) for i in (0,1)],
            'max_position_halfwidth': [str(max(c[i][1] for c in cases)) for i in (0,1)],
            'gap_age_cases': len(cases)}


def input_path_check(ticks=120):
    # Prescribed square-wave thrust, not a synthesized feedback policy.
    values = [Q('9.61'),Q('10.01')]
    maps = [InputTransport(v) for v in values]
    for t in maps:
        for i, terms in enumerate(t.terms):
            lhs = sum((w*t.h[j] for j,w in terms), np.array([Q(0)]*6))
            assert np.array_equal(lhs,t.h[i] @ t.f)
            assert all(w >= 0 for _,w in terms)
    def model(k):
        return maps[(k//5)%2]
    def chain(b,k):
        result=[b]
        for j in range(25):
            result.append(model(k+j).predict(result[-1]))
        return result
    b = maps[0].initial()
    x = np.array([Q('.005'),Q('-.004'),Q('.03'),Q('-.02'),Q('.001'),Q(0)],dtype=object)
    old = None
    shift = members = 0
    peak = [Q(0)]*2
    bounds=uniform_bounds()
    cap=list(map(Q,bounds['max_velocity_halfwidth']))
    digest=hashlib.sha256()
    for k in range(ticks+1):
        if k:
            previous=model(k-1)
            x=previous.f @ x+previous.offset
            b=old[1]
        t=model(k)
        indices=[4,5]+([0,1] if k%15==0 else [])
        y=[x[i]+t.noise[i]*Q((-1)**(k+j),2) for j,i in enumerate(indices)]
        b=t.update(b,indices,y)
        for i in (0,1):
            width=(b[i+2]+b[i+8])/2
            assert width<=cap[i]
            peak[i]=max(peak[i],width)
        cz_template=Template(t.h,b)
        cz,latent=cz_template.to_cz(),cz_template.witness(x)
        assert all(abs(v)<=1 for v in latent)
        assert np.array_equal(cz.c+cz.g @ latent,x)
        assert np.array_equal(cz.a @ latent,cz.b)
        members+=1
        new=chain(b,k)
        if old is not None:
            for i in range(25):
                assert all(a<=c for a,c in zip(new[i],old[i+1]))
                shift+=72
        old=new
        digest.update(('|'.join(map(str,b))+'\n').encode())
    return {'ticks':ticks,'shift_rows':shift,'posterior_memberships':members,
            'thrust_values':list(map(str,values)), 'peak_velocity_halfwidth':list(map(str,peak)),
            'posterior_hash':digest.hexdigest(),
            'scope':'known varying input path, affine witness only; no nonlinear safety or feedback certificate'}


def run():
    old=Transport()
    new=InputTransport(Q('14.715'))
    assert old.dx-new.dx == Q('4.905')*Q('.45')
    result={'authority':authority_certificate(),
            'old_horizontal_remainder':str(old.dx),'new_max_horizontal_remainder':str(new.dx),
            'removed_independent_term':str(old.dx-new.dx),
            'uniform_posterior_bounds':uniform_bounds(), 'variable_input_check':input_path_check(),
            'mpc_gate':'old global box blocked for all policies; new model requires joint feedback and terminal proof'}
    paths=[Path(__file__),ROOT/'verification/check_transport_template.py',ROOT/'verification/check_cz_template.py',ROOT/'verification/check_constrained_zonotope.py',ROOT/'configs/planar_baseline.json']
    result['source_sha256']={str(p.relative_to(ROOT)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths}
    return result

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--output',type=Path,required=True)
    args=parser.parse_args()
    if args.output.exists():
        parser.error('output must be new')
    result=run()
    args.output.parent.mkdir(parents=True,exist_ok=True)
    args.output.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
