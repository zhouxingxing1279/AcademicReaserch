"""Run exact startup-gate experiments: python -m experiments.cz_startup_predecessor."""
import argparse
import csv
import hashlib
import json
import platform
import statistics
import sys
from fractions import Fraction as F
from itertools import product
from pathlib import Path
from time import perf_counter

from src.outerloop.startup_gate import CZ, startup_gate


def diagonal(values):
    return tuple(tuple(v if i == j else F(0) for j in range(len(values))) for i,v in enumerate(values))


def box(radii, center=None):
    return CZ(center or (F(0),)*len(radii), diagonal(radii))


def setup(t, zoh, p_limit, v_limit):
    a = tuple(tuple(F(i == j)+(t if i < 3 and j == i+3 else 0) for j in range(6)) for i in range(6))
    b = tuple(tuple((t*t/2 if i < 3 and zoh else t if i >= 3 else F(0)) if j == i%3 else F(0) for j in range(3)) for i in range(6))
    rows = tuple(tuple(F(sign if i == j else 0) for j in range(6)) for i in range(6) for sign in (1,-1))
    bounds = tuple(limit for limit in (p_limit,)*3+(v_limit,)*3 for _ in range(2))
    return a,b,rows,bounds


def encode(value):
    if isinstance(value,F): return str(value)
    if isinstance(value,(tuple,list)): return [encode(v) for v in value]
    if isinstance(value,dict): return {key:encode(v) for key,v in value.items()}
    return value


def run_suite(full_grid=True):
    records, timings = [],[]

    def case(name, info, *, t=F(1), w=F(1,10), p_limit=F(1), v_limit=F(2), u_limit=F(1), zoh=True, expected, axis_interval=None):
        noise=box((w,)*3)
        a,b,hx,h=setup(t,zoh,p_limit,v_limit)
        started=perf_counter()
        result=startup_gate(a,b,b,info,noise,hx,h,(u_limit,)*3)
        seconds=perf_counter()-started
        if result.status != expected:
            raise AssertionError((name,result.status,expected))
        count=0
        margins=[]
        if result.command is not None:
            u=result.command
            if not all(abs(q)<=u_limit for q in u):
                raise AssertionError((name,'input bound'))
            for x,dist in product(info.vertices(),noise.vertices()):
                # Independently expand the scalar dynamics; do not reuse matrix products.
                for j in range(3):
                    p_next=x[j]+t*x[j+3]+(t*t*(u[j]+dist[j])/2 if zoh else 0)
                    v_next=x[j+3]+t*(u[j]+dist[j])
                    margins.extend((p_limit-abs(p_next),v_limit-abs(v_next)))
                count+=1
            if min(margins)<0:
                raise AssertionError((name,'unsafe shared command',min(margins)))
        records.append(encode({
            'id':name,'status':result.status,'model':'zoh' if zoh else 'euler',
            'T':t,'W':w,'Xp':p_limit,'Xv':v_limit,'U':u_limit,
            'information':{'center':info.center,'generators':info.generators,'equalities':info.equalities,'rhs':info.rhs},
            'command':result.command,'input_rows':result.rows,'input_limits':result.bounds,
            'state_supports':result.state_supports,'noise_supports':result.noise_supports,
            'initial_margins':result.initial_margins,
            'state_vertices':result.state_vertex_count,'disturbance_vertices':result.noise_vertex_count,
            'verified_joint_vertices':count,'minimum_state_margin':min(margins) if margins else None,
            'axis_interval':axis_interval}))
        timings.append({'id':name,'gate_seconds':seconds})
        return result

    for velocity,interval in ((F(1,10),('-2','2')),(F(2,5),('-3/2','3/2')),(F(1),None)):
        result=case('pr210_v_'+str(velocity).replace('/','_'),box((F(1,5),)*3+(velocity,)*3),
                    t=F(1,10),w=F(1,2),p_limit=F(1,4),v_limit=F(1),u_limit=F(2),
                    expected='feasible' if interval else 'infeasible',axis_interval=interval)
        # Independently read the axis-aligned input polytope, not only its feasibility.
        lo,hi=F(-2),F(2)
        for row,bound in zip(result.rows,result.bounds):
            if row[0]>0: hi=min(hi,bound/row[0])
            if row[0]<0: lo=max(lo,bound/row[0])
        recovered=[str(lo),str(hi)] if lo<=hi else None
        if recovered != (list(interval) if interval else None):
            raise AssertionError(('PR210 interval mismatch',velocity,recovered))

    eq=tuple(tuple(F(j==i or j==i+3) for j in range(6)) for i in range(3))
    correlated=CZ((0,)*6,diagonal((F(1),)*6),eq,(0,)*3)
    independent_vertices={tuple(-F(v) for v in velocity)+tuple(F(v) for v in velocity) for velocity in product((-1,1),repeat=3)}
    if set(correlated.vertices()) != independent_vertices:
        raise AssertionError('Coupled CZ vertex representation mismatch')
    case('correlated_cz',correlated,expected='feasible')
    case('coordinate_hull',box((F(1),)*6),expected='infeasible')
    case('causality_gap',box((F(0),)*3+(F(1),)*3),w=F(1,4),p_limit=F(2),v_limit=F(1),expected='infeasible')
    point=box((F(0),)*6,(F(0),)*3+(F(1),)*3)
    case('saturation_boundary',point,w=F(1,4),p_limit=F(2),v_limit=F(1),u_limit=F(1,4),expected='feasible')
    case('saturation_insufficient',point,w=F(1,4),p_limit=F(2),v_limit=F(1),u_limit=F(1,5),expected='infeasible')
    for zoh in (False,True):
        case('zoh_boundary' if zoh else 'euler_boundary',box((F(0),)*6),w=F(1),p_limit=F(1,4),zoh=zoh,expected='infeasible' if zoh else 'feasible')

    if full_grid:
        for number,(t,p,v,w) in enumerate(product((F(1,10),F(1,2),F(1)),(F(1,5),F(2,5)),(F(1,10),F(2,5),F(1)),(F(0),F(1,10),F(1,2)))):
            # Independent closed-form robust iff for centered product boxes.
            feasible=p+t*v+t*t*w/2<=F(1,2) and v+t*w<=1
            case(f'grid_{number:02d}',box((p,)*3+(v,)*3),t=t,w=w,p_limit=F(1,2),v_limit=F(1),u_limit=F(2),expected='feasible' if feasible else 'infeasible')
    return records,timings


def certificate(records):
    root=Path(__file__).resolve().parents[1]
    sources=('src/outerloop/startup_gate.py','experiments/cz_startup_predecessor.py')
    hashes={name:hashlib.sha256((root/name).read_bytes().replace(b'\r\n',b'\n')).hexdigest() for name in sources}
    return {'schema':1,'evidence':'exact rational finite instances; no full-loop guarantee',
            'source_sha256_lf':hashes,'cases':len(records),
            'feasible':sum(r['status']=='feasible' for r in records),
            'infeasible':sum(r['status']=='infeasible' for r in records),
            'verified_joint_vertices':sum(r['verified_joint_vertices'] for r in records),'records':records}


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--check',action='store_true',help='Recompute and exactly compare the committed mathematical certificate')
    parser.add_argument('--output',type=Path,default=Path('experiments/results/cz_startup_predecessor'))
    args=parser.parse_args()
    records,timings=run_suite()
    result=certificate(records)
    target=args.output/'certificate.json'
    if args.check:
        if json.loads(target.read_text(encoding='utf-8')) != result:
            raise SystemExit('FAIL: exact mathematical certificate or source hash differs')
    else:
        args.output.mkdir(parents=True,exist_ok=True)
        header={key:value for key,value in result.items() if key!='records'}
        prefix=json.dumps(header,indent=2)[:-2]
        serialized=',\n'.join('    '+json.dumps(record,separators=(',',':')) for record in records)
        target.write_text(prefix+',\n  "records": [\n'+serialized+'\n  ]\n}\n',encoding='utf-8')
        columns=('id','status','model','T','W','Xp','Xv','U','command','state_vertices','disturbance_vertices','verified_joint_vertices','minimum_state_margin')
        with (args.output/'summary.csv').open('w',encoding='utf-8',newline='') as handle:
            writer=csv.DictWriter(handle,fieldnames=columns,extrasaction='ignore')
            writer.writeheader(); writer.writerows(records)
        seconds=sorted(t['gate_seconds'] for t in timings)
        performance={'python':sys.version,'platform':platform.platform(),'processor':platform.processor(),
                     'solver':'none; fractions.Fraction exact vertex enumeration','random_seed':None,
                     'mean_seconds':statistics.mean(seconds),'p95_seconds':seconds[int(.95*(len(seconds)-1))],
                     'maximum_seconds':max(seconds),'timings':timings,'note':'Observed timings, not WCET or a real-time claim.'}
        (args.output/'performance.json').write_text(json.dumps(performance,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({key:value for key,value in result.items() if key not in ('records','source_sha256_lf')},indent=2))
    print('PASS exact certificate comparison' if args.check else 'PASS all registered cases; artifacts saved')


if __name__=='__main__': main()
