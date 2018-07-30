from services.db import DB
from services.misc import modernize_date


db = DB()


def mcc_dashboard(self, params):
    flights = db.fetchAll("""
    select * from flights 
    where status in ('prepare', 'freight')""", associate='id')
    flight_ids = tuple(flights.keys())
    for flight in flights.values():
        flight['departure'] = modernize_date(flight['departure'])
        flight['crew'] = []
    crews = db.fetchAll("""
    select f.flight_id, f.role, u.name
from flight_crews f 
join users u on f.user_id = u.id
    where f.flight_id in """ + str(flight_ids).replace(",)", ")"))
    for crew in crews:
        flight = flights[crew['flight_id']]
        del crew['flight_id']
        flight['crew'].append(crew)
    return flights
