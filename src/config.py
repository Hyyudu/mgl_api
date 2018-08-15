import os
DB_CONFIG = {
    'host': os.environ['MAGELLAN_MYSQL_HOST'],
    'database': 'magellan',
    'user': 'root',
    'password': os.environ['MYSQL_ROOT_PASSWORD'].strip()
}