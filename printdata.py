import time
import MySQLdb as mariadb
import json

interval = 1

dbconfig = {
    'user': 'sensem',
    'password': 'h@',
    'host': 'localhost',
    'database': 'smartfiets'
}

while True:
    try:
        mariadb_connection = mariadb.connect(**dbconfig)
        cursor = mariadb_connection.cursor()

        cursor.execute("SELECT latitude, longitude FROM gps_locations ORDER BY created_date DESC LIMIT 1")
        row = cursor.fetchone()

        if row:
            latitude = row[0]
            longitude = row[1]

            gps_data = {
                'latitude': latitude,
                'longitude': longitude
            }

            gps_json = json.dumps(gps_data)

            print("Laatste GPS-gegevens in JSON-formaat:")
            print(gps_json)
        else:
            print("Geen GPS-gegevens beschikbaar.")

        mariadb_connection.close()

    except mariadb.Error as e:
        print(f"Fout bij het verbinden met de database: {e}")

    time.sleep(interval)
