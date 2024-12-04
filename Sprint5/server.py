import socket
import threading
import logging

logging.basicConfig(level=logging.DEBUG)

class TicTacToe:
    def __init__(self):
        self.board = [' '] * 9
        self.current_player = 'X'
        self.winner = None

    def render_board(self):
        return f"""
         {self.board[0]} | {self.board[1]} | {self.board[2]}
        ---|---|---
         {self.board[3]} | {self.board[4]} | {self.board[5]}
        ---|---|---
         {self.board[6]} | {self.board[7]} | {self.board[8]}
        """

    def make_move(self, position):
        if self.board[position] == ' ':
            self.board[position] = self.current_player
            if self.check_winner():
                self.winner = self.current_player
            else:
                self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        return False

    def check_winner(self):
        winning_combinations = [
            (0, 1, 2), (3, 4, 5), (6, 7, 8),
            (0, 3, 6), (1, 4, 7), (2, 5, 8),
            (0, 4, 8), (2, 4, 6),
        ]
        for combo in winning_combinations:
            if self.board[combo[0]] == self.board[combo[1]] == self.board[combo[2]] != ' ':
                return True
        return False

    def is_draw(self):
        return ' ' not in self.board and self.winner is None


def broadcast_message(message, clients):
    for client in clients:
        try:
            client.sendall(message.encode())
        except:
            pass


def handle_client(client_socket, client_id, game, clients, game_lock):
    try:
        client_socket.sendall(f"Welcome Player {client_id + 1} ({game.current_player})!\n".encode())
        client_socket.sendall(game.render_board().encode())

        while True:
            client_socket.sendall("Your move (0-8): ".encode())
            position = client_socket.recv(1024).decode().strip()

            if not position:
                break

            try:
                position = int(position)
                if position < 0 or position > 8:
                    client_socket.sendall("Invalid position. Try again.\n".encode())
                    continue

                with game_lock:
                    if game.make_move(position):
                        broadcast_message(game.render_board(), clients)
                        if game.winner:
                            broadcast_message(f"Player {client_id + 1} ({game.current_player}) wins!\n", clients)
                            break
                        elif game.is_draw():
                            broadcast_message("The game is a draw!\n", clients)
                            break
                    else:
                        client_socket.sendall("Position already taken. Try again.\n".encode())
            except ValueError:
                client_socket.sendall("Invalid input. Enter a number between 0-8.\n".encode())
    except (ConnectionResetError, BrokenPipeError):
        logging.debug(f"Player {client_id + 1} disconnected.")
    finally:
        with game_lock:
            clients.remove(client_socket)
        client_socket.close()

        if len(clients) < 2:
            broadcast_message("The other player has disconnected. Game ending.\n", clients)


def start_server(port):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind(("0.0.0.0", port))
    server.listen(2)

    logging.debug(f"Server started on port {port}. Waiting for players...")

    game = TicTacToe()
    clients = []
    game_lock = threading.Lock()

    try:
        while len(clients) < 2:
            client_socket, addr = server.accept()
            logging.debug(f"Player connected from {addr}")
            clients.append(client_socket)

            client_id = len(clients) - 1
            threading.Thread(target=handle_client, args=(client_socket, client_id, game, clients, game_lock)).start()

        logging.debug("Both players connected. Game starting!")
    except KeyboardInterrupt:
        logging.debug("Server shutting down.")
    finally:
        server.close()


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Tic Tac Toe Server")
    parser.add_argument("-p", "--port", type=int, required=True, help="Port to run the server on")
    args = parser.parse_args()

    start_server(args.port)
