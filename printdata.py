import MySQLdb as mariadb

mariadb_connection = mariadb.connect(
    user='sensem',
    password='h@',
    database='smartfiets')

cursor = mariadb_connection.cursor()

stmt = "SELECT tijd, UNIX_TIMESTAMP(tijd) as t, waarde FROM meting"

cursor.execute(stmt)

print("Content-type: text/plain\n")
row = cursor.fetchone()
while row is not None:
    print("tijd: %s (%s), waarde: %s" % (row[0], row[1], row[2]))
    row = cursor.fetchone()

cursor.close()
mariadb_connection.close()

print("Einde script")
