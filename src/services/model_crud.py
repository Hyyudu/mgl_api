import json
from typing import List

from numpy import interp
from services.misc import api_fail, inject_db, roundTo, apply_percent, get_logger


logger = get_logger(__name__)

MODEL_WOW_PERIOD_HOURS = 2

@inject_db
def add_model(self, data):
    """ params: {<id>, name, level, description, size, node_type_code, company, kpi_price, {params}, "upkeep"} """
    avail_vendors = self.db.fetchColumn('select code from companies')
    if not data.get('company') in avail_vendors:
        return api_fail("Не существует компания с кодом '{}'".format(data.get('company', '')))
    # Добавляем модель
    new_model_id = self.db.insert('models', data)
    # Устанавливаем ей вау-период
    self.db.query(f'update models set premium_expires = created + interval {MODEL_WOW_PERIOD_HOURS} hour where id=:id', {"id": new_model_id})
    model_params = self.db.fetchDict(
        'select parameter_code, def_value from model_has_parameters where node_code=:node_type_code',
        data, 'parameter_code', 'def_value')
    insert_parameters = [
        {
            "model_id": new_model_id,
            "parameter_code": code,
            "value": data['params'].get(code, def_value)
        }
        for code, def_value in model_params.items()
    ]
    data['id'] = new_model_id
    self.db.insert('model_parameters', insert_parameters)

    upkeep_parameters = [
        {
            "model_id": new_model_id,
            "resource_code": code,
            "amount": value
        }
        for code, value in data['upkeep'].items()
    ]
    self.db.insert('models_upkeep', upkeep_parameters)
    data['params'] = {param['parameter_code']: param['value'] for param in insert_parameters}
    return {"status": "ok", "data": data}


@inject_db
def read_model(self, data):
    """ params = {id: int} """
    model = self.db.fetchRow('select * from models where id=:id', data)
    if not model:
        return api_fail("Model with id {} not found".format(data.get('id')))
    model['params'] = self.db.fetchDict('select parameter_code, value from v_model_params where model_id=:id', data,
                                        'parameter_code', 'value')
    model = apply_companies_perks(model)
    return {"status": "ok", "data": model}


@inject_db
def delete_model(self, data):
    """ params = {id: int} """
    model_nodes_id = self.db.fetchOne("select group_concat(id) from nodes where model_id = :id", data)

    self.db.query('delete from nodes where model_id=:id', data, need_commit=True)
    self.db.query('delete from model_parameters where model_id=:id', data, need_commit=True)
    self.db.query('delete from pumps where section="models" and entity_id=:id', data, need_commit=True)
    self.db.query(f'delete from pumps where section="nodes" and entity_id in {model_nodes_id}', need_commit=True)
    deleted = self.db.query('delete from models where id=:id', data, need_commit=True)
    return {"status": "ok", "deleted": deleted.rowcount}


def apply_companies_perks(model):
    if model['company'] == 'pre':
        if model['node_type_code'] == 'warp_engine':
            model['params']['distort_level'] *= 1.15
        if model['node_type_code'] != 'hull':
            model['params']['volume'] = apply_percent(model['params']['volume'], -8)
        else:
            model['params']['volume'] = apply_percent(model['params']['volume'], 8)

    elif model['company'] in ['gd', 'mst']:
        model['params']['az_level'] = apply_percent(model['params']['az_level'], 15)

    elif model['company'] == 'kkg':
        if model['node_type_code'] == 'lss':
            for field in ['thermal_def', 'co2_level', 'air_volume', 'air_speed']:
                model['params'][field] = apply_percent(model['params'][field], 11)

    elif model['company'] == 'mat':
        node_type = model['node_type_code']
        if node_type == 'march_engine':
            model['params']['thrust'] = apply_percent(model['params']['thrust'], 15)
        # elif node_type == 'shunter':
        #     model['params']['turn_accel'] = apply_percent(model['params']['turn_accel'], 15)
        elif node_type == 'fuel_tank':
            model['params']['fuel_volume'] = apply_percent(model['params']['fuel_volume'], 15)

    return model


@inject_db
def read_models(self=None, params=None, read_nodes=True):
    """ params = {<name>: str, <node_type_code>: str/list[str], <level>: int/list[int], <size>: str/list[str],
        <company>: str/list[str], <node_id>: int} """
    params = params or {}
    sql = "SELECT m.* from models m "
    if 'node_id' in params:
        sql += " join nodes n on n.model_id = m.id WHERE n.id = :node_id"
    else:
        add_where = self.db.construct_where(params)
        if add_where:
            sql += " where " + add_where
        params = self.db.construct_params(params)
    models = self.db.fetchAll(sql, params)
    if not models:
        return []

    ids = {"model_id": [model['id'] for model in models]}
    params_where = self.db.construct_where(ids)
    ids = self.db.construct_params(ids)
    all_params = self.db.fetchAll("select * from v_model_params where " + params_where, ids)
    if read_nodes:
        nodes_sql = """
            select n.id, n.model_id, n.name, n.az_level, n.status, n.date_created, m.node_type_code,
                n.password,
                if ((n.password is not null and n.password!="") and (
                    n.premium_expires = 0
                    or n.premium_expires is null
                    or n.premium_expires > Now()
                ), 1, 0) is_premium 
            from nodes n
            join models m on m.id = n.model_id
            where """ + params_where
        if 'node_id' in params:
            nodes_sql += f" and n.id={int(params['node_id'])}"
        all_nodes = self.db.fetchAll(nodes_sql, ids, 'id')
        if all_nodes:
            hull_ids = [id for id, node in all_nodes.items() if node['node_type_code'] == 'hull']
            if hull_ids:
                node_ids = str(tuple(hull_ids)).replace(",)", ")")

                hull_data_sql = f"""
                SELECT hp.hull_id, 
                    group_concat(concat(nt.name, ', ', lower(p.short_name), ': ', hp.value, '%') separator "<br>\n") perks,
                    hs.slots_json
                FROM hull_perks hp
                    JOIN node_types nt on hp.node_type_code = nt.code
                    JOIN parameters_list p on hp.parameter_code = p.code
                    JOIN hull_slots hs on hp.hull_id = hs.hull_id
                WHERE hp.hull_id  in {node_ids} 
                GROUP by hp.hull_id
                """
                hull_data = self.db.fetchAll(hull_data_sql, {}, 'hull_id')

                for hull_id, data in hull_data.items():
                    all_nodes[hull_id]['perks'] = data['perks']
                    all_nodes[hull_id]['slots'] = json.loads(data['slots_json'])

    for model in models:
        model['params'] = {item['parameter_code']: item['value'] for item in all_params
                           if item['model_id'] == model['id']}
        model = apply_companies_perks(model)
        model['params']['weight'] = calc_weight(
            model['node_type_code'],
            model['size'],
            model['params']['volume']
        )
        model['params'] = {key: roundTo(val) for key, val in model['params'].items()}
        if read_nodes:
            model['nodes'] = [node for node in all_nodes.values() if node['model_id'] == model['id']]
    return models


def calc_weight(node_type: str, size: str, volume: float) -> float:
    densities = {
        "hull": 0.2,
        "march_engine": 0.5,
        "shunter": 0.5,
        "warp_engine": 0.7,
        "scaner": 0.4,
        "radar": 0.4,
        "shields": 0.6,
        "fuel_tank": 0.9,
        "lss": 0.6,
    }
    node_weight_multiplier = 1.2
    hull_weight_add = {"small": 0, "medium": 900, "large": 3000}
    weight = volume * densities[node_type]
    return roundTo(weight + hull_weight_add[size] if node_type == 'hull' else weight * node_weight_multiplier)


@inject_db
def get_model_upkeep_price(self, params):
    """ params: {"model_id": int} """
    return self.db.fetchDict('select resource_code, amount from models_upkeep where model_id=:model_id',
                             params, 'resource_code', 'amount')


def _get_minlevel(techlevel):
    return 0 if techlevel == 1 else 1


def get_model_level_by_technologies(techs: List[List[int]]) -> int:
    """ [[tech1.level, tech1.balls], [tech2.level, tech2.balls], ...]"""
    out = []
    if not techs:
        return 0
    elif len(techs) == 1:
        out = [_get_minlevel(techs[0][0])] * 3
    elif len(techs) == 3:
        out = [_get_minlevel(round(sum([x[0] for x in techs]) / 3))]
    elif len(techs) == 2:
        if {_get_minlevel(techs[0][0]), _get_minlevel(techs[1][0])} == {0,1}:
            out = [0.5, 0.5]
        else:
            out = [_get_minlevel(techs[0][0])]*2
    for tech in techs:
        out.append(interp(tech[1], (0, 10), (_get_minlevel(tech[0]), tech[0]+1)))
    return round(sum(out)/4)