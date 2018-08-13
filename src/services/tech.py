from services.misc import inject_db, api_ok, drop, apply_percent, roundTo
from services.model_crud import calc_weight, apply_companies_perks


TECH_WOW_PERIOD_HOURS = 2


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
    """ params = {} / {"node_type_code": "shields", "company": "mat"} """

    if not params:
        tech_sql = f"""
            select distinct t.id, t.name, t.description, t.opened_at, t.level
            from technologies t where t.is_available = 1"""
    else:
        tech_sql = f"""
            select distinct t.id, t.name, t.description, t.opened_at, t.level, ti.company
            from technologies t 
                join tech_effects te on te.tech_id = t.id and te.node_code = :node_type_code
                left join tech_inventors ti on ti.tech_id = t.id and ti.company=:company
            where t.is_available = 1
                and (ti.company is not null or t.opened_at + INTERVAL {TECH_WOW_PERIOD_HOURS} hour < Now())
                """

    techs = self.db.fetchAll(tech_sql, params, "id")
    if not techs:
        return []
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


@inject_db
def calc_model_params(self, params):
    """ params = {"node_type_code": "radar", "company": "mat","size": "large", "tech_balls": {"1": 10, "2": 5}}"""
    data = self.db.fetchAll("""
    select parameter_code, def_value, increase_direction
    from model_has_parameters
    where node_code = :node_type_code""", params)
    techs = read_techs(None, {"company": params['company'], "node_type_code": params['node_type_code']})
    techs = {tech_id: {item['parameter_code']: item['value']
                       for item in tech_data['effects']
                       if item['node_code'] == params['node_type_code']}
             for tech_id, tech_data in techs.items()}
    model_params = {}
    for param in data:
        param_code = param['parameter_code']
        modifiers = sorted(
            [item.get(param_code, 0) * params['tech_balls'].get(str(tech_id), 0) for tech_id, item in techs.items()],
            reverse=int(param['increase_direction']) == 1)
        if param_code == 'volume':
            model_params['volume'] = apply_percent(param['def_value'], sum(modifiers))
        else:
            model_params[param_code] = param['def_value'] + modifiers[0]
    model_params['weight'] = calc_weight(params['node_type_code'], params['size'], model_params['volume'])
    return model_params


@inject_db
def preview_model_params(self, params):
    """ params = {"node_type_code": "radar", "company": "mat","size": "large", "tech_balls": {"1": 10, "2": 5}}"""
    model_params = calc_model_params(None, params)
    modif = {"small": "mult_small", "large": "mult_large", "medium": "1"}.get(params['size'])
    size_modifiers = self.db.fetchDict(f"""select parameter_code, {modif} modifier 
        from model_has_parameters   
        where node_code=:node_type_code""", params, 'parameter_code', 'modifier')
    # Применяем модификаторы размера
    for param, modifier in size_modifiers.items():
        model_params[param] = roundTo(model_params[param] * modifier)
    # Применяем модификаторы компании
    model = params
    model['params'] = model_params
    apply_companies_perks(model)
    model_params['weight'] = calc_weight(params['node_type_code'], params['size'], model_params['volume'])
    return model['params']
