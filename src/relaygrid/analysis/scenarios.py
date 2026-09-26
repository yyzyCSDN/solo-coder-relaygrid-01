from __future__ import annotations
from itertools import product

def cartesian_cases(parameters: dict[str,list]):
    names=sorted(parameters)
    return [dict(zip(names,vals)) for vals in product(*(parameters[n] for n in names))]

def pareto_front(cases,benefit_key,cost_key):
    front=[]
    for c in cases:
        dominated=False
        for d in cases:
            if d is c: continue
            if d[benefit_key]>=c[benefit_key] and d[cost_key]<=c[cost_key] and (d[benefit_key]>c[benefit_key] or d[cost_key]<c[cost_key]): dominated=True; break
        if not dominated: front.append(c)
    return front
