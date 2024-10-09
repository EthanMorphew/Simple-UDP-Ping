# By: Ethan Morphew
# 2024-10-02
# Ping Responder (Ponger)

import socket
import random
import time
import argparse

# Argument flags setup
parser =  argparse.ArgumentParser(prog='ponger.py', description='Responds to UDP messages from pinger')
parser.add_argument("-d", "--delay", help = "Introduce random response delay", default = False, action='store_true')
parser.add_argument("-f", "--failures", help = "Introduce random response failures/drops", default = False, action='store_true')
args = parser.parse_args()


localPort = 50555 # Can be changed
localIP = '0.0.0.0' # Binds to all local IPs -> Can be changed

localSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
localSocket.bind((localIP, localPort))

randomDelay = args.delay

randomDrops = args.failures
dropCount = 0
packetCount = 0



print("Listening on " + localSocket.getsockname()[0] + ":" + str(localSocket.getsockname()[1])) 
while True:
    try:
        data, clientAddress = localSocket.recvfrom(1024)
        packetCount += 1
        #Introduces random delay between 100ms and 500ms
        if randomDelay:
            time.sleep((random.random() * 0.4) + 0.1)
       
        #Introduces random packet loss (20% loss average)
        if randomDrops:
            if random.random() <= 0.2 and dropCount < 5:
                dropCount += 1
                continue #Drop the packet, do not send response

        if packetCount >= 10:
            packetCount = 0
            dropCount = 0

        pingMessage = data.decode().split(',')
        if pingMessage[0] == 'ping':
            localSocket.sendto(('pong,'+ str(pingMessage[1])).encode(),clientAddress)
    except:
        continue