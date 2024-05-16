import socket

def main():
    # Utwórz gniazdo klienta
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(('localhost', 8888))
    
    while True:
        try:
            # Wczytaj ruch od gracza
            move = input("Your move: ")
            
            # Wyślij ruch do serwera
            client_socket.send(move.encode())
        except KeyboardInterrupt:
            break

    # Zamknij gniazdo
    client_socket.close()

if __name__ == "__main__":
    main()
