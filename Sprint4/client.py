import socket
import threading
import argparse

def handle_server_messages(client):
    while True:
        try:
            data = client.recv(1024).decode()
            if not data:
                print("Disconnected from server.")
                break
            print(data.strip())
        except ConnectionError:
            print("Connection lost.")
            break


def start_client(server_ip, port):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((server_ip, port))
        print("Connected to the server!")
        
        threading.Thread(target=handle_server_messages, args=(client,), daemon=True).start()

        while True:
            user_input = input("Enter your move (0-8) or chat: ").strip()
            if user_input.lower() == "exit":
                print("Exiting the game. Goodbye!")
                client.sendall(b"exit")
                break
            client.sendall(user_input.encode())

    except ConnectionError as e:
        print(f"Connection error: {e}")
    except KeyboardInterrupt:
        print("\nClient interrupted. Exiting...")
    finally:
        client.close()
        print("Connection closed.")

#args
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Tic Tac Toe Client")
    parser.add_argument("-i", "--ip", type=str, required=True, help="The server's IP address or DNS")
    parser.add_argument("-p", "--port", type=int, required=True, help="The server's port number")
    args = parser.parse_args()

    start_client(args.ip, args.port)
