from torndsession.sessionhandler import SessionBaseHandler

from handlers.ApiHandler import ApiHandler
from services.model_crud import add_model, delete_model, read_model


class AddModelHandler(ApiHandler):
    func = add_model

    def get_exception_text(self, e):
        if e.errno == 1062:
            return "Model with this ID already exists"


class DeleteModelHandler(ApiHandler):
    func = delete_model


class ReadModelHandler(ApiHandler):
    func = read_model


class PingHandler(SessionBaseHandler):
    async def get(self):
        self.write("Hello, world<br>")
        try:
            data = self.session.get("data", 0)

            self.session["data"] = data + 1
            self.write('data=%s' % data)
        except:
            self.write('Some problem with session, nevermind')
