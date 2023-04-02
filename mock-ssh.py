import socket
import threading
import os

import paramiko


class SSHServer(paramiko.ServerInterface):
    def __init__(self):
        self.event = threading.Event()

    def check_auth_password(self, username, password):
        print(f"Authenticating {username} with password {password}")
        if username == "test" and password == "password":
            return paramiko.AUTH_SUCCESSFUL
        else:
            return paramiko.AUTH_FAILED

    def check_auth_publickey(self, username, key):
        with open(os.path.expanduser('~/.ssh/authorized_keys')) as f:
            for line in f:
                if key in line:
                    return paramiko.AUTH_SUCCESSFUL
        return paramiko.AUTH_FAILED

    def check_channel_request(self, kind, chanid):
        if kind == "session":
            return paramiko.OPEN_SUCCEEDED
        return paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def add_channel(self, *args, **kwargs):
        pass


def handle_connection(client):
    transport = paramiko.Transport(client)
    transport.add_server_key(paramiko.RSAKey.generate(1024))
    server = SSHServer()
    transport.start_server(server=server)
    channel = transport.accept(20)
    if channel is None:
        print("Failed to create channel")
        transport.close()
        return
    print("Authentication successful")
    while transport.is_active():
        command = input("Enter a command: ")
        if command.strip() == "exit":
            break
        if command.startswith("cat "):
            filename = command.split()[1]
            try:
                with open(filename, "r") as f:
                    data = f.read()
                channel.send(data)
            except FileNotFoundError:
                channel.send(f"No such file or directory: {filename}")
        else:
            channel.exec_command(command)
            exit_status = channel.recv_exit_status()
            print(f"Exit status: {exit_status}")
    channel.close()
    transport.close()


def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind(('localhost', 2222))
    server_socket.listen(5)
    while True:
        client, addr = server_socket.accept()
        threading.Thread(target=handle_connection, args=(client,)).start()


if __name__ == '__main__':
    main()
