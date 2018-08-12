from services.misc import group
from services.sync import count_elements_for_functext


sample_func = '!((aBC+Ad)(B+C+aD) + Bd + !(AbcD + bc))'


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
    r = count_elements_for_functext(sample_func)
    for key, val in r.items():
        print("{}: {}".format(key, val))
