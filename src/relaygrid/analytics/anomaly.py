from __future__ import annotations
from statistics import mean,pstdev

def zscore_flags(values: list[float],threshold: float=3.0):
    if len(values)<2: return [False]*len(values)
    m=mean(values); s=pstdev(values)
    if s==0: return [False]*len(values)
    return [abs((x-m)/s)>threshold for x in values]

def rate_of_change_flags(values: list[float],max_step: float):
    out=[False]
    out.extend(abs(b-a)>max_step for a,b in zip(values,values[1:]))
    return out
