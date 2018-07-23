import json
from torndsession.sessionhandler import SessionBaseHandler

from services.db import DB


class GetNodeParamsHandler(SessionBaseHandler):
    async def get(self):
        db = DB()
        result = db.fetchAll('select * from v_node_parameter_list')
        self.add_header("Content-type", "application/json")
        self.write(json.dumps(result))

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,access-control-allow-origin,authorization,content-type")

    def options(self):
        self.set_status(204)
        self.finish()