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
            if (self.board[combo[0]] == self.board[combo[1]] ==
                    self.board[combo[2]] != " "):
                return True
        return False


def broadcast_message(message, clients):
    """Send a message to all connected clients."""
    for client in clients:
        try:
            client.sendall(message.encode() + b"\n")
        except:
            pass  # Ignore errors for disconnected clients


def handle_client(client_socket, game, clients, client_id, game_lock):
    try:
        if client_id == 0:
            client_socket.sendall(b"Welcome to Tic Tac Toe! You are Player X.\n")
        else:
            client_socket.sendall(b"You are Player O.\n")

        while not game.game_over:
            with game_lock:
                # Send board state and prompt for move only if it's the player's turn
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
                    if "wins" in response or "draw" in response:
                        broadcast_message("Game Over!", clients)
                        print(f"\nFinal Board (Server Side):\n{board}\n")  # Display final board on the server
                        break
                else:
                    client_socket.sendall(b"Waiting for opponent...\n")
            # Prevent spamming: add a small delay to avoid fast re-checking in case the opponent has not moved yet
            threading.Event().wait(1)

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

    while len(clients) < 2:
        client_socket, addr = server.accept()
        print(f"Player {client_id + 1} connected from {addr}")
        clients.append(client_socket)
        threading.Thread(target=handle_client, args=(client_socket, game, clients, client_id, game_lock)).start()
        client_id += 1

    server.close()


if __name__ == "__main__":
    game_lock = threading.Lock()
    start_server()
