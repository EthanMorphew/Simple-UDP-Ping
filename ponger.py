# By: Ethan Morphew
# 2024-10-02
# Ping Responder (Ponger)

import socket
import random
import time

localPort = 50555
localIP = 'localhost'

localSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
localSocket.bind((localIP, localPort))

while True:
    try:
        data, clientAddress = localSocket.recvfrom(1024)
        pingMessage = data.decode().split(',')
        if pingMessage[0] == 'ping':
            randSleep = random.random()*3
            print(randSleep)
            time.sleep(randSleep)
            localSocket.sendto(('pong,'+ str(pingMessage[1])).encode(),clientAddress)
    except:
        continue