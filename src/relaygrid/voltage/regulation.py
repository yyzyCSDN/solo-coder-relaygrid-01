from __future__ import annotations

def regulator_tap(voltage_pu: float, current_tap: int, band_center: float=1.0, band_width: float=0.02, max_tap: int=16):
    low=band_center-band_width/2; high=band_center+band_width/2
    if voltage_pu<low and current_tap<max_tap: return current_tap+1
    if voltage_pu>high and current_tap>-max_tap: return current_tap-1
    return current_tap

def capacitor_decision(kvar_flow: float, voltage_pu: float, is_on: bool, on_threshold_kvar: float=500.0, off_threshold_kvar: float=250.0):
    if not is_on and kvar_flow>on_threshold_kvar and voltage_pu<1.03: return True
    if is_on and (kvar_flow<off_threshold_kvar or voltage_pu>1.05): return False
    return is_on

def estimate_tap_voltage(base_pu: float, tap: int, step_pu: float=0.00625):
    return base_pu*(1+tap*step_pu)
