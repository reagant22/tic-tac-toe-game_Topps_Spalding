import socket
import pickle
from tic_tac_toe import TicTacToe

HOST = '127.0.0.1'  # Server's IP address
PORT = 12783        # Port to listen on

# Initialize the server
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind((HOST, PORT))
s.listen(2)  # Listen for 2 clients
print("Waiting for players to connect...")

clients = []
game = TicTacToe("X")  # Initialize the game

# Accept connections from both clients
for _ in range(2):
    client_socket, client_address = s.accept()
    clients.append(client_socket)
    print(f"Connected to {client_address}!")

# Main game loop
while True:
    for i in range(2):  # Loop over each client
        client_socket = clients[i]
        other_client_socket = clients[1 - i]  # Get the other client

        # Send the current game state to the current player
        client_socket.send(pickle.dumps(game.symbol_list))
        
        # Wait for the current player's move
        move = client_socket.recv(4096)
        move = pickle.loads(move)

        # Process the move
        if game.edit_square(move):
            # If move is valid, send the updated game state to the other client
            other_client_socket.send(pickle.dumps(game.symbol_list))

            # Check for win or draw
            if game.did_win(game.player_symbol) or game.is_draw():
                # Notify both players of the end of the game
                for cs in clients:
                    cs.send(pickle.dumps("Game Over"))
                break

# Close sockets after the game
for cs in clients:
    cs.close()
