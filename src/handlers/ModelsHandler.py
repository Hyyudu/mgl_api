import json

from tornado.web import RequestHandler


class AddModelHandler(RequestHandler):
    async def post(self):
        body = self.request.body
        req = json.loads(body)
        self.write(req)

class PingHandler(RequestHandler):
    async def get(self):
        self.write("Hello, world")

