import unittest
import socket
import threading
import time
import logging
import sys

# Assuming the server code is in a file named 'server.py'
from server import start_server

class TestServer(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Start the server in a separate thread before running the tests."""
        cls.server_thread = threading.Thread(target=start_server, args=('127.0.0.1', 65432))
        cls.server_thread.daemon = True  # Ensure thread exits when the main program exits
        cls.server_thread.start()
        time.sleep(1)  # Give the server a second to start

    def test_message_echo(self):
        """Test if the server echoes messages correctly."""
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client_socket:
            client_socket.connect(('127.0.0.1', 65432))
            test_message = "Hello, Server!"
            client_socket.send(test_message.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            self.assertEqual(response, f"Echo: {test_message}")

    @classmethod
    def tearDownClass(cls):
        """Shut down the server after running the tests."""
        # Note: You would need to implement a clean shutdown mechanism in your server code.
        # Here we can simulate a shutdown by exiting the server thread
        # This method doesn't stop the server gracefully. Consider adding a shutdown signal to your server for real tests.
        # For testing purposes, we can just exit the process
        logging.info("Shutting down the server thread.")
        sys.exit(0)

if __name__ == '__main__':
    unittest.main()
