from socket import *
from datetime import *
import time


client_socket = socket(AF_INET, SOCK_DGRAM)
PORT = 12000

s_count = 0
r_count = 0
l_count = 0
seq = 1

while True:
    try:
        now = datetime.now()
        client_socket.settimeout(5)
        client_socket.sendto((str(seq) + '\t' + str(now)).encode(),
                             ('localhost', PORT))
        print(f"PING 127.0.0.1 : {PORT} at {now}")
        s_count += 1

        message, address = client_socket.recvfrom(1024)
        print(message.decode())
        r_count += 1
        seq += 1
        time.sleep(3)
    except TypeError:
        print("Server sent an unexpected response.")
        break
    except timeout:
        print("timeout")
        l_count += 1
        seq += 1
    except Exception as e:
        print(e)
        break
    except KeyboardInterrupt:
        print("\nSafely shutting down the client.")
        print("Statistics:")
        print("Packets sent, ", s_count)
        print("Packets received, ", r_count)
        print("Percentage Packet Loss",((1-(r_count/(s_count*1.0)))*100),"%")
        break

client_socket.close()