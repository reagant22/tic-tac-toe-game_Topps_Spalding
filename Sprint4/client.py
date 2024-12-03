import socket
import sys
import threading

class TicTacToeClient:
    def __init__(self, server_ip, server_port):
        self.server_ip = server_ip
        self.server_port = server_port
        self.client_socket = None
        self.username = None

    def connect_to_server(self):
        """Connects to the Tic-Tac-Toe server."""
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.client_socket.connect((self.server_ip, self.server_port))
            print("Connected to the server!")
        except Exception as e:
            print(f"Failed to connect to server: {e}")
            sys.exit(1)

    def handle_server_messages(self):
        """Handles messages from the server (such as game board and instructions)."""
        while True:
            try:
                data = self.client_socket.recv(1024).decode()
                if not data:
                    print("Disconnected from server.")
                    break
                print(data.strip())  # Print messages from the server properly formatted
            except ConnectionError:
                print("Connection lost.")
                break

    def prompt_for_move(self):
        """Prompts the player for their move and sends it to the server."""
        while True:
            move = input("Your move (0-8) or chat: ")
            if move.lower() == "exit":
                self.client_socket.sendall("exit".encode())
                print("Exiting game.")
                break
            try:
                move = int(move)
                if move < 0 or move > 8:
                    print("Invalid input. Please enter a number between 0 and 8.")
                else:
                    self.client_socket.sendall(str(move).encode())
            except ValueError:
                # If the user inputs a string that's not a valid number, treat it as a chat message
                self.client_socket.sendall(f"chat: {move}".encode())

    def run(self):
        """Main method to run the client."""
        self.connect_to_server()
        
        # Start a thread to listen to the server messages
        server_thread = threading.Thread(target=self.handle_server_messages)
        server_thread.daemon = True
        server_thread.start()

        # Now, prompt the user for their move or chat
        self.prompt_for_move()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 client.py <server_ip> <server_port>")
        sys.exit(1)

    server_ip = sys.argv[1]
    server_port = int(sys.argv[2])

    client = TicTacToeClient(server_ip, server_port)
    client.run()
