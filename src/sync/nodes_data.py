node_names = {"hull": "Корпус", "march_engine": "Маршевый двигатель", "shields": "Щиты"}

param_names = {
    "radiation_def": "Радиационная защита",
    "desinfect_level": "Уровень дезинфекции",
    "mechanical_def": "Механическая защита",
    "weight": "Масса",
    "volume": "Объем",
    "thrust": "Тяга",
    "thrust_rev": "Реверсная тяга",
    "accel": "Ускорение тяги",
    "accel_rev": "Ускорение реверсной тяги",
    "slowdown": "Сброс тяги",
    "slowdown_rev": "Сброс реверсной тяги",
    "heat_capacity": "Теплостойкость",
    "heat_sink": "Теплоотвод",
    "heat_prod": "Тепловыделение"
}

node_params = {
    123: {
        "type": "hull",
        "name": "Геракл-5Е",
        "params": {
            "weight": 2500,
            "volume": 1200
        },
        "slots": {
            "!": {1: 1},
            "*": {2: 8, 3: 8, 4: 2},
            "+": {2: 8, 3: 9, 4: 2, 5: 1}
        }
    },
    124: {
        "type": "shields",
        "name": "Эгида-12",
        "params": {
            "radiation_def": 150,
            "desinfect_level": 120,
            "mechanical_def": 1000,
            "weight": 200,
            "volume": 100,
        }
    },
    125: {
        "type": "march_engine",
        "name": "Ласточка-GT",
        "params": {
            "thrust": 1000,
            "thrust_rev": 200,
            "accel": 10,
            "accel_rev": 50,
            "slowdown": 30,
            "slowdown_rev": 50,
            "heat_prod": 80,
            "weight": 120,
            "volume": 80
        }
    }
}