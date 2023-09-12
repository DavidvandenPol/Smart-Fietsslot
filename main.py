from sense_hat import SenseHat
import time

sense = SenseHat()

acceleration_threshold = 1
speed_threshold = 2

prev_acceleration = None
speed_notification_time = None
knipper_interval = 0.5
knipper_duration = 10
measuring = False
show_red_lock = False

r = (255, 0, 0)
b = (0, 0, 0)
g = (0, 255, 0)
w = (255, 255, 255)

open_lock_icon = [
    b, b, b, g, g, b, b, b,
    b, b, g, b, b, g, b, b,
    b, b, g, b, b, g, b, b,
    b, b, g, b, b, b, b, b,
    b, g, g, g, g, g, g, b,
    b, g, g, g, g, g, g, b,
    b, g, g, g, g, g, g, b,
    b, g, g, g, g, g, g, b
]

lock_icon = [
    b, b, b, w, w, b, b, b,
    b, b, w, b, b, w, b, b,
    b, b, w, b, b, w, b, b,
    b, b, w, b, b, w, b, b,
    b, w, w, w, w, w, w, b,
    b, w, w, w, w, w, w, b,
    b, w, w, w, w, w, w, b,
    b, w, w, w, w, w, w, b
]

closed_lock_icon = [
    b, b, b, r, r, b, b, b,
    b, b, r, b, b, r, b, b,
    b, b, r, b, b, r, b, b,
    b, b, r, b, b, r, b, b,
    b, r, r, r, r, r, r, b,
    b, r, r, r, r, r, r, b,
    b, r, r, r, r, r, r, b,
    b, r, r, r, r, r, r, b
]

while True:
    events = sense.stick.get_events()
    for event in events:
        if event.action == "pressed" and event.direction == "middle":
            if measuring:
                measuring = False
                speed_notification_time = None
                sense.set_pixels(open_lock_icon)
                print("Meten gestopt.")
            else:
                measuring = True
                sense.set_pixels(open_lock_icon)
                print("Meten gestart.")

    if measuring:
        acceleration = sense.get_accelerometer_raw()
        x = acceleration['x']
        y = acceleration['y']
        z = acceleration['z']

        x = abs(x)
        y = abs(y)
        z = abs(z)

        if prev_acceleration is not None:
            delta_x = abs(x - prev_acceleration['x'])
            delta_y = abs(y - prev_acceleration['y'])
            delta_z = abs(z - prev_acceleration['z'])

            total_delta = delta_x + delta_y + delta_z

            if total_delta > acceleration_threshold:
                if speed_notification_time is None:
                    speed_notification_time = time.time()
                    show_red_lock = True
                print("Verschillingsmelding: Grote verandering in versnelling!")

            if speed_notification_time is not None:
                if time.time() - speed_notification_time >= knipper_duration:
                    speed_notification_time = None
                    show_red_lock = False
                elif (time.time() - speed_notification_time) % (2 * knipper_interval) < knipper_interval:
                    show_red_lock = False
                else:
                    show_red_lock = True

        prev_acceleration = acceleration

    if measuring:
        if show_red_lock:
            sense.set_pixels(closed_lock_icon)
        else:
            sense.set_pixels(lock_icon)
    else:
        sense.set_pixels(open_lock_icon)

    if measuring:
        print(f"Acceleratie - X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")