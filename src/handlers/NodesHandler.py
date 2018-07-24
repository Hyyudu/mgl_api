from handlers.ApiHandler import ApiHandler
from services.nodes_control import create_node, reserve_node


class CreateNodeHandler(ApiHandler):
    func = create_node


class ReserveNodeHandler(ApiHandler):
    func = reserve_node
