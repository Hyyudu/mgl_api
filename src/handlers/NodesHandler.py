from handlers.ApiHandler import ApiHandler
from services.nodes_control import create_node, reserve_node, get_my_reserved_nodes, set_password, check_password


class CreateNodeHandler(ApiHandler):
    func = create_node


class ReserveNodeHandler(ApiHandler):
    func = reserve_node


class GetMyReservedNodeHandler(ApiHandler):
    func = get_my_reserved_nodes


class SetPasswordNodeHandler(ApiHandler):
    func = set_password


class CheckPasswordNodeHandler(ApiHandler):
    func = check_password