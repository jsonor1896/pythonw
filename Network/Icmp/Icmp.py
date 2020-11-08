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

    def request_echo(self, pdst):
        """
        发送request echo请求
        :param pdst: 目的地ip地址
        :return: icmp响应数据包
        """
        ans, _ = self.__sendrecv(dst=pdst, payload=b'echo request')

        return ans

    def request_timestamp(self, pdst):
        """
        发送request timestamp请求，注意，在windows10 下需要使用管理员模式运行
        :param pdst: 目的地IP地址
        :return: icmp响应数据包
        """
        ans, _ = self.__sendrecv(dst=pdst, payload=b'timestamp')

        return ans

    def tracert(self, pdst):
        """
        路径检测
        :param pdst: 目的地IP地址
        """
        for ttl in range(0, 32):
            start = time.time()
            ans, unans = self.__sendrecv(dst=pdst, ttl=ttl, payload=b'tracert')
            interval = (time.time() - start) * 1000
            if ans:
                print('{:<5} reach {:<15} {:.2f}ms'.format(ttl, ans[IP].src, interval))
                if ans[ICMP].code == 0 and ans[ICMP].type == 0:
                    break
            else:
                print(f'{ttl}\treach *')

    def flood(self, pdst, randomsrc=False):
        """
        ICMP flood
        :param pdst: 目标主机ip地址
        :param randomsrc: 是否伪造ip地址
        """
        while True:
            if randomsrc:
                packet = self.__packet(dst=pdst, randomsrc=True, payload=b'abcdefg')
            else:
                packet = self.__packet(dst=pdst, payload=b'abcdefg')

            send(packet, count=1, verbose=self.__verbose)
            print(f'send packet dst = {pdst}, src = {packet[IP].src}')

    def scan_host(self, pdst):
        """
        扫描目标ip地址段，获取存活主机信息
        :param pdst: 目标ip地址段
        :return: 存活主机ip地址列表
        """
        host = []
        for ip in pdst:
            response = self.request_echo(str(ip))
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
            future_of_func = [executor.submit(self.request_echo, str(ip)) for ip in ips]
            for future in concurrent.futures.as_completed(future_of_func):
                res = future.result()
                if res:
                    active_hosts.append(future.result()[IP].src)

        return active_hosts

    def __packet(self, dst, ttl=64, type=8, code=0, randomsrc=False, payload=None):
        """
        打包一个特定的ICMP数据包
        :param dst: 目的地地址
        :param ttl: ttl值
        :param type: icmp的type
        :param code: icmp的code
        :param randomsrc: 是否随机ip地址
        :param payload: payload信息
        :return: ICMP数据包
        """
        if payload is None:
            payload = b'icmp payload'

        if randomsrc:
            src = RandIP()
            packet = IP(dst=dst, src=src, ttl=ttl) / ICMP(type=type, code=code) / payload
        else:
            packet = IP(dst=dst, ttl=ttl) / ICMP(type=type, code=code) / payload

        return packet

    def __sendrecv(self, dst, ttl=64, type=8, code=0, randomsrc=False, payload=None):
        """
        发送特定的ICMP协议数据，并返回响应数据结果
        :param dst: 目的地地址
        :param ttl: ttl值
        :param type: icmp的type
        :param code: icmp的code
        :param randomsrc: 是否随机ip地址
        :param payload: payload信息
        :return: 响应的数据包
        """
        packet = self.__packet(dst=dst, ttl=ttl, type=type, code=code, randomsrc=randomsrc, payload=payload)
        ans, unans = sr(packet, timeout=self.__timeout, verbose=self.__verbose)
        if len(ans) > 0:
            return ans[0][1], unans
        else:
            return None, unans


class InteractionIcmp:

    @staticmethod
    def run():
        parser = ArgumentParser('icmp tools')
        parser.add_argument('-v', '--verbose', action='store_true', help='display the debug information')
        parser.add_argument('-p', '--pdst', type=str, required=True, help='the destination ip of host')
        parser.add_argument('--spool', action='store_true', help='fake the source ip')
        parser.add_argument('-t', '--thread', type=int, default=4, help='the count of thread for scan host')

        mutual_group = parser.add_mutually_exclusive_group()
        mutual_group.add_argument('--echo', action='store_true', help='request echo icmp message')
        mutual_group.add_argument('--timestamp', action='store_true', help='timestamp request icmp message')
        mutual_group.add_argument('--tracert', action='store_true', help='icmp tracert')
        mutual_group.add_argument('--flood', action='store_true', help='icmp flood')
        mutual_group.add_argument('--scan', action='store_true', help='scan host')

        args = parser.parse_args()

        icmp = Icmp(verbose=args.verbose)

        if args.echo:
            response = icmp.request_echo(args.pdst)
            response.show() if response else print('do not find the host')
        elif args.timestamp:
            response = icmp.request_timestamp(args.pdst)
            response.show() if response else print('do not find the host')
        elif args.tracert:
            icmp.tracert(args.pdst)
        elif args.flood:
            icmp.flood(args.pdst, randomsrc=args.spool)
        elif args.scan:
            host = icmp.async_host_scan(args.pdst, process_count=args.thread)
            print('the list of active host')
            print(host)
        else:
            print('please input the correct arguments')


if __name__ == '__main__':
    InteractionIcmp.run()
