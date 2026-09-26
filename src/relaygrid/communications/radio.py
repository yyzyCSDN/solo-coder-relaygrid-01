from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class RadioSite:
    site_id: str
    tx_dbm: float
    antenna_gain_db: float
    latitude: float
    longitude: float
    height_m: float


def path_loss_db(distance_km:float,frequency_mhz:float,clutter_db:float=0.0):
    if distance_km<=0 or frequency_mhz<=0: raise ValueError("invalid radio path")
    return 32.44+20*math.log10(distance_km)+20*math.log10(frequency_mhz)+clutter_db


def received_dbm(site:RadioSite,distance_km:float,frequency_mhz:float,rx_gain_db:float=0.0,clutter_db:float=0.0):
    return site.tx_dbm+site.antenna_gain_db+rx_gain_db-path_loss_db(distance_km,frequency_mhz,clutter_db)


def availability_margin_db(rx_dbm:float,sensitivity_dbm:float,fade_margin_db:float=15.0): return rx_dbm-sensitivity_dbm-fade_margin_db


def coverage_state(margin_db:float):
    if margin_db>=10:return "robust"
    if margin_db>=0:return "marginal"
    return "unavailable"


def best_site(sites:list[tuple[RadioSite,float]],frequency_mhz:float,sensitivity_dbm:float):
    choices=[]
    for site,distance in sites:
        rx=received_dbm(site,distance,frequency_mhz)
        margin=availability_margin_db(rx,sensitivity_dbm)
        choices.append((margin,site.site_id,rx))
    return max(choices,default=None)
