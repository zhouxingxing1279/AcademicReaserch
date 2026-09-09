#!/usr/bin/env python3
"""Train one point-loss MLP pilot; no formal test seeds, no set-loss optimization."""
import argparse,hashlib,json,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'src'))
import numpy as np
import scipy
from scipy.optimize import minimize
from smf_mpc import plant
from smf_mpc.data import rng_for,split_for
from smf_mpc.sets import Box
from smf_mpc.neural_model import ResidualMLP,features
from smf_mpc.residual_envelope import envelope
from run_g1 import save_json


def generate(config,seeds):
    p=config['plant'];h=p['dt_s'];domain=Box(config['domain']['state_lower'],config['domain']['state_upper'])
    X=[];Y=[];metadata=[]
    for seed in seeds:
        rng=rng_for(seed,'model_a_collection')
        x=np.array([rng.uniform(-2,2),rng.uniform(1,3),rng.uniform(-1.5,1.5),rng.uniform(-1,1),rng.uniform(-.2,.2),rng.uniform(-.3,.3)])
        wind=rng.uniform(-.5,.5,2);phase=rng.uniform(0,2*np.pi,2);freq=rng.uniform(.3,.9,2)
        status='COMPLETED';points=[];labels=[]
        for k in range(1000):
            if not domain.contains(x):status='OUT_OF_DOMAIN';break
            t=k*h;ref=np.array([2*np.sin(freq[0]*t+phase[0]),2+.6*np.sin(freq[1]*t+phase[1])])
            # Offline excitation controller may use simulator truth; deployed estimator never does.
            acc=np.clip(1.8*(ref-x[:2])-1.7*x[2:4],[-3,-3],[3,3])
            target_phi=np.clip(-np.arctan2(acc[0],p['gravity_m_s2']+acc[1])+.04*np.sin(2*t+phase[0]),-.35,.35)
            T=p['mass_kg']*np.hypot(acc[0],p['gravity_m_s2']+acc[1])*(1+.05*np.cos(1.3*t+phase[1]))
            tau=p['inertia_kg_m2']*(25*(target_phi-x[4])-10*x[5])
            u=np.clip([T,tau],config['domain']['input_lower'],config['domain']['input_upper'])
            if k%5==0:
                points.append(features(x,u,config));labels.append(plant.aerodynamic_acceleration(x,u,wind,p['mass_kg'],p['gravity_m_s2']))
            x=plant.step(x,u,wind,config)
        arr=np.asarray(points).reshape(-1,5);lab=np.asarray(labels).reshape(-1,2)
        X.extend(points);Y.extend(labels)
        metadata.append({'seed':seed,'split':split_for(seed),'status':status,'last_tick':k,'sample_count':len(points),
                         'sample_sha256':hashlib.sha256(arr.astype('<f8').tobytes()+lab.astype('<f8').tobytes()).hexdigest()})
    return np.asarray(X),np.asarray(Y),metadata


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',type=Path,required=True)
    parser.add_argument('--maxiter',type=int,default=200);args=parser.parse_args()
    if args.output.exists() and any(args.output.iterdir()):parser.error('use an empty output directory')
    args.output.mkdir(parents=True,exist_ok=True)
    config=json.loads((ROOT/'configs/planar_baseline.json').read_text())
    start=time.perf_counter();X,Y,train_meta=generate(config,range(10000,10120));VX,VY,val_meta=generate(config,range(20000,20040))
    print(json.dumps({'training_points':len(X),'validation_points':len(VX),'data_seconds':time.perf_counter()-start}),flush=True)
    save_json(args.output/'data_manifest.json',{'kind':'G2_pilot_subsets_not_full_protocol','train':train_meta,'validation':val_meta,
        'collection':'20s episodes; current-state offline PD excitation; stride5; retain valid prefixes; analytic labels; static random wind',
        'formal_test_used':False})
    initial=ResidualMLP.initialize();history=[];best={'mse':float('inf'),'vector':initial.vector(),'iteration':0}
    def objective(vector):return ResidualMLP.from_vector(vector).loss_gradient(X,Y)
    def record(vector):
        model=ResidualMLP.from_vector(vector);vmse=float(np.mean(np.sum((model.predict(VX)-VY)**2,axis=1)))
        tmse=float(np.mean(np.sum((model.predict(X)-Y)**2,axis=1)))
        iteration=len(history);history.append({'iteration':iteration,'train_sum_squared_error_mean':tmse,'validation_sum_squared_error_mean':vmse})
        if vmse<best['mse']:best.update(mse=vmse,vector=np.array(vector),iteration=iteration)
        if iteration%25==0:print(json.dumps(history[-1]),flush=True)
    record(initial.vector());start=time.perf_counter()
    result=minimize(objective,initial.vector(),jac=True,method='L-BFGS-B',callback=record,
                    options={'maxiter':args.maxiter,'maxls':30,'ftol':1e-12,'gtol':1e-7})
    model=ResidualMLP.from_vector(best['vector']);train_seconds=time.perf_counter()-start
    save_json(args.output/'model.json',model.to_dict());save_json(args.output/'history.json',history)
    cert,lo,hi,bound=envelope(model,config,depth=14)
    save_json(args.output/'envelope.json',cert)
    np.savez_compressed(args.output/'envelope_leaves.npz',lower=lo,upper=hi,acceleration_halfwidth=bound)
    pred=model.predict(VX);errors=pred-VY
    save_json(args.output/'training_summary.json',{'backend':'NumPy analytic backprop + SciPy L-BFGS-B','numpy':np.__version__,'scipy':scipy.__version__,
        'seed':61001,'selected_iteration':best['iteration'],'optimizer_iterations':int(result.nit),'optimizer_success':bool(result.success),
        'optimizer_message':str(result.message),'training_seconds':train_seconds,'train_points':len(X),'validation_points':len(VX),
        'validation_rmse_per_axis':np.sqrt(np.mean(errors**2,axis=0)).tolist(),
        'zero_residual_validation_rmse_per_axis':np.sqrt(np.mean(VY**2,axis=0)).tolist(),
        'validation_max_absolute_error':np.max(np.abs(errors),axis=0).tolist(),
        'global_partition_halfwidth':cert['acceleration_halfwidth'],'architecture':[5,32,32,2],
        'scope':'single seed A pilot; no B/C/D; float64 envelope not strict certification'})
    sources=[*sorted((ROOT/'src').rglob('*.py')),Path(__file__).resolve()]
    save_json(args.output/'manifest.json',{'base_commit':'d73f407e5d35c02fa839e7aec688a0c403297228',
        'config_sha256':hashlib.sha256((ROOT/'configs/planar_baseline.json').read_bytes()).hexdigest(),
        'source_sha256':{str(f.relative_to(ROOT)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sources},
        'artifact_sha256':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted(args.output.iterdir()) if f.is_file()}})
    print(json.dumps({'validation_rmse':np.sqrt(np.mean(errors**2,axis=0)).tolist(),'global_envelope':cert['acceleration_halfwidth']}),flush=True)


if __name__=='__main__':main()
