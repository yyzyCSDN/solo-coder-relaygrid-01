from __future__ import annotations
def firm_capacity(bank_a_mva: float,bank_b_mva: float,peak_mva: float):
    a=bank_a_mva; b=bank_b_mva; c=peak_mva
    return max(0.0,min(a,b)-c)

def classify(value: float):
    if value>=1000: return "very_high"
    if value>=250: return "high"
    if value>=50: return "medium"
    return "low"

def rank(items):
    return sorted(items,key=lambda x:(-x[1],x[0]))
