from __future__ import annotations
import cmath
from dataclasses import dataclass

@dataclass(frozen=True)
class SequenceImpedance:
    z1: complex
    z2: complex
    z0: complex

@dataclass(frozen=True)
class FaultResult:
    kind: str
    current_a: float
    angle_deg: float


def _phasor_result(kind:str,current:complex):
    return FaultResult(kind,abs(current),cmath.phase(current)*180/3.141592653589793)


def three_phase_fault(kv_ll:float,z1:complex):
    if abs(z1)==0: raise ValueError("zero impedance")
    v_phase=kv_ll*1000/(3**0.5)
    return _phasor_result("3ph",v_phase/z1)


def line_ground_fault(kv_ll:float,z:SequenceImpedance,zf:complex=0j):
    denom=z.z1+z.z2+z.z0+3*zf
    if abs(denom)==0: raise ValueError("zero sequence path")
    v_phase=kv_ll*1000/(3**0.5)
    return _phasor_result("lg",3*v_phase/denom)


def line_line_fault(kv_ll:float,z:SequenceImpedance,zf:complex=0j):
    denom=z.z1+z.z2+zf
    if abs(denom)==0: raise ValueError("zero sequence path")
    v_phase=kv_ll*1000/(3**0.5)
    i1=v_phase/denom
    return _phasor_result("ll",(3**0.5)*i1)


def double_line_ground_fault(kv_ll:float,z:SequenceImpedance,zf:complex=0j):
    v_phase=kv_ll*1000/(3**0.5)
    parallel=(z.z2*(z.z0+3*zf))/(z.z2+z.z0+3*zf)
    i1=v_phase/(z.z1+parallel)
    return _phasor_result("llg",3*i1)


def interrupting_duty_ka(result:FaultResult,asymmetry_factor:float=1.6):
    if asymmetry_factor<1: raise ValueError("asymmetry factor")
    return result.current_a*asymmetry_factor/1000


def impedance_from_mva(kv_ll:float,mva:float,xr:float=10.0):
    if kv_ll<=0 or mva<=0 or xr<0: raise ValueError("invalid base")
    zmag=kv_ll*kv_ll/mva
    r=zmag/(1+xr*xr)**0.5
    x=r*xr
    return complex(r,x)
