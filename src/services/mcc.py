from services.misc import modernize_date, api_ok, api_fail, inject_db, get_logger


logger = get_logger(__name__)

@inject_db
def mcc_dashboard(self, params):
    """ no params"""
    flights = self.db.fetchAll("""
    SELECT f.id, f.dock, f.status, f.company, date_format(f.departure, "%d.%m.%Y %H:%i") departure, 
        n.id node_id, n.name node_name, m.name model_name
    FROM flights f
        LEFT JOIN builds b on f.id = b.flight_id and b.node_type_code = 'hull'
        LEFT JOIN nodes n on b.node_id = n.id
        LEFT JOIN models m on n.model_id = m.id
    WHERE status in ('prepare', 'freight')
    order by f.departure, f.dock""", associate='id')
    flight_ids = tuple(flights.keys())
    for flight in flights.values():
        flight['departure'] = modernize_date(flight['departure'])
        flight['crew'] = []
        if flight['node_name'] and flight['model_name']:
            flight['ship'] = (
                "{node_name}, класс {model_name}".format(**flight)
                if flight.get('node_name', '') != '{model_name}-{node_id}'.format(**flight)
                else flight.get('node_name', '')
            )
        del (flight['node_name'], flight['model_name'])
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


@inject_db
def mcc_set_all_crew(self, params):
    """ params = {"flight_id": int, "crew": [{"role": "pilot", "user_id": 1}, {"role": "radist", "user_id": 2}] }"""
    if not self.db.fetchRow('select * from flights where id=:flight_id', params):
        return api_fail("Полет с указанным номером не существует")
    self.db.query("delete from flight_crews where flight_id=:flight_id", params, need_commit=True)
    if params['crew']:
        for item in params['crew']:
            item['flight_id'] = params['flight_id']
        self.db.insert('flight_crews', params['crew'])
    return api_ok(crew=params['crew'])


@inject_db
def mcc_add_flight(self, params):
    """ params = {"departure": "2018-08-16 15:00:00", "dock": 2, "company": "pre"} """
    params['flight_id'] = self.db.insert('flights', params)
    return api_ok(flight=params)


@inject_db
def mcc_assign_flight(self, params):
    """ params = {"flight_id": int, "company": mat/mst/gd/pre/kkg/ideo} """
    company = params.get('company', '')
    if company not in ('mat', 'mst', 'gd', 'pre', 'kkg', 'ideo'):
        return api_fail("Неверный код компании")
    params['id'] = params['flight_id']
    self.db.update('flights', params, "id=:id")
    return api_ok(updated=self.db.affected_rows())


@inject_db
def get_nearest_flight_for_role(self, params):
    """ params: {user_id: int, role: string}  """
    flight = self.db.fetchRow("""
        select f.* from flights f
        join flight_crews fc on f.id = fc.flight_id
        where fc.role=:role and fc.user_id = :user_id
        and departure > Now()
        order by departure asc 
        limit 1""", params)
    if flight:
        flight['crew'] = self.db.fetchDict("""select fc.role, u.name
    from flight_crews fc
    left join users u on fc.user_id = u.id
    where fc.flight_id = :id""", flight, 'role', 'name')
    return flight


@inject_db
def get_nearest_flight_for_supercargo(self, user_id):
    return get_nearest_flight_for_role(self, {"user_id": user_id, "role": 'supercargo'})


@inject_db
def get_nearest_flight_for_engineer(self, user_id):
    return get_nearest_flight_for_role(self, {"user_id": user_id, "role": 'engineer'})


@inject_db
def freight_flight(self, params):
    """ params {flight_id: int} """
    return api_fail("Пока не реализовано")


@inject_db
def flight_died(self, params):
    """ params = {flight_id: int} """
    self.db.query("update flights set status='lost' where id=:flight_id", params)
    # Находим все узлы того полета
    node_ids = self.db.fetchColumn("select node_id from builds where flight_id=:flight_id", params)
    nodelist = "(" + ", ".join(node_ids) + ")"
    # Ставим всем узлам статус "утерян"
    self.db.query(f"update nodes set status_code='lost' where id in {nodelist}", None, need_commit=True)
    # Отключаем их насосы в экономике
    self.db.query(f"update pumps set date_end = Now() where section='nodes' and entity_id in {nodelist}",
                  need_commit=True)
    return api_ok()


@inject_db
def flight_returned(self, params):
    self.db.query("update flights set status='returned' where id = :flight_id", params)
    # Находим все узлы того полета
    nodes = self.db.fetchDict("select node_type_code, node_id from builds where flight_id=:flight_id", params,
                                 'node_type_code', 'node_id')
