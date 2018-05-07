import json

from tornado.httpclient import AsyncHTTPClient, HTTPClient, HTTPError
from tornado.web import RequestHandler

from src.services.db import DB


class GetCodeAsyncHandler(RequestHandler):
    async def post(self):
        res = {}
        http_client = AsyncHTTPClient()
        urls_to_check = json.loads(self.request.body)
        for url in urls_to_check:
            try:
                response = await http_client.fetch(url)
                res[url] = response.code
            except HTTPError as e:
                res[url] = e.code
            except Exception as e:
                res[url] = str(e)
        self.write(json.dumps(res))


class GetNodeParamsHandler(RequestHandler):
    async def get(self):
        db = DB()
        result = db.query('select * from v_node_parameter_list')
        self.add_header("Content-type", "application/json")
        self.write(json.dumps(result))
