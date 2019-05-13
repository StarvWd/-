'''
在v2基础上构造http响应返回信息
'''

import socket

def getLine(skt):
    '''
    从socket中读取一行
    :param skt:
    :return:http协议是ascll编码，传输的是bit流
    '''
    b1 = skt.recv(1)
    b2 = 0
    data = b''
    while b1 != b'\n' and b2 != b'\r':
        b2 = b1
        b1 = skt.recv(1)
        #print(type(b2))
        data  += bytes(b2)

    return data.strip(b'\r').decode()

def getHttpHeader(skt):
    '''
    得到传入socket的http请求头
    :param skt: 通信的socket
    :return: 解析后的请求头内容，字典rst
    '''
    rst={}
    #读取任意一行
    line = getLine(skt)

    while line:
        r = line.split(r': ')

        if len(r) == 2:
            rst[r[0]] = r[1]
        else:
            r = line.split(r'/')
            rst["method"] = r[0]
            rst['uri'] = r[1]
            rst['version'] = r[2]
        #print(r)

        line = getLine(skt)

    return rst

def sendRsp(skt, msg):
    '''
    构造http返回信息
    Content-Length表示主体长度
    :param skt:
    :param msg:返回的信息字符串
    :return:
    '''
    rsp_1 = "HTTP/1.1 200 OK\r\n"
    rsp_2 = "Date:  2019.5.13\r\n"
    rsp_3 = "Content-Length: {0}\r\n".format(len(msg))
    rsp_4 = "\r\n"
    rsp_content = msg
    rsp = rsp_1 + rsp_2 + rsp_3 + rsp_4 + rsp_content

    skt.send(rsp.encode())

sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
sock.bind(("127.0.0.1",7496))

sock.listen()
print("等待socket接入！")
skt,addr = sock.accept()
print("socket接入成功！")
#实际处理请求内容
http_info = getHttpHeader(skt)
print(http_info)

#反馈
msg = '''hello man\r\ni am fan'''
sendRsp(skt,msg)

skt.close()
sock.close()