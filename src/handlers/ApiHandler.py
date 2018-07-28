import json
from json import JSONDecodeError

from services.misc import api_fail
from tornado.web import RequestHandler


class ApiHandler(RequestHandler):
    func = None

    def get_exception_text(self, e):
        pass

    async def post(self):
        try:
            body = self.request.body
            try:
                req = json.loads(body)
            except JSONDecodeError:
                req = {}
            out = self.func(req)
            self.write(json.dumps(out, indent=4))
        except Exception as e:
            err_text = self.get_exception_text(e)
            if err_text:
                self.write(json.dumps(api_fail(err_text)))
            else:
                raise

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,access-control-allow-origin,authorization,content-type")

    def options(self):
        self.set_status(204)
        self.finish()

    def get(self):
        return self.post()