import socket
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = "100.25.104.144"
port = 5050
s.connect((host,port))
print("Connected To The Server")

class MyThd1(Thread):
    def run(self):
        while True:
            s_msg = input("Enter Your Msg : ")
            s_msg = s_msg.encode()
            s.send(s_msg)
            print("sent successfully")

class MyThd2(Thread):
    def run(self):
        while True:
            r_msg = s.recv(1024)
            r_msg = r_msg.decode()
            print("Received Msg : " + r_msg)

t1 = MyThd1()
t2 = MyThd2()
t1.start()
t2.start()