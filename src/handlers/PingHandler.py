from torndsession.sessionhandler import SessionBaseHandler


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
        self.set_header("Access-Control-Allow-Headers",
                        "x-requested-with,access-control-allow-origin,authorization,content-type")

    def options(self):
        self.set_status(204)
        self.finish()
