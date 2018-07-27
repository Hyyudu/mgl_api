from handlers.ApiHandler import ApiHandler
from services.economic import resource_list


class ResourceListHandler(ApiHandler):
    func = resource_list
