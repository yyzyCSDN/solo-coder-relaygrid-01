
from relaygrid.services.outage_service import OutageService
from relaygrid.services.telemetry_service import TelemetryService
from relaygrid.models import TelemetrySample
from relaygrid.forecast.demand import weather_adjusted,moving_profile
from relaygrid.gis.geometry import haversine_km
from relaygrid.communications.coverage import free_space_loss_db
from relaygrid.market.flexibility import FlexOffer,clear_offers
from relaygrid.analysis.scenarios import cartesian_cases

def test_outage_service_dedupes_same_group():
    s=OutageService(); s.add('g',10,0,10); s.add('g',10,8,15); assert s.customer_minutes()==150

def test_telemetry_service():
    s=TelemetryService(10); s.ingest(TelemetrySample('p',0,1,4)); assert s.snapshot(5)['p']['value']==4

def test_weather_adjusted_heat(): assert weather_adjusted(100,0)>100

def test_moving_profile(): assert moving_profile([1,3,5],2)==[1,2,4]

def test_haversine_zero(): assert haversine_km(1,2,1,2)==0

def test_path_loss_order(): assert free_space_loss_db(10,900)>free_space_loss_db(1,900)

def test_market_clear():
    chosen,rem=clear_offers([FlexOffer('a',10,1,1),FlexOffer('b',10,2,1)],15); assert rem==0 and chosen[0][0]=='a'

def test_cases(): assert len(cartesian_cases({'a':[1,2],'b':[3,4]}))==4
