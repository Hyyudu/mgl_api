from services.misc import inject_db, api_ok, drop


@inject_db
def create_tech(self, params):
    """ params = {name: str, description: str, level: int, is_available: 0/1, point_cost: {str: float},
    effects: [ {node_code: str, parameter_code: str, value: float},] }"""
    tech_id = self.db.insert('technologies', params)
    point_costs = [
        {"tech_id": tech_id,
         "resource_code": key,
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


@inject_db
def read_techs(self, params):
    """ params = {} / {"node_type_code": "shields"} """
    sql_part = ("join tech_effects te on te.tech_id = t.id and te.node_code = :node_type_code".format(**params)
        if params.get('node_type_code') else "")
    tech_sql = f"""
    select distinct t.id, t.name, t.description, t.opened_at, t.level
    from technologies t {sql_part}
    where t.is_available = 1"""
    techs = self.db.fetchAll(tech_sql, params, "id")
    tech_ids_sql = " tech_id in (" + ', '.join(map(str, techs.keys())) + ")"
    tech_effects = self.db.fetchAll(f"select * from tech_effects where {tech_ids_sql}",
                                    associate="tech_id", cumulative=True)
    tech_inventors = self.db.fetchAll(f"select * from tech_inventors where {tech_ids_sql}",
                                      associate="tech_id", cumulative=True)
    tech_point_costs = self.db.fetchAll(f"select * from tech_point_cost where {tech_ids_sql}",
                                        associate="tech_id", cumulative=True)
    for tech_id, tech in techs.items():
        tech['effects'] = drop(tech_effects.get(tech_id, []), 'tech_id')
        tech['inventors'] = [item['company'] for item in tech_inventors.get(tech_id, [])]
        tech['point_cost'] = {item['resource_code']: item['amount']
                              for item in tech_point_costs[tech_id]}
    return techs
