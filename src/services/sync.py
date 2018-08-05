import re
from collections import Counter
from itertools import product
from random import shuffle, choice, randint
from typing import List

from services.desync_penalties import desync_penalties
from services.misc import inject_db, roundTo
from services.model_crud import read_models


def xor(freq_vectors: List[str]) -> str:
    zp = zip(*freq_vectors)
    arr = [str(x.count('1') % 2) for x in zp]
    return "".join(arr)


def get_rand_func(size):
    src = list('abcd')
    shuffle(src)
    src = [choice([c, c.upper()]) for c in src]
    src += [c.lower() if c.isupper() else c.upper() for c in src]
    ret = "".join(c + choice(['', '+']) for c in src[:size]).rstrip('+')
    # Если функция тождественно сводится к 0 - перезапуск
    if '+' not in ret and max(Counter(ret.lower()).values()) > 1:
        return get_rand_func(size)
    braces = randint(0, 2) + size > 5
    if braces:
        while True:
            br_from = randint(0, len(ret) - 2)
            br_to = randint(br_from, len(ret) - 1)
            if not ret[br_from:].startswith('+') and not ret[:br_to].endswith('+') and (br_to - br_from > 1):
                break
        ret = ret[:br_from] + "(" + ret[br_from:br_to] + ")" + ret[br_to:]
    return ret


def getfunc(functext):
    # очищаем вход
    st = re.sub("[^ABCDabcd \(\)\!\+]", "", functext, len(functext))
    # добавляем and между перемножающимися скобками или в конструкциях вида a(b+c)
    st = re.sub(r"([abcdABCD\)])\s*\(", r"\1 & (", st)
    st = re.sub(r"\)\s*([abcdABCD])", r") & \1", st)
    st = re.sub(r"\)\s*\(", r") & (", st)
    # заменяем отрицания
    st = st.replace("!", " not ")
    # заменяем дизъюнкции
    st = st.replace("+", " or ")
    # Находим все конъюнктивные группы и меняем их
    p = re.findall("[abcdx]+", st, re.I)
    p.sort(key=len, reverse=True)
    for group in p:
        st = st.replace(group, " and ".join(list(group)))
    # заменяем a на not A и т.д.
    for c in list("ABCD"):
        st = re.sub("(?<!\w)" + c.lower() + "(?!\w)", " not " + c + " ", st)
    # убираем дублирующиеся пробелы
    st = re.sub(" +", " ", st)
    # заменяем & на and, раньше нельзя, чтобы "a" в and не путалось с переменной
    st = st.replace("&", "and")
    # print(st)
    f = lambda A, B, C, D: bool(eval(st))
    try:
        get_func_vector(f)
    except SyntaxError:
        print("Введенный вами код " + functext + " не является правильной логической функцией")
    else:
        return f


def get_func_vector(func):
    if func == "":
        return "0" * 16
    if not callable(func):
        func = getfunc(func)
    return "".join([str(int(func(A, B, C, D))) for A, B, C, D in product([0, 1], [0, 1], [0, 1], [0, 1])][::-1])


@inject_db
def get_node_vector(self, params):
    """ params: {node_id: int} """
    return self.db.fetchOne("""
    select fv.vector
from base_freq_vectors fv
join models m on fv.company = m.company and fv.node_code = m.node_type_code 
	and fv.`level` = m.`level` and fv.size = m.size
join nodes n on n.model_id = m.id
where n.id = :node_id""", params)


def get_node_params_with_desync(vector, params=None, node_id=None, node_type_code=None):
    if not params or not node_type_code:
        model = read_models(None, {"node_id": node_id})[0]
        params = model['params']
        node_type_code = model['node_type_code']
    for param, val in params.items():
        func = desync_penalties[node_type_code].get(param, lambda s: 0)
        percent = 100 + func(vector)
        params[param] = roundTo(val * percent / 100)
    return params
