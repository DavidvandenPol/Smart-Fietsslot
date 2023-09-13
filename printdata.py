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
cursor.close()
mariadb_connection.close()

output_json = {
    "long":  float(row[0]),
    "lat": float(row[1])
}

print("Content-type: application/json\n")
print(json.dumps(output_json))
