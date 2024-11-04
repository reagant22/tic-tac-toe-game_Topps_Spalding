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
symbols = ["X", "O"]
game = TicTacToe("X")  # Initialize the game

# Accept connections from both clients
for i in range(2):
    client_socket, client_address = s.accept()
    # clients.append(client_socket)
    clients.append((client_socket, symbols[i]))  
    client_socket.send(pickle.dumps(symbols[i])) 
    print(f"Connected to {client_address} as Player {symbols[i]}!")


# Main game loop
game_over = False
while not game_over:
    for i, (client_socket, player_symbol) in enumerate(clients):
        other_client_socket, _ = clients[1 - i]

        # Send the current game state to the current player
        client_socket.send(pickle.dumps(game.symbol_list))
        
        # Wait for the current player's move
        move = client_socket.recv(4096)
        move = pickle.loads(move)

        # Process the move
        if game.edit_square(move):
            # If move is valid, send the updated game state to the other client
            game.player_symbol = player_symbol
            other_client_socket.send(pickle.dumps(game.symbol_list))

            # Check for win or draw
            if game.did_win(player_symbol):  # CHANGE: Check win condition for the current player
                message = f"Player {player_symbol} wins!"  # CHANGE: Set win message
                game_over = True  
            elif game.is_draw():  
                message = "It's a draw!"  
                game_over = True  
            else:
                continue  # move to the next turn if no win/draw

            # Notify both players of the end of the game
            for cs, _ in clients:
                cs.send(pickle.dumps(message))  # game-over message to all clients
            break

# Close sockets after the game
for cs in clients:
    cs.close()
