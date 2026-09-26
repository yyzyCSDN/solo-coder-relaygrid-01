from __future__ import annotations
def stock_target(annual_failures: float,lead_months: float,criticality: float):
    a=annual_failures; b=lead_months; c=criticality
    return max(1,int(round(max(0.0,a)*max(1.0,b/12.0)*(1+max(0.0,c)))))

def classify(value: float):
    if value>=1000: return "very_high"
    if value>=250: return "high"
    if value>=50: return "medium"
    return "low"

def rank(items):
    return sorted(items,key=lambda x:(-x[1],x[0]))
