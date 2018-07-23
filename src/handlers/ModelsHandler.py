from torndsession.sessionhandler import SessionBaseHandler

from handlers.ApiHandler import ApiHandler
from services.model_crud import add_model, delete_model, read_model, read_models


class AddModelHandler(ApiHandler):
    func = add_model

    def get_exception_text(self, e):
        if e.errno == 1062:
            return "Model with this ID already exists"


class DeleteModelHandler(ApiHandler):
    func = delete_model


class ReadModelHandler(ApiHandler):
    func = read_model


class ReadModelsHandler(ApiHandler):
    func = read_models


class PingHandler(SessionBaseHandler):
    async def get(self):
        self.write("Hello, world<br>")
        try:
            data = self.session.get("data", 0)

            self.session["data"] = data + 1
            self.write('data=%s' % data)
        except:
            self.write('Some problem with session, nevermind')

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")
        self.set_header('Access-Control-Allow-Methods', 'POST, GET, OPTIONS')
        self.set_header("Access-Control-Allow-Headers", "x-requested-with,access-control-allow-origin,authorization,content-type")

    def options(self):
        self.set_status(204)
        self.finish()