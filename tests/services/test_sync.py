import pytest
from services.sync import get_desync_percent

@pytest.mark.parametrize("node_type_code, vector, percents", [
    ("march_engine", "01"*8, {
        "thrust": 20,
        "thrust_rev": 70,
        "accel": 100,
        "accel_rev": 70,
        "slowdown": 70,
        "slowdown_rev": 70,
        "heat_prod": 130
    }),
    ("scaner", "0"*8 + "1"*8, {
        "drop_range": 60,
        "drop_speed": 20,
        "scan_range": 100,
        "scan_speed": 60,
    })

])
def test_get_desync_percent(node_type_code, vector, percents):
    assert get_desync_percent(vector, node_type_code) == percents