from __future__ import annotations
from dataclasses import dataclass, field
from relaygrid.models import FeederSnapshot, SwitchState
from relaygrid.topology.radiality import would_create_cycle
from relaygrid.events.logbook import Event, Logbook
@dataclass
class GridSimulator:
    snapshot: FeederSnapshot
    now_s: float=0.0
    log: Logbook=field(default_factory=Logbook)
    def advance(self,seconds: float):
        if seconds<0: raise ValueError("cannot reverse simulation time")
        self.now_s+=seconds; return self.now_s
    def operate_switch(self,branch_id: str,state: SwitchState):
        if branch_id not in self.snapshot.branches: raise KeyError(branch_id)
        if state==SwitchState.CLOSED and self.snapshot.switch_state.get(branch_id)==SwitchState.OPEN and would_create_cycle(self.snapshot,branch_id): raise ValueError("cycle")
        self.snapshot.switch_state[branch_id]=state
        self.log.append(Event(self.now_s,"switch",branch_id,state.value))
        return state
    def energized_bus_count(self):
        source=next(iter(self.snapshot.buses),None)
        if source is None: return 0
        adj={b:set() for b in self.snapshot.buses}
        for br in self.snapshot.closed_branches(): adj[br.source].add(br.target); adj[br.target].add(br.source)
        seen=set(); stack=[source]
        while stack:
            b=stack.pop()
            if b in seen: continue
            seen.add(b); stack.extend(adj[b]-seen)
        return len(seen)
