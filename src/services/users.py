import json

import requests
from services.misc import inject_db, get_logger


logger = get_logger(__name__)

@inject_db
def read_users_from_alice(self, params):
    req = {
        "selector": {
            "$and": [
                {"profileType": "human"},
                {"isAlive": True}
            ]
        },
        "fields": ["_id", "firstName", "lastName", 'password'],
        "limit": 200,
    }
    r = requests.post("https://couchdb.alice.magellan2018.ru/models/_find", data=json.dumps(req),
                      headers={"Content-Type": "application/json"})
    users = json.loads(r.text)
    print(json.dumps(users, indent=4))
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
    return self.db.fetchAll("""
        select u.id, u.name, COUNT(fc.flight_id) AS flight_count from users u 
        left join flight_crews fc on fc.user_id = u.id
        where is_active=1 
        group by u.id, u.name
        order by 1""")