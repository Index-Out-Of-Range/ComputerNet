import socket
import sys

server_host = sys.argv[1]
server_port = sys.argv[2]
filename = sys.argv[3]

se = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
se.connect((server_host, int(server_port)))
try:
    se.send("GET /{} HTTP/1.1\r\n".format(filename).encode())
    se.send("Host: {}:{}\r\n".format(server_host, server_port).encode())
    se.send("Connection: keep-alive\r\n".encode())
    se.send("Cache-Control: max-age=0\r\n".encode())
    se.send("Accept: text/html,application/xhtml+xml,"
            "application/xml;q=0.9,image/webp,*/*;q=0.8\r\n".encode())
    se.send("Upgrade-Insecure-Requests: 1\r\n".encode())
    se.send("User-Agent: Mozilla/5.0 (Windows NT 10.0; WOW64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.110 Safari/537.36\r\n".encode())
    se.send("Accept-Encoding: gzip, deflate, sdch\r\n".encode())
    se.send("Accept-Language: zh-CN,zh;q=0.8\r\n".encode())
    se.send("Cookie: JSESSIONID=8E827CDF1932CAC60C4D4AA4DD39C171; "
            "sid=a1m649tme0i2bu00b03rbnc806\r\n\r\n".encode())
except socket.error as e:
    print("Error sending data:%s" % e)
buffer = []
while True:
    d = se.recv(1024)
    # print('d:', d)
    if d:
        buffer.append(d)
    else:
        break
data = b''.join(buffer)
se.close()
header, html = data.split(b'\r\n\r\n', 1)
with open('receive.html', 'wb') as f:
    f.write(html)
