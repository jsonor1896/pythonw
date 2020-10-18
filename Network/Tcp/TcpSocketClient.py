import socket


class TcpSocketClient:

    def __init__(self, dst_ip, dst_port):
        """
        构造一个tcp socket的客户端
        :param dst_ip: 目的地ip地址
        :param dst_port: 目的地端口号
        """
        self.__dst_ip = dst_ip
        self.__dst_port = dst_port
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)

    def connect(self):
        """
        连接到服务器
        """
        self.__socket.connect((self.__dst_ip, self.__dst_port))

    def send(self, message:str):
        """
        向服务器发送特定消息
        :param message: 特定的字符消息
        """
        self.__socket.sendall(message.encode())

    def recv(self):
        """
        接收数据
        :return: 消息信息
        """
        message = self.__socket.recv(1024)
        return message

    def close(self):
        self.__socket.close()


if __name__ == '__main__':
    client = TcpSocketClient('192.168.2.59', 10001)
    client.connect()
    message = client.recv()
    print('recv message ', message)






