from Network.Tcp import TcpSocketClient


class FtpRaw:
    """
    使用socket实现FTP
    """

    def __init__(self, hostname):
        """
        使用socket实现一个原生的FTP
        :param hostname: FTP主机地址
        """
        self.__client = TcpSocketClient.TcpSocketClient(hostname, 21)

    def login(self, usr, pwd):
        """
        登录FTP主机
        :param usr: 用户名
        :param pwd: 密码
        """
        self.__client.connect()
        self.__srv()
        self.__srv(f'USER {usr}')
        self.__srv(f'PASS {pwd}')
        self.__srv('bye')
        self.__client.close()

    def __srv(self, message:str=None):
        """
        发送信息并接受消息，并打印信息
        """
        if message:
            self.__client.send(message + '\r\n')
        response = self.__client.recv()
        print(f'[*] get reponse message: {response}')


if __name__ == '__main__':
    ftp = FtpRaw('192.168.181.134')
    ftp.login('zhangsan', '123123')