import socket
from threading import Thread

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_ip = "localhost"
port  = 443
s.bind((server_ip,port))
print("Server Is Running On " + server_ip +" "+ str(port))

s.listen(1)
conn, addr = s.accept()
print("Connected")
print(addr)

class send(Thread):
    def run(self):
        while True:
            msg = input("Enter Your message : ")
            msg = msg.encode()
            conn.send(msg)
            print("Your msg is sent. ")

class receive(Thread):
    def run(self):
        while True:
            r_msg = conn.recv(1024)
            r_msg = r_msg.decode()
            print("received msg : " + r_msg)
           
t1 = send()
t2 = receive()
t1.start()
t2.start()
