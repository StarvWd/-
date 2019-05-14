
'''
修改sendRst函数，使其返回静态页面
页面在webapp文件夹中
'''


#将具体的参数放在一个类中形成配置文件
class ServerContent:
    ip = '127.0.0.1'
    port = 9968

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
                thr.join()

                skt.close()
                print("Socket {0} handling is done......".format(addr))

class SocketHandle:
    def __init__(self, sock):
        self.sock = sock
        self.headInfo = dict()

    def startHandle(self):
        self.headHandler()   #解析HTTP协议
        self.reqRoute()      #调用路由

    def reqRoute(self):
        uri = self.headInfo['uri']
        if uri == '/':
            self.sendRsp(r'.\webapp\item.html')
            return None
        if uri == r'/favicon.ico':
            self.sendStaticRsp(r'.\webapp\fav.jfif')
            return None

    def sendStaticRsp(self, fp):
        with open(fp, mode='rb') as f:
            ico = f.read()
            self.sendRspAll(ico)

    def sendRsp(self, fp):
        with open(fp, mode='r', encoding='utf-8') as f:
            data = f.read()
            self.sendRspAll(data)

    def sendRspAll(self, msg):
        '''rsp_1 = "{0} {1} {2}\r\n".format(ServerContent.head_protocal,ServerContent.head_code_200,ServerContent.head_status_OK)
        rsp_2 = "Date:  2019.5.13\r\n"
        rsp_3 = "{1}: {0}\r\n".format(len(msg),ServerContent.head_content_length)
        rsp_4 = "\r\n"

        rsp_content = msg
        rsp = rsp_1 + rsp_2 + rsp_3 + rsp_4 + rsp_content
        self.sock.send(rsp.encode())
        '''
        self.sendRspLine("HTTP/1.1 200 OK")
        self.sendRspLine("Date:  2019.5.13")
        self.sendRspLine("Content-Length: {0}".format(len(msg)))
        self.sendRspLine('')
        self.sendRspLine(msg)


    def sendRspLine(self,line):
        if type(line) == bytes:
            self.sock.send(line)
        else:
            line += "\r\n"
            self.sock.send(line.encode())
        return None

    def headHandler(self):
        tmpHead = self.__getAllLine()
        for line in tmpHead:
            #print(line)
            #print(type(line))
            if r": " in line:
                infos = line.split(r': ')
                self.headInfo[infos[0]] = infos[1]
            else:
                infos = line.split(r' ')
                self.headInfo["method"] = infos[0]
                self.headInfo['uri'] = infos[1]
                self.headInfo['version'] = infos[2]

        print(self.headInfo)

    def __getAllLine(self):
        rst = []
        while True:
            line = self.__getLine()
            if line:
                rst.append(line)
            else:
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