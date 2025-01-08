import time
import socket
from datetime import datetime

groups = {}
nicknames = {}

def handle_client(conn, addr):
    """Handle client connection"""
    group_name = None

    try:
        conn.sendall("Enter your nickname: ".encode('utf-8')) # Enter nickname
        nickname = conn.recv(1024).decode('utf-8').strip()
        if not nickname:
            conn.sendall("[ERROR] Nickname cannot be empty. Disconnecting...\n".encode('utf-8'))
            conn.close()
            return
        nicknames[conn] = nickname
        
        conn.sendall("Enter group name: ".encode('utf-8'))
        group_name = conn.recv(1024).decode('utf-8').strip()

        # Check group name
        if not group_name:
            conn.sendall("[ERROR] Group name cannot be empty. Disconnecting...\n".encode('utf-8'))
            conn.close()
            return

        # Add to group
        if group_name not in groups:
            groups[group_name] = []
        groups[group_name].append(conn)
        print(f"[INFO] {addr} joined group '{group_name}'. Members: {groups[group_name]}")

        conn.sendall(f"\n[Server] Welcome, {nickname}! You have Joined group: {group_name}\n".encode('utf-8'))

        # Message handling loop
        while True:
            data = conn.recv(1024)
            if not data:
                break

            message = data.decode('utf-8').strip()
            if message.lower() == '/quit':
                print(f"[INFO] {addr} ({nickname}) left group '{group_name}'")
                quit_msg = f"[{get_time()}] [Server] {nickname} has left the group.\n"
                broadcast_message(group_name, quit_msg, conn)
                break

            # Broadcast message
            chat_msg = f"[{get_time()}] {nickname}: {message}\n"
            broadcast_message(group_name, chat_msg, conn)

    except Exception as e:
        print(f"[ERROR] {addr} ({nickname}): {e}")
    finally:
        # Clean up
        if group_name and group_name in groups:
            groups[group_name].remove(conn)
            if not groups[group_name]:  # Delete group if empty
                del groups[group_name]
        conn.close()
        print(f"[INFO] Connection closed: {addr} ({nickname})")


def broadcast_message(group_name, message, sender_conn):
    """Broadcast message within a group"""
    if group_name in groups:
        start_time = time.time()  # Broadcast start time
        for client in groups[group_name]:
            if client != sender_conn:
                try:
                    client.sendall(f"{message}\n".encode('utf-8'))
                except Exception as e:
                    print(f"[ERROR] Failed to send message: {e}")
                    groups[group_name].remove(client)
        end_time = time.time()  # Broadcast end time
        print(f"[INFO] Broadcasted message to group '{group_name}' in {end_time - start_time:.4f} seconds")

def get_time():
    """Get current time as a formatted string"""
    return datetime.now().strftime('%m-%d %H:%M')
