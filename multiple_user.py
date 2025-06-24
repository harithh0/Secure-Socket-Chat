import socket
import threading
from collections.abc import Buffer
from typing import List

RED = "\033[31m"
GREEN = "\033[32m"
RESET = "\033[0m"


class Client:

    def __init__(self, username, socket):
        self.username = username
        self.socket = socket


class ChatServer:

    def __init__(self, server_ip="localhost", server_port=8888):
        self.server_ip = server_ip
        self.server_port = server_port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.total_users: List[Client] = []

    def bind_n_listen(self):
        self.server_socket.bind((self.server_ip, self.server_port))
        self.server_socket.listen()

    def accept_clients(self):
        while True:
            conn, addr = self.server_socket.accept()
            thread = threading.Thread(target=self.handle_client,
                                      args=(conn, addr),
                                      daemon=True)
            thread.start()

    def handle_client(self, conn, addr):
        with conn:
            print(f"connected from {addr}")
            username = conn.recv(1024)
            if username:
                self.total_users.append({
                    "username": username.decode(),
                    "user_socket": conn
                })
                conn.sendall(b"SERVER:SUCCESS")
            self.send_connection_msg(username.decode(), conn)
            while True:
                data = conn.recv(1024)
                print("data recv:", data.decode())
                if not data:  # if len of data sent is 0 -> means use disconnected
                    print(f"disconnected from {addr}")

                    self.send_connection_msg(conn)

                    self.total_users.remove(conn)
                    break
                if data != " ":
                    self.send_msg_to_all(username.decode(), conn, data)

    def send_msg_to_all(self, user_sending_msg_username,
                        user_sending_conn: socket.socket, msg: bytes):
        for user in self.total_users:
            user_socket = user.get("user_socket")
            if user_socket != user_sending_conn:
                full_message = (
                    f"{RED}{user_sending_msg_username}:{RESET} {msg.decode()}")
                user_socket.sendall(full_message.encode())

    def send_connection_msg(self, username: str,
                            user_sending_conn: socket.socket):
        msg = f"{GREEN}{username} connected from {user_sending_conn.getpeername()[0]} {RESET}\n".encode(
        )
        for user in self.total_users:
            user_socket = user.get("user_socket")
            if user_socket != user_sending_conn:
                user_socket.sendall(msg)


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
