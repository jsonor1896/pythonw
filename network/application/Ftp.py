import ftplib


class Ftp:

    def __init__(self, hostname):
        """
        Ftp对象
        :param hostname: 主机地址
        """
        self.__hostname = hostname
        self.__ftp = ftplib.FTP()
        self.__connected = False

    def connect(self, port=0):
        """
        连接主机FTP端口
        :return: 连接成功返回weclome语句,否则返回False
        """
        try:
            resp = self.__ftp.connect(self.__hostname, port)
            # print(f'\n[+] {self.__hostname} FTP Connect Success')
            self.__connected = True
            return resp
        except ConnectionRefusedError as connect_error:
            print(f'\n[-] {self.__hostname} FTP Connect Failed!')
            return False

    def login(self, usr, pwd):
        """
        使用用户名和密码登录目标FTP服务器
        :param usr: 用户名
        :param pwd: 密码
        :return: 登录成功返回True，否则返回False
        """
        if not self.__connected:
            raise ConnectionError('Do not connect to the server before login.')

        try:
            self.__ftp.login(usr, pwd)
            print(f'\n[*] {self.__hostname} FTP ({usr}:{pwd}) Login Success!')
            self.__ftp.quit()
            return True
        except Exception as e:
            print(f'\n[*] {self.__hostname} FTP ({usr}:{pwd}) Login Failed!')
            return False

    def anonymous(self):
        """
        匿名登录服务器
        :return: 登录成功返回True，否则返回False
        """
        return self.login('anonymous', '')


if __name__ == '__main__':
    ftp = Ftp('192.168.181.134')
    resp = ftp.connect()
    if resp: ftp.login('zhangsan', '123123')
