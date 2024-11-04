import socket
import pickle
from tic_tac_toe import TicTacToe

HOST = '127.0.0.1'  # Server's IP address
PORT = 12783        # Port to connect to

# Connect to the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
print(f"Connected to the game server!")

# Receive the player's symbol from the server
player_symbol = pickle.loads(s.recv(1024))  
print(f"You are Player {player_symbol}") 

player_symbol = "X" if s.getsockname()[1] == 12783 else "O"  # Determine symbol based on socket port
game = TicTacToe(player_symbol)

while True:
    # Receive and display the current game state
    game.symbol_list = pickle.loads(s.recv(1024))
    game.draw_grid()

    # Check if the game is over
    if isinstance(game.symbol_list, str):
        print(game.symbol_list)
        break

    # player turn to make a move
    if player_symbol == game.player_symbol:
        print(f"Your turn! Enter coordinate (e.g., 1A): ")
        move = input()
    
    # Send move to the server
        move = pickle.dumps(move)
        s.send(move)
    else:
        print("Waiting for the other player's move...")  # CHANGE: Inform player it's the other player's turn

s.close()
