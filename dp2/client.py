from socket import *
import time

HOST = 'localhost'
PORT = 12000
BUFSIZE = 1024
loss_count = 0
minimum = maximum = total = 0

client_socket = socket(AF_INET, SOCK_DGRAM)

for i in range(10):
    try:
        start_time = time.time()
        client_socket.sendto('A'.encode(), (HOST, PORT))
        client_socket.settimeout(1.0)

        message, address = client_socket.recvfrom(1024)
        end_time = time.time()
        RTT = end_time - start_time
        total += RTT
        if i == 0:
            maximum = minimum = RTT
        else:
            if RTT > maximum:
                maximum = RTT
            elif RTT < minimum:
                minimum = RTT
        print("Ping i:{} rtt:{}".format(i, RTT))
    except timeout:
        loss_count += 1
        print("Request timeout")

print("Minimum RTT: {}".format(minimum))
print("Maximum RTT: {}".format(maximum))
print("Average RTT: {}".format(total / (10 - loss_count)))
print("Loss rate: {}0%".format(loss_count))