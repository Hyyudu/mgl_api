import json
from collections import OrderedDict, defaultdict
from random import randint, choice
from typing import Dict, Any, List

from services.economic import add_node_upkeep_pump
from services.mcc import get_nearest_flight_for_supercargo
from services.misc import modernize_date, api_fail, gen_array_by_weight, node_type_list, inject_db
from services.model_crud import read_models
from services.sync import get_rand_func, xor, get_func_vector


@inject_db
def create_node(self, params):
    """ params: {model_id: int, password: str} """
    model_id = params.get('model_id', 0)
    if not model_id:
        raise Exception("Не указан model_id!")
    model_id_dict = {"id": model_id}
    model = read_models(None, model_id_dict, read_nodes=False)

    if len(model) < 0:
        raise Exception(f"No model with id {model_id}")
    model = model[0]
    existing_nodes = self.db.fetchOne('select count(*) from nodes where model_id=:id', model_id_dict)
    insert_data = {
        "model_id": model_id,
        "name": "",
        "az_level": model['params']['az_level'],
        "password": params.get('password', ''),
        'premium_expires': None if not existing_nodes else model['premium_expires']
    }
    node_id = self.db.insert('nodes', insert_data)
    add_node_upkeep_pump(None, node_id=node_id, model=model)
    if model['node_type_code'] != 'hull':
        result = self.db.fetchRow('select * from nodes where id=:id', {"id": node_id})
        return result
    else:
        return create_hull(self, model, node_id=node_id)


@inject_db
def check_reserve_node(self, data):
    """ data = {user_id: int, node_id: int, password: str} """
    flight = get_nearest_flight_for_supercargo(None, data.get('user_id', 0))
    if not flight:
        return api_fail("Вы не назначены ни на какой полет в качестве суперкарго")
    flight['departure'] = modernize_date(flight['departure'])
    if flight.get('status', '') == 'freight':
        return api_fail("""Вы назначены суперкарго на полет №{id} (вылет {departure}, док №{dock}).
    В настоящее время ваш корабль уже зафрахтован, внесение изменений в конструкцию невозможно""".format(**flight))
    node = self.db.fetchRow("""select n.*, ns.name status, m.node_type_code,
            (n.premium_expires > Now() or n.premium_expires = 0 or n.premium_expires is null) as is_premium
         from nodes n 
            left join node_statuses ns on n.status_code = ns.code
            left join models m on m.id = n.model_id
         where n.id=:node_id""", data)
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
    if node['node_type_code'] != 'hull':
        flight_has_hull = self.db.fetchRow('select * from builds where flight_id=:id and node_type_code="hull"', flight)
        if not flight_has_hull:
            return api_fail("Сначала необходимо зарезервировать корпус!")
    return {"flight_id": flight['id'], "node_id": data['node_id']}


@inject_db
def set_password(self, data):
    """ params: {node_id: int, password: string} """
    affected = self.db.update('nodes', {"id": data.get('node_id', 0), 'password': data.get('password', '')}, 'id=:id')
    return {"result": "ok", "affected": affected}


@inject_db
def check_password(self, data):
    """ params: {node_id: int, password: string} """
    row = self.db.fetchRow('select id, password from nodes where id=:node_id', data)
    if not row:
        return api_fail("Неверный ID узла: {}".format(data.get('node_id', '')))
    if row.get('password') != data.get('password'):
        return api_fail('Пароль неверен')
    return {"result": "ok"}


@inject_db
def get_all_params(self, data) -> List[Dict[str, Any]]:
    return self.db.fetchAll('select * from v_node_parameter_list')


def generate_slots(amount: int) -> Dict[str, int]:
    detail_distribution = OrderedDict({
        "sum2": 6,
        "sum3": 8,
        "sum4": 3,
        "sum5": 1,
        "inv": 2,
        "con2": 6,
        "con3": 8,
        "con4": 4,
    })
    slots = gen_array_by_weight(detail_distribution, amount)
    return slots


@inject_db
def generate_hull_perks(self, size: int) -> List[Dict[str, Any]]:
    params_to_boost = self.db.fetchAll('''select node_code, parameter_code, increase_direction 
            from model_has_parameters where hull_boost=1''')
    param_dict = defaultdict(dict)
    for row in params_to_boost:
        param_dict[row['node_code']][row['parameter_code']] = row['increase_direction']
    if size == 'small':
        perks = [1, 1, -1]
    elif size == 'large':
        perks = [1, -1, -1]
    else:
        perks = [1, -1] if randint(0, 1) else [1, 1, -1, -1]
    while True:
        out = []
        outset = []
        for dir in perks:
            node_type_code = choice(list(param_dict.keys()))
            parameter = choice(list(param_dict[node_type_code].keys()))
            value = (20 if randint(1, 4) == 4 else 10) * dir * param_dict[node_type_code][parameter]
            out.append({"node_type_code": node_type_code, 'parameter_code': parameter, 'value': value})
            outset.append(node_type_code + "." + parameter)
        if len(outset) == len(set(outset)):
            break
    return out


@inject_db
def generate_hull_vectors(self, model: Dict) -> List[Dict[str, Any]]:
    distinction = model['params'].get('configurability', 0) - model['params'].get('brand_lapse', 0)
    node_types = node_type_list()
    params = {
        "size": model.get('size'),
        "level": model.get('level'),
        "company": model.get("company")
    }
    base_vectors_sql = "select node_code, vector from base_freq_vectors where " + self.db.construct_where(params)
    params = self.db.construct_params(params)
    vectors = self.db.fetchDict(base_vectors_sql, params, 'node_code', 'vector')
    lapse_functions = {}
    if distinction > 0:
        lapse = gen_array_by_weight(node_types, distinction)
        lapse_functions = {system: get_rand_func(size) for system, size in lapse.items()}
        for system, func in lapse_functions.items():
            vectors[system] = xor([vectors[system], get_func_vector(func)])
    ret = [
        {
            "node_type_code": system,
            "vector": vector,
            "lapse_func": lapse_functions.get(system, ''),
            # "lapse_vector": get_func_vector(lapse_functions.get(system, ''))
        }
        for system, vector in vectors.items()
    ]
    return ret


@inject_db
def create_hull(self, model: Dict, node_id: int):
    node_name = model['name'] + "-" + str(node_id)
    self.db.update('nodes', {"name": node_name, "id": node_id}, "id=:id")
    node = self.db.fetchRow('select * from nodes where id=:id', {"id": node_id})
    model['params']['configurability'] = round(model['params']['configurability'])
    model['params']['brand_lapse'] = round(model['params']['brand_lapse'])
    # создать слоты
    node['slots'] = generate_slots(model['params'].get('configurability'))
    self.db.insert('hull_slots', {"hull_id": node_id, "slots_json": json.dumps(node['slots'])})

    # создать бонусы/пенальти
    node['perks'] = generate_hull_perks(self, model['size'])
    for perk in node['perks']:
        perk['hull_id'] = node_id
        self.db.insert('hull_perks', perk)

    # создать частотные рисунки
    node['vectors'] = generate_hull_vectors(self, model)
    for vector in node['vectors']:
        vector['hull_id'] = node_id
        self.db.insert('hull_vectors', vector)

    return node
