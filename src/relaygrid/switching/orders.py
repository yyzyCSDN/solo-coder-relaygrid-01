from __future__ import annotations
from dataclasses import dataclass, field, replace
from enum import Enum

class OrderState(str,Enum):
    DRAFT="draft"
    CHECKED="checked"
    APPROVED="approved"
    EXECUTING="executing"
    COMPLETE="complete"
    CANCELLED="cancelled"

@dataclass(frozen=True)
class SwitchingStep:
    sequence: int
    action: str
    device_id: str
    expected_state: str
    hold_point: bool=False
    note: str=""

@dataclass(frozen=True)
class OrderRevision:
    revision: int
    state: OrderState
    steps: tuple[SwitchingStep,...]
    author: str
    checker: str|None=None
    approver: str|None=None

@dataclass
class SwitchingOrder:
    order_id: str
    revisions: list[OrderRevision]=field(default_factory=list)
    acknowledgements: dict[int,tuple[str,float]]=field(default_factory=dict)

    @property
    def current(self):
        if not self.revisions: raise ValueError("order has no revision")
        return self.revisions[-1]

    def create(self,steps:list[SwitchingStep],author:str):
        if self.revisions: raise ValueError("already created")
        self._validate_steps(steps)
        self.revisions.append(OrderRevision(1,OrderState.DRAFT,tuple(steps),author))
        return self.current

    def revise(self,steps:list[SwitchingStep],author:str):
        if self.current.state not in {OrderState.DRAFT,OrderState.CHECKED}: raise ValueError("cannot revise approved order")
        self._validate_steps(steps)
        self.revisions.append(OrderRevision(self.current.revision+1,OrderState.DRAFT,tuple(steps),author))
        self.acknowledgements.clear()
        return self.current

    def check(self,checker:str):
        if checker==self.current.author: raise ValueError("independent checker required")
        if self.current.state!=OrderState.DRAFT: raise ValueError("order not draft")
        self.revisions[-1]=replace(self.current,state=OrderState.CHECKED,checker=checker)
        return self.current

    def approve(self,approver:str):
        if self.current.state!=OrderState.CHECKED: raise ValueError("order not checked")
        if approver in {self.current.author,self.current.checker}: raise ValueError("independent approver required")
        self.revisions[-1]=replace(self.current,state=OrderState.APPROVED,approver=approver)
        return self.current

    def start(self):
        if self.current.state!=OrderState.APPROVED: raise ValueError("order not approved")
        self.revisions[-1]=replace(self.current,state=OrderState.EXECUTING)

    def acknowledge(self,sequence:int,operator:str,timestamp:float):
        if self.current.state!=OrderState.EXECUTING: raise ValueError("order not executing")
        step=next((s for s in self.current.steps if s.sequence==sequence),None)
        if step is None: raise KeyError(sequence)
        expected=min(s.sequence for s in self.current.steps if s.sequence not in self.acknowledgements)
        if sequence!=expected: raise ValueError("step out of order")
        self.acknowledgements[sequence]=(operator,timestamp)
        if len(self.acknowledgements)==len(self.current.steps): self.revisions[-1]=replace(self.current,state=OrderState.COMPLETE)

    def _validate_steps(self,steps):
        seq=[s.sequence for s in steps]
        if seq!=list(range(1,len(steps)+1)): raise ValueError("steps must be contiguous")
        for s in steps:
            if s.action not in {"open","close","verify","test"}: raise ValueError(s.action)
