from collections import OrderedDict
from random import choices

from services.db import DB

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


def add_model(self, data):
    """ data: {<id>, name, level, description, size, node_type_code, company, {params}} """
    avail_vendors = db.fetchDict('select code, id from companies', {}, 'code', 'id')
    if not data.get('company') in avail_vendors:
        return {"status": "fail", "errors": "Не существует компания с кодом '{}'".format(data.get('company', ''))}
    new_model_id = db.insert('models', data)
    model_params = db.fetchColumn('select parameter_code from model_has_parameters where node_code=:node_type_code',
                                  data)
    insert_parameters = [
        {
            "model_id": new_model_id,
            "parameter_code": code,
            "value": data['params'].get(code, 0)
        }
        for code in model_params
    ]
    data['id'] = new_model_id
    db.insert('model_parameters', insert_parameters)

    if data['node_type_code'] == 'hull':
        slots = choices(detail_distribution.keys(), detail_distribution.values(),
                        k=data['params'].get('configurability', 0))
        insert_slots = [
            {
                "hull_id": data['id'],
                "slot_type": key,
                "amount": slots.count(key)
            } for key in detail_distribution
        ]
        db.insert_many('hull_slots', insert_slots)
        data['params']['insert_slots'] = insert_slots

    data['params'] = {param['parameter_code']: param['value'] for param in insert_parameters}
    return {"status": "ok", "data": data}


def read_model(self, data):
    model = db.fetchRow('select * from models where id=:id', data)
    if not model:
        return {"status": "fail", "errors": "Model with id {} not found".format(data.get('id'))}
    model['created'] = str(model[b'created'])
    del (model[b'created'])
    model['params'] = db.fetchDict('select parameter_code, value from v_model_params where model_id=:id', data,
                                   'parameter_code', 'value')
    model = apply_companies_perks(model)
    return {"status": "ok", "data": model}


def delete_model(self, data):
    db.query('delete from model_parameters where model_id=:id', data, need_commit=True)
    deleted = db.query('delete from models where id=:id', data, need_commit=True)
    return {"status": "ok", "deleted": deleted.rowcount}


def apply_companies_perks(model):
    if model['company'] == 'pre':
        if model['node_type_code'] == 'warp_engine':
            model['params']['distort'] *= 1.1
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


def read_all_models(self, params):
    sql = "SELECT * from models WHERE 1=1"
    add_where = db.construct_where(params)
    if add_where:
        sql += " and " + add_where
    result = db.fetchAll(sql)
    for item in result:
        item['created'] = str(item[b'created'])
        del (item[b'created'])
    return result
