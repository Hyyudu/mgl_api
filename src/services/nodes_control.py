from collections import OrderedDict
from typing import Dict, Any

from services.db import DB
from services.misc import modernize_date, api_fail
from services.model_crud import read_models


db = DB()
detail_distribution = OrderedDict({
    "sum2": 6,
    "sum3": 8,
    "sum4": 3,
    "sum5": 1,
    "inv": 4,
    "con2": 6,
    "con3": 8,
    "con4": 2,
})


def create_node(self, params):
    """ params: {model_id: int, password: str} """
    model_id = params.get('model_id')
    if not model_id:
        raise Exception("Model id not specified!")
    model_id_dict = {"id": model_id}
    model = read_models(None, model_id_dict)

    if len(model) < 0:
        raise Exception("No model with id {}".format(model_id))
    model = model[0]
    existing_nodes = db.fetchOne('select count(*) from nodes where model_id=:id', model_id_dict)
    if model['node_type_code'] != 'hull':
        insert_data = {
            "model_id": model_id,
            "name": "",
            "az_level": model['params']['az_level'],
            "password": params.get('password', ''),
            'premium_expires': None if not existing_nodes else model['premium_expires']
        }
        new_id = db.insert('nodes', insert_data)
        result = db.fetchRow('select * from nodes where id=:id', {"id": new_id})
        return result


def get_nearest_flight_for_supercargo(user_id):
    flight = db.fetchRow("""
        select f.* from flights f
        join flight_crews fc on f.id = fc.flight_id
        where fc.role='supercargo' and fc.user_id = :user_id
        and departure > Now()
        order by departure asc 
        limit 1""", {"user_id": user_id})
    return flight


def check_reserve_node(data):
    flight = get_nearest_flight_for_supercargo(data.get('user_id', 0))
    if not flight:
        return api_fail("Вы не назначены ни на какой полет в качестве суперкарго")
    flight['departure'] = modernize_date(flight['departure'])
    if flight.get('status', '') == 'freight':
        return api_fail("""Вы назначены суперкарго на полет №{id} (вылет {departure}, док №{dock}).
    В настоящее время ваш корабль уже зафрахтован, внесение изменений в конструкцию невозможно""".format(**flight))
    node = db.fetchRow("""select n.*, ns.name status,
            (n.premium_expires > Now() or n.premium_expires = 0 or n.premium_expires is null) as is_premium
         from nodes n 
            left join node_statuses ns on n.status_code = ns.code
         where id=:node_id""", data)
    if not node:
        return api_fail("Узел с бортовым номером {} не существует и никогда не существовал".format(data.get('node_id')))
    if node.get('status_code') != 'free':
        return api_fail("Узел с бортовым номером {} сейчас находится в статусе '{}' и недоступен вам для резерва".
                        format(node.get('id'), node.get('status')))
    if node.get('is_premium'):
        if not data.get('password'):
            return api_fail("Этот узел находится в премиум-доступе. Выясните у создателей пароль доступа")
        elif data.get('password') != node.get('password'):
            return api_fail('Ваш пароль для доступа к этому узлу неверен')
    return {"flight_id": flight['id'], "node_id": data['node_id']}


def reserve_node(self, data):
    """ data = {"user_id": int, "node_id": int, "password": str} """
    reserve_result = check_reserve_node(data)
    if 'errors' in reserve_result:
        return reserve_result
    reserved_data = db.fetchRow("""
    select m.node_type_code, b.node_id
from nodes n
join models m on n.model_id = m.id
left join builds b on b.node_type_code = m.node_type_code and b.flight_id=:flight_id
where n.id=:node_id""", reserve_result)
    reserve_result['node_type_code'] = reserved_data['node_type_code']
    if reserved_data.get('node_id'):
        db.query('update nodes set status_code="free" where id=:node_id', reserved_data)
        db.query('delete from builds where flight_id=:flight_id and node_type_code=:node_type_code',
                 reserve_result)
    db.insert('builds', reserve_result)
    db.query('update nodes set status_code="reserved" where id=:node_id', reserve_result, need_commit=True)
    return {"status": "ok"}


def get_my_reserved_nodes(self, data) -> Dict[str, Any]:
    """ data: {"user_id": int} """
    flight = get_nearest_flight_for_supercargo(data.get('user_id'))
    if not flight:
        return api_fail("Суперкарго {} не назначен ни на какой полет".format(data.get('user_id')))
    nodes = db.fetchDict(
        "select node_type_code, node_id from builds where flight_id=:id",
        flight, "node_type_code", "node_id"
    )
    return {"result": "ok", "flight": flight, "nodes": nodes}
