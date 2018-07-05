from src.services.model_crud import (
    add_model,
    read_model,
    delete_model,
)
from src.services.db import DB

db1 = DB()

def test_delete_model():
    delete_model(None, {"id": 1})
    assert db1.fetchAll("select * from model_parameters where model_id = 1") == []
    assert db1.fetchAll("select * from models where id = 1") == []

def test_add_model():
    data = {
        "id": 1,
        "name": "Тестобак-1",
        "description": "Просто тестовый бак",
        "level": 1,
        "node_type_code": "fuel_tank",
        "size": "medium",
        "company_id": 3,
        "params": {
            "az_level": 100,
            "fuel_volume": 200,
            "compact": 5,
            "radiation_def": 20,
            "weight": 300,
            "volume": 400,
        }
    }
    add_model(None, data)

    new_model = read_model(None, {"id": 1}).get('data')
    assert all([new_model[field] == data[field] for field in data])