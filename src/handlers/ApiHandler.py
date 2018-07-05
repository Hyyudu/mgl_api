import json

from tornado.web import RequestHandler


class ApiHandler(RequestHandler):
    func = None

    def get_exception_text(self, e):
        pass

    async def post(self):
        try:
            body = self.request.body
            req = json.loads(body)
            out = self.func(req)
            self.write(json.dumps(out))
        except Exception as e:
            err_text = self.get_exception_text(e)
            if err_text:
                self.write(json.dumps({"status": "status", "errors": err_text}))
            else:
                raise
