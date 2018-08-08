from services.misc import inject_db, api_ok


@inject_db
def create_tech(self, params):
    """ params = {name: str, description: str, level: int, is_available: 0/1, point_cost: {str: float},
    effects: [ {node_code: str, parameter_code: str, value: float},] }"""
    tech_id = self.db.insert('tech', params)
    point_costs = [
        {"tech_id": tech_id,
         "resource_id": key,
         "amount": value}
        for key, value in params['point_cost'].items()
    ]
    self.db.insert('tech_point_cost', point_costs)
    tech_effects = [
        {**{"tech_id": tech_id}, **effect}
        for effect in params['effects']
    ]
    self.db.insert('tech_effects', tech_effects)
    params['id'] = tech_id
    return api_ok(tech=params)
