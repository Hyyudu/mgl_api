import json

from tornado.web import RequestHandler

from src.services.db import DB


class GetNodeParamsHandler(RequestHandler):
    async def get(self):
        db = DB()
        result = db.query('select * from v_node_parameter_list')
        self.add_header("Content-type", "application/json")
        self.write(json.dumps(result))

class AddModelHandler(RequestHandler):
    async def post(self):
        req = json.loads(self.request.body)
        self.write(req['foo'])