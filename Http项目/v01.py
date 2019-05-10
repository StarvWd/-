import socket
#创建socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#绑定
sock.bind(("127.0.0.1", 7852))
#监听
sock.listen()

#while(True):
#接受一个传进来的socket
skt, addr = sock.accept()
print("sock={0}".format(skt))

msg = skt.recv(100)
print(type(msg))
print(msg.decode())

skt.send("ok hello".encode())
skt.close()
sock.close()
