from sense_hat import SenseHat
import time
import MySQLdb as mariadb



sense = SenseHat()

acceleration_threshold = 1
speed_threshold = 2

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

while True:
    events = sense.stick.get_events()
    for event in events:
        if event.action == "pressed" and event.direction == "middle":
            if measuring:
                measuring = False
                speedNotificationTime = None
                sense.set_pixels(openLockIcon)
                print("Meten gestopt.")
            else:
                measuring = True
                sense.set_pixels(openLockIcon)
                print("Meten gestart.")

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

            if speedNotificationTime is not None:
                if time.time() - speedNotificationTime >= blinkDuration:
                    speedNotificationTime = None
                    showRedLock = False
                elif (time.time() - speedNotificationTime) % (2 * blinkInterval) < blinkInterval:
                    showRedLock = False
                    showNoLock = True
                else:
                    showRedLock = True

        prevAcceleration = acceleration

    if measuring:
        if showRedLock:
            sense.set_pixels(closedLockIcon)
        elif showNoLock:
            sense.set_pixels(noIcon)
            showNoLock = False
        else:
            sense.set_pixels(lockIcon)
    else:
        sense.set_pixels(openLockIcon)

    if measuring:
        print(f"Acceleratie - X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")
