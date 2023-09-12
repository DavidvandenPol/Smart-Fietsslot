from gps import *
import time
import MySQLdb as mariadb
import sys
import getopt

verbose = True
interval = 1

gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 

dbconfig = {
    'user': 'sensem',
    'password': 'h@',
    'host': 'localhost',
    'database': 'smartfiets'
}

while True:
    mariadb_connection = mariadb.connect(**dbconfig)
    if verbose:
        print("Database connected")
    cursor = mariadb_connection.cursor()
    print("Application started!")
    report = gpsd.next()

    if report['class'] == 'TPV':
        longitude = getattr(report,'lat',0.0),"\t",
        latitude = getattr(report,'lon',0.0),"\t",

        str_lat = str(latitude)
        str_long = str(longitude)
    
        LocationData = str_lat + ', ' + str_long
        
        cursor.execute("INSERT INTO locatiedata (data) VALUES", (LocationData))
    
        mariadb_connection.commit()

        if verbose:
            print("Locatie committed")

        cursor.close()
        mariadb_connection.close()
        
    time.sleep(interval)
