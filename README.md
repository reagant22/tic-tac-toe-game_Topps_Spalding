# Tic-Tac-Toe Game Example

This is a simple Tic-Tac-Toe game implemented using Python and sockets.

## **How to Play:**

1. **Start the Server:**
   - Run the server on the host machine:
     ```bash
     python server.py -p PORT
     ```
     - Replace PORT with the desired port number (e.g., 12345).

2. **Connect Clients:**
   - On each player’s machine, run the client:
     ```bash
     python client.py SERVER_IP PORT
     ```
     - Replace SERVER_IP with the server's IP address.
     - Replace PORT with the same port number used to start the server.

3. **Gameplay:**
   - Players alternate turns selecting a position on the board (0-8) to place their symbol (X or O).
   - The first player to align three symbols in a row (horizontally, vertically, or diagonally) wins!
   - If all slots are filled without a winner, the game ends in a draw.

4. **Exit:**
   - Type `exit` to end the game.

**Technologies used:**
* Python
* Sockets
* *threads/locks

**Additional resources:**
* [Link to Python documentation]
* [Link to sockets tutorial]


**Sprint One
Implementing Client and server services.

Start server by running python/python3 server.py then run python/python3 client.py the test case for this will auto generate a response for you if you want to use that.

**Sprint Four
- Introduced the ability for players to play multiple games without restarting the server.
- Refactored the codebase for improved readability and maintainability.
- Enhanced error handling and logging.
