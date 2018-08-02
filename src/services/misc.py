from numpy import unique
from random import choices
from services.db import DB


db = DB()


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
    sumvals = sum(array.values())
    generated =choices(list(array.keys()), k=cnt, weights=[i/sumvals for i in array.values()])
    ret = dict(zip(*unique(generated, return_counts=True)))
    return ret if cnt > 1 else list(ret.keys())[0]