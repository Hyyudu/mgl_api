from handlers.GetCodesHandler import GetNodeParamsHandler
from handlers.ModelsHandler import *

app_urls = [
    ("/get-params", GetNodeParamsHandler),
    ("/model/add", AddModelHandler),
    ("/model/read", ReadModelHandler),
    ("/model/read_all", ReadModelsHandler),
    ("/model/delete", DeleteModelHandler),
    ("/ping", PingHandler),
]
