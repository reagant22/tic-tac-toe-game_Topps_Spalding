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
        
        # Display the rows with current symbols
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
        # Winning combinations
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

    def play_game(self):
        while True:
            self.draw_grid()
            print(f"Player {self.current_player}, enter your move (e.g., '1A' for row 1, column A):")
            move = input().strip()

            if len(move) != 2 or move[0] not in "123" or move[1].upper() not in "ABC":
                print("Invalid move. Please enter a valid coordinate (e.g., '1A').")
                continue

            if not self.edit_square(move):
                print("That square is already taken. Try again.")
                continue

            if self.did_win(self.current_player):
                self.draw_grid()
                print(f"Player {self.current_player} wins!")
                break

            if self.is_draw():
                self.draw_grid()
                print("It's a draw!")
                break

            self.switch_player()

# Example usage
if __name__ == "__main__":
    game = TicTacToe()
    game.play_game()
