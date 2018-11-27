# import socket module
from socket import *
import datetime

serverSocket = socket(AF_INET, SOCK_STREAM)
# Prepare a sever socket
address = ('', 6789)
serverSocket.bind(address)
serverSocket.listen(5)

while True:
    # Establish the connection6
    print('Ready to serve...')
    connectionSocket, addr = serverSocket.accept()
    print('addr:', addr)
    try:
        message = connectionSocket.recv(1024).decode()
        print('message:', message)
        filename = message.split()[1]
        f = open(filename[1:])
        output_data = f.read()
        # print('output_data:', output_data)
        # Send one HTTP header line into socket
        now = datetime.datetime.now()
        first_header = "HTTP/1.1 200 OK"
        header_info = {
            "Date": now.strftime("%Y-%m-%d %H:%M"),
            "Content-Length": len(output_data),
            "Keep-Alive": "timeout=%d,max=%d" % (10, 100),
            "Connection": "Keep-Alive",
            "Content-Type": "text/html"
        }
        following_header = "\r\n".join("%s:%s" % (item, header_info[item])
                                       for item in header_info)
        # print("following_header:", following_header)
        connectionSocket.send("%s\r\n%s\r\n\r\n".encode() % (first_header.encode(),
                                                             following_header.encode()))
        # Send the content of the requested file to the client
        for i in range(0, len(output_data)):
            connectionSocket.send(output_data[i].encode())
        connectionSocket.send("\r\n".encode())

        connectionSocket.close()
    except IOError:
        # Send response message for file not found
        # Close client socket
        connectionSocket.send("HTTP/1.1 404 Not Found\r\nContent-Type: "
                              "text/html\r\n\r\n<!doctype "
                              "html><html><body><h1>404 Not "
                              "Found</h1></body></html>".encode())
        connectionSocket.close()

serverSocket.close()
# sys.exit()  # Terminate the program after sending the corresponding data
