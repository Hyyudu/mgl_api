node_names = {"hull": "Корпус", "march_engine": "Маршевый двигатель", "shields": "Щиты"}

param_names = {
    "radiation_def": "Радиационная защита",
    "desinfect_level": "Уровень дезинфекции",
    "mechanical_def": "Механическая защита",
    "weight": "Масса",
    "volume": "Объем",
    "thrust": "Тяга",
    "thrust_rev": "Реверсная тяга",
    "thrust_acc": "Ускорение тяги",
    "thrust_rev_acc": "Ускорение реверсной тяги",
    "thrust_slow": "Сброс тяги",
    "thrust_rev_slow": "Сброс реверсной тяги",
    "heat_capacity": "Теплостойкость",
    "heat_sync": "Теплоотвод",
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
            "thrust_acc": 10,
            "thrust_rev_acc": 50,
            "thrust_slow": 30,
            "thrust_rev_slow": 50,
            "heat_capacity": 30000,
            "heat_sync": 800,
            "weight": 120,
            "volume": 80
        }
    }
}