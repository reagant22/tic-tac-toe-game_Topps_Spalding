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

            # Process each message from the server
            messages = data.strip().split("\n")
            for message in messages:
                print(message)
        except ConnectionError:
            print("Connection lost.")
            break


def start_client(host="127.0.0.1", port=65431):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client.connect((host, port))
        print("Connected to the server!")
        
        # Start a thread to handle incoming server messages
        server_thread = threading.Thread(target=handle_server_messages, args=(client,), daemon=True)
        server_thread.start()

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


if __name__ == "__main__":
    start_client()
