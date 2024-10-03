# By: Ethan Morphew
# 2024-10-02
# Ping Sender (Pinger)

import socket
import time
import argparse

parser =  argparse.ArgumentParser(prog='pinger.py', description='Sends UDP messages to ponger')
parser.add_argument("-b", "--backoff", help = "Exponentialy increase timeout if packet is not received", default = False, action='store_true')
args = parser.parse_args()

#Remote Addressd
remotePort = 50555
remoteIP = "10.0.0.2"
remoteAddress = (remoteIP,remotePort)

#Ping Settings
pingTimeout = 2
pingRepeats = 10

pingBackoff = args.backoff

#Socket Setup
remoteSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#Stats
pingSuccesses = 0
returnTimes = []

print("Pinging " + remoteAddress[0] + ":" + str(remoteAddress[1]) + " " + str(pingRepeats) + " times")

#Loops through sending udp "ping" messages 
for i in range(pingRepeats):
   remoteSocket.settimeout(pingTimeout)
   remoteSocket.sendto(("ping," + str(i)).encode(),remoteAddress)
   sendTime = time.time()
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
            returnTimes.append(rtt)
            print(str(i) + ": Pong " + pongMessage[1] + " Received From " + recvAddress[0] + " RTT: " + str(rtt) + "ms")
            break
         #Received a ping with wrong seq number or garbage message, adjust timeout window and continue.
         else:
            remoteSocket.settimeout(pingTimeout - (recvTime - sendTime))
      #if socket timeout triggered we are over the time limit and move on to the next packet.
      except socket.timeout:
         print(str(i) + ": Request Timed Out")
         # If timeout occurs icrease timeout duration
         if pingBackoff:
            pingTimeout = pingTimeout * pingTimeout
         break
#Calculate Statistics
if(len(returnTimes) > 0):
   avgRtt = round(sum(returnTimes)/len(returnTimes))
   minRtt = min(returnTimes)
   maxRtt = max(returnTimes)
   print("Average RTT: " + str(avgRtt) + "ms Max RTT: " + str(maxRtt) + "ms Min RTT:" + str(minRtt) + "ms")
print("Loss Rate: " + str(100 - (pingSuccesses/pingRepeats * 100)) + "%")