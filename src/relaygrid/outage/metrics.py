from __future__ import annotations

def merge_intervals(intervals: list[tuple[float,float]]):
    clean=sorted((a,b) for a,b in intervals if b>a)
    out: list[list[float]]=[]
    for a,b in clean:
        if not out or a>out[-1][1]: out.append([a,b])
        else: out[-1][1]=max(out[-1][1],b)
    return [(a,b) for a,b in out]

def interruption_minutes(intervals: list[tuple[float,float]]) -> float:
    return sum(b-a for a,b in merge_intervals(intervals))

def customer_minutes(events: list[tuple[int,float,float]]) -> float:
    by_customers: dict[int,list[tuple[float,float]]]={}
    for customers,start,end in events:
        if customers < 0: raise ValueError("customers cannot be negative")
        by_customers.setdefault(customers,[]).append((start,end))
    return sum(customers*interruption_minutes(iv) for customers,iv in by_customers.items())

def saidi(customer_minutes_total: float, customers_served: int) -> float:
    if customers_served <= 0: raise ValueError("customers served must be positive")
    return customer_minutes_total/customers_served

def saifi(interrupted_customers: int, customers_served: int) -> float:
    if customers_served <= 0: raise ValueError("customers served must be positive")
    return interrupted_customers/customers_served
