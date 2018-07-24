from collections import OrderedDict

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


def reserve_node(self, data):
    flight = db.fetchRow("""
select f.* from flights f
join flight_crews fc on f.id = fc.flight_id
where fc.role='supercargo' and fc.user_id = :user_id
and departure > Now()
order by departure asc 
limit 1""", data)
    if not flight:
        return api_fail("Вы не назначены ни на какой полет в качестве суперкарго")
    flight['departure'] = modernize_date(flight['departure'])
    if flight.get('status', '') == 'freight':
        return api_fail("""Вы назначены суперкарго на полет №{id} (вылет {departure}, док №{dock}).
В настоящее время ваш корабль уже зафрахтован, внесение изменений в конструкцию невозможно""".format(**flight))
    node = db.fetchRow('select * from nodes where id=:node_id', data)
    if not node:
        return api_fail("Узел с бортовым номером {} не существует и никогда не существовал".format(data.get('node_id')))
    return {"status": "ok"}
