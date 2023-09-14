#!/usr/bin/python3

import MySQLdb as mariadb
import json

mariadb_connection = mariadb.connect(
    user='sensem',
    password='h@',
    database='smartfiets')

cursor = mariadb_connection.cursor()

# Query voor het ophalen van GPS-locatiegegevens
stmt = "SELECT latitude, longitude FROM gps_locations ORDER BY created_date DESC LIMIT 1"
cursor.execute(stmt)
row = cursor.fetchone()

# JSON-structuur voor GPS-locatie
output_json = {
    "location": {
        "long":  float(row[1]),
        "lat": float(row[0])
    },
    "islocked": 0,  # Voeg hier de vergrendelingsstatus in als dat van toepassing is
    "notification": 0  # Voeg hier de meldingsstatus in als dat van toepassing is
}

# Query voor het ophalen van vergrendelingsstatus
stmt_2 = "SELECT islocked FROM gyro_status;"
cursor.execute(stmt_2)
row = cursor.fetchone()

# Voeg de vergrendelingsstatus toe aan de JSON-structuur
output_json["islocked"] = round(float(row[0]))

# Query voor het ophalen van meldingsstatus
stmt_3 = "SELECT notification FROM gyro_notifications;"
cursor.execute(stmt_3)
row = cursor.fetchone()

# Voeg de meldingsstatus toe aan de JSON-structuur
output_json["notification"] = round(float(row[0]))

cursor.close()
mariadb_connection.close()

# Plaats de JSON-structuur in een lijst om hetzelfde formaat te behouden als eerder
combined_json = [output_json]

print("Content-type: application/json\n")
print(json.dumps(combined_json))
