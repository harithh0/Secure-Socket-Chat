import socket

SERVER_PORT = 8888
SERVER_IP = "localhost"


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

    def handle_chatting(self):
        x = input(">\r")
        while True:
            chunk = self.socket.recv(1024)
            if not chunk:  # if chunk is empty
                break
            else:
                print(chunk.decode())


def main():
    username = str(input("Enter your username: "))[:10]  # allow only 10 max
    chat = ChatClient(username)
    connection_result = chat.connect_to_server()
    if connection_result == 1:
        print("yay")
        chat.handle_chatting()


main()
