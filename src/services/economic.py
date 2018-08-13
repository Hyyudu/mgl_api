from collections import defaultdict

from services.misc import api_fail, api_ok, inject_db, get_logger
from services.model_crud import get_model_upkeep_price


logger = get_logger(__name__)


@inject_db
def add_pump(self, data):
    """ params: {company, section, comment, is_income, amount, resources {code: value} } """
    avail_vendors = self.db.fetchColumn('select code from companies')
    if not data.get('company') in avail_vendors:
        return api_fail("Не существует компания с кодом '{}'".format(data.get('company', '')))
    avail_sections = self.db.fetchColumn('select code from pump_sections')
    if not data.get('section') in avail_sections:
        return api_fail(
            "Неизвестная секция {}. Возможные секции: {}".format(data.get('section'), ', '.join(avail_sections)))
    pump_id = self.db.insert('pumps', data)
    insert_parameters = [
        {
            "pump_id": pump_id,
            "resource_code": code,
            "value": def_value
        }
        for code, def_value in data.get('resources').items()
    ]
    data['id'] = pump_id
    self.db.insert('pump_resources', insert_parameters)

    data['resources'] = {param['resource_code']: param['value'] for param in insert_parameters}
    return {"status": "ok", "data": data}


@inject_db
def read_pumps(self, params):
    """ params= {<company>: str/list[str], <section>: str/list[str], <is_income>: 1/0 }"""
    sql = """SELECT * from pumps WHERE date_begin < Now()
        and (date_end is null or date_end = 0 or date_end > Now() )
    """
    add_where = self.db.construct_where(params)
    if add_where:
        sql += " and " + add_where
    sql += " order by company, is_income, section, entity_id, comment"
    params = self.db.construct_params(params)
    pumps = self.db.fetchAll(sql, params)
    if not pumps:
        return []
    pumps = {pump['id']: pump for pump in pumps}
    pump_ids = tuple(pumps.keys())
    pump_resources = self.db.fetchAll(
        "select * from pump_resources where pump_id in " + str(pump_ids).replace(",)", ")"))
    for res in pump_resources:
        pumps[res['pump_id']].setdefault('resources', {})
        pumps[res['pump_id']]['resources'][res['resource_code']] = res['value']
    return pumps


@inject_db
def stop_pump(self, params):
    """ params {pump_id: int} """
    self.db.query("update pumps set date_end=Now() where id=:pump_id", params, need_commit=True)
    return api_ok()


@inject_db
def resource_list(self, params=None):
    """ no params """
    logger.info("Прочитан список ресурсов")
    return self.db.fetchAll('select * from resources')


def get_insufficient_for(company: str, model_id: int = None, target: str = None, upkeep_price=None):
    company_income = get_company_income(None, {"company": company})
    if not upkeep_price:
        upkeep_price = get_model_upkeep_price(None, {"model_id": model_id})
    val_modifier = {"model": 0.5, "node": 1, "both": 1.5}
    upkeep_price = {key: val * val_modifier[target] for key, val in upkeep_price.items()}
    res_names = {item['code']: item['name'] for item in resource_list(None)}
    insufficient = {res_names[key]: upkeep_price[key] - company_income.get(key, 0)
                    for key in upkeep_price.keys()
                    if (upkeep_price[key] - company_income.get(key, 0)) > 0}
    return insufficient


def get_insufficient_for_model(company: str, model_id: int = None, upkeep_price=None):
    return get_insufficient_for(company, model_id, 'model', upkeep_price)


def get_insufficient_for_node(company: str, model_id: int = None, upkeep_price=None):
    return get_insufficient_for(company, model_id, 'node', upkeep_price)


def get_insufficient_for_both(company: str, model_id: int = None, upkeep_price=None):
    return get_insufficient_for(company, model_id, 'both', upkeep_price)


@inject_db
def add_model_upkeep_pump(self, model_id=None, model=None):
    if not model:
        model = self.db.fetchRow("select id, name, company from models where id=:id", {"id": model_id})
    logger.info(f"Добавлен насос для модели {model_id}")


@inject_db
def add_node_upkeep_pump(self, node_id=None, model=None):
    if not model:
        model = self.db.fetchRow("""select m.id, m.name, m.company
    from models m join nodes n on m.id = n.model_id
    where n.id = :node_id""", {"node_id": node_id})
    upkeep_price = get_model_upkeep_price(None, {"model_id": model['id']})
    if get_insufficient_for_node(company=model['company'], model_id=model['id'], upkeep_price=upkeep_price):
        return api_fail("Вашего дохода не хватает для создани  узла")

    pump = {
        "company": model['company'],
        "section": "nodes",
        "entity_id": node_id,
        "comment": "Поддержка узла {} модели {}".format(node_id, model['name']),
        "is_income": 0,
        "resources": upkeep_price
    }
    add_pump(self, pump)
    return api_ok(pump=pump)


@inject_db
def set_mine(self, params):
    """ params: {"entity_id": str, "company": str, "resources": [str]} """
    pump = {
        "company": params['company'],
        "section": "mines",
        "entity_id": params['entity_id'],
        "comment": "Шахта на планете {entity_id}".format(params),
        "is_income": 1,
        "resources": params['resources']
    }
    add_pump(self, pump)
    return pump


@inject_db
def get_nodes_kpi(self, params):
    """ params = {node_type_code: str} """
    data = self.db.fetchAll("""
    select cnt, name, company, kpi_price, full_kpi
    from v_nodes_kpi
    where node_type_code=:node_type_code""", params, associate='company', cumulative=True)
    sum_kpi = self.db.fetchOne("""select sum(full_kpi) from v_nodes_kpi 
        where node_type_code=:node_type_code""", params)
    table = {key: ["{name} = {kpi_price} * {cnt} = {full_kpi}".format(**item) for item in items] +
                  ["Итого: {} ({}%)".format(
                      sum([x['full_kpi'] for x in data[key]]),
                      round(sum([x['full_kpi'] for x in data[key]]) * 100 / sum_kpi),
                  )]
             for key, items in data.items()}
    return table


@inject_db
def get_company_income(self, params):
    """ params = {"company": str} """
    return {key: int(val) for key, val in
                self.db.fetchDict("select resource_code, value from v_total_income where company=:company", params,
                             "resource_code", "value").items()
            }

@inject_db
def calc_model_upkeep(self, params):
    """ params {tech_id: balls}  """
    tech_ids_sql = " tech_id in (" + ', '.join(map(str, params.keys())) + ")"
    tech_point_costs = self.db.fetchAll(f"""select tech_id, resource_code, amount 
        from tech_point_cost where {tech_ids_sql}""", associate="tech_id", cumulative=True)
    upkeep_price = defaultdict(int)
    for tech_id, costs in tech_point_costs.items():
        for cost_item in costs:
            upkeep_price[cost_item['resource_code']] += int(cost_item['amount']) * params[str(tech_id)]
    return dict(upkeep_price)
