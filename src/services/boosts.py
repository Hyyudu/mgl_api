from services.db import DB
from services.misc import api_fail, api_ok


db = DB()

def boosts_read(self, params):
    """ no params """
    return db.fetchAll("""select node_type, base_time, az_bonus, az_damage, boost_percent, code, password
    from boosts where used_datetime is null""")


def boost_use(self, params):
    """ params = {"password": str} """
    boost = db.fetchRow('select code, used_datetime from boosts where password=:password', params)
    if not boost:
        return api_fail("Пароль неверен")
    if boost['used_datetime']:
        return api_fail("Этот буст уже был использован")
    db.query("update boosts set used_datetime=now() where password=:password", params)
    return api_ok()