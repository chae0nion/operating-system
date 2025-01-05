# -*- coding: utf-8 -*-
import socket
import sys
import threading

HOST = '127.0.0.1'
PORT = 5000

def receive_messages(sock):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("[Connection has been lost.]")
                break
            print(data.decode('utf-8'), end="")
        except:
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print(f"[Server {HOST}:{PORT} Connected.]")
    except Exception as e:
        print(f"[-] Server Connected Failed: {e}")
        sys.exit(1)

    thread = threading.Thread(target=receive_messages, args=(client_socket,))
    thread.daemon = True
    thread.start()

    try:
        while True:
            message = sys.stdin.readline()
            if not message:
                break
            client_socket.sendall(message.encode('utf-8'))

            if message.strip().lower() == '/quit':
                break

    except KeyboardInterrupt:
        pass
    finally:
        client_socket.close()
        print("[Client exited]")


if __name__ == "__main__":
    main()
