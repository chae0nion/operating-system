import socket
import threading
import time
from server_utils import handle_client

HOST = '127.0.0.1'
PORT = 5000



def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(5)
    print(f"[INFO] Server running on {HOST}:{PORT}")

    try:
        while True:
            conn, addr = server_socket.accept()
            print(f"[INFO] New connection: {addr}")
            start_time = time.time()
            threading.Thread(target=handle_client, args=(conn, addr)).start()
            
            end_time = time.time()
            print(f"[INFO] Thread for {addr} started in {end_time - start_time: .4f} seconds")

    except KeyboardInterrupt:
        print("[INFO] Server shutting down...")
    finally:
        server_socket.close()

if __name__ == "__main__":
    main()