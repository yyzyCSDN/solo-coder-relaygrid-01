from __future__ import annotations
from dataclasses import dataclass, field
@dataclass
class StateStore:
    analog: dict[str,float]=field(default_factory=dict)
    discrete: dict[str,str]=field(default_factory=dict)
    versions: dict[str,int]=field(default_factory=dict)
    def apply(self, point_id: str, value, version: int):
        if version <= self.versions.get(point_id,-1): return False
        self.versions[point_id]=version
        if isinstance(value,(int,float)): self.analog[point_id]=float(value)
        else: self.discrete[point_id]=str(value)
        return True
    def snapshot(self): return {"analog":dict(self.analog),"discrete":dict(self.discrete),"versions":dict(self.versions)}

def reconcile(commanded: dict[str,str], observed: dict[str,str]):
    return {k:(commanded[k],observed.get(k)) for k in commanded if observed.get(k)!=commanded[k]}
