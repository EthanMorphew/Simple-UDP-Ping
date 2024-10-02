# By: Ethan Morphew
# 2024-10-02
# Ping Sender (Pinger)

import socket
import sys
import time

remotePort = 50555
remoteIP = 'localhost'
remoteAddress = (remoteIP,remotePort)

remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

remoteSocket.sendto('ping' ,remoteAddress)
start = time.time()
try:
   pongMessage, recvAddress = remoteSocket.recvfrom(1024)
   end = time.time()
   rtt = end-start
except:
   print('An Error Occured!')
