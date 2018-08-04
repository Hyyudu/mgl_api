start_nodes = [
    {
        "company": "mat",
        "size": "small",
        "node_type_code": "march_engine",
        "name": "Восход",
        "params": {
            "thrust": 2,
            "accel": 1,
            "slowdown": -1,
            "heat_prod": -2,
            "volume": 0
        }
    },
    {
        "company": "mat",
        "size": "medium",
        "node_type_code": "march_engine",
        "name": "Заря",
        "params": {
            "thrust": 4,
            "accel": -3,
            "slowdown": -1,
            "heat_prod": -2,
            "volume": 2
        }
    },
    {
        "company": "mat",
        "size": "large",
        "node_type_code": "march_engine",
        "name": "Буран",
        "params": {
            "thrust": 5,
            "accel": 5,
            "slowdown": 2,
            "heat_prod": 0,
            "volume": 1
        }
    },
    {
        "company": "gd",
        "size": "large",
        "node_type_code": "march_engine",
        "name": "Ларри Пейдж",
        "params": {
            "thrust": 3,
            "accel": 2,
            "slowdown": 2,
            "heat_prod": 1,
            "volume": 2
        }
    },
    {
        "company": "gd",
        "size": "medium",
        "node_type_code": "march_engine",
        "name": "Сергей Брин",
        "params": {}
    },
    {
        "company": "mst",
        "size": "medium",
        "node_type_code": "march_engine",
        "name": "МСТ-ГД-4",
        "params": {
            "thrust": 0,
            "accel": 0,
            "slowdown": 0,
            "heat_prod": 0,
            "volume": 1
        }
    },
    {
        "company": "pre",
        "size": "large",
        "node_type_code": "march_engine",
        "name": "F-1",
        "params": {
            "thrust": 5,
            "accel": 4,
            "slowdown": 1,
            "heat_prod": -1,
            "volume": 0
        }
    },
    {
        "company": "kkg",
        "size": "small",
        "node_type_code": "march_engine",
        "name": "Subortus-S",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "medium",
        "node_type_code": "march_engine",
        "name": "Subortus-M",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "large",
        "node_type_code": "march_engine",
        "name": "Subortus-L",
        "params": {}
    },
    {
        "company": "mat",
        "size": "small",
        "node_type_code": "shunter",
        "name": "Эклипс",
        "params": {
            "turn": 0,  # макс. скорость поворота/тяга стрейфа
            "turn_acc": 2,  # скорость набора тяги
            "turn_slow": -1,  # скорость сброса тяги
            "heat_prod": 0,  # тепловыделение
            "volume": -1,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "medium",
        "node_type_code": "shunter",
        "name": "Галант",
        "params": {
            "turn": -3,  # макс. скорость поворота/тяга стрейфа
            "turn_acc": 5,  # скорость набора тяги
            "turn_slow": -1,  # скорость сброса тяги
            "heat_prod": 3,  # тепловыделение
            "volume": 2,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "large",
        "node_type_code": "shunter",
        "name": "Аутлендер",
        "params": {
            "turn": 5,  # макс. скорость поворота/тяга стрейфа
            "turn_acc": 5,  # скорость набора тяги
            "turn_slow": 1,  # скорость сброса тяги
            "heat_prod": 0,  # тепловыделение
            "volume": 1,  # масса/объем
        }
    },
    {
        "company": "gd",
        "size": "medium",
        "node_type_code": "shunter",
        "name": "Дисней",
        "params": {
            "turn": 0,  # макс. скорость поворота/тяга стрейфа
            "turn_acc": -1,  # скорость набора тяги
            "turn_slow": 0,  # скорость сброса тяги
            "heat_prod": 0,  # тепловыделение
            "volume": 1,  # масса/объем
        }
    },
    {
        "company": "mst",
        "size": "medium",
        "node_type_code": "shunter",
        "name": "МСТ-МД-3",
        "params": {
            "turn": 0,  # макс. скорость поворота/тяга стрейфа
            "turn_acc": 0,  # скорость набора тяги
            "turn_slow": 0,  # скорость сброса тяги
            "heat_prod": 0,  # тепловыделение
            "volume": 1,  # масса/объем
        }
    },
    {
        "company": "pre",
        "size": "large",
        "node_type_code": "shunter",
        "name": "J-2",
        "params": {
            "turn": 5,  # макс. скорость поворота/тяга стрейфа
            "turn_acc": 4,  # скорость набора тяги
            "turn_slow": 1,  # скорость сброса тяги
            "heat_prod": -1,  # тепловыделение
            "volume": 0,  # масса/объем
        }
    },
    {
        "company": "kkg",
        "size": "small",
        "node_type_code": "shunter",
        "name": "Timerus-S",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "medium",
        "node_type_code": "shunter",
        "name": "Timerus-M",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "large",
        "node_type_code": "shunter",
        "name": "Timerus-L",
        "params": {}
    },
    {
        "company": "mat",
        "size": "small",
        "node_type_code": "warp_engine",
        "name": "Галилей",
        "params": {
            "distort": -3,  # уровень искривления
            "warp_enter_consumption": 3,  # цена входа в варп
            "distort_acc": -1,  # набор/сброс искривления
            "distort_slow": -1,  # набор/сброс искривления
            "fuel_consumption": 3,  # потребление топлива
            "turn_consumption": -2,  # поворот в варпе
            "turn_speed": -2,  # поворот в варпе
            "volume": 0,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "medium",
        "node_type_code": "warp_engine",
        "name": "Ньютон",
        "params": {
            "distort": -3,  # уровень искривления
            "warp_enter_consumption": -1,  # цена входа в варп
            "distort_acc": 4,  # набор/сброс искривления
            "distort_slow": 4,  # набор/сброс искривления
            "fuel_consumption": -3,  # потребление топлива
            "turn_consumption": 3,  # поворот в варпе
            "turn_speed": 3,  # поворот в варпе
            "volume": 0,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "large",
        "node_type_code": "warp_engine",
        "name": "Архимед",
        "params": {}
    },
    {
        "company": "gd",
        "size": "large",
        "node_type_code": "warp_engine",
        "name": "Джафар",
        "params": {
            "distort": 3,  # уровень искривления
            "warp_enter_consumption": 3,  # цена входа в варп
            "distort_acc": 0,  # набор/сброс искривления
            "distort_slow": 0,  # набор/сброс искривления
            "fuel_consumption": 1,  # потребление топлива
            "turn_consumption": 0,  # поворот в варпе
            "turn_speed": 0,  # поворот в варпе
            "volume": 0,  # масса/объем
        }
    },
    {
        "company": "gd",
        "size": "medium",
        "node_type_code": "warp_engine",
        "name": "Аид",
        "params": {}
    },
    {
        "company": "mst",
        "size": "medium",
        "node_type_code": "warp_engine",
        "name": "МСТ-ПА-2",
        "params": {}
    },
    {
        "company": "pre",
        "size": "large",
        "node_type_code": "warp_engine",
        "name": "Waverider Mk1",
        "params": {
            "distort": 5,  # уровень искривления
            "warp_enter_consumption": 2,  # цена входа в варп
            "distort_acc": 4,  # набор/сброс искривления
            "distort_slow": 4,  # набор/сброс искривления
            "fuel_consumption": 5,  # потребление топлива
            "turn_consumption": 3,  # поворот в варпе
            "turn_speed": 3,  # поворот в варпе
            "volume": 0,  # масса/объем
        }
    },
    {
        "company": "kkg",
        "size": "small",
        "node_type_code": "warp_engine",
        "name": "Fortus-S",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "medium",
        "node_type_code": "warp_engine",
        "name": "Fortus-M",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "large",
        "node_type_code": "warp_engine",
        "name": "Fortus-L",
        "params": {}
    },
    {
        "company": "mat",
        "size": "small",
        "node_type_code": "radar",
        "name": "Арагорн",
        "params": {
            "range_max": 5,  # дальность действия
            "angle_min": 3,  # угол охвата
            "angle_max": 3,  # тоже угол охвата
            "angle_change": 0,  # скорость изменения угла/дальности
            "range_change": 0,  # скорость изменения угла/дальности
            "rotate_speed": 0,  # скорость поворота
            "volume": 1,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "medium",
        "node_type_code": "radar",
        "name": "Сусанин",
        "params": {
            "range_max": -2,  # дальность действия
            "angle_min": -2,  # угол охвата
            "angle_max": -2,  # тоже угол охвата
            "angle_change": 1,  # скорость изменения угла/дальности
            "range_change": 1,  # скорость изменения угла/дальности
            "rotate_speed": 1,  # скорость поворота
            "volume": 2,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "large",
        "node_type_code": "radar",
        "name": "Одиссей",
        "params": {
            "range_max": 2,  # дальность действия
            "angle_min": 2,  # угол охвата
            "angle_max": 2,  # тоже угол охвата
            "angle_change": -3,  # скорость изменения угла/дальности
            "range_change": -3,  # скорость изменения угла/дальности
            "rotate_speed": -3,  # скорость поворота
            "volume": 2,  # масса/объем
        }
    },
    {
        "company": "gd",
        "size": "large",
        "node_type_code": "radar",
        "name": "Patents Search",
        "params": {
            "range_max": 2,  # дальность действия
            "angle_min": 1,  # угол охвата
            "angle_max": 1,  # тоже угол охвата
            "angle_change": 1,  # скорость изменения угла/дальности
            "range_change": 1,  # скорость изменения угла/дальности
            "rotate_speed": 1,  # скорость поворота
            "volume": -1,  # масса/объем
        }
    },
    {
        "company": "gd",
        "size": "medium",
        "node_type_code": "radar",
        "name": "Suggest",
        "params": {}
    },
    {
        "company": "mst",
        "size": "medium",
        "node_type_code": "radar",
        "name": "МСТ-СР-2",
        "params": {}
    },
    {
        "company": "pre",
        "size": "large",
        "node_type_code": "radar",
        "name": "AN/ZPY-1 Starlite",
        "params": {
            "range_max": -1,  # дальность действия
            "angle_min": 1,  # угол охвата
            "angle_max": 1,  # тоже угол охвата
            "angle_change": 0,  # скорость изменения угла/дальности
            "range_change": 0,  # скорость изменения угла/дальности
            "rotate_speed": 2,  # скорость поворота
            "volume": 0,  # масса/объем
        }
    },
    {
        "company": "kkg",
        "size": "small",
        "node_type_code": "radar",
        "name": "Caperus-S",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "medium",
        "node_type_code": "radar",
        "name": "Caperus-M",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "large",
        "node_type_code": "radar",
        "name": "Caperus-L",
        "params": {}
    },
    {
        "company": "mat",
        "size": "medium",
        "node_type_code": "scaner",
        "name": "МарсСкан",
        "params": {}
    },
    {
        "company": "gd",
        "size": "large",
        "node_type_code": "scaner",
        "name": "R2-D2",
        "params": {
            "scan_speed": 0,  # скорость сканирования
            "scan_range": 2,  # дальность сканирования
            "drop_speed": -2,  # скорость сброса груза
            "drop_range": 1,  # дальность сброса груза
            "volume": -1,  # масса/объем
        }
    },
    {
        "company": "gd",
        "size": "medium",
        "node_type_code": "scaner",
        "name": "С-3РО",
        "params": {}
    },
    {
        "company": "mst",
        "size": "medium",
        "node_type_code": "scaner",
        "name": "МСТ-КР-2",
        "params": {}
    },
    {
        "company": "pre",
        "size": "medium",
        "node_type_code": "scaner",
        "name": "E-2 Hawkeye",
        "params": {
            "scan_speed": -1,  # скорость сканирования
            "scan_range": -1,  # дальность сканирования
            "drop_speed": 1,  # скорость сброса груза
            "drop_range": 4,  # дальность сброса груза
            "volume": 0,  # масса/объем
        }
    },
    {
        "company": "kkg",
        "size": "small",
        "node_type_code": "scaner",
        "name": "Invenirus-S",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "meduim",
        "node_type_code": "scaner",
        "name": "Invenirus-M",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "large",
        "node_type_code": "scaner",
        "name": "Invenirus-L",
        "params": {}
    },
    {
        "company": "mat",
        "size": "small",
        "node_type_code": "fuel_tank",
        "name": "Нагасаки",
        "params": {
            "fuel_volume": 5,  # объем топлива
            "fuel_protection": -1,  # защита топлива
            "radiation_def": -3,  # радиационная защита
            "volume": -1,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "medium",
        "node_type_code": "fuel_tank",
        "name": "Волоколамск",
        "params": {
            "fuel_volume": 4,  # объем топлива
            "fuel_protection": -3,  # защита топлива
            "radiation_def": -3,  # радиационная защита
            "volume": 2,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "large",
        "node_type_code": "fuel_tank",
        "name": "Припять",
        "params": {
            "fuel_volume": 5,  # объем топлива
            "fuel_protection": 0,  # защита топлива
            "radiation_def": 4,  # радиационная защита
            "volume": 1,  # масса/объем
        }
    },
    {
        "company": "gd",
        "size": "large",
        "node_type_code": "fuel_tank",
        "name": "Гаррисон",
        "params": {
            "fuel_volume": 4,  # объем топлива
            "fuel_protection": -2,  # защита топлива
            "radiation_def": 4,  # радиационная защита
            "volume": -1,  # масса/объем
        }
    },
    {
        "company": "gd",
        "size": "medium",
        "node_type_code": "fuel_tank",
        "name": "Лукьяненко",
        "params": {}
    },
    {
        "company": "mst",
        "size": "medium",
        "node_type_code": "fuel_tank",
        "name": "МСТ-ТБ-2",
        "params": {}
    },
    {
        "company": "pre",
        "size": "medium",
        "node_type_code": "fuel_tank",
        "name": "FT-1",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "small",
        "node_type_code": "fuel_tank",
        "name": "Lacus-s",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "medium",
        "node_type_code": "fuel_tank",
        "name": "Lacus-M",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "large",
        "node_type_code": "fuel_tank",
        "name": "Lacus-L",
        "params": {}
    },
    {
        "company": "mat",
        "size": "small",
        "node_type_code": "shields",
        "name": "Зевс",
        "params": {
            "radiation_def": 1,  # радиационная защита
            "desinfect_level": -2,  # уровень дезинфекции
            "mechanical_def": 1,  # механическая защита
            "heat_reflection": 1,  # степень отражения
            "heat_capacity": 1,  # теплоемкость
            "heat_sink": 1,  # теплоотвод
            "volume": 0,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "medium",
        "node_type_code": "shields",
        "name": "Ормузд",
        "params": {
            "radiation_def": -2,  # радиационная защита
            "desinfect_level": -2,  # уровень дезинфекции
            "mechanical_def": -2,  # механическая защита
            "heat_reflection": 0,  # степень отражения
            "heat_capacity": 2,  # теплоемкость
            "heat_sink": 2,  # теплоотвод
            "volume": 2,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "large",
        "node_type_code": "shields",
        "name": "Перун",
        "params": {}
    },
    {
        "company": "gd",
        "size": "large",
        "node_type_code": "shields",
        "name": "Микки Маус",
        "params": {
            "radiation_def": 2,  # радиационная защита
            "desinfect_level": 1,  # уровень дезинфекции
            "mechanical_def": 2,  # механическая защита
            "heat_reflection": 1,  # степень отражения
            "heat_capacity": 2,  # теплоемкость
            "heat_sink": 3,  # теплоотвод
            "volume": -1,  # масса/объем
        }
    },
    {
        "company": "gd",
        "size": "medium",
        "node_type_code": "shields",
        "name": "Дональд Дак",
        "params": {
            "radiation_def": 2,  # радиационная защита
            "desinfect_level": 1,  # уровень дезинфекции
            "mechanical_def": 2,  # механическая защита
            "heat_reflection": 1,  # степень отражения
            "heat_capacity": 2,  # теплоемкость
            "heat_sink": 3,  # теплоотвод
            "volume": -1,  # масса/объем
        }
    },
    {
        "company": "mst",
        "size": "large",
        "node_type_code": "shields",
        "name": "Свалинн-2",
        "params": {
            "radiation_def": 2,  # радиационная защита
            "desinfect_level": 3,  # уровень дезинфекции
            "mechanical_def": 3,  # механическая защита
            "heat_reflection": 3,  # степень отражения
            "heat_capacity": 3,  # теплоемкость
            "heat_sink": 3,  # теплоотвод
            "volume": 1,  # масса/объем
        }
    },
    {
        "company": "mst",
        "size": "medium",
        "node_type_code": "shields",
        "name": "Охайн-мини",
        "params": {}
    },
    {
        "company": "mst",
        "size": "small",
        "node_type_code": "shields",
        "name": "Охайн-микро",
        "params": {}
    },
    {
        "company": "pre",
        "size": "small",
        "node_type_code": "shields",
        "name": "Interceptor",
        "params": {
            "radiation_def": 0,  # радиационная защита
            "desinfect_level": -1,  # уровень дезинфекции
            "mechanical_def": -1,  # механическая защита
            "heat_reflection": -1,  # степень отражения
            "heat_capacity": 0,  # теплоемкость
            "heat_sink": 3,  # теплоотвод
            "volume": 0,  # масса/объем
        }
    },
    {
        "company": "kkg",
        "size": "small",
        "node_type_code": "shields",
        "name": "Мендель",
        "params": {
            "radiation_def": 1,  # радиационная защита
            "desinfect_level": 1,  # уровень дезинфекции
            "mechanical_def": 1,  # механическая защита
            "heat_reflection": 1,  # степень отражения
            "heat_capacity": 0,  # теплоемкость
            "heat_sink": 1,  # теплоотвод
            "volume": -1,  # масса/объем
        }
    },
    {
        "company": "kkg",
        "size": "medium",
        "node_type_code": "shields",
        "name": "Вейсман",
        "params": {
            "radiation_def": 3,  # радиационная защита
            "desinfect_level": 2,  # уровень дезинфекции
            "mechanical_def": 2,  # механическая защита
            "heat_reflection": 2,  # степень отражения
            "heat_capacity": 2,  # теплоемкость
            "heat_sink": 2,  # теплоотвод
            "volume": -1,  # масса/объем
        }
    },
    {
        "company": "kkg",
        "size": "large",
        "node_type_code": "shields",
        "name": "Морган",
        "params": {
            "radiation_def": 1,  # радиационная защита
            "desinfect_level": 1,  # уровень дезинфекции
            "mechanical_def": 1,  # механическая защита
            "heat_reflection": 1,  # степень отражения
            "heat_capacity": 0,  # теплоемкость
            "heat_sink": 1,  # теплоотвод
            "volume": -1,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "small",
        "node_type_code": "hull",
        "name": "Нинья",
        "params": {
            "configurability": 1,  # конфигурабельность
            "brand_lapse": 1,  # бренд-лапс
            "volume": 1,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "medium",
        "node_type_code": "hull",
        "name": "Пинта",
        "params": {
            "configurability": 2,  # конфигурабельность
            "brand_lapse": -2,  # бренд-лапс
            "volume": 0,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "large",
        "node_type_code": "hull",
        "name": "Санта-Мария",
        "params": {
            "configurability": 0,  # конфигурабельность
            "brand_lapse": 0,  # бренд-лапс
            "volume": 0,  # масса/объем
        }
    },
    {
        "company": "gd",
        "size": "large",
        "node_type_code": "hull",
        "name": "Adventureland",
        "params": {
            "configurability": 3,  # конфигурабельность
            "brand_lapse": 1,  # бренд-лапс
            "volume": 2,  # масса/объем
        }
    },
    {
        "company": "gd",
        "size": "medium",
        "node_type_code": "hull",
        "name": "Mickey's Toontown",
        "params": {}
    },
    {
        "company": "mst",
        "size": "large",
        "node_type_code": "hull",
        "name": "Ленинград-5",
        "params": {
            "configurability": 4,  # конфигурабельность
            "brand_lapse": 4,  # бренд-лапс
            "volume": 5,  # масса/объем
        }
    },
    {
        "company": "mst",
        "size": "medium",
        "node_type_code": "hull",
        "name": "Ленинград-3",
        "params": {}
    },
    {
        "company": "mst",
        "size": "small",
        "node_type_code": "hull",
        "name": "МСТ-М4",
        "params": {}
    },
    {
        "company": "pre",
        "size": "medium",
        "node_type_code": "hull",
        "name": "Unity",
        "params": {
            "configurability": 2,  # конфигурабельность
            "brand_lapse": 2,  # бренд-лапс
            "volume": 3,  # масса/объем
        }
    },
    {
        "company": "kkg",
        "size": "small",
        "node_type_code": "hull",
        "name": "Cutis-S",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "medium",
        "node_type_code": "hull",
        "name": "Cutis-M",
        "params": {}
    },
    {
        "company": "kkg",
        "size": "large",
        "node_type_code": "hull",
        "name": "Cutis-L",
        "params": {}
    },
    {
        "company": "mat",
        "size": "small",
        "node_type_code": "lss",
        "name": "Калина",
        "params": {
            "thermal_def": 0,  # термическая защита
            "co2_level": -2,  # поддержание уровня CO2
            "air_volume": 0,  # поддержание давления
            "air_speed": 0,  # поддержание давления
            "lightness": 0,  # уровень освещения
            "volume": 2,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "medium",
        "node_type_code": "lss",
        "name": "Гранта",
        "params": {
            "thermal_def": 1,  # термическая защита
            "co2_level": -2,  # поддержание уровня CO2
            "air_volume": 0,  # поддержание давления
            "air_speed": 0,  # поддержание давления
            "lightness": -1,  # уровень освещения
            "volume": 2,  # масса/объем
        }
    },
    {
        "company": "mat",
        "size": "large",
        "node_type_code": "lss",
        "name": "Приора",
        "params": {
            "thermal_def": 1,  # термическая защита
            "co2_level": -2,  # поддержание уровня CO2
            "air_volume": -1,  # поддержание давления
            "air_speed": -1,  # поддержание давления
            "lightness": 0,  # уровень освещения
            "volume": 2,  # масса/объем
        }
    },
    {
        "company": "gd",
        "size": "large",
        "node_type_code": "lss",
        "name": "Юрий Гагарин",
        "params": {
            "thermal_def": 2,  # термическая защита
            "co2_level": 3,  # поддержание уровня CO2
            "air_volume": 3,  # поддержание давления
            "air_speed": 3,  # поддержание давления
            "lightness": 0,  # уровень освещения
            "volume": -1,  # масса/объем
        }
    },
    {
        "company": "gd",
        "size": "medium",
        "node_type_code": "lss",
        "name": "Жугдэрдэмидийн Гуррагча",
        "params": {}
    },
    {
        "company": "mst",
        "size": "large",
        "node_type_code": "lss",
        "name": "ЛайфХак-Ультра",
        "params": {
            "thermal_def": 5,  # термическая защита
            "co2_level": 4,  # поддержание уровня CO2
            "air_volume": 5,  # поддержание давления
            "air_speed": 5,  # поддержание давления
            "lightness": 2,  # уровень освещения
            "volume": 1,  # масса/объем
        }
    },
    {
        "company": "mst",
        "size": "medium",
        "node_type_code": "lss",
        "name": "Ж-С-2",
        "params": {}
    },
    {
        "company": "mst",
        "size": "small",
        "node_type_code": "lss",
        "name": "Ж-М-4",
        "params": {}
    },
    {
        "company": "pre",
        "size": "medium",
        "node_type_code": "lss",
        "name": "EdEn",
        "params": {
            "thermal_def": 2,  # термическая защита
            "co2_level": 0,  # поддержание уровня CO2
            "air_volume": 0,  # поддержание давления
            "air_speed": 0,  # поддержание давления
            "lightness": -1,  # уровень освещения
            "volume": 0,  # масса/объем
        }
    },
    {
        "company": "kkg",
        "size": "small",
        "node_type_code": "lss",
        "name": "Гален",
        "params": {
            "thermal_def": 3,  # термическая защита
            "co2_level": 1,  # поддержание уровня CO2
            "air_volume": 2,  # поддержание давления
            "air_speed": 2,  # поддержание давления
            "lightness": -1,  # уровень освещения
            "volume": 1,  # масса/объем
        }
    },
    {
        "company": "kkg",
        "size": "medium",
        "node_type_code": "lss",
        "name": "Гиппократ",
        "params": {
            "thermal_def": 5,  # термическая защита
            "co2_level": 4,  # поддержание уровня CO2
            "air_volume": 5,  # поддержание давления
            "air_speed": 5,  # поддержание давления
            "lightness": 1,  # уровень освещения
            "volume": 2,  # масса/объем
        }
    },
    {
        "company": "kkg",
        "size": "large",
        "node_type_code": "lss",
        "name": "Авиценна",
        "params": {
            "thermal_def": 3,  # термическая защита
            "co2_level": 3,  # поддержание уровня CO2
            "air_volume": 2,  # поддержание давления
            "air_speed": 2,  # поддержание давления
            "lightness": -2,  # уровень освещения
            "volume": 1,  # масса/объем
        }
    }
]
