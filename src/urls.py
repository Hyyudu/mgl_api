from handlers.GetCodesHandler import GetNodeParamsHandler
from handlers.MiscHandler import RefreshUsersHandler
from handlers.ModelsHandler import *
from handlers.NodesHandler import *

app_urls = [
    ("/get-params", GetNodeParamsHandler),
    ("/model/add", AddModelHandler),
    ("/model/read", ReadModelHandler),
    ("/model/read_all", ReadModelsHandler),
    ("/model/delete", DeleteModelHandler),
    ("/node/create", CreateNodeHandler),
    ("/users/refresh", RefreshUsersHandler),
    ("/ping", PingHandler),
]
