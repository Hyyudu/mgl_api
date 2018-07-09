from services.db import DB

db = DB()


def add_model(self, data):
    """ data: {<id>, name, level, description, size, node_type_code, company, {params}} """
    avail_vendors = db.fetchDict('select code, id from companies', {}, 'code', 'id')
    if not data.get('company') in avail_vendors:
        return {"status": "fail", "errors": "Не существует компания с кодом '{}'".format(data.get('company',''))}
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
    data['params'] = {param['parameter_code']: param['value'] for param in insert_parameters}
    return {"status": "ok", "data": data}



def read_model(self, data):
    model = db.fetchRow('select * from models where id=:id', data)
    if not model:
        return {"status": "fail", "errors": "Model with id {} not found".format(data.get('id'))}
    model['created'] = str(model[b'created'])
    del(model[b'created'])
    model['params'] = db.fetchDict('select parameter_code, value from model_parameters where model_id=:id', data,
                                   'parameter_code', 'value')
    return {"status": "ok", "data": model}

def delete_model(self, data):
    db.query('delete from model_parameters where model_id=:id', data, need_commit=True)
    deleted = db.query('delete from models where id=:id', data, need_commit=True)
    return {"status": "ok", "deleted": deleted.rowcount}
