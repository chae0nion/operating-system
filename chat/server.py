# -*- coding: utf-8 -*-
import socket
import multiprocessing
import select
import time
import sys

from server_config import HOST, PORT, BACKLOG
from server_utils import handle_client

def main():
    # 자식 → 메인 통신용 큐
    manager = multiprocessing.Manager()
    message_queue = manager.Queue()  # (conn, message) 받는 용도
    close_queue = manager.Queue()    # conn(닫힌 소켓)을 받는 용도

    # 메인 프로세스에서 관리할 소켓 리스트(일반 리스트로 사용)
    client_sockets = []

    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((HOST, PORT))
    server_socket.listen(BACKLOG)

    print(f"[+] Server running: {HOST}:{PORT}")

    # 논블로킹/이벤트 드리븐으로 만드는 경우 select 등을 쓸 수 있음(선택사항)
    server_socket.setblocking(False)

    try:
        while True:
            # 1) 클라이언트 accept (논블로킹)
            try:
                conn, addr = server_socket.accept()
                print(f"[ACCEPT] New Connection: {addr}")
                client_sockets.append(conn)

                p = multiprocessing.Process(
                    target=handle_client,
                    args=(conn, addr, message_queue, close_queue)
                )
                p.daemon = True
                p.start()

            except BlockingIOError:
                # accept()가 블로킹이 아니므로, 연결이 없으면 예외 발생 → 무시
                pass

            # 2) 자식 프로세스가 보낸 메시지(message_queue) 처리
            #    (conn, message)를 받아서 모든 client_sockets에 브로드캐스트
            while not message_queue.empty():
                sender_conn, msg = message_queue.get()
                for cs in client_sockets[:]:
                    try:
                        cs.sendall(msg.encode('utf-8'))
                    except:
                        # 전송 실패 → 제거
                        client_sockets.remove(cs)
                        cs.close()

            # 3) 자식 프로세스가 보낸 소켓 종료(close_queue) 처리
            while not close_queue.empty():
                closed_conn = close_queue.get()
                if closed_conn in client_sockets:
                    client_sockets.remove(closed_conn)
                    closed_conn.close()

            # CPU 점유를 너무 많이 하지 않도록 잠깐 쉼
            time.sleep(0.01)

    except KeyboardInterrupt:
        print("\n[+] Server exit...")

    finally:
        server_socket.close()
        for cs in client_sockets:
            cs.close()
        print("[+] Done.")


if __name__ == "__main__":
    main()
