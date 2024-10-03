# By: Ethan Morphew
# 2024-10-02
# Ping Responder (Ponger)

import socket
import random
import time
import sys

localPort = 50555
localIP = 'localhost'

localSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
localSocket.bind((localIP, localPort))

randomDelay = False
randomDrops = False

print("Listening on " + localSocket.getsockname()[0] + ":" + str(localSocket.getsockname()[1])) 
while True:
    try:
        data, clientAddress = localSocket.recvfrom(1024)

        if randomDelay:
            time.sleep((random.random() * 0.4) + 0.1)

        pingMessage = data.decode().split(',')
        if pingMessage[0] == 'ping':
            localSocket.sendto(('pong,'+ str(pingMessage[1])).encode(),clientAddress)
    except:
        continue