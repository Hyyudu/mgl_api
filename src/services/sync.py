import re
from random import shuffle, choice, randint
from typing import List
from collections import Counter

from sync.magellan import get_func_vector


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
    braces = randint(0, 2)+size > 5
    if braces:
        while True:
            br_from = randint(0, len(ret)-2)
            br_to = randint(br_from, len(ret)-1)
            if not ret[br_from:].startswith('+') and not ret[:br_to].endswith('+') and (br_to - br_from > 1):
                break
        ret = ret[:br_from]+ "("+ret[br_from:br_to] + ")" + ret[br_to:]
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