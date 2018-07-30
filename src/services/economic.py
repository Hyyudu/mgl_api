from services.db import DB
from services.misc import api_fail


db = DB()


def add_pump(self, data):
    """ data: {company, section, comment, is_income, amount, resources {code: value} } """
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
    sql = "SELECT * from pumps WHERE 1=1"
    add_where = db.construct_where(params)
    if add_where:
        sql += " and " + add_where
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

def resource_list(self, data):
    return db.fetchAll('select * from resources')
