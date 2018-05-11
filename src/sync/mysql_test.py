import pymysql

conn = pymysql.connect(host='localhost', user='root', password = '', db='artemius', charset='utf8')
with conn.cursor() as cursor:
    cursor.execute("select family_id, metal, family_name from families")
    for row in cursor:
        print(row)