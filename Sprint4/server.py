import socket
import threading


class TicTacToeGame:
    # No changes needed to the game logic class
    ...


def broadcast_message(message, clients):
    """Send a message to all connected clients."""
    for client in clients[:]:
        try:
            client.sendall(message.encode() + b"\n")
        except:
            clients.remove(client)


def handle_client(client_socket, game, clients, client_id, game_lock):
    try:
        if client_id == 0:
            client_socket.sendall(b"Welcome to Tic Tac Toe! You are Player X.\n")
        else:
            client_socket.sendall(b"You are Player O.\n")

        while not game.game_over:
            with game_lock:
                if game.current_player == ("X" if client_id == 0 else "O"):
                    board = game.display_board()
                    client_socket.sendall(f"\nGame Board:\n{board}\nYour move (0-8): ".encode())

                message = client_socket.recv(1024).decode().strip()

                # Handle chat messages
                if not message.isdigit():
                    broadcast_message(f"Player {client_id + 1} says: {message}", clients)
                    continue

                # Handle game moves
                position = int(message)
                if game.current_player == ("X" if client_id == 0 else "O"):
                    response = game.make_move(position)
                    board = game.display_board()

                    broadcast_message(f"\nGame Board:\n{board}\n", clients)
                    broadcast_message(response, clients)
                    if game.game_over:
                        broadcast_message("Game Over! Would you like to play again? (yes/no)", clients)
                        break
                else:
                    client_socket.sendall(b"Waiting for opponent...\n")

        client_socket.sendall(b"Would you like to play again? (yes/no): ")
        rematch_response = client_socket.recv(1024).decode().strip().lower()
        if rematch_response == "yes":
            with game_lock:
                if client_id == 0:
                    game.reset()
                broadcast_message("Rematch starting...\n", clients)
        else:
            broadcast_message("One of the players declined the rematch. Game over!\n", clients)

    except Exception as e:
        print(f"Error with client {client_id}: {e}")
    finally:
        client_socket.close()


def start_server(host="127.0.0.1", port=65431):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(2)
    print("Server started. Waiting for players to join...")
    game = TicTacToeGame()
    clients = []
    client_id = 0

    try:
        while len(clients) < 2:
            client_socket, addr = server.accept()
            print(f"Player {client_id + 1} connected from {addr}")
            clients.append(client_socket)
            threading.Thread(
                target=handle_client,
                args=(client_socket, game, clients, client_id, game_lock),
                daemon=True
            ).start()
            client_id += 1
    finally:
        server.close()
        print("Server shutting down...")


if __name__ == "__main__":
    game_lock = threading.Lock()
    start_server()
