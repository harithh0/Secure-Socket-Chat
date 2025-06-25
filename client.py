import socket
import ssl
import threading
import time

from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.patch_stdout import patch_stdout

SERVER_PORT = 8888
SERVER_IP = "localhost"

session = PromptSession()


class ChatClient:

    def __init__(self, username, server_ip=SERVER_IP, server_port=SERVER_PORT):
        self.username = username
        self.server_ip = server_ip
        self.server_port = server_port
        self.context = ssl.create_default_context()

        # WARN: for self signed certs only:
        self.context.check_hostname = False
        self.context.verify_mode = ssl.CERT_NONE

        # TODO: make sure to add 'server_hostname' from the FQDN when creating cert
        self.socket = self.context.wrap_socket(
            socket.socket(socket.AF_INET, socket.SOCK_STREAM))

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
            elif chunk.decode() == "SERVER:CLOSE":
                self.socket.close()
                print("server closed exitting...")
                exit()
            else:
                with patch_stdout():
                    # prints with supporting ANSI (color) from server
                    print_formatted_text(ANSI(f"{chunk.decode()}"))

    def handle_chatting(self):
        threading.Thread(target=self.__listen_for_messages,
                         daemon=True).start()
        while True:
            user_input = session.prompt("> ")
            try:
                self.socket.sendall(user_input.encode())
            except Exception:
                print("something went wrong sending message to server")
                exit()


def main():
    username = str(input("Enter your username: "))[:10]  # allow only 10 max
    chat = ChatClient(username)
    connection_result = chat.connect_to_server()
    if connection_result == 1:
        print("Successfuly connected")
        chat.handle_chatting()
    else:
        print("Unable to connect")
        return


main()
