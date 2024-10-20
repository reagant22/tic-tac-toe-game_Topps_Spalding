import json
import socket
import threading

class TicTacToe:
    def __init__(self):
        # Initialize the grid with blank spaces
        self.symbol_list = [" "] * 9
        self.current_player = 'X'  # Player X starts

    def restart(self):
        # Clear the grid for a new game
        self.symbol_list = [" "] * 9
        self.current_player = 'X'  # Reset to player X

    def draw_grid(self):
        print("\n       A   B   C\n")
        for row in range(3):
            row_string = f"   {row + 1}   " + " ║ ".join(self.symbol_list[row * 3: row * 3 + 3])
            print(row_string)
            if row < 2:
                print("      ═══╬═══╬═══")
        print("\n")

    def edit_square(self, grid_coord):
        # Convert coordinates such as "1A" to "A1"
        if grid_coord[0].isdigit():
            grid_coord = grid_coord[1] + grid_coord[0]

        col = grid_coord[0].upper()
        row = int(grid_coord[1]) - 1

        # Convert "A1" to index
        grid_index = (row * 3) + (ord(col) - ord('A'))

        # Check if the square is empty
        if self.symbol_list[grid_index] == " ":
            self.symbol_list[grid_index] = self.current_player
            return True
        return False

    def did_win(self, player_symbol):
        winning_combinations = [
            [0, 1, 2],  # Top row
            [3, 4, 5],  # Middle row
            [6, 7, 8],  # Bottom row
            [0, 3, 6],  # Left column
            [1, 4, 7],  # Middle column
            [2, 5, 8],  # Right column
            [0, 4, 8],  # Diagonal top-left to bottom-right
            [2, 4, 6]   # Diagonal top-right to bottom-left
        ]

        for combo in winning_combinations:
            if all(self.symbol_list[i] == player_symbol for i in combo):
                return True
        return False

    def is_draw(self):
        return " " not in self.symbol_list and not self.did_win('X') and not self.did_win('O')

    def switch_player(self):
        self.current_player = 'O' if self.current_player == 'X' else 'X'

class TicTacToeServer:
    def __init__(self):
        self.clients = {}
        self.game = TicTacToe()
    
    def handle_client(self, client_socket, addr):
        print(f"Connection from {addr} has been established!")
        player_id = None

        while True:
            try:
                msg = client_socket.recv(1024).decode('utf-8')
                if not msg:
                    break
                self.process_message(json.loads(msg), client_socket)
            except ConnectionResetError:
                break

        if player_id:
            del self.clients[player_id]
        client_socket.close()

    def process_message(self, message, client_socket):
        msg_type = message['type']
        if msg_type == 'join':
            self.handle_join(message['data'], client_socket)
        elif msg_type == 'move':
            self.handle_move(message['data'], client_socket)
        elif msg_type == 'chat':
            self.handle_chat(message['data'])
        elif msg_type == 'quit':
            self.handle_quit(message['data'])

    def handle_join(self, data, client_socket):
        player_id = data['player']
        self.clients[player_id] = client_socket
        print(f"{player_id} joined the game.")
        self.broadcast(f"{player_id} has joined the game.")
    
    def handle_move(self, data, client_socket):
        player_id = data['player']
        move = data['move']
        
        if self.game.edit_square(move):
            if self.game.did_win(self.game.current_player):
                self.broadcast(f"{player_id} wins!")
                self.broadcast(self.get_board_state())
                self.game.restart()  # Reset for next game
            elif self.game.is_draw():
                self.broadcast("It's a draw!")
                self.broadcast(self.get_board_state())
                self.game.restart()  # Reset for next game
            else:
                self.game.switch_player()
                self.broadcast(self.get_board_state())
        else:
            client_socket.send(json.dumps({"error": "Invalid move!"}).encode('utf-8'))

    def get_board_state(self):
        return {
            "type": "board_update",
            "data": {
                "board": self.game.symbol_list,
                "current_player": self.game.current_player
            }
        }

    def handle_chat(self, data):
        # Chat handling logic (optional)
        pass

    def handle_quit(self, data):
        player_id = data['player']
        if player_id in self.clients:
            del self.clients[player_id]
        self.broadcast(f"{player_id} has left the game.")

    def broadcast(self, msg):
        for client in self.clients.values():
            client.send(json.dumps(msg).encode('utf-8'))

    def start(self):
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.bind(('localhost', 12345))
        server_socket.listen(5)
        print("Server started, waiting for clients...")

        while True:
            client_socket, addr = server_socket.accept()
            threading.Thread(target=self.handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    server = TicTacToeServer()
    server.start()
