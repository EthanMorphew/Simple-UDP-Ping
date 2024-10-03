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
pingWindow = pingTimout
pingRepeats = 10

#Socket Setup
remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
remoteSocket.settimeout(pingTimout)

#Stats
pingSuccesses = 0

print("Pinging " + remoteAddress[0] + ":" + str(remoteAddress[1]) + " " + str(pingRepeats) + " times")

#Loops through sending udp "ping" messages 
for i in range(pingRepeats):
   remoteSocket.sendto(("ping," + str(i)).encode(),remoteAddress)
   pingWindow = 2
   start = time.time()
   while time.time() - start < pingTimout:
      try:
         data, recvAddress = remoteSocket.recvfrom(1024)
         pongMessage = data.decode().split(',')
         print(pongMessage)
         print(pingWindow)
         print(i)
         print('#########')
         if pongMessage[0] == "pong" and pongMessage[1] == i:
            pingSuccesses += 1
            end = time.time()
            rtt = int((end-start)*1000)
            print(str(i) + ": Pong " + pongMessage[1] + " Received From " + recvAddress[0] + " RTT: " + str(rtt) + "ms")
         elif pongMessage[0] == "pong" and pongMessage[1] != i:
            pingWindow = pingWindow - (time.time() - start)
         else:   
            print(str(i) + ": Pong Message Corrupted")
      except socket.timeout:
         print(str(i) + ": Request Timed Out")

print("Ping Success: " + str(pingSuccesses/pingRepeats*100) + "%")