# By: Ethan Morphew
# 2024-10-02
# Ping Sender (Pinger)

import socket
import time
import sys

#Remote Address
remotePort = 50555
remoteIP = "localhost"
remoteAddress = (remoteIP,remotePort)

#Ping Settings
pingTimout = 2
pingRepeats = 10

pingBackoff = False

#Socket Setup
remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Stats
pingSuccesses = 0

print("Pinging " + remoteAddress[0] + ":" + str(remoteAddress[1]) + " " + str(pingRepeats) + " times")

#Loops through sending udp "ping" messages 
for i in range(pingRepeats):
   remoteSocket.settimeout(pingTimout)
   sendTime = time.time()
   remoteSocket.sendto(("ping," + str(i)).encode(),remoteAddress)
   # Loops until correct ping seq is received or timeout occurs
   while True:
      try:
         data, recvAddress = remoteSocket.recvfrom(1024)
         recvTime = time.time()
         pongMessage = data.decode().split(',')
         #Successful Case, print to console and send the next ping.
         if pongMessage[0] == "pong" and pongMessage[1] == str(i):
            pingSuccesses += 1
            rtt = int((recvTime - sendTime) * 1000)
            print(str(i) + ": Pong " + pongMessage[1] + " Received From " + recvAddress[0] + " RTT: " + str(rtt) + "ms")
            break
         #Received a ping with wrong seq number or garbage message, adjust timeout window and continue.
         else:
            remoteSocket.settimeout(pingTimout - (recvTime - sendTime))
      #if socket timeout triggered we are over the time limit and move on to the next packet.
      except socket.timeout:
         print(str(i) + ": Request Timed Out")
         break

print("Ping Success: " + str(pingSuccesses/pingRepeats * 100) + "%")