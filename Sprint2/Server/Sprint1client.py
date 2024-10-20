import json
import socket
import threading

class TicTacToeClient:
    def __init__(self, player_id):
        self.player_id = player_id
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.connect(('localhost', 12345))
        threading.Thread(target=self.receive_messages).start()
        self.send_join()

    def send_join(self):
        message = {
            "type": "join",
            "data": {
                "player": self.player_id
            }
        }
        self.send_message(message)

    def send_move(self, position):
        message = {
            "type": "move",
            "data": {
                "player": self.player_id,
                "move": position  # Send move as "1A", "2B", etc.
            }
        }
        self.send_message(message)

    def send_chat(self, message_text):
        # Chat message logic (optional)
        pass

    def send_quit(self):
        message = {
            "type": "quit",
            "data": {
                "player": self.player_id
            }
        }
        self.send_message(message)
        self.socket.close()

    def send_message(self, message):
        self.socket.send(json.dumps(message).encode('utf-8'))

    def receive_messages(self):
        while True:
            try:
                msg = self.socket.recv(1024).decode('utf-8')
                if msg:
                    try:
                        msg_data = json.loads(msg)  # Try to parse the JSON
                        if msg_data['type'] == 'board_update':
                            self.display_board(msg_data['data'])
                        else:
                            print(msg)
                    except json.JSONDecodeError:
                        print("Received non-JSON message:", msg)  # Print raw message for debugging
                else:
                    break
            except ConnectionResetError:
                break


    def display_board(self, data):
        board = data['board']
        current_player = data['current_player']
        print("\nCurrent Board:")
        for row in range(3):
            print(f"   {row + 1}   " + " ║ ".join(board[row * 3: row * 3 + 3]))
            if row < 2:
                print("      ═══╬═══╬═══")
        print(f"Next player: {current_player}\n")

if __name__ == "__main__":
    player_id = input("Enter your player ID: ")
    client = TicTacToeClient(player_id)

    while True:
        command = input("Enter move (e.g., '1A') or 'quit': ")
        if command.lower() == 'quit':
            client.send_quit()
            break
        elif len(command) == 2 and command[0] in "123" and command[1].upper() in "ABC":
            client.send_move(command)
        else:
            print("Invalid input. Please use the format '1A', '2B', etc.")
