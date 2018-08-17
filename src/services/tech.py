from random import randint

from services.economic import calc_model_upkeep, get_insufficient_for_both, add_pump
from services.misc import inject_db, api_ok, drop, apply_percent, roundTo, api_fail, get_logger, dict2str
from services.model_crud import (
    calc_weight, apply_companies_perks, add_model, get_model_level_by_technologies,
    MODEL_WOW_PERIOD_HOURS,
)
from services.nodes_control import create_node


TECH_WOW_PERIOD_HOURS = 2

logger = get_logger(__name__)

@inject_db
def create_tech(self, params):
    """ params = {name: str, description: str, level: int, is_available: 0/1, point_cost: {str: float},
    effects: [ {node_code: str, parameter_code: str, value: float},], inventors: [str] }"""
    tech_id = self.db.insert('technologies', params)
    point_costs = [
        {"tech_id": tech_id,
         "resource_code": key,
         "amount": value}
        for key, value in params['point_cost'].items()
    ]
    self.db.insert('tech_point_cost', point_costs)
    tech_inventors = [
        {"tech_id": tech_id, "company": company}
        for company in params.get("inventors", [])
    ]

    self.db.insert('tech_inventors', tech_inventors)

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
                and (ti.company is not null or coalesce(t.opened_at, '2000-01-01') + INTERVAL {TECH_WOW_PERIOD_HOURS} hour < Now())
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
    techs = read_techs(self, {"company": params['company'], "node_type_code": params['node_type_code']})
    techs = {tech_id: {item['parameter_code']: item['value']
                       for item in tech_data['effects']
                       if item['node_code'] == params['node_type_code']}
             for tech_id, tech_data in techs.items()}
    model_params = {}
    for param in data:
        param_code = param['parameter_code']
        modifiers = sorted(
            [item.get(param_code, 0) * params['tech_balls'].get(int(tech_id), 0) for tech_id, item in techs.items()],
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
    model_params = calc_model_params(self, params)
    modif = {"small": "mult_small", "large": "mult_large", "medium": "1"}.get(params['size'])
    size_modifiers = self.db.fetchDict(f"""select parameter_code, {modif} modifier 
        from model_has_parameters   
        where node_code=:node_type_code""", params, 'parameter_code', 'modifier')
    # Применяем модификаторы размера
    for param, modifier in size_modifiers.items():
        model_params[param] = roundTo(model_params[param] * modifier)

    techs = read_techs(self, params)

    model_params['level'] = get_model_level_by_technologies([
        [techs.get(key, techs.get(int(key))).get('level'), value]
        for key, value in params['tech_balls'].items()
    ])

    # Применяем модификаторы компании
    model = params
    model['params'] = model_params
    apply_companies_perks(model)
    model_params['weight'] = calc_weight(params['node_type_code'], params['size'], model_params['volume'])
    return model['params']


@inject_db
def develop_model(self, params):
    """ params = {
        "node_type_code": "radar",
        "company": "mat",
        "size": "large",
        "tech_balls": {"1": 10, "2": 5},
        "name": "Азаза",
        "description": "",
        "password": ""
    }
    """
    existing_model_name = self.db.fetchRow("select * from models where name=:name", params)
    if existing_model_name:
        return api_fail("Модель с названием {name} уже создана".format(**params))
    # Читаем используемые технологии
    techs = read_techs(self, params)
    # Чистим неиспользуемые техи
    params['tech_balls'] = {
        int(key): value
        for key, value in params['tech_balls'].items()
        if int(key) in techs.keys()
    }
    # Считаем, сколько апкипа жрет модель
    model_upkeep = calc_model_upkeep(self, params['tech_balls'])
    # проверяем, хватает ли доходов
    insufficient = get_insufficient_for_both(company=params['company'], upkeep_price=model_upkeep)
    if insufficient:
        return api_fail("Для создания модели и стартового узла по этой модели вам не хватает ресурсов: "+
                        dict2str(insufficient))


    # Вычисляем параметры
    model_params = calc_model_params(self, params)
    # Находим цену в KPI
    model_kpi_price = sum([
        ball * techs.get(tech_id, {}).get('level', 0) ** 2
        for tech_id, ball in params['tech_balls'].items()
    ])
    model_level = get_model_level_by_technologies([
        [techs[key].get('level'), value]
        for key, value in params['tech_balls'].items()
    ])

    model_data = add_model(self, {
        "name": params['name'],
        "description": params.get("description", ''),
        "level": model_level,
        "kpi_price": model_kpi_price,
        "size": params['size'],
        "node_type_code": params['node_type_code'],
        "company": params['company'],
        'params': model_params,
        "upkeep": model_upkeep,
    })
    model_id = model_data['data']['id']
    # Создаем временный насос
    model_pump = add_pump(self, {
        "company": params['company'],
        'section': 'models',
        'entity_id': model_id,
        'comment': f'Разработка модели {model_id} {params["name"]}',
        "is_income": 0,
        "resources": {code: value / 2 for code, value in model_upkeep.items()}
    })
    # Устанавливаем насосу время окончания
    self.db.query(f"""update pumps set date_end = Now() + interval {MODEL_WOW_PERIOD_HOURS} hour
            where id=:id""", model_pump['data'], need_commit=True)
    # Создаем стартовый узел
    if not params.get('password'):
        params['password'] = str(randint(1000, 9999)) if params['company'] != 'pre' else ''
    create_node(self, {"model_id": model_id, "password": params['password']})
    return api_ok(params=params)
