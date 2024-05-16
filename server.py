import threading
import socket
import signal
import sys
import time


SERVER = 'localhost'
PORT = 8888
ADDR = (SERVER,PORT)
server = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
server.bind(ADDR)
FORMAT = 'utf-8'
clients = []


def send(msg,client):
    message = msg.encode(FORMAT)
    client.send(message)

def send_to_opp(msg,sender):
    for client in clients:
        if client!=sender:
            send(msg,client)
            


def handle_client(conn,addr):
    clients.append(conn)
    connected = True
    while connected:
        move = conn.recv(128).decode(FORMAT)
        if not move:
            break
        send_to_opp(move,conn)
        
        
    clients.remove(conn)       
    print(f"[{addr}] DISCONNECTED")



def start_server():
    
    server.listen()
    conn1, addr1 = server.accept()
    client_thread1 = threading.Thread(target=handle_client, args=(conn1, addr1))
    conn1.send("white".encode(FORMAT))
    client_thread1.start()
     






if __name__== "__main__":
    print("Initializing server...")
    start_server()