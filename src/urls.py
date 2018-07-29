from handlers.EconomicsHandler import ResourceListHandler, AddPumpHandler, ReadPumpsHandler
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
    GetMyReservedNodeHandler,
    SetPasswordNodeHandler,
    CheckPasswordNodeHandler,
)


app_urls = [
    ("/get-params", GetNodeParamsHandler),
    ("/model/add", AddModelHandler),
    ("/model/read", ReadModelHandler),
    ("/model/read_all", ReadModelsHandler),
    ("/model/delete", DeleteModelHandler),
    ("/node/create", CreateNodeHandler),
    ("/node/set_password", SetPasswordNodeHandler),
    ("/node/check_password", CheckPasswordNodeHandler),
    ("/node/get_my_reserved", GetMyReservedNodeHandler),
    ("/node/reserve", ReserveNodeHandler),
    ("/users/refresh", RefreshUsersHandler),
    ("/economics/resources", ResourceListHandler),
    ("/economics/add_pump", AddPumpHandler),
    ("/economics/read_pumps", ReadPumpsHandler),

    ("/ping", PingHandler),
]
