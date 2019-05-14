#将具体的参数放在一个类中形成配置文件
class ServerContent:
    ip = '127.0.0.1'
    port = 9999

    head_protocal = "HTTP/1.1 "
    head_code_200 = "200 "
    head_status_OK = "OK"

    head_content_length = "Content-Length: "
    head_content_type = "Content-Type: "
    content_type_html = "text/html"

    blank_line = ""

import socket
import threading
'''
两个对象
一个负责监听接入 webserver
一个负责具体通信 sockethandle
'''

class Webserver():
    def __init__(self, ip=ServerContent.ip, port = ServerContent.port):
        self.ip = ip
        self.port = port
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind((self.ip,self.port))
        self.sock.listen(1)
        print("webserver is starting")
    def start(self):
        while True:
            skt, addr = self.sock.accept()
            if skt:
                sockHandle = SocketHandle(skt)
                thr = threading.Thread(target=sockHandle.startHandle)
                thr.setDaemon(True)
                thr.start()
                thr.join(5)

                skt.close()
                print("Socket {0} handling is done......".format(addr))

class SocketHandle:
    def __init__(self, sock):
        self.sock = sock
        self.headInfo = set()

    def startHandle(self):
        self.headHandler()  #解析HTTP协议
        self.sendRsp()      #返回内容

    def sendRsp(self):
        rsp_1 = "{0} {1} {2}\r\n".format(ServerContent.head_protocal,ServerContent.head_code_200,ServerContent.head_status_OK)
        rsp_2 = "Date:  2019.5.13\r\n"
        msg = "hello man"
        rsp_3 = "{1}: {0}\r\n".format(len(msg),ServerContent.head_content_length)
        rsp_4 = "\r\n"
        rsp_content = msg
        rsp = rsp_1 + rsp_2 + rsp_3 + rsp_4 + rsp_content

        self.sock.send(rsp.encode())
    def headHandler(self):
        self.headInfo = self.__getAllLine()
        print(self.headInfo)

    def __getAllLine(self):
        line = self.__getLine()
        rst = list()
        while line:
            rst.append(line)
            line = self.__getLine()
        return rst

    def __getLine(self):
        b1 = self.sock.recv(1)
        b2 = 0
        data = b''
        while b1 != b'\n' and b2 != b'\r':
            b2 = b1
            b1 = self.sock.recv(1)
            data += bytes(b2)

        return data.strip(b'\r').decode()


if __name__ == '__main__':
    ws = Webserver()
    ws.start()