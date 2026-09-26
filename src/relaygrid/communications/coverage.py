from __future__ import annotations
import math

def free_space_loss_db(distance_km: float, frequency_mhz: float):
    if distance_km<=0 or frequency_mhz<=0: raise ValueError("positive inputs required")
    return 32.44+20*math.log10(distance_km)+20*math.log10(frequency_mhz)

def link_margin_db(tx_dbm: float, tx_gain_db: float, rx_gain_db: float, path_loss_db: float, rx_sensitivity_dbm: float, misc_loss_db: float=0.0):
    rx=tx_dbm+tx_gain_db+rx_gain_db-path_loss_db-misc_loss_db
    return rx-rx_sensitivity_dbm

def redundant_sites(primary: set[str], backup: set[str], required: set[str]):
    return sorted(required & primary & backup)
