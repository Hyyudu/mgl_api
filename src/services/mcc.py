from services.db import DB
from services.misc import modernize_date, api_ok, api_fail


db = DB()


def mcc_dashboard(self, params):
    flights = self.db.fetchAll("""
    select * from flights 
    where status in ('prepare', 'freight')""", associate='id')
    flight_ids = tuple(flights.keys())
    for flight in flights.values():
        flight['departure'] = modernize_date(flight['departure'])
        flight['crew'] = []
    crews = self.db.fetchAll("""
    select f.flight_id, f.role, u.name, u.id user_id
from flight_crews f 
join users u on f.user_id = u.id
    where f.flight_id in """ + str(flight_ids).replace(",)", ")"))
    for crew in crews:
        flight = flights[crew['flight_id']]
        del crew['flight_id']
        flight['crew'].append(crew)
    return flights


def mcc_set_crew(self, params):
    """ params = {"flight_id": 1, "role": "pilot", "user_id": 2} """
    db.query("""delete from flight_crews 
        where flight_id = :flight_id and (role=:role or user_id=:user_id)""", params, need_commit=True)
    db.insert('flight_crews', params)
    return api_ok()


def mcc_add_passenger(self, params):
    """ params = {"flight_id": 1, "user_id": 2} """
    cnt = db.fetchOne('select count(*) from flight_crews where flight_id=:flight_id and role="_other"', params)
    if cnt >= 5:
        return api_fail("В полет разрешается брать не более 5 пассажиров!")
    params['role'] = "_other"
    db.query("""delete from flight_crews 
        where flight_id = :flight_id and user_id=:user_id""", params, need_commit=True)
    db.insert('flight_crews', params)
    return api_ok()


def mcc_set_all_crew(self, params):
    """ params = {"flight_id": int, "crew": [{"role": "pilot", "user_id": 1}, {"role": "radist", "user_id": 2}] }"""
    if not db.fetchRow('select * from flights where id=:flight_id', params):
        return api_fail("Полет с указанным номером не существует")
    db.query("delete from flight_crews where flight_id=:flight_id", params, need_commit=True)
    for item in params['crew']:
        item['flight_id'] = params['flight_id']
    db.insert('flight_crews', params['crew'])
    return api_ok(crew=params['crew'])

def mcc_remove(self, params):
    """ params = {"flight_id": 1, "user_id": 2} """
    deleted = db.query("delete from flight_crews where flight_id = :flight_id and user_id = :user_id",
                       params, need_commit=True)
    return api_ok(deleted=db.cursor.rowcount)


def mcc_add_flight(self, params):
    """ params = {"departure": "2018-08-16 15:00:00", "dock": 2} """
    params['flight_id'] = db.insert('flights', params)
    return api_ok(flight=params)