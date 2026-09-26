from __future__ import annotations
def tie_score(transfer_kw: float,customers: float,length_km: float):
    a=transfer_kw; b=customers; c=length_km
    return max(0.0,a)*max(0.0,b)/max(0.1,c)

def classify(value: float):
    if value>=1000: return "very_high"
    if value>=250: return "high"
    if value>=50: return "medium"
    return "low"

def rank(items):
    return sorted(items,key=lambda x:(-x[1],x[0]))
