import json

from tornado.web import RequestHandler


class AddModelHandler(RequestHandler):
    async def post(self):
        body = self.request.body
        req = json.loads(body)
        self.write(req)
