import re
from collections import defaultdict
from itertools import product
from random import shuffle, random

sample_func = '!((aBC+Ad)(B+C+aD) + Bd + !(AbcD + bc))'


def get_rand_func(size):
    src = list('abcd')
    shuffle(src)
    src = [c if random() < 0.5 else c.upper() for c in src[:size]]
    return "".join(src) if random() < 0.5 else "+".join(src)


def count_elements(st):
    # print(st)
    res = {'!': 0, '+': defaultdict(int), '*': defaultdict(int)}
    steps = 0
    # Подсчитываем все инверторы
    res['!'] = {1: st.count('!')}
    st = st.replace("!", '')

    st = st.replace(" ", '')
    while st != 'x':
        # Находим все конъюнктивные группы и меняем их
        p = re.findall("[abcdx]+", st, re.I)
        p.sort(key=len, reverse=True)
        for group in p:
            if len(group) > 1:
                res['*'][len(group)] += st.count(group)
            st = st.replace(group, 'x')
            # print(st)
            # print(res)
        # находим все суммы и меняем их
        p = re.findall("((?:[abcdx]\+)+[abcdx])", st, re.I)
        p.sort(key=len, reverse=True)
        # print(p)
        for group in p:
            if len(group) > 1:
                res['+'][group.count('+') + 1] += st.count(group)
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
        res['+'] = dict(res['+'])
        res['*'] = dict(res['*'])
        return res


def group(lst, n):
    """ Группировка элементов последовательности по count элементов """
    return [lst[i:i + n] for i in range(0, len(lst), n)]


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
    if not callable(func):
        func = getfunc(func)
    return "".join([str(int(func(A, B, C, D))) for A, B, C, D in product([0, 1], [0, 1], [0, 1], [0, 1])][::-1])


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


def get_vector_carno(vector):
    vector = vector[::-1]
    arr = [0, 1, 3, 2, 4, 5, 7, 6, 12, 13, 15, 14, 8, 9, 11, 10]
    groups = group(arr, 4)
    lst = [['', 'cd', 'cD', 'CD', 'Cd']]
    rows = ['ab', 'aB', 'AB', 'Ab']
    for i, grp in enumerate(groups):
        lst += [[rows[i]] + [vector[x] for x in grp]]
    table_view(lst, free_space_right=1)


if __name__ == "__main__":
    print(sample_func)
    r = count_elements(sample_func)
    for key, val in r.items():
        print("{}: {}".format(key, val))
