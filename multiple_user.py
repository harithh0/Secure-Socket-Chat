import socket
import threading
from collections.abc import Buffer
from typing import List

HOST = "localhost"
PORT = 8888

total_users: List[socket.socket] = []
RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"


def send_msg_to_all(user_sending_conn: socket.socket, msg: bytes):
    for user in total_users:
        if user != user_sending_conn:
            full_message = f"{RED}{user.getpeername()[0]}:{RESET} {msg.decode()}"
            user.sendall(full_message.encode())


def send_connection_msg(user_sending_conn: socket.socket, msg: bytes):
    for user in total_users:
        if user != user_sending_conn:
            user.sendall(msg)


def handle_client(conn, addr):
    print("total users", total_users)
    with conn:
        print(f"connected from {addr}")
        send_connection_msg(conn,
                            f"{GREEN}{addr[0]} connected{RESET}\n".encode())
        total_users.append(conn)
        while True:
            data = conn.recv(1024)
            if not data:  # if len of data sent is 0 -> means use disconnected
                print(f"disconnected from {addr}")

                send_connection_msg(
                    conn, f"{RED}{addr[0]} disconnected{RESET}\n".encode())

                total_users.remove(conn)
                break
            if data != " ":
                send_msg_to_all(conn, data)


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
