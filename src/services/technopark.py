import json
from typing import Dict, Any

from services.mcc import get_nearest_flight_for_supercargo
from services.misc import inject_db, api_fail, roundTo, apply_percent
from services.model_crud import read_models
from services.nodes_control import check_reserve_node
from services.sync import get_node_vector, get_node_params_with_desync


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

    # Применить перки корпуса
    hull_perks = self.db.fetchAll("""select hp.node_type_code, hp.parameter_code, hp.value
    from hull_perks hp
    join builds b on hp.hull_id = b.node_id and b.node_type_code = "hull"
    where b.flight_id = :flight_id """, params, 'parameter_code', 'value')

    for node_type, node in nodes.items():
        hull_perks_for_system = {
            perk['parameter_code']: perk['value']
            for perk in hull_perks
            if perk['node_type_code'] == 'node_type'
        }
        node['params'] = {key: apply_percent(value['value'], hull_perks_for_system.get(key, 100))
                          for key, value in json.loads(node['params_json']).items()}
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


@inject_db
def reserve_node(self, params):
    """ params = {"user_id": int, "node_id": int, "password": str} """
    build_item = check_reserve_node(None, params)
    # build_item =  {"flight_id":int, "node_id": int}
    if 'errors' in build_item:
        return build_item
    already_reserved = self.db.fetchRow("""
    select m.node_type_code, b.node_id
from nodes n
join models m on n.model_id = m.id
left join builds b on b.node_type_code = m.node_type_code and b.flight_id=:flight_id
where n.id=:node_id""", build_item)
    build_item['node_type_code'] = already_reserved['node_type_code']
    if already_reserved.get('node_id'):
        # Убираем ранее зарезервированный нод
        self.db.query('update nodes set status_code="free" where id=:node_id', already_reserved)
        self.db.query('delete from builds where flight_id=:flight_id and node_type_code=:node_type_code',
                 build_item)
    if build_item['node_type_code'] != 'hull':
        # рассчитываем вектора
        build_item['vector'] = build_item['total'] = get_node_vector(None, params)
        build_item['correction'] = "0"*16
        params_json = get_node_params_with_desync(
            vector=build_item['vector'],
            node_id=params['node_id']
        )

        build_item['params_json'] = json.dumps(params_json)

    else:
        model = read_models(None, {"node_id": build_item['node_id']})[0]
        hull_params = {
            "weight": model['params']['weight'],
            "volume": model['params']['volume'],
            "az_level": model['nodes'][0]['az_level']
        }
        build_item['params_json'] = json.dumps({
            key: {"percent": 100, "value": value}
            for key, value in hull_params.items()
        })
    self.db.insert('builds', build_item)
    self.db.query("""update nodes 
        set status_code="reserved", 
            connected_to_hull_id = null 
        where id=:node_id""", build_item, need_commit=True)
    return {"status": "ok"}


@inject_db
def get_my_reserved_nodes(self, params) -> Dict[str, Any]:
    """ params: {"user_id": int} """
    flight = get_nearest_flight_for_supercargo(None, params.get('user_id'))
    if not flight:
        return api_fail("Суперкарго {} не назначен ни на какой полет".format(params.get('user_id')))
    nodes = self.db.fetchDict(
        "select node_type_code, node_id from builds where flight_id=:id",
        flight, "node_type_code", "node_id"
    )
    return {"result": "ok", "flight": flight, "nodes": nodes}