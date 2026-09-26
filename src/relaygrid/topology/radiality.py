from __future__ import annotations
from relaygrid.models import FeederSnapshot, SwitchState

def energized_edges(snapshot: FeederSnapshot):
    out=[]
    for br in snapshot.branches.values():
        if br.switchable and snapshot.switch_state.get(br.branch_id, SwitchState.CLOSED) != SwitchState.CLOSED:
            continue
        out.append((br.branch_id, br.source, br.target))
    return out

def would_create_cycle(snapshot: FeederSnapshot, branch_id: str) -> bool:
    if branch_id not in snapshot.branches:
        raise KeyError(branch_id)
    br=snapshot.branches[branch_id]
    parent={b:b for b in snapshot.buses}
    rank={b:0 for b in snapshot.buses}
    def find(x):
        while parent[x]!=x:
            parent[x]=parent[parent[x]]
            x=parent[x]
        return x
    def union(a,b):
        ra,rb=find(a),find(b)
        if ra==rb:
            return False
        if rank[ra]<rank[rb]: ra,rb=rb,ra
        parent[rb]=ra
        if rank[ra]==rank[rb]: rank[ra]+=1
        return True
    for eid,a,b in energized_edges(snapshot):
        if eid==branch_id:
            continue
        union(a,b)
    return find(br.source)==find(br.target)

def close_if_radial(snapshot: FeederSnapshot, branch_id: str) -> FeederSnapshot:
    if would_create_cycle(snapshot, branch_id):
        raise ValueError("closing branch would create a cycle")
    out=snapshot.copy()
    out.switch_state[branch_id]=SwitchState.CLOSED
    return out

def connected_components(snapshot: FeederSnapshot):
    adj: dict[str,set[str]]={b:set() for b in snapshot.buses}
    for _,a,b in energized_edges(snapshot):
        adj[a].add(b); adj[b].add(a)
    comps=[]; seen=set()
    for start in sorted(adj):
        if start in seen: continue
        stack=[start]; comp=set()
        while stack:
            cur=stack.pop()
            if cur in seen: continue
            seen.add(cur); comp.add(cur); stack.extend(adj[cur]-seen)
        comps.append(comp)
    return comps
