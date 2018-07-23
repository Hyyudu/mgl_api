from handlers.ApiHandler import ApiHandler
from services.misc import read_users_from_alice


class RefreshUsersHandler(ApiHandler):
    func = read_users_from_alice
