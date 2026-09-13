"""Exact fixed-schedule reachable support and admissible input witness."""
import argparse, hashlib, json
from fractions import Fraction as F
from pathlib import Path
from check_gain_screen import verify as previous

h=F(1,50); ell=F(9,2); D=F(572143,160000); eps=F(1,50)

def advance(z,w,n,success,actual_t=None):
    p,v,hp,hv=z
    t=-5*hp-3*hv if actual_t is None else actual_t
    pn=p+h*v;vn=v+h*(t+w);pp=hp+h*hv;vp=hv+h*t
    if success:
        r=pn+n-pp
        pp+=r;vp+=ell*r
    return [pn,vn,pp,vp]

def dot(a,b):return sum(x*y for x,y in zip(a,b))
def support(c,cols):return sum(abs(dot(c,g)) for g in cols)

def verify():
    previous()
    # Same initial p appears in true and estimated position; n0 is independent.
    cols=[[eps,0,eps,0],[0,F(1,10),0,0],[0,0,eps,0]]
    labels=['initial_p','initial_v','initial_position_noise']
    directions={'height':[1,0,0,0],'velocity':[0,1,0,0],'input_offset':[0,0,-5,-3]}
    limits={'height':F(3,2),'velocity':F(3),'input_offset':F(981,200)}
    table=[]
    for k in range(31):
        vals={name:support(c,cols) for name,c in directions.items()}
        bad=[name for name in vals if vals[name]>limits[name]]
        table.append({'tick':k,**{name:str(x) for name,x in vals.items()}})
        if bad:
            assert k==30 and bad==['input_offset']
            break
        assert k<30
        success=(k+1)%5==0
        cols=[advance(g,0,0,success) for g in cols]
        cols.append([0,h*D,0,0]);labels.append('acceleration_'+str(k))
        if success:
            cols.append([0,0,eps,ell*eps]);labels.append('position_noise_'+str(k+1))
    c=directions['input_offset']
    signs=[F(1 if dot(c,g)>=0 else -1) for g in cols]
    primitive=dict(zip(labels,signs))
    z=[eps*signs[0],F(1,10)*signs[1],eps*(signs[0]+signs[2]),F(0)]
    for k in range(31):
        t=-5*z[2]-3*z[3]
        assert abs(z[0])<=limits['height'] and abs(z[1])<=limits['velocity']
        if k<30:assert abs(t)<=limits['input_offset']
        else:
            assert t==vals['input_offset']>limits['input_offset']
            break
        success=(k+1)%5==0
        z=advance(z,D*primitive['acceleration_'+str(k)],eps*primitive.get('position_noise_'+str(k+1),F(0)),success)
    witness_t=t
    # Saturation changes the state map, but not the observer-error identity,
    # provided both prediction and plant receive the identical actual input.
    for success in (False,True):
        for j in range(7):
            z0=[F(i==j) for i in range(4)]
            w,n,t=F(j==4),F(j==5),F(j==6)
            nxt=advance(z0,w,n,success,actual_t=t)
            ep=z0[0]-z0[2]+h*(z0[1]-z0[3]);ev=z0[1]-z0[3]+h*w
            assert nxt[0]-nxt[2]==(-n if success else ep)
            assert nxt[1]-nxt[3]==(ev-ell*ep-ell*n if success else ev)
    return {'status':'EXACT_VERTICAL_INPUT_VIOLATION_CERTIFIED','source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'schedule':'position succeeds every 5 ticks including zero','primitive_count':len(cols),'support_history':table,'first_any_support_violation_tick':30,'violated_quantity':'input_offset','attaining_normalized_primitive':{k:str(v) for k,v in primitive.items()},'witness_state_tick_30':list(map(str,z)),'witness_input_offset':str(witness_t),'witness_thrust':str(F(981,100)+witness_t),'input_support_tick_30_display':float(vals['input_offset']),'height_support_tick_30_display':float(vals['height']),'velocity_support_tick_30_display':float(vals['velocity']),'observer_error_cancels_any_common_actual_input':True,'global_earliest_over_all_schedules':False,'physical_aerodynamic_witness_proved':False,'saturated_state_safety_proved':False}

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--output',type=Path,required=True);a=p.parse_args();r=verify()
    with a.output.open('x') as f:json.dump(r,f,indent=2);f.write('\n')
    print(r['status'])
