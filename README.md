# Tic-Tac-Toe Game Example

This is a simple Tic-Tac-Toe game implemented using Python and sockets.

## **How to Play:**

1. **Start the Server:**
   - Run the server on the host machine:
     ```bash
     python server.py -p PORT
     ```

2. **Connect Clients:**
   - On each player’s machine, run the client:
     ```bash
     python client.py -i SERVER_IP -p PORT
     ```

3. **Gameplay:**
   - Players choose a slot (0-8) to place their symbol ('X' or 'O').
   - The first to get three in a row wins.

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
Adding play/rematch capability and overall rework of code.
