from src.services.db import DB

db = DB()

def add_model(data):
    new_model_id = db.insert('models', data)
    model_params = db.fetchColumn('select parameter_code from model_has_parameters where node_code=:node_type_code', data)
