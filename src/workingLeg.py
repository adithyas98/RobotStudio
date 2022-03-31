#!/usr/bin/env python3.10


from math import sin, cos, pi
from pylx16a.lx16a import *
import time

LX16A.initialize("/dev/tty.usbserial-1420")

try:
    servo1 = LX16A(1)
    #servo2 = LX16A(2)
    #servo3 = LX16A(3)
    servo1.set_angle_limits(0, 240)
    #servo2.set_angle_limits(0, 240)
    #servo3.set_angle_limits(0, 240)
except ServoTimeoutError as e:
    print(f"Servo guy {e.id_} isn't responding :( ")
    quit()

t = 0
while True:
    servo1.move(sin(4*t) * 60 + 60)
    #servo2.move(cos(t) * 60 + 60)
    #servo3.move(cos(t) * 60 + 60)
    #angle = servo1.get_physical_angle()
    #print(angle)
    time.sleep(0.05)
    t += 0.1
