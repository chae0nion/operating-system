# -*- coding: utf-8 -*-
import socket
import multiprocessing

def handle_client(conn, addr, message_queue, close_queue):
    """
    클라이언트와의 통신을 담당하는 자식 프로세스용 함수.
      - 메시지 수신 → message_queue로 전달
      - 종료 시점에 close_queue로 "소켓 닫힘" 이벤트 전달
    """
    print(f"[+] Added User: {addr}")
    try:
        # 사용자명 요청
        prompt = "nickname: "
        conn.sendall(prompt.encode('utf-8'))
        username = conn.recv(1024).decode('utf-8').strip()

        # 입장 메시지
        welcome_msg = f"\n[Server] {username} Joined.\n"
        message_queue.put((None, welcome_msg))  
        # 큐에는 (소켓, 메시지) 튜플 형태로 보냄
        # 혹은 소켓 없이 메시지만 보내고, 브로드캐스트 시점엔 메인에서 전송

        while True:
            data = conn.recv(1024)
            if not data:
                break

            msg = data.decode('utf-8').strip()
            if msg.lower() == '/quit':
                quit_msg = f"\n[Server] {username} left.\n"
                # 종료 메시지 보내고 루프 종료
                message_queue.put((None, quit_msg))
                break

            # 일반 채팅 메시지
            chat_msg = f"{username}: {msg}\n"
            message_queue.put((conn, chat_msg))

    except Exception as e:
        print(f"[-] Error({addr}): {e}")
    finally:
        conn.close()
        # 메인 프로세스에게 "이 소켓이 닫혔다"고 알림
        close_queue.put(conn)
        print(f"[-] socket closed: {addr}")
