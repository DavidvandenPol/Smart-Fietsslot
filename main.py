from sense_hat import SenseHat
import time

sense = SenseHat()

# Drempelwaarden voor versnelling en snelheid van verandering
acceleration_threshold = 1
speed_threshold = 2

prev_acceleration = None
speed_notification_time = None
knipper_interval = 0.5  # Interval van 0,5 seconde (2 keer per seconde)
knipper_duration = 10  # Knipperen gedurende 10 seconden
measuring = False  # Houdt bij of we aan het meten zijn of niet

# Kleuren voor het sloticoontje
r = (255, 0, 0)  # Rood
b = (0, 0, 0)    # Zwart (uit)
g = (0, 255, 0)  # Groen
w = (255, 255, 255)  # Wit

# Het sloticoontje als een lijst van pixels
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
    events = sense.stick.get_events()  # Krijg joystick events
    
    for event in events:
        if event.action == "pressed" and event.direction == "middle":
            if measuring:
                measuring = False
                speed_notification_time = None
                sense.set_pixels(open_lock_icon)  # Toon een wit slotje
                print("Meten gestopt.")
            else:
                measuring = True
                sense.set_pixels(open_lock_icon)  # Toon een wit slotje
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
            
            if delta_x > speed_threshold or delta_y > speed_threshold or delta_z > speed_threshold:
                if speed_notification_time is None:
                    speed_notification_time = time.time()
                    sense.set_pixels(closed_lock_icon)  # Toon een rood slotje
                print("Snelheidsmelding: Versnelling veranderde snel!")

            if speed_notification_time is not None:
                # Schakel het sloticoontje uit na 10 seconden
                if time.time() - speed_notification_time >= knipper_duration:
                    speed_notification_time = None
                    sense.set_pixels(lock_icon)  # Toon een normaal slotje (niet rood)
                # Laat het sloticoontje knipperen tijdens de 10 seconden
                elif (time.time() - speed_notification_time) % (2 * knipper_interval) < knipper_interval:
                    sense.clear()
                else:
                    sense.set_pixels(closed_lock_icon)  # Toon een rood slotje

        prev_acceleration = acceleration
    
    # Toon het juiste sloticoontje op basis van de meetstatus
    if measuring:
        sense.set_pixels(lock_icon)
    else:
        sense.set_pixels(open_lock_icon)
    
    # Print de acceleratie in de terminal als we aan het meten zijn
    if measuring:
        print(f"Acceleratie - X: {x:.2f}, Y: {y:.2f}, Z: {z:.2f}")

