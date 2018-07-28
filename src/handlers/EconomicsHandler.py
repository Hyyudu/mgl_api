from handlers.ApiHandler import ApiHandler
from services.economic import resource_list, add_pump, read_pumps


class ResourceListHandler(ApiHandler):
    func = resource_list


class AddPumpHandler(ApiHandler):
    func = add_pump


class ReadPumpsHandler(ApiHandler):
    func = read_pumps