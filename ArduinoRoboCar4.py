from pyfirmata import Arduino, util
import numpy as np
import random
import time

board = Arduino('COM25')
it = util.Iterator(board)
it.start()
pin8 = board.get_pin('d:8:o')
pin9 = board.get_pin('d:9:o')
pin10 = board.get_pin('d:10:o')
pin11 = board.get_pin('d:11:o')
servo1 = board.get_pin('d:5:s')
servo2 = board.get_pin('d:6:s')
echo_pin = board.get_pin('d:7:o')

def stop(t=0):
    pin8.write(0)
    pin9.write(0)
    pin10.write(0)
    pin11.write(0)
    if t: time.sleep(t)

def RF(t):
    pin10.write(0)
    pin11.write(1)
    time.sleep(t)
    stop()

def RB(t):
    pin10.write(1)
    pin11.write(0)
    time.sleep(t)
    stop()

def LF(t):
    pin8.write(0)
    pin9.write(1)
    time.sleep(t)
    stop()

def LB(t):
    pin8.write(1)
    pin9.write(0)
    time.sleep(t)
    stop()

def F(t):
    RF(0.1)
    LF(t)
    stop()

def B(t):
    RB(0.1)
    LB(t)
    stop()

def ping(n=3):
    """Returns the average distance measured by the ultrasonic sensor."""
    return sum([util.ping_time_to_distance(echo_pin.ping()) for _ in range(n)]) / n

def scan():
    """Scan the environment to detect obstacles using ultrasonic sensor."""
    servo1.write(0)
    time.sleep(0.5)
    distances = []
    for angle in range(0, 180, 10):
        servo1.write(angle)
        time.sleep(0.2)
        dist = ping(3)
        distances.append(dist)
    return distances

def find_obstacle(distances, threshold=30):
    """Finds the closest obstacle within a threshold distance."""
    for i, dist in enumerate(distances):
        if dist < threshold:
            return True, i 
    return False, -1  

def follow_line():
    """Main function to control the robot based on sensor data."""
    distances = scan()
    obstacle_detected, angle_idx = find_obstacle(distances)
    
    if obstacle_detected:
        print(f"Obstacle detected at angle {angle_idx * 10} degrees. Turning.")
        angle_to_turn = angle_idx * 10
        servo1.write(angle_to_turn)
        F(1) 
        stop()
    else:
        print("No obstacle detected. Moving forward.")
        F(2)

while True:
    follow_line()
    time.sleep(1)

board.exit()
