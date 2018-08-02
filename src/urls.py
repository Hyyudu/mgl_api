from handlers.ApiHandler import ApiHandler
from handlers.ModelsHandler import (
    PingHandler,
)
from services.boosts import boosts_read, boost_use
from services.economic import read_pumps, resource_list, add_pump
from services.mcc import mcc_dashboard, mcc_set_crew, mcc_add_passenger, mcc_remove
from services.misc import read_users_from_alice
from services.model_crud import add_model, read_model, read_models, delete_model
from services.nodes_control import (
    create_node, get_all_params, set_password, check_password, get_my_reserved_nodes,
    reserve_node,
)

url = lambda uri, func: (uri, ApiHandler, {"func": func})

app_urls = [
    url("/get-params", get_all_params),
    ("/model/add", ApiHandler, {
        "func": add_model,
        "get_exception_text": lambda self, e: "Model with this ID already exists" if e.errno == 1062 else None
    }),
    url("/model/read", read_model),
    url("/model/read_all", read_models),
    url("/model/delete", delete_model),
    url("/node/create", create_node),
    url("/node/set_password", set_password),
    url("/node/check_password", check_password),
    url("/node/get_my_reserved", get_my_reserved_nodes),
    url("/node/reserve", reserve_node),
    url("/users/refresh", read_users_from_alice),
    url("/economics/resources", resource_list),
    url("/economics/add_pump", add_pump),
    url("/economics/read_pumps", read_pumps),
    url("/mcc/dashboard", mcc_dashboard),
    url("/mcc/set_crew", mcc_set_crew),
    url("/mcc/add_passenger", mcc_add_passenger),
    url("/mcc/remove", mcc_remove),
    url("/boosts/read", boosts_read),
    url("/boosts/use", boost_use),

    ("/ping", PingHandler),
]
