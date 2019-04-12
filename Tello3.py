#
# Tello Python3 Control Demo 
#
# http://www.ryzerobotics.com/
#
# 1/1/2018

import threading 
import socket
import sys
import time


host = '192.168.10.2'
port = 9000
locaddr = (host,port) 


# Create a UDP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

tello_address = ('192.168.10.1', 8889)

sock.bind(locaddr)

def recv():
    count = 0
    while True: 
        try:
            data, server = sock.recvfrom(1518)
            print(data.decode(encoding="utf-8"))
        except Exception:
            print ('\nExit . . .\n')
            break


print ('\r\n\r\nTello Python3 Demo.\r\n')

print ('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

print ('end -- quit demo.\r\n')


#recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()

def speed(s):
    fast = ("speed "+str(s)).encode(encoding="utf-8")
    sock.sendto(fast, tello_address)
    print(f"speed set {s}")

def forward(d):
    move = ("forward "+str(d)).encode(encoding="utf-8")
    sock.sendto(move, tello_address)
    print(f"flying forward... {d}")

def rotate(r):
    rotation = ("cw "+str(r)).encode(encoding="utf-8")
    sock.sendto(rotation, tello_address)

def forwardWithSpeed(d,s):
    speed(s)
    forward(d)

def rect():
    speed(25)
    for x in range(2):
        forward(50)
        time.sleep(2)
        rotate(90)
        time.sleep(2)
        forward(100)

while True: 

    try:
        msg = input("")

        if not msg:
            break

        if 'forward' in msg:
            distance = input("How far? (20-500cm) \n")
            print(distance + " cm")
            speed = input("How fast? (10-100cm/s) \n")
            print(speed + " cm/s")
            forwardWithSpeed(distance, speed)

        if 'f1' in msg:
            forward(100,10);

        if 'f2' in msg:
            forward(100,50);

        if 'f3' in msg:
            forward(100,100);

        if 'end' in msg:
            print ('...')
            sock.close()
            break

        if 'command' or 'forward' in msg:
            msg = msg.encode(encoding="utf-8")
            sent = sock.sendto(msg, tello_address)

    except KeyboardInterrupt:
        print ('\n . . .\n')
        sock.close()  
        break
