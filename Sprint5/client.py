import socket
import sys

def main():
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <server_ip> <server_port>")
        return

    server_ip = sys.argv[1]
    try:
        server_port = int(sys.argv[2])
    except ValueError:
        print("Invalid port number. Please provide a numeric value.")
        return

    # Create a socket
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Attempt to connect to the server
    try:
        client_socket.connect((server_ip, server_port))
    except ConnectionRefusedError:
        print("Unable to connect to the server. Please check the server's status.")
        exit(1)
    except socket.gaierror:
        print("Invalid server IP address. Please check and try again.")
        exit(1)

    print("Connected to the server!")

    # Main game loop or further interactions go here
    try:
        while True:
            message = input("Enter your move (0-8) or chat: ")
            client_socket.sendall(message.encode())
            response = client_socket.recv(1024).decode()
            print(response)
    except KeyboardInterrupt:
        print("\nClient interrupted. Exiting...")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
