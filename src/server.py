import tornado.ioloop
from tornado.web import (
    Application,
)

from urls import app_urls


class App(Application):
    def __init__(self):
        settings = dict(
            debug=True,
        )
        session_settings = dict(
            driver='memory',
            driver_settings={'host': self},
            force_persistence=True,
            sid_name='torndsessionID',
            session_lifetime=1800
        )
        settings['session'] = session_settings
        Application.__init__(self, app_urls, **settings)


if __name__ == "__main__":
    app = tornado.httpserver.HTTPServer(App())
    app.listen(8888)

    try:
        tornado.ioloop.IOLoop.current().start()
    finally:
        app.stop()
