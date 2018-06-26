from services.db import DB

db = DB()


def add_model(data):
    """ data: {<id>, name, level, description, size, node_type_code, vendor, {params}} """
    avail_vendors = db.fetchDict('select code, id from companies', {}, 'id', 'code')
    data['company_id'] = avail_vendors.get(data['vendor'], data['vendor'])
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
    db.insert('model_parameters', insert_parameters)


def read_model(model_id):
    model = db.fetchRow('select * from models where id=:model_id', vars())
    model['params'] = db.fetchDict('select parameter_code, value from model_parameters where model_id=:model_id', vars(),
                                   'parameter_code', 'value')
    return model

def delete_model(model_id):
    db.query('delete from model_parameters where model_id=:model_id', vars(), need_commit=True)
    db.query('delete from models where id=:model_id', vars(), need_commit=True)
