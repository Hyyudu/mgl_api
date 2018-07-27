from services.db import DB

db = DB()


def add_model(self, data):
    """ data: {<id>, name, level, description, size, node_type_code, company, {params}} """
    avail_vendors = db.fetchColumn('select code from companies')
    if not data.get('company') in avail_vendors:
        return {"status": "fail", "errors": "Не существует компания с кодом '{}'".format(data.get('company', ''))}
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
    model = db.fetchRow('select * from models where id=:id', data)
    if not model:
        return {"status": "fail", "errors": "Model with id {} not found".format(data.get('id'))}
    model['params'] = db.fetchDict('select parameter_code, value from v_model_params where model_id=:id', data,
                                   'parameter_code', 'value')
    model = apply_companies_perks(model)
    return {"status": "ok", "data": model}


def delete_model(self, data):
    db.query('delete from nodes where model_id=:id', data, need_commit=True)
    db.query('delete from model_parameters where model_id=:id', data, need_commit=True)
    deleted = db.query('delete from models where id=:id', data, need_commit=True)
    return {"status": "ok", "deleted": deleted.rowcount}


def apply_companies_perks(model):
    if model['company'] == 'pre':
        if model['node_type_code'] == 'warp_engine':
            model['params']['distort_level'] *= 1.1
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

    return model


def read_models(self, params):
    sql = "SELECT * from models WHERE 1=1"
    add_where = db.construct_where(params)
    if add_where:
        sql += " and " + add_where
    params = db.construct_params(params)
    models = db.fetchAll(sql, params)
    if not models:
        return []

    ids = {"model_id": [model['id'] for model in models]}
    params_where = db.construct_where(ids)
    ids = db.construct_params(ids)
    all_params = db.fetchAll("select * from v_model_params where " + params_where, ids)

    all_nodes = db.fetchAll('select id, model_id, name, az_level, status_code, date_created'
                            ' from nodes where ' + params_where, ids)

    for model in models:
        model['params'] = {item['parameter_code']: item['value'] for item in all_params
                           if item['model_id'] == model['id']}
        model = apply_companies_perks(model)
        model['params']['weight'] = calc_weight(
            model['node_type_code'],
            model['size'],
            model['params']['volume']
        )
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
    return round(weight + hull_weight_add[size] if node_type == 'hull' else weight * node_weight_multiplier)
