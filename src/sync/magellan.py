from services.misc import group
from services.sync import count_elements_for_functext


sample_func = '!((aBC+Ad)(B+C+aD) + Bd + !(AbcD + bc))'








if __name__ == "__main__":
    print(sample_func)
    r = count_elements_for_functext(sample_func)
    for key, val in r.items():
        print("{}: {}".format(key, val))
