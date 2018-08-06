from services.db import DB
from services.misc import api_fail, inject_db, roundTo


db = DB()


def add_model(self, data):
    """ params: {<id>, name, level, description, size, node_type_code, company, {params}} """
    avail_vendors = db.fetchColumn('select code from companies')
    if not data.get('company') in avail_vendors:
        return api_fail("Не существует компания с кодом '{}'".format(data.get('company', '')))
    new_model_id = db.insert('models', data)
    db.query('update models set premium_expires = created + interval 3 hour where id=:id', {"id": new_model_id})
    model_params = db.fetchDict(
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
    db.insert('model_parameters', insert_parameters)

    data['params'] = {param['parameter_code']: param['value'] for param in insert_parameters}
    return {"status": "ok", "data": data}


def read_model(self, data):
    """ params = {id: int} """
    model = db.fetchRow('select * from models where id=:id', data)
    if not model:
        return api_fail("Model with id {} not found".format(data.get('id')))
    model['params'] = db.fetchDict('select parameter_code, value from v_model_params where model_id=:id', data,
                                   'parameter_code', 'value')
    model = apply_companies_perks(model)
    return {"status": "ok", "data": model}


def delete_model(self, data):
    """ params = {id: int} """
    db.query('delete from nodes where model_id=:id', data, need_commit=True)
    db.query('delete from model_parameters where model_id=:id', data, need_commit=True)
    deleted = db.query('delete from models where id=:id', data, need_commit=True)
    return {"status": "ok", "deleted": deleted.rowcount}


def apply_companies_perks(model):
    if model['company'] == 'pre':
        if model['node_type_code'] == 'warp_engine':
            model['params']['distort_level'] *= 1.12
        if model['node_type_code'] != 'hull':
            model['params']['volume'] *= 0.92
        else:
            model['params']['volume'] *= 1.08

    elif model['company'] in ['gd', 'mst']:
        model['params']['az_level'] *= 1.15

    elif model['company'] == 'kkg':
        if model['node_type_code'] == 'lss':
            for field in ['thermal_def', 'co2_level', 'air_volume', 'air_speed']:
                model['params'][field] *= 1.09

    elif model['company'] == 'mat':
        node_type = model['node_type_code']
        if node_type == 'march_engine':
            model['params']['thrust'] *= 1.12
        elif node_type == 'shunter':
            model['params']['strafe'] = 1.12 * model['params'].get('strafe', 0)
        elif node_type == 'fuel_tank':
            model['params']['fuel_volume'] *= 1.12

    return model


@inject_db
def read_models(self=None, params=None):
    """ params = {<name>: str, <node_type_code>: str/list[str], <level>: int/list[int], <size>: str/list[str],
        <company>: str/list[str], <node_id>: int} """
    params = params or {}
    sql = "SELECT m.* from models m "
    if 'node_id' in params:
        sql += " join nodes n on n.model_id = m.id WHERE n.id = :node_id"
    else:
        add_where = db.construct_where(params)
        if add_where:
            sql += " where " + add_where
        params = self.db.construct_params(params)
    models = self.db.fetchAll(sql, params)
    if not models:
        return []

    ids = {"model_id": [model['id'] for model in models]}
    params_where = self.db.construct_where(ids)
    ids = self.db.construct_params(ids)
    all_params = self.db.fetchAll("select * from v_model_params where is_hidden=0 and " + params_where, ids)

    all_nodes = self.db.fetchAll("""
        select id, model_id, name, az_level, status_code, date_created,
            if (password is not null and (
                premium_expires = 0
                or premium_expires is null
                or premium_expires > Now()
            ), 1, 0) is_premium 
        from nodes where """ + params_where, ids)

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
        model['nodes'] = [node for node in all_nodes if node['model_id'] == model['id']]
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


def get_model_upkeep_price(self, params):
    """ params: {"model_id": int} """
    return db.fetchDict('select resource_code, amount from models_upkeep where model_id=:model_id',
                        params, 'resource_code', 'amount')
