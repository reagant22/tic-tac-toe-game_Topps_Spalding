import socket
import threading
import logging
import signal
import sys

# config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def handle_client(client_socket):
    """Function to handle client connections."""
    try:
        while True:
            message = client_socket.recv(1024).decode('utf-8')
            if not message:
                break
            logging.info(f"Received message: {message}")
            client_socket.send(f"Echo: {message}".encode('utf-8'))
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        logging.info("Client disconnected.")
        client_socket.close()

def start_server(host='127.0.0.1', port=65432):
    """Start the TCP server."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port))
    server_socket.listen(5)
    logging.info(f"Server listening on {host}:{port}")

    try:
        while True:
            client_socket, addr = server_socket.accept()
            logging.info(f"Connection from {addr} established.")
            client_handler = threading.Thread(target=handle_client, args=(client_socket,))
            client_handler.start()
    except KeyboardInterrupt:
        logging.info("Server shutting down.")
    finally:
        server_socket.close()

def signal_handler(sig,frame):
    sys.exit(0)

if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal_handler)
    start_server()
