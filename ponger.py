# By: Ethan Morphew
# 2024-10-02
# Ping Responder (Ponger)

import socket

localPort = 50555
localIP = 'localhost'

localSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
localSocket.bind((localIP, localPort))

while True:
    try:
        pingMessage, clientAddress = localSocket.recvfrom(1024)
        if pingMessage.decode() == 'ping':
            localSocket.sendto('pong'.encode(),clientAddress)
    except:
        continue