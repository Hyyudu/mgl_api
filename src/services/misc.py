import logging
from collections import defaultdict
from random import choices, randint

from services.db import DB

NODE_NAMES = {
    "march_engine": "маршевый двигатель",
    "shunter": "маневровый двигатель",
    "warp_engine": "двигатель Уайта",
    "fuel_tank": "топливный бак",
    "radar": "радар",
    "scaner": "сканер",
    "lss": "СЖО",
    "shields": "щиты",
    "hull": "корпус",
}

def get_logger(name, log_file='logs/main.log', level=logging.INFO):
    """Function setup as many loggers as you want"""
    formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
    handler = logging.FileHandler(log_file)
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)

    return logger

def get_error_logger(name):
    return get_logger(name, log_file="logs/error.log")


class DBHolder():
    def __init__(self):
        self.db = DB()


def node_type_list(without_hull=True):
    db = DB()
    ret = db.fetchColumn("select code from node_types")
    if without_hull:
        ret.remove('hull')
    return ret


def modernize_date(date):
    return date.replace("2018", "2349")


def api_fail(msg, **kwargs):
    res = {"status": "fail", "errors": msg}
    if kwargs:
        res.update(kwargs)
    return res


def api_ok(**kwargs):
    res = {"status": "ok"}
    if kwargs:
        res.update(kwargs)
    return res


def gen_array_by_weight(array, cnt=1, min_step=1, max_step=1):
    left = cnt
    if type(array) != dict:
        array = dict.fromkeys(array, 1)
    sumvals = sum(array.values())
    ret = defaultdict(int)
    while left > 0:
        choice = choices(list(array.keys()), k=1, weights=[i / sumvals for i in array.values()])[0]
        amount = min(left, randint(min_step, max_step))
        ret[choice] += amount
        left -= amount
    ret = dict(ret)
    return ret if cnt > 1 else list(ret.keys())[0]


def group(lst, n):
    """ Группировка элементов последовательности по count элементов """
    return [lst[i:i + n] for i in range(0, len(lst), n)]


def inject_db(func):
    def wrapper(obj, *args, **kwargs):
        if not obj:
            obj = DBHolder()
            obj.db: DB
        return func(obj, *args, **kwargs)

    wrapper.__doc__ = func.__doc__
    return wrapper


def url_params(app_urls):
    ret = ""
    for item in app_urls:
        ret += item[0] + "\n"
        if len(item) > 2:
            ret += (item[2].get('func').__doc__ or "")
        ret += "\n\n"
    return ret


def roundTo(val, prec=3):
    return round(val, prec - len(str(int(val))))


def apply_percent(value, percent=100):
    return roundTo(value * (100 + percent) / 100)


def drop(arr, field: str):
    if isinstance(arr, (list, tuple, set)):
        for dct in arr:
            del (dct[field])
    else:
        del (arr[field])
    return arr


def dict2str(dct, separator=", "):
    return ", ".join([f"{key}: {val}" for key, val in dct.items()])