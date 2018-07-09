import json
from random import random

from numpy import interp

estimates = {
    "march_engine": {
        "thrust": {-3: 700, 0: 1000, 5: 1500},
        "thrust_rev": {0: 0},
        "accel": {-3: 16, 0: 20, 5: 28},
        "slowdown": {-1: 16, 0: 20, 2: 28},
        "accel_rev": {0: 0},
        "slowdown_rev": {0: 0},
        "heat_prod": {-3: 100, 0: 80, 5: 60},
        "volume": {-1: 315, 0: 277.5, 2: 240}
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
    }
}

model = {
    "vendor": "mat",
    "node_type_code": "shunter",
    "name": "Аутлендер",
    "size": "large",
    "params": {
        "turn": 5,
        "turn_acc": 5,
        "turn_slow": 1,
        "heat_prod": 0,
        "volume": 1,
    }
}

est = estimates[model['node_type_code']]

advance = sum(model['params'].values()) / sum([max(arr) for arr in est.values()])
model['level'] = 2 if advance > 0.9 else 1 if advance > 0.45 else 0

for name, arr in est.items():
    val = interp(model['params'].get(name, 0), list(arr.keys()), list(arr.values()))
    accuracy = 0.97
    val = round(val * (random() * 2 * (1 - accuracy) + accuracy))
    model['params'][name] = val

print(json.dumps(model))
