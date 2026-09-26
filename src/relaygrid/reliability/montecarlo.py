from __future__ import annotations
import random

def simulate_failures(rates_per_year: dict[str,float],years: float,seed: int=0):
    rng=random.Random(seed); out=[]
    for asset,rate in sorted(rates_per_year.items()):
        expected=max(0.0,rate*years); whole=int(expected); frac=expected-whole
        count=whole+(1 if rng.random()<frac else 0)
        out.extend([asset]*count)
    return out

def percentile(values: list[float],p: float):
    if not values: return 0.0
    s=sorted(values); idx=min(len(s)-1,max(0,round((len(s)-1)*p))); return s[idx]
