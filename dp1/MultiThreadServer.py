from socket import *
import datetime
import threading


class ThreadServer(threading.Thread):
    def __init__(self, connect, address):
        threading.Thread.__init__(self)
        self.connectionSocket = connect
        self.addr = address

    def run(self):
        while True:
            try:
                print(
                    'thread %s is running...' % threading.current_thread().name)
                message = self.connectionSocket.recv(1024)
                if not message:
                    break
                print("message:", message)
                filename = message.split()[1]
                f = open(filename[1:])
                output_data = f.read()
                now = datetime.datetime.now()
                first_header = "HTTP/1.1 200 OK"
                header_info = {
                    # "Date": now.strftime("%Y-%m-%d %H:%M"),
                    "Content-Length": len(output_data),
                    "Keep-Alive": "timeout=%d,max=%d" % (10, 100),
                    "Connection": "Keep-Alive",
                    "Content-Type": "text/html"
                }

                following_header = "\r\n".join(
                    "%s:%s" % (item, header_info[item]) for item in header_info)
                self.connectionSocket.send("%s\r\n%s\r\n\r\n".encode()
                                           % (first_header.encode(),
                                              following_header.encode()))
                for i in range(0, len(output_data)):
                    self.connectionSocket.send(output_data[i].encode())
                # self.connectionSocket.send("\r\n".encode())
                self.connectionSocket.close()
                break
            except IOError:
                self.connectionSocket.send("HTTP/1.1 404 Not "
                                       "Found\r\n\r\n".encode())

if __name__ == '__main__':
    server_socket = socket(AF_INET, SOCK_STREAM)
    server_port = 6789
    server_socket.bind(('', server_port))
    server_socket.listen(5)
    threads = []
    while True:
        print("Ready to serve...")
        connection_soccket, addr = server_socket.accept()
        print("addr", addr)
        ts = ThreadServer(connection_soccket, addr)
        ts.setDaemon(True)
        ts.start()
        threads.append(ts)

    server_socket.close()
