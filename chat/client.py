# -*- coding: utf-8 -*-
import socket
import sys
import threading

HOST = '127.0.0.1'
PORT = 5000

def receive_messages(sock, ready):
    while True:
        try:
            data = sock.recv(1024)
            if not data:
                print("[Connection has been lost.]")
                break
            elif data != "" and ready[0]:
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

    ready = [False]
    thread = threading.Thread(target=receive_messages, args=(client_socket, ready))
    thread.daemon = True
    thread.start()

    server_prompt = client_socket.recv(1024).decode('utf-8')  # 닉네임 요청 메시지 수신
    print(server_prompt, end="")  # 요청 메시지 출력
    nickname = input().strip()  # 닉네임 입력
    client_socket.sendall(nickname.encode('utf-8'))  # 닉네임 서버로 전송

    ready[0] = True

    try:
        while True:
            message = sys.stdin.readline()
            if not message:
                break
            if message.strip() == "":
                continue
            else:
                print("[You]: ", end="") 
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
