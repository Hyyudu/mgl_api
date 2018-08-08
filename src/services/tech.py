import json

from services.misc import inject_db


@inject_db
def create_tech(self, params):
    """ params = {name: str, description: str, level: int, is_available: 0/1, point_cost: {str: float},
    effects: [ {node_code: str, parameter_code: str, value: float},] }"""
    self.db.insert('tech')