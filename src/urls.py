from handlers.EconomicsHandler import ResourceListHandler
from handlers.GetCodesHandler import GetNodeParamsHandler
from handlers.MiscHandler import RefreshUsersHandler
from handlers.ModelsHandler import (
    AddModelHandler,
    ReadModelHandler,
    ReadModelsHandler,
    DeleteModelHandler,
    PingHandler,
)
from handlers.NodesHandler import (
    CreateNodeHandler,
    ReserveNodeHandler,
)


app_urls = [
    ("/get-params", GetNodeParamsHandler),
    ("/model/add", AddModelHandler),
    ("/model/read", ReadModelHandler),
    ("/model/read_all", ReadModelsHandler),
    ("/model/delete", DeleteModelHandler),
    ("/node/create", CreateNodeHandler),
    ("/node/reserve", ReserveNodeHandler),
    ("/users/refresh", RefreshUsersHandler),
    ("/economics/resources", ResourceListHandler),

    ("/ping", PingHandler),
]
