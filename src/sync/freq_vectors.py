from random import randint, shuffle

from src.sync.magellan import get_func_vector, get_rand_func
from src.sync.sync import Sync

S = Sync()
companies = [1, 2, 3, 4, 5]
maxtier = 10
sizes = ['small', 'medium', 'large']
nodes = ['march_engine', 'warp_engine', 'shunter', 'radar', 'scaner', 'fuel_tank', 'shields', 'lss']

data = {}
for company in companies:
    data[company] = {}
    for node in nodes:
        data[company][node] = {}
        for tier in range(maxtier):
            data[company][node][tier] = {}
            if tier == 0:
                data[company][node][tier]['medium'] = {"vector": bin(randint(100, 2 ** 16))[2:].ljust(16, '0'),
                                                       "correction": ""}
            else:
                corr = get_rand_func(1)
                data[company][node][tier]['medium'] = {
                    "vector": S.xor([data[company][node][tier - 1]['medium']['vector'], get_func_vector(corr)]),
                    "correction": corr
                }
            corrections = [get_rand_func(1), get_rand_func(2)]
            shuffle(corrections)
            for i, size in enumerate(('small', 'large')):
                data[company][node][tier][size] = {
                    "vector": S.xor([data[company][node][tier]['medium']['vector'], get_func_vector(corrections[i])]),
                    "correction": corrections[i]
                }


for company in companies:
    for node in nodes:
        for tier in range(maxtier):
            for size in sizes:
                val = data[company][node][tier][size]
                print(";".join([str(company), node, str(tier), size, val['vector'], val['correction']]))
