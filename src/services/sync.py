import json
import re
from collections import Counter, defaultdict
from itertools import product
from random import shuffle, choice, randint
from typing import List

from services.desync_penalties import desync_penalties
from services.misc import inject_db, roundTo, api_fail, api_ok, group
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
    SELECT fv.vector
    FROM base_freq_vectors fv
        JOIN models m on fv.company = m.company and fv.node_code = m.node_type_code 
            and fv.`level` = m.`level` and fv.size = m.size
        JOIN nodes n on n.model_id = m.id
    WHERE n.id = :node_id""", params)


def calc_node_params_with_desync(vector, params=None, node_id=None, node_type_code=None):
    if not params or not node_type_code:
        model = read_models(None, {"node_id": node_id}, read_nodes=False)[0]
        params = model['params']
        node_type_code = model['node_type_code']
    desync_percents = get_desync_percent(vector, node_type_code)
    for param, val in params.items():
        percent = desync_percents.get(param, 100)
        params[param] = {"percent": percent, "value": roundTo(val * percent / 100)}
    return params


def get_desync_percent(vector, node_type_code):
    ret = {
        param: 100 + func(vector)
        for param, func in desync_penalties[node_type_code].items()
    }
    return ret


@inject_db
def get_build_data(self, params):
    """ params = {flight_id: int, <node_type_code>: str} """
    if 'node_type_code' in params:
        data = self.db.fetchRow("""select * from v_builds where """+ self.db.construct_where(params), params)
        data['params'] = json.loads(data['params_json'] or '{}')
        data['slots'] = json.loads(data['slots_json'] or '{}')
        return data
    else:
        ret = self.db.fetchAll("select * from v_builds where flight_id=:flight_id", params, 'node_type_code')
        for data  in ret.values():
            data['params'] = json.loads(data['params_json'] or '{}')
            data['slots'] = json.loads(data['slots_json'] or '{}')
        return ret

@inject_db
def set_build_correction(self, params):
    """ params: {flight_id: int, node_type_code: str, correction: str}"""
    existing = self.db.fetchAll("""
    select * from builds where flight_id = :flight_id""", params, 'node_type_code')
    if not existing:
        return api_fail(
            "Полет {flight_id) не существует, либо для него не зарезервировано ни одного узла!".format(**params))
    update_row = existing.get(params['node_type_code'])
    if not update_row:
        return api_fail("Для полета не зарезервирован узел {node_type_code}".format(**params))
    update_row['correction_func'] = params['correction']
    update_row['correction'] = get_func_vector(params['correction'])
    update_row['total'] = xor([update_row['vector'], update_row['correction']])
    update_row['params'] = calc_node_params_with_desync(
        update_row['total'],
        node_id=update_row['node_id']
    )
    update_row['params_json'] = json.dumps(update_row['params'])
    update_row['slots'] = count_elements_for_functext(params['correction'])
    update_row['slots_json'] = json.dumps(update_row['slots'])
    self.db.update('builds', update_row, 'flight_id = :flight_id and node_type_code=:node_type_code')
    del(params['correction'])
    return api_ok(node_sync=get_build_data(self, params))


def count_elements_for_functext(st):
    # print(st)
    res = defaultdict(int)
    steps = 0
    # Подсчитываем все инверторы
    inv = st.count('!')
    if inv:
        res['inv'] = inv
    st = st.replace("!", '')

    st = st.replace(" ", '')
    while st != 'x':
        # Находим все конъюнктивные группы и меняем их
        p = re.findall("[abcdx]+", st, re.I)
        p.sort(key=len, reverse=True)
        for group in p:
            if len(group) > 1:
                res[f'con{len(group)}'] += st.count(group)
            st = st.replace(group, 'x')
            # print(st)
            # print(res)
        # находим все суммы и меняем их
        p = re.findall("((?:[abcdx]\+)+[abcdx])", st, re.I)
        p.sort(key=len, reverse=True)
        # print(p)
        for group in p:
            if len(group) > 1:
                res[f'sum{group.count("+") + 1}'] += st.count(group)
            st = st.replace(group, 'x')
            # print(st)
            # print(res)
        # находим все скобки с одним элементом и меняем их
        st = re.sub("\((\w)\)", "\\1", st)
        # print(st)
        steps += 1
        if steps > 1000:
            break
    else:
        return dict(res)


def get_vector_carno(vector):
    vector = vector[::-1]
    arr = [0, 1, 3, 2, 4, 5, 7, 6, 12, 13, 15, 14, 8, 9, 11, 10]
    groups = group(arr, 4)
    lst = [['', 'cd', 'cD', 'CD', 'Cd']]
    rows = ['ab', 'aB', 'AB', 'Ab']
    for i, grp in enumerate(groups):
        lst += [[rows[i]] + [vector[x] for x in grp]]
    table_view(lst, free_space_right=1)


def table_view(data, free_space_right=4, free_space_left=1, column_separator="|"):
    datas = [x for x in data if isinstance(x, (list, tuple))]
    zipdata = list(zip(*datas))
    column_widths = [max([len(str(x)) for x in col]) + free_space_right + free_space_left for col in zipdata]
    line_width = sum(column_widths) + len(column_separator) * (len(zipdata) - 1)
    for item in data:
        if isinstance(item, str):
            print(item * line_width)
        else:
            while "sum" in item:
                ind = item.index("sum")
                item[ind] = sum(
                    [x[ind] for x in data if isinstance(x, (tuple, list)) and isinstance(x[ind], (int, float))])
            print(column_separator.join(
                [" " * free_space_left + "{:<{x}}".format(item[i], x=x - free_space_left) for i, x in
                 enumerate(column_widths)]).format(*item))
