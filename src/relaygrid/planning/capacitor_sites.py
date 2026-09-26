from __future__ import annotations
def site_score(kvar_need: float,loss_reduction_kw: float,switch_ops: float):
    a=kvar_need; b=loss_reduction_kw; c=switch_ops
    return max(0.0,a)*max(0.0,b)/(1+max(0.0,c))

def classify(value: float):
    if value>=1000: return "very_high"
    if value>=250: return "high"
    if value>=50: return "medium"
    return "low"

def rank(items):
    return sorted(items,key=lambda x:(-x[1],x[0]))
