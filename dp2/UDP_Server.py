# UDPPingerServer.py
# We will need the following module to generate randomized lost packets
import random
from socket import *
import time

# Create a UDP socket
# Notice the use of SOCK_DGRAM for UDP packets
serverSocket = socket(AF_INET, SOCK_DGRAM)
# Assign IP address and port number to socket
serverSocket.bind(('', 12000))

last_seq = this_seq = transform_time = 0
last_timestamp = this_timestamp = time.time()

while True:
    # Generate random number in the range of 0 to 10
    rand = random.randint(0, 10)
    # Receive the client packet along with the address it is coming from
    message, address = serverSocket.recvfrom(1024)
    # Capitalize the message from the client
    message = message.decode().split()
    if message[1] == '0':
        last_timestamp = message[0]
        last_seq = message[1]
    else:
        this_seq = int(message[1])
        if rand > 3:
            this_timestamp = message[0]
            transform_time = float(this_timestamp) - float(last_timestamp)

    # If rand is less is than 4, we consider the packet lost and do not respond
    if rand < 4 or message[1] == '0':
        continue

    last_timestamp = this_timestamp

    if transform_time> 1.0:
        if int(last_seq) != 0:
            left = int(last_seq) + 1
        else:
            left = int(last_seq)
        for i in range(left, int(this_seq)):
            print(f"Packet {i} has lost.")
    last_seq = this_seq
    # Otherwise, the server responds
    serverSocket.sendto(message[2].encode(), address)
