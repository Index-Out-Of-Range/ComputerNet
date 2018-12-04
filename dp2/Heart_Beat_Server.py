from socket import *
from datetime import *
import random

server_socket = socket(AF_INET, SOCK_DGRAM)
PORT = 12000

print("Ready to server...")
server_socket.bind(('', PORT))
server_start = datetime.now()

ip_table = dict()
packets_lost = dict()

while True:
    try:
        server_socket.settimeout(30)
        message, address = server_socket.recvfrom(1024)
        message_list = message.decode().split('\t')
        message = datetime.strptime(message_list[1], "%Y-%m-%d %H:%M:%S.%f")
        try:
            if not address in ip_table:
                ip_table[address] = [0, 0, 0]
                packets_lost[address] = 0
            ip_table[address][0] += 1
            print(f"Received packet no.{ip_table[address][0]} from {address}.")
            print(f"The sequence number sent with the packet was {message_list[0]}")
            now = datetime.now()
            response = now - message
            ip_table[address][2] = now
            reply = f"Packet delivery delay = {str(response)},Number of " \
                f"packets lost in between = {packets_lost[address]}"
            packets_lost[address] = 0
            rand = random.randint(0, 10)
            if rand<4:
                continue
            server_socket.sendto(reply.encode(), address)
            print(
                f"Sent response to {address} with a delay of {response.total_seconds()}")
        except TypeError:
            print(
                f"Client ad {address} sent an unrecognized packet. Replying with an appropriate response.")
            response = f"The datatype supported by this server is string. " \
                f"Given data is {str(type(message))}"
            server_socket.sendto(response.encode(), address)
    except KeyboardInterrupt:
        print("\nSafely closing down the server...")
        print("*" * 70 + "\n")
        print("Summary")
        server_end = datetime.now()
        print(f"Server started serving on port {PORT} on {server_start}, "
              f"and is exiting on {server_end}")
        print(f"Server ran for a duration of {server_end - server_start}")
        print("Client\t\t\tNumber of Packet Received\tPacket Lost "
              "Percentage\tLast Heartbeat received at")

        for key in ip_table:
            percentage = ((int(ip_table[key][1])) / (int(ip_table[key][
                                                             0]) * 1.0) * 100)
            print(key, "\t", ip_table[key][0], '\t\t\t\t',
                  ("%.2f") % percentage, '%\t\t\t', ip_table[key][2])
        print()
        print("*" * 70 + "\n")
        break

    except Exception as e:
        print(e)

server_socket.close()
