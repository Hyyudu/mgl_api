import json

import requests
from services.misc import inject_db


@inject_db
def read_users_from_alice(self, params):
    req = {
        "selector": {
            "$and": [
                {"profileType": "human"},
                {"isAlive": True}
            ]
        },
        "fields": ["_id", "firstName", "lastName"],
        "limit": 200,
    }
    r = requests.post("https://couchdb.alice.magellan2018.ru/models/_find", data=json.dumps(req),
                      headers={"Content-Type": "application/json"})
    users = json.loads(r.text)
    if 'docs' in users:
        ins_data = [
            {
                "id": user['_id'],
                "name": (user['firstName'] + " " + user['lastName']).strip(),
                "is_active": 1
            }
            for user in users['docs']
        ]
    self.db.query('update users set is_active=0')
    self.db.insert('users', ins_data, on_duplicate_key_update="is_active=1")
    return {"status": "ok", "affected": self.db.affected_rows()}


@inject_db
def users_list(self, params):
    """ no params """
    return self.db.fetchAll('select id, name from users where is_active=1 order by 1')