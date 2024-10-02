# By: Ethan Morphew
# 2024-10-02
# Ping Sender (Pinger)

import socket
import time

remotePort = 50555
remoteIP = '1.1.1.1'
remoteAddress = (remoteIP,remotePort)

remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
remoteSocket.settimeout(2)

for i in range(10):
   remoteSocket.sendto('ping'.encode(),remoteAddress)
   start = time.time()
   try:
      pongMessage, recvAddress = remoteSocket.recvfrom(1024)
   except socket.timeout:
         print("Remote host did not respond")
   pongMessage = pongMessage.decode()
   end = time.time()
   rtt = end-start
   print('Pong received from '+ recvAddress[0] + ' RTT: ' + str(rtt))
print("Ping Complete!")