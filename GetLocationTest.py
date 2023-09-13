from gps import *
import time
import MySQLdb as mariadb
import sys
import getopt

verbose = True
interval = 3


#gpsd = gps(mode=WATCH_ENABLE|WATCH_NEWSTYLE) 

dbconfig = {
    'user': 'sensem',
    'password': 'h@',
    'host': 'localhost',
    'database': 'smartfiets'
}

while True:
    
    #report = gpsd.next()
    

        
    # instantiate a database connection
    mariadb_connection = mariadb.connect(**dbconfig)
    if verbose:
        print("Database connected")
        
    # create the database cursor for executing SQL queries
    cursor = mariadb_connection.cursor()
        
    #report = gpsd.next()
       
    #longitude_values = getattr(report,'lat',0.0)
    #latitude_values = getattr(report,'lon',0.0)
         
        
    longitude_values_default = 52.500917809
    latitude_values_default = 6.079951038
        
    if longitude_values_default and latitude_values_default != 0.0:
        # store measurement in database
        print(longitude_values_default)
        print(latitude_values_default)
            
        insert_query = "INSERT INTO gps_locations (longitude, latitude) VALUES (%s, %s)"
        cursor.execute(insert_query, (longitude_values_default, latitude_values_default))
        
        
        # commit measurements
        mariadb_connection.commit()

        if verbose:
            print("Locatie committed")

    # close db connection
    cursor.close()
    mariadb_connection.close()
        
    time.sleep(interval)



