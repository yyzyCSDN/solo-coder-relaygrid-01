
from relaygrid.models import Bus,Branch,FeederSnapshot,SwitchState,TelemetrySample
from relaygrid.topology.radiality import connected_components
from relaygrid.protection.coordination import iec_inverse_time, coordinated
from relaygrid.powerflow.voltage_drop import receiving_voltage_kv_ll
from relaygrid.der.islanding import Resource, black_start_order
from relaygrid.faults.location import locate_reactance
from relaygrid.crew.routing import RoadEdge, shortest_minutes
from relaygrid.telemetry.quality import newest_valid
from relaygrid.assets.thermal import hottest_spot_step
from relaygrid.outage.metrics import merge_intervals
from relaygrid.storage.dispatch import StorageState, soc
from relaygrid.switching.interlocks import validate_sequence
from relaygrid.reliability.sectionalizer import Section, expected_customer_hours

def snap():
    buses={x:Bus(x,12.47) for x in 'ABCD'}
    branches={
      'ab':Branch('ab','A','B',.1,.1,300,False),
      'bc':Branch('bc','B','C',.1,.1,300,False),
      'cd':Branch('cd','C','D',.1,.1,300,True,False),
      'ad':Branch('ad','A','D',.1,.1,300,True,False),
    }
    return FeederSnapshot(buses,branches,{'cd':SwitchState.OPEN,'ad':SwitchState.OPEN})

def test_components_open_ties(): assert len(connected_components(snap()))==2

def test_inverse_time_monotonic(): assert iec_inverse_time(10,5,.1) < iec_inverse_time(7,5,.1)

def test_coordination_simple(): assert coordinated(0.8,0.3,0.2,0.08)

def test_voltage_drop_reasonable():
    v=receiving_voltage_kv_ll(12.47,500,150,.2,.15); assert v > 0

def test_black_start_former_first():
    r=[Resource('pv',100),Resource('bat',80,grid_forming=True)]; assert black_start_order(r)[0]=='bat'

def test_fault_midpoint(): assert abs(locate_reactance(1.5,.5,.1,20).distance_km-10)<1e-9

def test_road_shortest():
    e=[RoadEdge('a','b',5),RoadEdge('b','c',6),RoadEdge('a','c',20)]; assert shortest_minutes('a','c',e)==11

def test_latest_sequence():
    s=[TelemetrySample('x',10,1,1),TelemetrySample('x',15,2,2)]; assert newest_valid(s).value==2

def test_thermal_moves_up(): assert hottest_spot_step(60,30,1.2,30)>60

def test_merge_intervals(): assert merge_intervals([(0,5),(4,8),(10,12)])==[(0,8),(10,12)]

def test_storage_soc(): assert soc(StorageState(50,100))==.5

def test_interlock_unknown_action(): assert validate_sequence([('noop','x')],[],set(),set())

def test_reliability_positive(): assert expected_customer_hours([Section('s',100,.2,4)])>0
