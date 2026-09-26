from __future__ import annotations
import math

def phase_voltage_from_line_line(kv_ll: float) -> float:
    if kv_ll <= 0: raise ValueError("voltage must be positive")
    return kv_ll*1000.0/math.sqrt(3.0)

def three_phase_current_a(kw: float, kvar: float, kv_ll: float) -> float:
    if kv_ll <= 0: raise ValueError("voltage must be positive")
    kva=math.hypot(kw,kvar)
    return kva*1000.0/(math.sqrt(3.0)*kv_ll*1000.0)

def receiving_voltage_kv_ll(sending_kv_ll: float, kw: float, kvar: float, r_ohm: float, x_ohm: float) -> float:
    v_phase=phase_voltage_from_line_line(sending_kv_ll)
    p_phase=kw*1000.0/3.0
    q_phase=kvar*1000.0/3.0
    drop=(r_ohm*p_phase+x_ohm*q_phase)/v_phase
    recv_phase=max(0.0,v_phase-drop)
    return recv_phase*math.sqrt(3.0)/1000.0

def voltage_pu(kv_ll: float, nominal_kv_ll: float) -> float:
    if nominal_kv_ll <= 0: raise ValueError("nominal voltage must be positive")
    return kv_ll/nominal_kv_ll

def within_band(kv_ll: float, nominal_kv_ll: float, low: float=0.95, high: float=1.05) -> bool:
    pu=voltage_pu(kv_ll,nominal_kv_ll)
    return low <= pu <= high
