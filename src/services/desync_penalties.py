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
        "heat_prod":        lambda s:   5 * (s[4:]).count('1'),
    },
    "warp_engine": {
        "distort":          lambda s: -15 * s[3::4].count('1'),
        "distort_acc":      lambda s: -10 * s[9:].count('1'),
        "distort_slow":     lambda s: -15 * (s[1]+s[3]+s[5]+s[10]+s[12]+s[14]).count('1'),
        "warp_enter_consumption": lambda s:  20 * (s[1::3]+s[2::3]).count('1'),
        "consumption":      lambda s: 12 * (s[:9:2]+s[7::2]).count('1'),
        "turn_consumption": lambda s: 20 * s[:9:2].count('1'),
        "turn_speed":       lambda s: -15 * (s[1:8:2]+s[0]).count('1'),
    },
    "scaner": {
        "drop_range":       lambda s: -10 * s[::2].count('1'),
        "drop_speed":       lambda s: -10 * s[8:].count('1'),
        "scan_range":       lambda s: -10 * s[:8].count('1'),
        "scan_speed":       lambda s: -10 * s[1::2].count('1'),
    },
    "radar": {
        "range_max":        lambda s: -9 * s[1::2].count('1'),
        "angle_min":        lambda s: 17 * s[-8::2].count('1'),
        "angle_max":        lambda s: -14 * s[:7:2].count('1'),
        "angle_change":     lambda s: -16 * s[-4:].count('1'),
        "range_change":     lambda s: -13 * s[-8:-4].count('1'),
        "rotate_speed":     lambda s: -10 * s[:8].count('1'),
    },
    "fuel_tank": {
        "fuel_volume":      lambda s: -9 * s[8:].count('1'),
        "radiation_def":    lambda s: -9 * s[:7].count('1'),
        "fuel_protection":  lambda s: -7 * s[2:-2].count('1'),

    },
    "lss": {
        "thermal_def":      lambda s: -9 * s[:8].count('1'),
        "co2_level":        lambda s: -8 * s[8:].count('1'),
        "air_volume":       lambda s: -7 * s[4:12].count('1'),
        "air_speed":        lambda s: -9 * (s[:4]+s[-4:]).count('1'),
        "lightness":        lambda s: -10 * s[::3].count('1'),
    },
    "shields": {
        "radiation_def":    lambda s: -7 * (s[4:8]+s[-4:]).count('1'),
        "desinfect_level":  lambda s: -9 * (s[:4]+s[8:12]).count('1'),
        "mechanical_def":   lambda s: -8 * s[6:-2].count('1'),
        "heat_reflection":  lambda s: -8 * (s[:6]+s[-2:]).count('1'),
        "heat_capacity":    lambda s: -7 * s[2:9].count('1'),
        "heat_sink":        lambda s: -6 * (s[:2]+s[10:]).count('1'),
    }
}