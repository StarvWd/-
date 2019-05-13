import socket
#创建socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#绑定
sock.bind(("127.0.0.1", 7852))
#监听
sock.listen()

#while(True):
#接受一个传进来的socket
print("等待socket接入")
skt, addr = sock.accept()
print("socket接入成功！")
print("sock={0}".format(skt))

msg = skt.recv(500)
print(type(msg))
print(msg.decode())

skt.send("ok hello".encode())
skt.close()
sock.close()
