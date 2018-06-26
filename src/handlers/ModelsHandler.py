import json

from tornado.web import RequestHandler
from torndsession.sessionhandler import SessionBaseHandler

from services.model_crud import add_model


class AddModelHandler(RequestHandler):
    async def post(self):
        body = self.request.body
        req = json.loads(body)
        out = add_model(req)
        self.write(json.dumps(out))

class PingHandler(SessionBaseHandler):
    async def get(self):
        self.write("Hello, world")
        data = self.session.get("data", 0)
        self.write('data=%s' % data)
        self.session["data"] = data + 1
