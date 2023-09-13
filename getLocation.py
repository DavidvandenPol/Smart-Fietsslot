from gps import *
import time
import MySQLdb as mariadb

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
    report = gpsd.next()
    
    if report['class'] == 'TPV':
        mariadb_connection = mariadb.connect(**dbconfig)
        if verbose:
            print("DB connected")
        
        cursor = mariadb_connection.cursor()
        report = gpsd.next()
       
        longitude_values = getattr(report,'lat',0.0)
        latitude_values = getattr(report,'lon',0.0)
         
        if longitude_values and latitude_values != 0.0:
            print(longitude_values)
            print(latitude_values)
            
            insert_query = "INSERT INTO gps_locations (longitude, latitude) VALUES (%s, %s)"
            insert_delete_row = "DELETE FROM gps_locations ORDER BY id LIMIT 1;"

            cursor.execute(insert_query, (longitude_values, latitude_values))
            cursor.execute(insert_delete_row)

            mariadb_connection.commit()

            if verbose:
                print("done")


        cursor.close()
        mariadb_connection.close()
        
    time.sleep(interval)
