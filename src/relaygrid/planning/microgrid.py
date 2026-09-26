from __future__ import annotations
def coverage_score(critical_kw: float,der_kw: float,storage_kwh: float):
    a=critical_kw; b=der_kw; c=storage_kwh
    return min(max(0.0,a),max(0.0,b))+min(max(0.0,a)*4,max(0.0,c))

def classify(value: float):
    if value>=1000: return "very_high"
    if value>=250: return "high"
    if value>=50: return "medium"
    return "low"

def rank(items):
    return sorted(items,key=lambda x:(-x[1],x[0]))
