from services.db import DB


db = DB()

def add_pump(self, data):
    """ data: {company, section, comment, is_inclume, amount, resources {code: value} } """
    if not data.get('company') in avail_vendors:
        return {"status": "fail", "errors": "Не существует компания с кодом '{}'".format(data.get('company', ''))}
    pump_id = db.insert('pumps', data)
    insert_parameters = [
        {
            "pump_id": pump_id,
            "resource_code": code,
            "value": data['resources'].get(code, 0)
        }
        for code, def_value in data.get('resources').items()
    ]
    data['id'] = pump_id
    db.insert('pump_resources', insert_parameters)

    data['resources'] = {param['parameter_code']: param['value'] for param in insert_parameters}
    return {"status": "ok", "data": data}


def resource_list(self, data):
    return db.fetchAll('select * from resources')