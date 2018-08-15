from services.db import DB


db = DB()

data = {
    "march_engine": {
        "thrust": [700, 1000, 1500, 3000, 5000, 5500],
        "thrust_rev": [0, 0, 0, 1500, 2500, 2700],
        "accel": [16, 20, 28, 100, 300, 400],
        "accel_rev": [0, 0, 0, 100, 300, 400],
        "slowdown": [16, 20, 28, 100, 300, 400],
        "slowdown_rev": [0, 0, 0, 100, 300, 400],
        "heat_prod": [83, 80, 75, 60, 45, 40],
        "volume": [294, 259, 224],
    },
    "warp_engine": {
        "distort": [800, 1000, 1200, 1500, 2000, 2200],
        "warp_enter_consumption": [30, 25, 21, 18, 15, 12],
        "distort_acc": [3, 4, 6, 8, 12, 16],
        "distort_slow": [3, 4, 6, 8, 12, 16],
        "consumption": [0.12, 0.1, 0.08, 0.05, 0.03, 0.025],
        "turn_speed": [0.8, 1, 1.2, 3, 5, 6],
        "turn_consumption": [1.1, 1, 0.9, 0.6, 0.25, 0.2],
        "volume": [315, 277.5, 240],
    },

    "shunter": {
        "turn": [45, 60, 80, 240, 540, 720],
        "strafe": [0, 0, 0, 1500, 2500, 2700],
        "turn_acc": [80, 90, 105, 210, 300, 360],
        "strafe_acc": [0, 0, 0, 100, 300, 400],
        "turn_slow": [80, 90, 105, 210, 300, 360],
        "strafe_slow": [0, 0, 0, 100, 300, 400],
        "heat_prod": [92, 80, 60, 50, 40, 30],
        "volume": [210, 185, 160],
    },

    "scaner": {
        "drop_range": [20, 25, 30, 75, 130, 180],
        "drop_speed": [38, 41, 45, 75, 150, 225],
        "scan_range": [42, 50, 60, 100, 150, 180],
        "scan_speed": [2.5, 2.8, 3, 5, 10, 15],
        "volume": [147, 129.5, 112],
    },

    "radar": {
        "range_max": [30, 40, 50, 120, 180, 200],
        "angle_min": [25, 20, 15, 10, 5, 3],
        "angle_max": [30, 35, 40, 60, 75, 90],
        "angle_change": [0.8, 1, 1.2, 3, 5, 5],
        "range_change": [0.8, 1, 1.2, 8, 20, 25],
        "rotate_speed": [10, 12, 15, 45, 90, 120],
        "volume": [210, 185, 160],
    },

    "fuel_tank": {
        "fuel_volume": [800, 1000, 1300, 1800, 2500, 2700],
        "fuel_protection": [3, 5, 8, 40, 70, 80],
        "radiation_def": [80, 100, 140, 250, 400, 500],
        "volume": [336, 296, 256],
    },

    "lss": {
        "thermal_def": [4, 10, 20, 40, 60, 75],
        "co2_level": [50, 100, 200, 370, 470, 500],
        "air_volume": [2050, 2200, 2500, 3300, 4200, 4500],
        "air_speed": [2, 2, 2, 2, 2, 2],
        "lightness": [0, 20, 36.5, 57.5, 70, 80],
        "volume": [273, 240.5, 208],

    },

    "shields": {
        "radiation_def": [7, 10, 14, 30, 45, 50],
        "desinfect_level": [50, 80, 120, 220, 300, 350],
        "mechanical_def": [90, 100, 120, 180, 240, 280],
        "heat_reflection": [90, 100, 120, 180, 240, 280],
        "heat_capacity": [382.5, 450, 553.5, 1350, 2200, 2500],
        "heat_sink": [85, 100, 120, 300, 500, 600],
        "volume": [315, 277.5, 240],
    },

    "hull": {
        "configurability": [16, 19, 24, 35, 50, 60],
        "brand_lapse": [17, 19, 23, 33, 45, 50],
        "volume": [2000, 2500, 3000],
    }
}




for node_type_code, params in data.items():
    for param, values in params.items():
        print('{"node_type_code": "'+node_type_code+'", "parameter_code": "'+param+'", "value": 0}, ')
        # update_row = {
        #     "node_code": node_type_code,
        #     "parameter_code": param,
        #     "val_start_bad": values[0],
        #     "val_start_normal": values[1],
        #     "val_start_good": values[2]
        # }
        # if len(values) == 6:
        #     update_row.update({
        #         "val_middle": values[3],
        #         "val_end": values[4],
        #         "val_ideal": values[5]
        #     })
        # db.update('model_has_parameters', update_row,
        #           " node_code = :node_code and parameter_code=:parameter_code")
        # exit()