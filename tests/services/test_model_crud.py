import pytest

from src.services.db import DB
from src.services.model_crud import (
    add_model,
    read_model,
    delete_model,
    calc_weight)

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
        "company": "kkg",
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


def test_delete_model2():
    delete_model(None, {"id": 1})


@pytest.mark.parametrize("node_type, size, volume, weight", [
    ("hull", "small", 1000, 200),
    ("hull", "medium", 1000, 1100),
    ("hull", "large", 1000, 3200),
    ("march_engine", "small", 100, 100 * 0.5 * 1.2),
    ("shunter", "medium", 100, 100 * 0.5 * 1.2),
    ("warp_engine", "large", 100, 100 * 0.7 * 1.2),
])
def test_calc_weight(node_type, size, volume, weight):

    assert calc_weight(node_type, size, volume) == weight
