import json

from tornado.web import RequestHandler
from torndsession.sessionhandler import SessionBaseHandler


class AddModelHandler(RequestHandler):
    async def post(self):
        body = self.request.body
        req = json.loads(body)
        self.write(req)


class PingHandler(SessionBaseHandler):
    async def get(self):
        self.write("Hello, world")
        data = self.session.get("data", 0)
        self.write('data=%s' % data)
        self.session["data"] = data + 1
