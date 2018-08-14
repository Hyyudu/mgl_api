from handlers.ApiHandler import ApiHandler
from handlers.PingHandler import (
    PingHandler,
)
from services.boosts import boosts_read, boost_use
from services.economic import (
    read_pumps, resource_list, add_pump, stop_pump, set_mine, get_nodes_kpi,
    get_company_income,
)
from services.mcc import (
    mcc_dashboard,
    mcc_set_crew,
    mcc_add_passenger,
    mcc_remove,
    mcc_add_flight,
    mcc_set_all_crew,
    get_nearest_flight_for_role,
    mcc_assign_flight,
    freight_flight,
    flight_died,
)
from services.misc import url_params
from services.model_crud import add_model, read_model, read_models, delete_model, get_model_upkeep_price
from services.nodes_control import (
    create_node,
    get_all_params,
    set_password,
    check_password,
)
from services.sync import set_build_correction
from services.tech import create_tech, read_techs, calc_model_params, preview_model_params, develop_model
from services.technopark import (
    get_flight_params, reserve_node, get_my_reserved_nodes, load_luggage, unload_luggage,
    get_luggage,
)
from services.users import read_users_from_alice, users_list
from tornado.web import RequestHandler


def url(uri, func, is_tableview=None, **kwargs):
    init_params = {"func": func}
    if kwargs:
        init_params.update(kwargs)
    return uri, ApiHandler, init_params


class UrlsHandler(RequestHandler):
    def get(self):
        self.write("<xmp>" + url_params(app_urls) + "</xmp>")


app_urls = [
    url("/get-params", get_all_params),
    url("/model/add", add_model, {
        "get_exception_text": lambda self, e: "Модель с таким ID уже создана" if e.errno == 1062 else None
    }),
    url("/model/read", read_model),
    url("/model/read_all", read_models),
    url("/model/delete", delete_model),
    url("/model/get_upkeep_price", get_model_upkeep_price),

    url("/node/create", create_node),
    url("/node/set_password", set_password),
    url("/node/check_password", check_password),
    url("/node/get_my_reserved", get_my_reserved_nodes),
    url("/node/reserve", reserve_node),

    url("/tech/create", create_tech),
    url("/tech/read", read_techs),
    url("/tech/calc_model_params", calc_model_params),
    url("/tech/preview_model_params", preview_model_params),
    url("/tech/develop_model", develop_model),

    url("/technopark/get_flight_params", get_flight_params),
    url("/technopark/load_luggage", load_luggage),
    url("/technopark/unload_luggage", unload_luggage),
    url("/technopark/get_luggage", get_luggage),

    url("/sync/set_correction", set_build_correction),

    url("/users/refresh", read_users_from_alice),
    url("/users/list", users_list),

    url("/economics/resources", resource_list),
    url("/economics/add_pump", add_pump),
    url("/economics/read_pumps", read_pumps),
    url("/economics/stop_pump", stop_pump),
    url("/economics/set_mine", set_mine),
    url("/economics/get_nodes_kpi", get_nodes_kpi),
    url("/economics/get_company_income", get_company_income),

    url("/mcc/dashboard", mcc_dashboard),
    url("/mcc/set_crew", mcc_set_crew),
    url("/mcc/add_passenger", mcc_add_passenger),
    url("/mcc/add_flight", mcc_add_flight, {
        "get_exception_text": lambda self, e: "В это время в этом доке уже намечен полет" if e.errno == 1062 else None
    }),
    url("/mcc/remove", mcc_remove),
    url("/mcc/assign_flight", mcc_assign_flight),
    url("/mcc/set_all_crew", mcc_set_all_crew),
    url('/mcc/get_nearest_flight_for_role', get_nearest_flight_for_role),
    url('/mcc/freight', freight_flight),
    url('/mcc/flight_died', flight_died),

    url("/boosts/read", boosts_read),
    url("/boosts/use", boost_use),

    ("/ping", PingHandler),
    ("/urls_params", UrlsHandler)
]
