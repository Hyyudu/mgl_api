import json
from torndsession.sessionhandler import SessionBaseHandler

from services.db import DB


class GetNodeParamsHandler(SessionBaseHandler):
    async def get(self):
        db = DB()
        result = db.fetchAll('select * from v_node_parameter_list')
        self.add_header("Content-type", "application/json")
        self.write(json.dumps(result))
