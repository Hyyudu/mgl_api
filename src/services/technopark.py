import json

from services.misc import inject_db, api_fail


@inject_db
def get_flight_params(self, params):
    """ params = {flight_id: int}"""
    if not 'flight_id' in params:
        return api_fail('Этот url надо вызывать через POST и передавать в тело {"flight_id": int}')
    nodes = self.db.fetchAll("""
select b.node_type_code, n.name ship_name, m.name model_name, m.company, b.params_json
from builds b
join nodes n on n.id = b.node_id
join models m on n.model_id = m.id
where b.flight_id = :flight_id""", params, 'node_type_code')
    for node_type, node in nodes.items():
        node['params'] = {key: value['value'] for key, value in json.loads(node['params_json']).items()}
    flight = self.db.fetchRow("""
    select f.id flight_id, f.departure flight_start_time, f.status,
        f.dock from flights f
        where id = :flight_id""", params)
    known_resources = self.db.fetchAll("select code, name from resources where is_active=1 order by 1")
    cargo = self.db.fetchAll("""
    select fl.code, fl.company, l.weight 
from flight_luggage fl 
join v_luggages l on fl.code = l.code and (fl.company = l.company or (fl.company is null and l.company is null))
where fl.id = :flight_id""", params)

    flight['ship'] = {
        "name": nodes['hull']['ship_name'],
        "nodes_weight": sum([float(node['params']['weight']) for node in nodes.values()])
    }
    flight['params'] = {node_type: node['params'] for node_type, node in nodes.items()}
    flight['known_minerals'] = known_resources
    flight['cargo'] = {"mines": [], "beacons": [], "modules": []}
    for item in cargo:
        flight['cargo'][item['code'] + 's'].append({"company": item['company'], "weight": item['weight']})
    return flight
