import socket
import threading
import os
import time

prev_msg = None
HEADER = 64
PORT = 2001
SERVER = "192.168.56.100"
# SERVER = socket.gethostbyname(socket.gethostname())
ADDR = (SERVER, PORT)
FORMAT = 'utf-8'
DISCONNECT_MESSAGE = "DISCONNECT"

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind(ADDR)

PEER_SERWER = "192.168.56.101"
PORT2 = 2000
ADDR2 = (PEER_SERWER, PORT2)
server2 = socket.socket(socket.AF_INET, socket.SOCK_STREAM)


clients = set()
clients_lock = threading.Lock()

def server_to_server():
    while True:
        try:
            server2.connect(ADDR2)

        except:
            pass


def reading():
    while True:
        try:
            print(server2.recv(2048).decode(FORMAT))
        except:
            pass


def listener(conn, addr):
    print(f"accepted connection from {addr}")
    global prev_msg
    with clients_lock:
        clients.add(conn)
    try:
        while True:
            msg_length = conn.recv(HEADER).decode(FORMAT)
            if not msg_length:
                break
            else:
                msg_length = int(msg_length)

                msg = conn.recv(msg_length).decode(FORMAT)
                if msg == DISCONNECT_MESSAGE:
                    break
                else:
                    if prev_msg != msg:
                        prev_msg = msg
                        with clients_lock:
                            for c in clients:
                                c.sendall(msg.encode(FORMAT))
                        msglen = len(msg.encode(FORMAT))
                        send_msglen = str(msglen).encode(FORMAT)
                        send_msglen += b' ' * (HEADER - len(send_msglen))
                        server2.send(send_msglen)
                        server2.send(msg.encode(FORMAT))
                        time.sleep(0.5)

    finally:
        with clients_lock:
            clients.remove(conn)
            conn.close


def start():
    server.listen()
    print(f"[Listening] server is listening on {SERVER}")
    while True:
        conn, addr = server.accept()
        thread = threading.Thread(target=listener, args=(conn, addr))
        stos = threading.Thread(target=server_to_server)
        read = threading.Thread(target=reading)
        

        stos.start()
        read.start()
        thread.start()

        print(f"[Active Connections] {(threading.active_count()-1)/3}")

print("Serwer is starting")
start()