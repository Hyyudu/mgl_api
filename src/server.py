import tornado.ioloop
from tornado.web import (
    Application,
)

from src.urls import app_urls


def make_app():
    return Application(app_urls)


if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
