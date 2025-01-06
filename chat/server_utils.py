import socket

def add_to_group(group_name, conn, groups):
    if group_name not in groups:
        groups[group_name] = []
    if conn not in groups[group_name]:
        groups[group_name].append(conn)

def remove_from_group(group_name, conn, groups):
    if group_name in groups:
        groups[group_name].remove(conn)
        if not groups[group_name]:  # 그룹이 비어 있으면 제거
            del groups[group_name]

