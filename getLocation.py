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
    
    report = gpsd.next()
    
    if report['class'] == 'TPV':
        
        # instantiate a database connection
        mariadb_connection = mariadb.connect(**dbconfig)
        if verbose:
            print("Database connected")
        
        # create the database cursor for executing SQL queries
        cursor = mariadb_connection.cursor()
        
        report = gpsd.next()
       
        longitude_values = getattr(report,'lat',0.0)
        latitude_values = getattr(report,'lon',0.0)
         
        
        
        if longitude_values and latitude_values != 0.0:
            # store measurement in database
            print(longitude_values)
            print(latitude_values)
            
            insert_query = "INSERT INTO gps_locations (longitude, latitude) VALUES (%s, %s)"
            cursor.execute(insert_query, (longitude_values, latitude_values))
        
        
            # commit measurements
            mariadb_connection.commit()

            if verbose:
                print("Locatie committed")

        # close db connection
        cursor.close()
        mariadb_connection.close()
        
    time.sleep(interval)


