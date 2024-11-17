import socket

def start_client(host="127.0.0.1", port=65431):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client.connect((host, port))

    try:
        while True:
            data = client.recv(1024).decode()
            if not data:
                break
            print(data)
            if "Your move" in data:
                move = input("Enter your move (0-8): ")
                client.sendall(move.encode())
    finally:
        client.close()


if __name__ == "__main__":
    start_client()
