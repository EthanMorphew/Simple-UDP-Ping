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

#Stats
pingSuccesses = 0

print("Pinging " + remoteAddress[0] + ":" + str(remoteAddress[1]) + " " + str(pingRepeats) + " times")

#Loops through sending udp "ping" messages 
for i in range(pingRepeats):
   
   remoteSocket.sendto(("ping," + str(i)).encode(),remoteAddress)
   pingWindow = pingTimout
   start = time.time()
   
   while True:
      try:
         remoteSocket.settimeout(pingWindow)
         data, recvAddress = remoteSocket.recvfrom(1024)
         pongMessage = data.decode().split(',')
         #Successful Case, print to console and send the next ping.
         if pongMessage[0] == "pong" and pongMessage[1] == str(i):
            pingSuccesses += 1
            end = time.time()
            rtt = int((end - start) * 1000)
            print(str(i) + ": Pong " + pongMessage[1] + " Received From " + recvAddress[0] + " RTT: " + str(rtt) + "ms")
            break
         #Received a ping with wrong seq number or garbage message, adjust timeout window and continue.
         else:
            pingWindow = pingTimout - (time.time() - start)
            print(pingWindow)
      #if socket timeout triggered we are over the time limit and move on to the next packet.
      except socket.timeout:
         print(str(i) + ": Request Timed Out")
         break

print("Ping Success: " + str(pingSuccesses/pingRepeats*100) + "%")