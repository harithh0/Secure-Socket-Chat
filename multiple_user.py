import socket
import threading
from collections.abc import Buffer
from typing import List

HOST = "localhost"
PORT = 8888

total_users: List[dict[str, socket.socket]] = []
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"


def send_msg_to_all(user_sending_msg_username,
                    user_sending_conn: socket.socket, msg: bytes):
    for user in total_users:
        user_socket = user.get("user_socket")
        if user_socket != user_sending_conn:
            full_message = f"{RED}{user_sending_msg_username}:{RESET} {msg.decode()}"
            user_socket.sendall(full_message.encode())


def send_connection_msg(username: str, user_sending_conn: socket.socket):
    msg = f"{GREEN}{username} connected from {user_sending_conn.getpeername()[0]} {RESET}\n".encode(
    )
    for user in total_users:
        user_socket = user.get("user_socket")
        if user_socket != user_sending_conn:
            user_socket.sendall(msg)


def handle_client(conn, addr):
    with conn:
        print(f"connected from {addr}")

        username = conn.recv(1024)
        if username:
            total_users.append({
                "username": username.decode(),
                "user_socket": conn
            })
            conn.sendall(b"SERVER:SUCCESS")
        send_connection_msg(username.decode(), conn)
        while True:
            data = conn.recv(1024)
            print("data recv:", data.decode())
            if not data:  # if len of data sent is 0 -> means use disconnected
                print(f"disconnected from {addr}")

                send_connection_msg(
                    conn, f"{RED}{addr[0]} disconnected{RESET}\n".encode())

                total_users.remove(conn)
                break
            if data != " ":
                send_msg_to_all(username.decode(), conn, data)


with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen()
    # while True:
    while True:
        conn, addr = s.accept()
        print(total_users)
        thread = threading.Thread(target=handle_client,
                                  args=(conn, addr),
                                  daemon=True)
        thread.start()
