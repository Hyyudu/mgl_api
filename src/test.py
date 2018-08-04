import json

from services.misc import gen_array_by_weight


print(gen_array_by_weight(['a','b','c','d'], 33, min_step=3, max_step=5))