import random

from scapy.layers.inet import *


class Udp:

    def __init__(self, verbose=False):
        """
        构造一个udp对象
        :param verbose: 是否显示测试信息
        """
        self.__verbose = verbose

    def alive(self, dpst):
        """
        使用UDP协议来测试用户的主机是否处于存活状态
        原理：
            如果主机存活，则会返回icmp目的地无法到达信息
        :param dpst: 目的地址
        :return: 如果存活返回True，否则返回False
        """
        packet = IP(dst=dpst) / UDP(dport = random.randint(65535))
        response = sr1(packet, timeout=2, verbose=self.__verbose)

        if response:
            return response[ICMP].code == 3 and response[ICMP].type == 3
        else:
            return False


if __name__ == '__main__':
    udp = Udp()
    print(udp.alive('10.129.8.1'))