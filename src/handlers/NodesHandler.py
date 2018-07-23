from torndsession.sessionhandler import SessionBaseHandler

from handlers.ApiHandler import ApiHandler
from services.nodes_control import create_node


class CreateNodeHandler(ApiHandler):
    func = create_node
