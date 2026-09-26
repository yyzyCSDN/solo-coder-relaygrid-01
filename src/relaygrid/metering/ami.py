from __future__ import annotations
from collections import defaultdict

def last_gasp_clusters(messages: list[tuple[str,float,str]], window_s: float=30.0):
    ordered=sorted(messages,key=lambda x:x[1]); clusters=[]; cur=[]; start=None
    for meter,ts,feeder in ordered:
        if start is None or ts-start<=window_s:
            cur.append((meter,ts,feeder)); start=ts if start is None else start
        else:
            clusters.append(cur); cur=[(meter,ts,feeder)]; start=ts
    if cur: clusters.append(cur)
    return clusters

def infer_feeder(cluster):
    counts=defaultdict(int)
    for _,_,feeder in cluster: counts[feeder]+=1
    return max(counts,key=lambda f:(counts[f],f)) if counts else None

def ping_success_ratio(results: list[bool]) -> float:
    return sum(bool(x) for x in results)/len(results) if results else 0.0
