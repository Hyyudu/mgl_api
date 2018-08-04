from services.db import DB
from services.misc import api_fail, api_ok
from services.model_crud import get_model_upkeep_price


db = DB()


def add_pump(self, data):
    """ params: {company, section, comment, is_income, amount, resources {code: value} } """
    avail_vendors = db.fetchColumn('select code from companies')
    if not data.get('company') in avail_vendors:
        return api_fail("Не существует компания с кодом '{}'".format(data.get('company', '')))
    avail_sections = db.fetchColumn('select code from pump_sections')
    if not data.get('section') in avail_sections:
        return api_fail(
            "Неизвестная секция {}. Возможные секции: {}".format(data.get('section'), ', '.join(avail_sections)))
    pump_id = db.insert('pumps', data)
    insert_parameters = [
        {
            "pump_id": pump_id,
            "resource_code": code,
            "value": def_value
        }
        for code, def_value in data.get('resources').items()
    ]
    data['id'] = pump_id
    db.insert('pump_resources', insert_parameters)

    data['resources'] = {param['resource_code']: param['value'] for param in insert_parameters}
    return {"status": "ok", "data": data}


def read_pumps(self, params):
    """ params= {<company>: str/list[str], <section>: str/list[str], <is_income>: 1/0 }"""
    sql = """SELECT * from pumps WHERE date_begin < Now()
        and (date_end is null or date_end = 0 or date_end > Now() )
    """
    add_where = db.construct_where(params)
    if add_where:
        sql += " and " + add_where
    sql += " order by company, is_income, section, entity_id, comment"
    params = db.construct_params(params)
    pumps = db.fetchAll(sql, params)
    if not pumps:
        return []
    pumps = {pump['id']: pump for pump in pumps}
    pump_ids = tuple(pumps.keys())
    pump_resources = db.fetchAll("select * from pump_resources where pump_id in " + str(pump_ids).replace(",)", ")"))
    for res in pump_resources:
        pumps[res['pump_id']].setdefault('resources', {})
        pumps[res['pump_id']]['resources'][res['resource_code']] = res['value']
    return pumps


def stop_pump(self, params):
    """ params {pump_id: int} """
    db.query("update pumps set date_end=Now() where id=:pump_id", params, need_commit=True)
    return api_ok()


def resource_list(self, params):
    """ no params """
    return db.fetchAll('select * from resources')


def add_node_upkeep_pump(node_id):
    model = db.fetchRow("""select m.id, m.name, m.company
from models m join nodes n on m.id = n.model_id
where n.id = :node_id""", {"node_id": node_id})
    upkeep_price = get_model_upkeep_price(None, {"model_id": model['id']})
    pump = {
        "company": model['company'],
        "section": "nodes",
        "entity_id": node_id,
        "comment": "Поддержка узла {} модели {}".format(node_id, model['name']),
        "is_income": 0,
        "resources": upkeep_price
    }
    add_pump(None, pump)
    return pump
