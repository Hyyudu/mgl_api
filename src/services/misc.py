import json
import requests
from services.db import DB

db = DB()


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
    db.query('update users set is_active=0')
    db.insert('users', ins_data, on_duplicate_key_update="is_active=1")
    return {"status": "ok", "affected": db.affected_rows()}