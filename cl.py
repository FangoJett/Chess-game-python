import socket


FORMAT = 'utf-8'


def main():
    # Utwórz gniazdo klienta
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8888))
    
    
    
    
    while True:
        try:
            
            
            move = client_socket.recv(1024).decode(FORMAT)
            print(move)
            move = input("Your move: ")
            client_socket.send(move.encode())
            
        except KeyboardInterrupt:
            break

    # Zamknij gniazdo
    client_socket.close()

if __name__ == "__main__":
    main()
