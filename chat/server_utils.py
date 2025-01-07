import time
import socket

groups = {}


def handle_client(conn, addr):
    """클라이언트 연결 처리"""
    group_name = None

    try:
        conn.sendall("Enter group name: ".encode('utf-8'))
        group_name = conn.recv(1024).decode('utf-8').strip()

        # 그룹 이름 확인
        if not group_name:
            conn.sendall("[ERROR] Group name cannot be empty. Disconnecting...\n".encode('utf-8'))
            conn.close()
            return

        # 그룹에 추가
        if group_name not in groups:
            groups[group_name] = []
        groups[group_name].append(conn)
        print(f"[INFO] {addr} joined group '{group_name}'. Members: {groups[group_name]}")

        conn.sendall(f"[Server] Joined group: {group_name}\n".encode('utf-8'))

        # 메시지 처리 루프
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode('utf-8').strip()
            if message.lower() == '/quit':
                print(f"[INFO] {addr} left group '{group_name}'")
                break

            # 메시지 브로드캐스트
            broadcast_message(group_name, f"{addr}: {message}", conn)

    except Exception as e:
        print(f"[ERROR] {addr}: {e}")
    finally:
        # 그룹에서 제거
        if group_name and group_name in groups:
            groups[group_name].remove(conn)
            if not groups[group_name]:  # 그룹이 비어 있으면 삭제
                del groups[group_name]
        conn.close()
        print(f"[INFO] Connection closed: {addr}")


def broadcast_message(group_name, message, sender_conn):
    """그룹 내 메시지 브로드캐스트"""
    if group_name in groups:
        start_time = time.time()  # 브로드캐스트 시작 시간
        for client in groups[group_name]:
            if client != sender_conn:
                try:
                    client.sendall(f"{message}\n".encode('utf-8'))
                except Exception as e:
                    print(f"[ERROR] Failed to send message: {e}")
                    groups[group_name].remove(client)
        end_time = time.time()  # 브로드캐스트 완료 시간
        print(f"[INFO] Broadcasted message to group '{group_name}' in {end_time - start_time:.4f} seconds")
