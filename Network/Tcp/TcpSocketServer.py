import socket


class TcpSocketServer:

    def __init__(self, bind_port, bind_ip='127.0.0.1'):
        """
        初始化Tcp Socket Server服务
        :param bind_port: 端口信息
        :param bind_ip: 绑定的ip地址
        """
        self.__bind_port = bind_port
        self.__bind_ip = bind_ip
        '''
        socket的几个重要参数理解:
        1. Family: 
            AF_UNIX：面向linux
            AF_INTE：面向网络的
        2. Type:
            SOCK_STREAM：TCP
            SOCK_DGRAM： UDP
        3. Proto
        
        '''
        self.__socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, socket.IPPROTO_TCP)
        self.__socket.bind((self.__bind_ip, self.__bind_port))
        self.__socket.listen(2048)
        self.__connects = {}

    def accept(self):
        """
        接受TCP链接请求
        :return: 实际通信的socket链接
        """
        conn, addr = self.__socket.accept()
        key = str(addr[0]) + str(addr[1])
        self.__connects[key] = conn

        return key

    def send(self, address, message):
        """
        向指定的地址address主机发送消息message
        :param address: 主机地址key
        :param message: 发送的消息内容
        :return:
        """
        conn = self.__connect(address)
        if conn:
            conn.sendall(message.encode())

    def recv(self, address):
        """
        接收指定地址address主机的消息
        :param address: 主机地址
        :return: 收到的消息
        """
        conn = self.__connect(address)
        if conn:
            message = conn.recv(1024)
            return message

    def close(self, address):
        """
        关闭指定地址的socket链接
        :param address: 主机地址
        """
        conn = self.__connect(address)
        if conn:
            conn.close()

    def __connect(self, address):
        """
        获取链接信息
        :param address: 主机地址
        :return: 链接的socket链接
        """
        return self.__connects[address]


if __name__ == '__main__':
    server = TcpSocketServer(10001, '192.168.2.59')
    address_key = server.accept()
    server.send(address_key, 'hello world, you connect to my server, now say bytebyte')
    server.close(address_key)




