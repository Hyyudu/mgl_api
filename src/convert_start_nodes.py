import json
from copy import deepcopy
from random import uniform

from numpy import interp

from src.services.model_crud import add_model


def roundTo(val, prec=3):
    return round(val, prec - len(str(int(val))))


estimates = {
    "march_engine": {
        "thrust": {-3: 700, 0: 1000, 5: 1500},
        "thrust_rev": {0: 0},
        "accel": {-3: 16, 0: 20, 5: 28},
        "slowdown": {-1: 16, 0: 20, 2: 28},
        "accel_rev": {0: 0},
        "slowdown_rev": {0: 0},
        "heat_prod": {-3: 100, 0: 80, 5: 60},
        "volume": {-1: 294, 0: 259, 2: 224}
    },
    "shunter": {
        "turn": {-3: 45, 0: 60, 5: 80},
        "strafe": {0: 0},
        "strafe_acc": {0: 0},
        "strafe_slow": {0: 0},
        "turn_acc": {-3: 80, 0: 90, 5: 105},
        "turn_slow": {-3: 80, 0: 90, 5: 105},
        "heat_prod": {-3: 92, 0: 80, 5: 60},
        "volume": {-1: 210, 0: 185, 2: 160},
    },
    "radar": {
        "range_max": {-3: 30, 0: 40, 5: 50},
        "angle_min": {-2: 25, 0: 20, 3: 15},
        "angle_max": {-2: 30, 0: 35, 3: 40},
        "angle_change": {-3: 0.8, 0: 1, 5: 1.2},
        "range_change": {-3: 0.8, 0: 1, 5: 1.2},
        "rotate_speed": {-3: 10, 0: 12, 5: 15},
        "volume": {-1: 210, 0: 185, 2: 160},
    },
    "warp_engine": {
        "distort": {-3: 800, 0: 1000, 5: 1200},
        "warp_enter_consumption": {-2: 30, 0: 21, 3: 21},
        "distort_acc": {-2: 3, 0: 4, 4: 6},
        "distort_slow": {-2: 3, 0: 4, 4: 6},
        "fuel_consumption": {-3: 0.12, 0: 0.1, 5: 0.08},
        "turn_consumption": {-2: 1.1, 0: 1, 3: 0.9},
        "turn_speed": {-2: 0.8, 0: 1, 3: 1.2},
        "volume": {-1: 333, 0: 288, 2: 259}
    },
    "fuel_tank": {
        "fuel_volume": {-3: 800, 0: 1000, 5: 1300},
        "fuel_protection": {-3: 3, 0: 5, 5: 7},
        "radiation_def": {-3: 80, 0: 100, 5: 140},
        "volume": {-1: 336, 0: 296, 2: 256},
    },
    "shields": {
        "radiation_def": {-2: 7, 0: 10, 4: 14},
        "desinfect_level": {-2: 50, 0: 80, 4: 120},
        "mechanical_def": {-2: 8, 0: 10, 4: 13},
        "heat_reflection": {-2: 8, 0: 10, 4: 13},
        "heat_capacity": {-2: 382.5, 0: 450, 4: 550},
        "heat_sink": {-2: 85, 0: 100, 4: 120},
        "volume": {-1: 315, 0: 277.5, 2: 240},
    },
    "hull": {
        "configurability": {-3: 16, 0: 19, 5: 24},
        "brand_lapse": {-2: 17, 0: 19, 4: 23},
        "volume": {
            "small": {-3: 800, 0: 1300, 5: 1800},
            "medium": {-3: 2000, 0: 2500, 5: 3000},
            "large": {-3: 3500, 0: 4250, 5: 5000}
        }
    },
    "scaner": {
        "scan_speed": {-3: 25, 0: 2.8, 5: 3},
        "scan_range": {-3: 42, 0: 50, 5: 60},
        "drop_speed": {-2: 38, 0: 41, 4: 45},
        "drop_range": {-2: 20, 0: 25, 4: 30},
        "volume": {-1: 147, 0: 129.5, 2: 112},

    },
    "lss": {
        "thermal_def": {-3: 4, 0: 10, 5: 20},  # термическая защита
        "co2_level": {-2: 50, 0: 100, 4: 200},  # поддержание уровня CO2
        "air_volume": {0: 0},  # поддержание давления
        "air_speed": {0: 0},  # поддержание давления
        "lightness": {-1: 0, 1: 20, 2: 36.5},  # уровень освещения
        "volume": {-1: 273, 0: 240, 2: 208},  # масса/объем
    }
}


def get_model_params(model1):
    model = deepcopy(model1)
    est = estimates[model['node_type_code']]
    if 'medium' in est['volume']:
        est['volume'] = est['volume'][model['size']]

    advance = sum(model['params'].values()) / sum([max(arr) for arr in est.values()])
    model['level'] = 2 if advance > 0.85 else 1 if advance > 0.45 else 0

    for name, arr in est.items():
        val = interp(model['params'].get(name, 0), list(arr.keys()), list(arr.values()))
        accuracy = 0.02
        val = roundTo(val * (uniform(1 - accuracy, 1 + accuracy)))
        if name in ('configurability', 'brand_lapse'):
            val = round(val)
        model['params'][name] = val

    return model


if __name__ == "__main__":
    from start_nodes import start_nodes
    for model in start_nodes:
        add_model(None, get_model_params(model))
