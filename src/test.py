import json

from services.nodes_control import create_node
from services.model_crud import read_models

# models = read_models()
# for i, model in enumerate(models):
#     print("Creating {} of {}".format(i, len(models)))
#     create_node(None, {"model_id": model['id']})