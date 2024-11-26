import socket
import threading
import argparse

class TicTacToeGame:
    def __init__(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.winner = None

    def make_move(self, position):
        if self.board[position] == " ":
            self.board[position] = self.current_player
            if self.check_winner():
                self.winner = self.current_player
                return True
            self.current_player = "O" if self.current_player == "X" else "X"
            return True
        return False

    def check_winner(self):
        win_positions = [
            [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Rows
            [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Columns
            [0, 4, 8], [2, 4, 6]              # Diagonals
        ]
        for pos in win_positions:
            if self.board[pos[0]] == self.board[pos[1]] == self.board[pos[2]] != " ":
                return True
        return False

    def is_draw(self):
        return all(cell != " " for cell in self.board) and self.winner is None

    def reset(self):
        self.board = [" "] * 9
        self.current_player = "X"
        self.winner = None

    def render_board(self):
        return (
            f"\n {self.board[0]} | {self.board[1]} | {self.board[2]} \n"
            f"---+---+---\n"
            f" {self.board[3]} | {self.board[4]} | {self.board[5]} \n"
            f"---+---+---\n"
            f" {self.board[6]} | {self.board[7]} | {self.board[8]} \n"
        )


def broadcast_message(message, clients):
    """Send a message to all connected clients."""
    for client in clients:
        try:
            client.sendall(message.encode())
        except Exception:
            continue


def handle_client(client_socket, client_id, game, clients, game_lock):
    """Handle communication with a single client."""
    try:
        client_socket.sendall(f"You are Player {client_id + 1} ({'X' if client_id == 0 else 'O'}).\n".encode())
        if len(clients) < 2:
            client_socket.sendall("Waiting for another player to join...\n".encode())

        while len(clients) < 2:
            pass  # Wait until both players have joined

        broadcast_message("Both players are connected. Let's start the game!", clients)
        broadcast_message(game.render_board(), clients)

        while True:
            if game.winner or game.is_draw():
                if game.winner:
                    broadcast_message(f"Player {1 if game.current_player == 'X' else 2} ({game.current_player}) wins!", clients)
                elif game.is_draw():
                    broadcast_message("The game is a draw!", clients)
                game.reset()
                broadcast_message("Game reset. Starting a new round.\n", clients)
                broadcast_message(game.render_board(), clients)

            if client_id == (0 if game.current_player == "X" else 1):
                client_socket.sendall("Your turn. Enter a position (0-8): ".encode())
                position = client_socket.recv(1024).decode().strip()
                if position.lower() == "exit":
                    broadcast_message(f"Player {client_id + 1} has left the game. Ending session.", clients)
                    break
                try:
                    position = int(position)
                    if position < 0 or position > 8:
                        client_socket.sendall("Invalid position. Please choose between 0-8.\n".encode())
                        continue

                    with game_lock:
                        if game.make_move(position):
                            broadcast_message(game.render_board(), clients)
                        else:
                            client_socket.sendall("Position already taken. Try again.\n".encode())
                except ValueError:
                    client_socket.sendall("Invalid input. Please enter a number between 0-8.\n".encode())
            else:
                client_socket.sendall("Waiting for the other player's move...\n".encode())
    except Exception as e:
        print(f"Error with client {client_id + 1}: {e}")
    finally:
        client_socket.close()
        clients.remove(client_socket)
        print(f"Player {client_id + 1} disconnected.")


def start_server(port):
    """Start the Tic Tac Toe server."""
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(2)
    print(f"Server started on 0.0.0.0:{port}. Waiting for players to join...")

    game = TicTacToeGame()
    clients = []
    game_lock = threading.Lock()

    try:
        while True:
            client_socket, addr = server.accept()
            print(f"New connection from {addr}")
            clients.append(client_socket)
    