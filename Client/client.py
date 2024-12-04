import socket
import sys
import threading

def listen_to_server(client_socket):
    """Listen to server messages and print them."""
    try:
        while True:
            response = client_socket.recv(1024).decode()
            if not response:
                print("Server disconnected.")
                break
            print("\n" + response)
    except ConnectionResetError:
        print("\nServer connection lost.")
    finally:
        client_socket.close()
        sys.exit(0)

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

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client_socket.connect((server_ip, server_port))
    except ConnectionRefusedError:
        print("Unable to connect to the server. Please check the server's status.")
        return
    except socket.gaierror:
        print("Invalid server IP address. Please check and try again.")
        return

    print("Connected to the server!")


    listener_thread = threading.Thread(target=listen_to_server, args=(client_socket,), daemon=True)
    listener_thread.start()

    try:
        while True:
            message = input("Enter your move (0-8) or chat: ").strip()
            if not message:
                continue
            client_socket.sendall(message.encode())
    except KeyboardInterrupt:
        print("\nClient interrupted. Exiting...")
    finally:
        client_socket.close()

if __name__ == "__main__":
    main()
    
