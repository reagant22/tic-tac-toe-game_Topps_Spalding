import socket
import threading

def handle_server_messages(client):
    """Receive messages from the server."""
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


def start_client(host="127.0.0.1", port=65431):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        print("Connected to the server!")
        
        # Start a thread to handle incoming server messages
        threading.Thread(target=handle_server_messages, args=(client,), daemon=True).start()

        while True:
            # Send either game moves or chat messages
            user_input = input("Enter your move (0-8) or chat: ").strip()
            if user_input.lower() == "exit":
                print("Exiting the game. Goodbye!")
                break
            client.sendall(user_input.encode())

    except ConnectionError as e:
        print(f"Connection error: {e}")
    except KeyboardInterrupt:
        print("\nClient interrupted. Exiting...")
    finally:
        client.close()
        print("Connection closed.")


if __name__ == "__main__":
    start_client()
