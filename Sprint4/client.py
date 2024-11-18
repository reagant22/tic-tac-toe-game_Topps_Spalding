import socket

def start_client(host="127.0.0.1", port=65431):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        client.connect((host, port))
        print("Connected to the server!")  # connection confirmation

        while True:
            data = client.recv(1024).decode()
            if not data:
                print("Disconnected from server.")  # disconnection message
                break

            print(data.strip())  

            # If it's the player's turn to move
            if "Your move" in data:
                while True:  # input validation for move
                    move = input("Enter your move (0-8): ").strip()
                    if move.isdigit() and int(move) in range(9):
                        client.sendall(move.encode())
                        break
                    print("Invalid input. Please enter a number between 0 and 8.")

            # If the game is over (win, draw, etc.), ask for a rematch
            elif "Game Over!" in data or "Would you like to play again?" in data:  # game end prompts
                while True:  # input validation for rematch
                    rematch = input("Do you want to play again? (yes/no): ").strip().lower()
                    if rematch in {"yes", "no"}:
                        client.sendall(rematch.encode())
                        break
                    print("Invalid input. Please enter 'yes' or 'no'.")

                if rematch == "no":
                    print("Thanks for playing! Goodbye!")
                    break

    except ConnectionError as e:  # error handling for connection issues
        print(f"Connection error: {e}")

    except KeyboardInterrupt:  # graceful shutdown on Ctrl+C
        print("\nClient interrupted. Exiting...")

    finally:
        client.close()
        print("Connection closed.")  


if __name__ == "__main__":
    start_client()
