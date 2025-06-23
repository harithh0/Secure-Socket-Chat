import socket

SERVER_PORT = 8888
SERVER_IP = "localhost"


class ChatClient:

    def __init__(self, server_ip=SERVER_IP, server_port=SERVER_PORT):
        self.server_ip = server_ip
        self.server_port = server_port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect_to_server(self):
        self.socket.connect((self.server_ip, self.server_port))
        self.socket.sendall(b"hey")


def main():
    chat = ChatClient()
    chat.connect_to_server()


main()
