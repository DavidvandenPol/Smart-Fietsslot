from sense_hat import SenseHat
import time
import MySQLdb as mariadb
import pygame

pygame.init()
pygame.mixer.init()

sound = pygame.mixer.Sound("alarm.wav")

sense = SenseHat()

dbconfig = {
    'user': 'sensem',
    'password': 'h@',
    'host': 'localhost',
    'database': 'smartfiets'
}

acceleration_threshold = 3
speed_threshold = 3

prevAcceleration = None
speedNotificationTime = None
blinkInterval = 0.5
blinkDuration = 10
measuring = False
showRedLock = False
showNoLock = False

r = (255, 0, 0)
b = (0, 0, 0)
g = (0, 255, 0)
w = (255, 255, 255)

openLockIcon = [
    b, b, b, g, g, b, b, b,
    b, b, g, b, b, g, b, b,
    b, b, g, b, b, g, b, b,
    b, b, g, b, b, b, b, b,
    b, g, g, g, g, g, g, b,
    b, g, g, g, g, g, g, b,
    b, g, g, g, g, g, g, b,
    b, g, g, g, g, g, g, b
]

lockIcon = [
    b, b, b, w, w, b, b, b,
    b, b, w, b, b, w, b, b,
    b, b, w, b, b, w, b, b,
    b, b, w, b, b, w, b, b,
    b, w, w, w, w, w, w, b,
    b, w, w, w, w, w, w, b,
    b, w, w, w, w, w, w, b,
    b, w, w, w, w, w, w, b
]

closedLockIcon = [
    b, b, b, r, r, b, b, b,
    b, b, r, b, b, r, b, b,
    b, b, r, b, b, r, b, b,
    b, b, r, b, b, r, b, b,
    b, r, r, r, r, r, r, b,
    b, r, r, r, r, r, r, b,
    b, r, r, r, r, r, r, b,
    b, r, r, r, r, r, r, b
]

noIcon = [
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b,
    b, b, b, b, b, b, b, b
]
mariadb_connection = mariadb.connect(**dbconfig)
cursor = mariadb_connection.cursor()

insert_query_1 = "DELETE FROM gyro_status ORDER BY id LIMIT 1"
insert_query_2 = "INSERT INTO gyro_status VALUES(1,false)"
cursor.execute(insert_query_1)
cursor.execute(insert_query_2)
mariadb_connection.commit()

insert_notification = "INSERT INTO gyro_notifications (notification) VALUES (FALSE);"
cursor.execute(insert_notification)
mariadb_connection.commit()

while True:
    mariadb_connection = mariadb.connect(**dbconfig)
    cursor = mariadb_connection.cursor()
    
    events = sense.stick.get_events()
    for event in events:
        if event.action == "pressed" and event.direction == "middle":
            if measuring:
                measuring = False
                sound.stop()
                speedNotificationTime = None
                sense.set_pixels(openLockIcon)
                print("Meten gestopt.")
                
                insert_query_notlocked = "UPDATE gyro_status SET islocked = false;"
                cursor.execute(insert_query_notlocked)
                mariadb_connection.commit()

                cursor = mariadb_connection.cursor()
                cursor.execute("UPDATE gyro_notifications SET notification = FALSE WHERE id = 1")
                mariadb_connection.commit()
                cursor.close()
                mariadb_connection.close()
            else:
                measuring = True
                sense.set_pixels(openLockIcon)
                print("Meten gestart.")
                
                insert_query_locked = "UPDATE gyro_status SET islocked = true;"
                cursor.execute(insert_query_locked)
                mariadb_connection.commit()
                cursor.close()
                mariadb_connection.close()
    if measuring:
        acceleration = sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']

        x = abs(x)
        y = abs(y)
        z = abs(z)

        if prevAcceleration is not None:
            delta_x = abs(x - prevAcceleration['x'])
            delta_y = abs(y - prevAcceleration['y'])
            delta_z = abs(z - prevAcceleration['z'])

            total_delta = delta_x + delta_y + delta_z

            if total_delta > acceleration_threshold:
                if speedNotificationTime is None:
                    speedNotificationTime = time.time()
                    showRedLock = True

                print("Verschillingsmelding: Grote verandering in versnelling!")
                cursor = mariadb_connection.cursor()
                cursor.execute("UPDATE gyro_notifications SET notification = TRUE WHERE id = 1")
                mariadb_connection.commit()
                sound.play()  
                
            if speedNotificationTime is not None:
                if time.time() - speedNotificationTime >= blinkDuration:
                    speedNotificationTime = None
                    showRedLock = False
                    cursor = mariadb_connection.cursor()
                    cursor.execute("UPDATE gyro_notifications SET notification = FALSE WHERE id = 1")
                    mariadb_connection.commit()
                elif (time.time() - speedNotificationTime) % (2 * blinkInterval) < blinkInterval:
                    showRedLock = False
                    showNoLock = True
                else:
                    showRedLock = True
                    sound.play()
                    
        prevAcceleration = acceleration

    if measuring:
        if showRedLock:
            sense.set_pixels(closedLockIcon)
            showRedLock = False
        elif showNoLock:
            sense.set_pixels(noIcon)
            showNoLock = False
        else:
            sense.set_pixels(lockIcon)
    else:
        sense.set_pixels(openLockIcon)

    #if measuring:
        #print(f"Acceleratie - X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")

