import sys, numpy as np, simula_test as S
from multiprocessing import Pool
def job(args):
    el, v, kind = args
    rng = np.random.default_rng(int(el*-10)+int(v*100))
    SA,_ = S.build_sensors(); SA[7].el = el
    if kind == "step":
        R=[S.run_trial(SA,True,S.scene('gradino discesa',0,dark=True),v,rng) for _ in range(60)]
        return (el,v,kind,np.mean([r['ok'] for r in R]),np.median([r['trig'] for r in R if r['trig']]))
    fa=0;T=0
    for _ in range(12):
        r=S.run_trial(SA,True,S.scene('vuoto',0),v,rng,length=20.0); fa+=r['fa']; T+=r['time']
    return (el,v,kind,fa/(T/60),None)
jobs=[(el,v,k) for el in (-41,-33) for v in (1.0,1.4) for k in ("step","fa")]
with Pool() as p:
    for r in p.map(job,jobs): print(r)
