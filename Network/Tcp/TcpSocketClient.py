import socket


class TcpSocketClient:

    def __init__(self, dst_ip, dst_port):
        self.__dst_ip = dst_ip
        self.__dst_port = dst_port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    def connect(self):
        self.__socket.connect((self.__dst_ip, self.__dst_port))

    def send(self, message:str):
        self.__socket.sendall(message.encode())

    def recv(self):
        message = self.__socket.recv(1024)
        return message

    def close(self):
        self.__socket.close()


if __name__ == '__main__':
    client = TcpSocketClient('192.168.2.59', 10001)
    client.connect()
    message = client.recv()
    print('recv message ', message)






