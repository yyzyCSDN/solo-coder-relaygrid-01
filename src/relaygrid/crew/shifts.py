from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class Shift:
    crew_id: str
    start_min: float
    end_min: float
    max_work_min: float
    min_rest_min: float

@dataclass(frozen=True)
class Assignment:
    crew_id: str
    job_id: str
    start_min: float
    end_min: float
    emergency: bool=False


def worked_minutes(assignments:list[Assignment],crew_id:str,start:float,end:float):
    total=0.0
    for a in assignments:
        if a.crew_id!=crew_id: continue
        total+=max(0.0,min(end,a.end_min)-max(start,a.start_min))
    return total


def available_for(shift:Shift,assignments:list[Assignment],start:float,duration:float):
    end=start+duration
    if start<shift.start_min or end>shift.end_min: return False
    overlap=any(a.crew_id==shift.crew_id and not (end<=a.start_min or start>=a.end_min) for a in assignments)
    if overlap: return False
    projected=worked_minutes(assignments,shift.crew_id,shift.start_min,shift.end_min)+duration
    return projected<=shift.max_work_min


def next_available(shift:Shift,assignments:list[Assignment],after:float,duration:float,step:float=15.0):
    t=max(after,shift.start_min)
    while t+duration<=shift.end_min:
        if available_for(shift,assignments,t,duration): return t
        t+=step
    return None


def rest_violation(previous:Assignment,next_assignment:Assignment,min_rest_min:float):
    if previous.crew_id!=next_assignment.crew_id: return False
    return next_assignment.start_min-previous.end_min<min_rest_min
