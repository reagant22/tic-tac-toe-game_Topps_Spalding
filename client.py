import socket
import logging
import time

# config
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

def start_client(server_host='127.0.0.1', server_port=65432):
    """Start the TCP client."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    while True:
        try:
            client_socket.connect((server_host, server_port))
            logging.info(f"Connected to server at {server_host}:{server_port}")
            break  
        except ConnectionRefusedError:
            logging.error("Connection failed. Retrying in 5 seconds...")
            time.sleep(5)  # wait

    try:
        while True:
            message = input("Enter a message (or 'exit' to quit): ")
            if message.lower() == 'exit':
                break
            
            client_socket.send(message.encode('utf-8'))
            response = client_socket.recv(1024).decode('utf-8')
            logging.info(f"Received from server: {response}")
    except Exception as e:
        logging.error(f"Error: {e}")
    finally:
        client_socket.close()
        logging.info("Client disconnected.")

if __name__ == "__main__":
    start_client()
