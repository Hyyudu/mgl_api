from handlers.ApiHandler import ApiHandler
from services.nodes_control import create_node, reserve_node, get_my_reserved_nodes


class CreateNodeHandler(ApiHandler):
    func = create_node


class ReserveNodeHandler(ApiHandler):
    func = reserve_node


class GetMyReservedNodeHandler(ApiHandler):
    func = get_my_reserved_nodes
