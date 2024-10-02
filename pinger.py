# By: Ethan Morphew
# 2024-10-02
# Ping Sender (Pinger)

import socket
import time

#Ping Settings
remotePort = 50555
remoteIP = "localhost"
remoteAddress = (remoteIP,remotePort)

pingTimout = 2
pingRepeats = 10

#Socket Setup
remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
remoteSocket.settimeout(pingTimout)

#Stats
pingSuccesses = 0

print("Pinging " + remoteAddress[0] + ":" + str(remoteAddress[1]) + " " + str(pingRepeats) + " times")

#Loops through sending udp "ping" messages 
for i in range(pingRepeats):
   remoteSocket.sendto("ping".encode(),remoteAddress)
   start = time.time()
   try:
      pongMessage, recvAddress = remoteSocket.recvfrom(1024)
      pongMessage = pongMessage.decode()
      if pongMessage == "pong":
         pingSuccesses += 1
         end = time.time()
         rtt = int((end-start)*1000)
         print(str(i+1) + ": Pong Received From " + recvAddress[0] + " RTT: " + str(rtt) + "ms")
      else:
         print(str(i+1) + ": Pong Message Corrupted")
   except socket.timeout:
         print(str(i+1) + ": Request Timed Out")
print("Ping Success: " + str(pingSuccesses/pingRepeats*100) + "%")