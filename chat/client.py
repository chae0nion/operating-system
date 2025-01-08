import socket
import threading
import sys

HOST = '127.0.0.1'
PORT = 5000

def receive_messages(sock):
    """Continuosly receive message from the server"""
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("[DISCONNECTED] Connection to server lost.")
                break
            # Remove debug message and display clean message
            print(data.decode('utf-8').strip())
        except Exception as e:
            print(f"[ERROR] Failed to receive message: {e}")
            break

def main():
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        client_socket.connect((HOST, PORT))
        print(f"[CONNECTED] Connected to {HOST}:{PORT}")

        nickname = input("Enter your nickname: ").strip() # Enter nickname
        if not nickname:
            print("[ERROR] Nickname cannot be empty.")
            client_socket.close()
            return
        client_socket.sendall(nickname.encode('utf-8'))  # Send nickname to server
        
        group_name = input("Enter group name: ").strip()
        if not group_name:
            print("[ERROR] Group name cannot be empty.")
            client_socket.close()
            return
        client_socket.sendall(group_name.encode('utf-8'))

        # Start threading to receive message
        thread = threading.Thread(target=receive_messages, args=(client_socket,))
        thread.daemon = True
        thread.start()

        # Input message and send loop
        while True:
            try:
                message = input().strip()
                if not message:
                    continue
                if message.lower() == '/quit':
                    print("[EXITING] Exiting group chat...")
                    break
                client_socket.sendall(message.encode('utf-8'))
            except Exception as e:
                print(f"[ERROR] Failed to send message: {e}")
                break

    except ConnectionRefusedError:
        print("[ERROR] Could not connect to the server. Please ensure the server is running.")
    except KeyboardInterrupt:
        print("\n[EXITING] Client shutting down.")
    finally:
        client_socket.close()
        print("[DISCONNECTED] Connection closed.")

if __name__ == "__main__":
    main()
