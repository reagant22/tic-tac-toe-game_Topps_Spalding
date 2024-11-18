import socket
import threading

# Tic Tac Toe game logic
class TicTacToeGame:
    def __init__(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.game_over = False

    def display_board(self):
        return (
            f"{self.board[0]} | {self.board[1]} | {self.board[2]}\n"
            "---------\n"
            f"{self.board[3]} | {self.board[4]} | {self.board[5]}\n"
            "---------\n"
            f"{self.board[6]} | {self.board[7]} | {self.board[8]}"
        )

    def make_move(self, position):
        if self.board[position] == " " and not self.game_over:
            self.board[position] = self.current_player
            if self.check_winner():
                self.game_over = True
                return f"Player {self.current_player} wins!"
            elif " " not in self.board:
                self.game_over = True
                return "It's a draw!"
            else:
                self.current_player = "O" if self.current_player == "X" else "X"
                return "Move accepted"
        return "Invalid move"

    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6)
        ]
        for combo in winning_combinations:
            if (
                self.board[combo[0]] == self.board[combo[1]] ==
                self.board[combo[2]] != " "
            ):
                return True
        return False

    def reset(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.game_over = False


def broadcast_message(message, clients):  
    """Send a message to all connected clients."""
    for client in clients[:]:  # Iterate over a copy to allow safe removal
        try:
            client.sendall(message.encode() + b"\n")
        except:
            clients.remove(client)  # Remove disconnected clients


def handle_client(client_socket, game, clients, client_id, game_lock):
    try:
        if client_id == 0:
            client_socket.sendall(b"Welcome to Tic Tac Toe! You are Player X.\n")
        else:
            client_socket.sendall(b"You are Player O.\n")

        while not game.game_over:
            with game_lock:  # Synchronize shared game state
                if game.current_player == ("X" if client_id == 0 else "O"):
                    board = game.display_board()
                    client_socket.sendall(f"\nGame Board:\n{board}\nYour move (0-8): ".encode())
                    move = client_socket.recv(1024).decode().strip()

                    if not move.isdigit() or int(move) not in range(9):
                        client_socket.sendall(b"Invalid input. Try again.\n")
                        continue
                    
                    position = int(move)
                    response = game.make_move(position)
                    board = game.display_board()

                    broadcast_message(f"\nGame Board:\n{board}\n", clients)
                    broadcast_message(response, clients)
                    if game.game_over:
                        broadcast_message("Game Over! Would you like to play again? (yes/no)", clients)
                        print(f"\nFinal Board (Server Side):\n{board}\n")  # Display final board on the server
                        break
                else:
                    client_socket.sendall(b"Waiting for opponent...\n")

            threading.Event().wait(0.5)  

        client_socket.sendall(b"Would you like to play again? (yes/no): ")  # Prompted individual clients
        rematch_response = client_socket.recv(1024).decode().strip().lower()
        if rematch_response == "yes":
            with game_lock:
                if client_id == 0:  # prevent duplicate resets
                    game.reset()
                broadcast_message("Rematch starting...\n", clients)
        else:
            broadcast_message("One of the players declined the rematch. Game over!\n", clients)
    except Exception as e:  
        print(f"Error with client {client_id}: {e}")
    finally:
        client_socket.close()


# Server setup
def start_server(host="127.0.0.1", port=65431):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((host, port))
    server.listen(2)
    print("Server started. Waiting for players to join...")
    game = TicTacToeGame()
    clients = []
    client_id = 0

    try:  # shutdown handling
        while len(clients) < 2:
            client_socket, addr = server.accept()
            print(f"Player {client_id + 1} connected from {addr}")
            clients.append(client_socket)
            threading.Thread(
                target=handle_client,
                args=(client_socket, game, clients, client_id, game_lock),
                daemon=True  # threads to daemon mode for easier cleanup
            ).start()
            client_id += 1
    finally:
        server.close()
        print("Server shutting down...")  # Added shutdown message


if __name__ == "__main__":
    game_lock = threading.Lock()
    start_server()
