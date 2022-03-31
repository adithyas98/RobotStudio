#!/usr/bin/env python3.10

import socket

def sendStatus():
    '''
    Method will check to see if the robot has booted properly
    and if all servos are connected. The server will send a status
    message over a TCP socket Connection
    '''


    HOST = "192.168.255.30"  # Standard loopback interface address (localhost)
    PORT = 65432  # Port to listen on (non-privileged ports are > 1023)
    #do the servo checks
    Error = False#initialize a variable
    try:
        servo1 = LX16A(1)
        servo2 = LX16A(2)
        servo3 = LX16A(3)
        servo1.set_angle_limits(0, 240)
        servo2.set_angle_limits(0, 240)
        servo3.set_angle_limits(0, 240)
    except ServoTimeoutError as e:
        print(f"Servo guy {e.id_} isn't responding :( ")
        Error = True


    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        conn, addr = s.accept()
        with conn:
            print(f"Connected by {addr}")
            while True:
                data = conn.recv(1024)
                if not data:
                    break
                if not Error:
                    conn.sendall("Everything Seems to be Fine!!")
                else:
                    conn.sendall("Something went wrong")



def getStatus():
    '''
    This will connect and send a status inquiry 
    '''
    HOST = "192.168.255.51"  # The server's hostname or IP address
    PORT = 65432  # The port used by the server

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT))
        s.sendall(b"Status")
        data = s.recv(1024)

    print(data)#retrieve the status of the robot!

def homeServo():
    '''
    Method will home the servo moters
    '''
    servo1.set_angle_limits(0, 240)
    servo2.set_angle_limits(0, 240)
    servo3.set_angle_limits(0, 240)
    #now move the servos to 0 degrees
    servo1.move(0)
    servo2.move(0)
    servo3.move(0)


