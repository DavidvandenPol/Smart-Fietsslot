#!/usr/bin/python3

import MySQLdb as mariadb
import json

mariadb_connection = mariadb.connect(
    user='sensem',
    password='h@',
    database='smartfiets')

cursor = mariadb_connection.cursor()

stmt = "SELECT latitude, longitude FROM gps_locations ORDER BY created_date DESC LIMIT 1"

cursor.execute(stmt)
row = cursor.fetchone()


output_json = {
    "long":  float(row[0]),
    "lat": float(row[1]),
}
stmt_2 = "SELECT islocked FROM gyro_status;"
cursor.execute(stmt_2)
row = cursor.fetchone()

output_json_2 = {
    "islocked": round(float(row[0]))
}

cursor.close()
mariadb_connection.close()

print("Content-type: application/json\n")
print(json.dumps(output_json))
print(json.dumps(output_json_2))
