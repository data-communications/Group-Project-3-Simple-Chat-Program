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
port = 8888
locaddr = (host, port)

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
            print('\nExit . . .\n')
            break


print('\r\n\r\nTello Python3 Demo.\r\n')

print('Tello: command takeoff land flip forward back left right \r\n       up down cw ccw speed speed?\r\n')

print('end -- quit demo.\r\n')

# recvThread create
recvThread = threading.Thread(target=recv)
recvThread.start()


def speed(s):
    fast = ("speed " + str(s)).encode(encoding="utf-8")
    sock.sendto(fast, tello_address)
    print(f"speed set {s}")

def forward(d):
    d = ("forward " + str(d)).encode(encoding="utf-8")
    sock.sendto(d, tello_address)
    print(f"flying forward... {d}")

def rotate(r):
    sock.sendto(("ccw " + str(r)).encode(encoding="utf-8"), tello_address)
    print(f"rotating counterclockwise {r} degrees")

def forwardWithSpeed(d, s):
    speed(s)
    time.sleep(3)
    forward(d)

def rectangle():
    for x in range(2):
        sock.sendto("forward 50".encode(encoding="utf-8"), tello_address)
        time.sleep(6)
        sock.sendto("ccw 90".encode(encoding="utf-8"), tello_address)
        time.sleep(3)
        sock.sendto("forward 100".encode(encoding="utf-8"), tello_address)
        time.sleep(8)
        sock.sendto("ccw 90".encode(encoding="utf-8"), tello_address)
        time.sleep(3)

while True:

    try:
        msg = input("")


        if not msg:
            break

        if 'forward' in msg:
            forwardWithSpeed(100, 25)
            time.sleep(7)
            forwardWithSpeed(100, 50)
            time.sleep(7)
            forwardWithSpeed(100, 100)

        if 'rectangle' in msg:
            sock.sendto("speed 50".encode(encoding="utf-8"), tello_address)
            time.sleep(2)
            rectangle()
            time.sleep(2)
            sock.sendto("land".encode(encoding="utf-8"), tello_address)

        if "circle" in msg:
            sock.sendto('command'.encode(encoding="utf-8"), tello_address)
            time.sleep(3)
            sock.sendto('takeoff'.encode(encoding="utf-8"), tello_address)
            time.sleep(4)
            sock.sendto('curve 50 50 0 100 0 0 50'.encode(encoding="utf-8"), tello_address)
            time.sleep(6)
            rotate(180)
            time.sleep(4)
            sock.sendto('curve 50 50 0 100 0 0 50'.encode(encoding="utf-8"), tello_address)
            time.sleep(6)
            rotate(180)

        if 'end' in msg:
            print('...')
            sock.close()
            break

        if "takeoff" in msg:
            sock.sendto('takeoff'.encode(encoding="utf-8"), tello_address)

        if "land" in msg:
            sock.sendto(msg.encode(encoding="utf-8"), tello_address)

        if "command" in msg:
            sock.sendto('command'.encode(encoding="utf-8"), tello_address)

    except KeyboardInterrupt:
        print('\n . . .\n')
        sock.close()
        break
