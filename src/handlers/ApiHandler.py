import json
from json import JSONDecodeError

from services.db import DB
from services.misc import api_fail
from tornado.web import RequestHandler


class ApiHandler(RequestHandler):
    func = None

    def initialize(self, **kwargs):
        for key, val in kwargs.items():
            setattr(self, key, val)
        self.db = DB()

    def get_exception_text(self, e, data):
        return ''

    async def post(self):
        try:
            body = self.request.body
            try:
                req = json.loads(body)
            except JSONDecodeError:
                req = {}
            out = self.func(self, req)
            self.write(json.dumps(out, indent=4))
        except Exception as e:
            err_text = self.get_exception_text(self, e)
            fail_args = {"msg": err_text} if err_text else {"msg": str(e), "args": e.args}
            self.write(json.dumps(api_fail(**fail_args)))
            if not err_text:
                raise e


    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Access-Control-Allow-Headers",
                        "x-requested-with,access-control-allow-origin,authorization,content-type")

    def options(self):
        self.set_status(204)
        self.finish()

    def get(self):
        return self.post()
