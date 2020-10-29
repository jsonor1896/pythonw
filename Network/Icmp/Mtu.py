from scapy.layers.inet import *

from Network.Tools import Tools


class Mtu:

    @classmethod
    def __send(cls, size, pdst=None):
        """
        发送固定大小的数据包
        :param size: 数据包大小
        :param pdst: 目标ip地址
        :return: 如果成功发送，返回True，否则返回False
        """
        ICMP_HEADER_SIZE = 20 + 8
        payload = Tools.random_bytes_message(size - ICMP_HEADER_SIZE)
        if pdst is None:
            pdst = socket.gethostbyname('www.baidu.com')
        message = IP(flags='DF', dst=pdst) / ICMP() / payload
        answered = sr1(message, timeout=2, verbose=False)

        return answered is not None

    @classmethod
    def __get_baidu_ip(cls):
        """
        获取百度的ip地址
        :return: 百度的ip地址
        """
        return socket.gethostbyname('www.baidu.com')

    @classmethod
    def calc(cls, minmtu=1440, maxmtu=1510):
        """
        通过icmp协议进行网络mtu的估计
        :param minmtu: 起始mtu测试值，默认是1440
        :param maxmtu: 最大mtu测试值，默认是1510
        :return: mtu值
        """
        pdst = cls.__get_baidu_ip()
        for size in range(maxmtu, minmtu, -1):
            res = cls.__send(size, pdst)
            if res:
                print(f'[+] {size} bytes message send success')
                return size
            else:
                print(f'[-] {size} bytes message send failed, the payload size is too larger for send')


if __name__ == '__main__':
   Mtu.calc()