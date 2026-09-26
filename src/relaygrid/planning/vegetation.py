from __future__ import annotations
def trim_priority(growth_rate: float,clearance_m: float,customers: float):
    a=growth_rate; b=clearance_m; c=customers
    return max(0.0,a)*max(0.0,c)/max(0.1,b)

def classify(value: float):
    if value>=1000: return "very_high"
    if value>=250: return "high"
    if value>=50: return "medium"
    return "low"

def rank(items):
    return sorted(items,key=lambda x:(-x[1],x[0]))
