import socket
import threading
import time

from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.patch_stdout import patch_stdout

SERVER_PORT = 8888
SERVER_IP = "localhost"

session = PromptSession()

# def typing_watcher(session):
#     was_typing = False
#     while True:
#         time.sleep(0.1)
#         is_typing = bool(session.default_buffer.text)
#         if is_typing and not was_typing:
#             print("[Typing started]")
#         elif not is_typing and was_typing:
#             print("[Typing stopped]")
#         was_typing = is_typing
#
#
# threading.Thread(target=typing_watcher, args=(session, ), daemon=True).start()


class ChatClient:

    def __init__(self, username, server_ip=SERVER_IP, server_port=SERVER_PORT):
        self.username = username
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        try:
            self.socket.connect((self.server_ip, self.server_port))
        except Exception as e:
            print("cannot connect", str(e))
            return None
        self.socket.sendall(self.username.encode())

        print("Waiting for server...")
        x = self.socket.recv(1024)
        if x.decode() == "SERVER:SUCCESS":
            return 1

    def __listen_for_messages(self):
        while True:
            chunk = self.socket.recv(1024)
            if not chunk:  # if chunk is empty
                break
            else:
                with patch_stdout():
                    # prints with supporting ANSI (color) from server
                    print_formatted_text(ANSI(f"{chunk.decode()}"))

    def handle_chatting(self):
        threading.Thread(target=self.__listen_for_messages,
                         daemon=True).start()
        while True:
            user_input = session.prompt("> ")
            self.socket.sendall(user_input.encode())


def main():
    username = str(input("Enter your username: "))[:10]  # allow only 10 max
    chat = ChatClient(username)
    connection_result = chat.connect_to_server()
    if connection_result == 1:
        print("yay")
        chat.handle_chatting()


main()
