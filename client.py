import socket
import threading

HEADER = 64
PORT = 2000
FORMAT = 'utf-8'
SERVER = "192.168.56.101"
ADDR = (SERVER, PORT)
DISCONNECT_MESSAGE = "DISCONNECT"
connected = True

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)

def send(msg):
    message = msg.encode(FORMAT)
    msg_length = len(message)
    send_length = str(msg_length).encode(FORMAT)
    send_length += b' ' *(HEADER - len(send_length))
    client.send(send_length)
    client.send(message)
    
def reading():
    while connected:
        try:
            print(client.recv(2048).decode(FORMAT))
        except:
            pass

a = threading.Thread(target = reading)
a.start()

while connected:
    mess = input() 
    if mess != "disconnect":
        send(mess)
    else:
        connected = False
send(DISCONNECT_MESSAGE)