import socket
import pickle
from tic_tac_toe import TicTacToe

HOST = '127.0.0.1'  # Server's IP address
PORT = 12783        # Port to connect to

# Connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print(f"Connected to the game server!")

player_symbol = "X" if s.getsockname()[1] == 12783 else "O"  # Determine symbol based on socket port
game = TicTacToe(player_symbol)

while True:
    # Receive and display the current game state
    game.symbol_list = pickle.loads(s.recv(1024))
    game.draw_grid()

    # Player's turn to make a move
    print(f"Your turn! Enter coordinate (e.g., 1A): ")
    move = input()
    
    # Send the move to the server
    move = pickle.dumps(move)
    s.send(move)

    # Wait for the server to notify the end of the game
    response = s.recv(1024)
    response = pickle.loads(response)
    if response == "Game Over":
        print("Game Over! Thanks for playing!")
        break

s.close()
