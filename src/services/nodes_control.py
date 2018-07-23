from collections import OrderedDict

from services.db import DB
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
