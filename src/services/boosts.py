from services.misc import api_fail, api_ok, inject_db, get_logger


logger = get_logger(__name__)


@inject_db
def boosts_read(self, params):
    """ no params """
    return self.db.fetchAll("""select node_type, base_time, az_bonus, az_damage, boost_percent, code, password
    from boosts where used_datetime is null""")


@inject_db
def boost_use(self, params):
    """ params = {"password": str} """
    boost = self.db.fetchRow('select code, used_datetime from boosts where password=:password', params)
    if not boost:
        return api_fail("Пароль неверен")
    if boost['used_datetime']:
        return api_fail("Этот буст уже был использован")
    self.db.query("update boosts set used_datetime=now() where password=:password", params)
    logger.info("Использован буст с паролем {password}".format(**params))
    return api_ok()
