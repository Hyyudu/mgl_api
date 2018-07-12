desync_penalties = {
    "march_engine": {
        "thrust":           lambda s: -10 * s[1::2].count('1'),
        "thrust_rev":       lambda s: -10 * s[8:14].count('1'),
        "accel":            lambda s: -10 * s[::2].count('1'),
        "accel_rev":        lambda s: -10 * s[2:8].count('1'),
        "slowdown":         lambda s: -15 * (s[:2]+s[-2:]).count('1'),
        "slowdown_rev":     lambda s: -15 * (s[:2]+s[-2:]).count('1'),
        "heat_prod":        lambda s:   5 * (s[2:14]).count('1'),
    },
    "shunter": {
        "turn":             lambda s: -10 * s[::2].count('1'),
        "strafe":           lambda s: -10 * s[8:].count('1'),
        "turn_acc":         lambda s: -10 * s[1::2].count('1'),
        "strafe_acc":       lambda s: -15 * s[4:8].count('1'),
        "turn_slow":        lambda s: -15 * s[:4].count('1'),
        "strafe_slow":      lambda s: -15 * s[:4].count('1'),
        "heat_prod":        lambda s:   5 * (s[4:]).count(1),
    },
    "warp_engine": {
        "distort":          lambda s: -15 * s[3::4].count('1'),
        "distort_acc":      lambda s: -10 * s[9:].count('1'),
        "distort_slow":     lambda s: -15 * (s[1]+s[3]+s[5]+s[10]+s[12]+s[14]).count('1'),
        "warp_enter_consumption": lambda s:  20 * (s[1::3]+s[2::3]).count('1'),
        "consumption":      lambda s: 12 * (s[:9:2]+s[7::2]).count('1'),
        "turn_consumption": lambda s: 20 * s[:9:2].count(1),
        "turn_speed":       lambda s: -15 * (s[1:8:2]+s[0]).count('1'),
    },
    "scaner": {
        "drop_range":       lambda s: -10 * s[1::2].count(1),
        "drop_speed":       lambda s: -10 * s[8:].count(1),
        "scan_range":       lambda s: -10 * s[:8].count(1),
        "scan_speed":       lambda s: -10 * s[1::2].count(1),
    },
    "radar": {
        "range_max": 40,
        "angle_min": 20,
        "angle_max": 35,
        "angle_change": 1,
        "range_change": 1,
        "rotate_speed": 12
    },
    "fuel_tank": {
        "fuel_volume": 1000,
        "compact": 1,
        "radiation_def": 100
    },
    "lss": {
        "thermal_def": 10,
        "co2_level": 10,
        "air_volume": 10000,
        "air_speed": 50,
        "lightness": 20
    },
    "shields": {
        "radiation_def": 10,
        "desinfect_level": 100,
        "mechanical_def": 100,
        "heat_reflection": 10,
        "heat_capacity": 10000,
        "heat_sink": 50
    }
}