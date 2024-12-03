import socket

def start_client(host="127.0.0.1", port=65431):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, port))
        print("Connected to the server!")

        while True:
            data = client.recv(1024).decode()
            if not data:
                print("Disconnected from server.")
                break

            print(data.strip())

            # Allow either a game move or a chat message
            if "Your move" in data or "Enter your move (0-8) or chat:" in data:
                while True:
                    message = input("Enter your move (0-8) or chat: ").strip()
                    if message.isdigit() and int(message) in range(9):
                        client.sendall(message.encode())  # Valid game move
                        break
                    elif message.startswith("/chat:"):
                        client.sendall(message.encode())  # Chat message
                        break
                    else:
                        print("Invalid input. Enter a number (0-8) or a chat message using '/chat:'.")
            
            elif "Would you like to play again?" in data:
                while True:
                    rematch = input("Do you want to play again? (yes/no): ").strip().lower()
                    if rematch in {"yes", "no"}:
                        client.sendall(rematch.encode())
                        break
                    print("Invalid input. Please enter 'yes' or 'no'.")
                if rematch == "no":
                    print("Thanks for playing! Goodbye!")
                    break

    except ConnectionError as e:
        print(f"Connection error: {e}")

    except KeyboardInterrupt:
        print("\nClient interrupted. Exiting...")

    finally:
        client.close()
        print("Connection closed.")

if __name__ == "__main__":
    start_client()
