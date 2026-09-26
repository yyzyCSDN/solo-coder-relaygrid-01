from __future__ import annotations
def transfer_margin(source_capacity_kw: float,existing_kw: float,tie_limit_kw: float):
    a=source_capacity_kw; b=existing_kw; c=tie_limit_kw
    return max(0.0,min(a-b,c))

def classify(value: float):
    if value>=1000: return "very_high"
    if value>=250: return "high"
    if value>=50: return "medium"
    return "low"

def rank(items):
    return sorted(items,key=lambda x:(-x[1],x[0]))
