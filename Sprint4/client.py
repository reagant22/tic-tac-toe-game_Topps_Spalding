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
            
            # If it's the player's turn to move
            if "Your move" in data:
                move = input("Enter your move (0-8): ")
                client.sendall(move.encode())
                
            # If the game is over (win, draw, etc.), ask for a rematch
            elif "Game Over!" in data:
                rematch = input("Do you want to play again? (yes/no): ")
                client.sendall(rematch.encode())
                
                # If the rematch is not "yes", exit the loop
                if rematch.lower() != "yes":
                    print("Thanks for playing!")
                    break
    finally:
        client.close()


if __name__ == "__main__":
    start_client()
