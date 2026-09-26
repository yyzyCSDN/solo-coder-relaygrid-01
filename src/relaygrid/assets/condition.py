from __future__ import annotations

def health_index(age_years: float, moisture_ppm: float, dga_score: float, maintenance_overdue_days: float):
    score=100.0
    score-=min(35.0,max(0.0,age_years-10)*1.2)
    score-=min(25.0,max(0.0,moisture_ppm-15)*0.8)
    score-=min(25.0,max(0.0,dga_score)*25.0)
    score-=min(15.0,max(0.0,maintenance_overdue_days)/30.0)
    return max(0.0,score)

def risk_class(health: float, consequence: float):
    risk=(100-health)*max(0.0,consequence)
    return "critical" if risk>=6000 else "high" if risk>=3500 else "medium" if risk>=1500 else "low"
