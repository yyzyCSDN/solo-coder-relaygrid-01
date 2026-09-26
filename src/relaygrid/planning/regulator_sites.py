from __future__ import annotations
def site_score(distance_km: float,voltage_deficit_pu: float,customers: float):
    a=distance_km; b=voltage_deficit_pu; c=customers
    return max(0.0,b)*max(0.0,c)/(1+a)

def classify(value: float):
    if value>=1000: return "very_high"
    if value>=250: return "high"
    if value>=50: return "medium"
    return "low"

def rank(items):
    return sorted(items,key=lambda x:(-x[1],x[0]))
