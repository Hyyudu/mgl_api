from random import choices
from collections import Counter
from services.db import DB


db = DB()

def node_type_list(without_hull=True):
    ret = db.fetchColumn("select code from node_types")
    if without_hull:
        ret.remove('hull')
    return ret


def modernize_date(date):
    return date.replace("2018", "2435")


def api_fail(msg):
    return {"status": "fail", "errors": msg}


def api_ok(**kwargs):
    res = {"status": "ok"}
    if kwargs:
        res.update(kwargs)
    return res


def gen_array_by_weight(array, cnt=1):
    if type(array) != dict:
        array = dict.fromkeys(array, 1)
    sumvals = sum(array.values())
    generated =choices(list(array.keys()), k=cnt, weights=[i/sumvals for i in array.values()])
    ret = dict(Counter(generated))
    return ret if cnt > 1 else list(ret.keys())[0]


def group(lst, n):
    """ Группировка элементов последовательности по count элементов """
    return [lst[i:i + n] for i in range(0, len(lst), n)]