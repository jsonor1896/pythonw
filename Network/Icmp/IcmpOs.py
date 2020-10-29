# !/usr/bin/python
# -*- coding:utf-8 -*-
import concurrent
import ipaddress
import os
import subprocess
from argparse import ArgumentParser
from concurrent.futures.process import ProcessPoolExecutor


class IcmpOs:
    """
    通过调用系统命令的方式进行ping扫描
    在windows 10下运行的时候发现无论是os.system()还是subprocess.call()在任何情况下返回的都是0，因此无法使用
    但是在kali下在ping完成的情况下返回0，如果无法ping通则返回非零值
    """

    def __init__(self, pdst):
        """
        目的地ip地址
        :param pdst: ip地址段信息
        """
        self.__ips = list(ipaddress.ip_network(pdst).hosts())

    @classmethod
    def ping_os(cls, ip):
        """
        调用系统命令ping实现对单个ip地址的ping操作
        linux下命令的重定向：ping www.baidu.com > /dev/null
        :return: 如果ping成功，返回True，否则返回False
        """
        with open(os.devnull, 'w') as fnull:
            cmd = 'ping {} {}'.format(ip, '-c 1')
            # 也可以用 os.system(cmd, shell=True, stdout=fnull, stderr=fnull)
            result = subprocess.call(cmd, shell=True, stdout=fnull, stderr=fnull)

        return (str(ip), False) if result else (str(ip), True)

    def start(self):
        """
        开始进行ping扫描
        :return: 主机存活状态信息集合[(ip,live_status)...]
        """
        scan_result = []
        for ip in self.__ips:
            res = self.ping_os(ip)
            scan_result.append(res)

        return scan_result

    def start_multiprocess(self):
        """
        使用多核进行加速
        :return: 主机存活的集合
        """
        scan_result = []

        with ProcessPoolExecutor(max_workers=10) as executor:
            future_of_func = [executor.submit(self.ping_os, ip) for ip in self.__ips]
            for future in concurrent.futures.as_completed(future_of_func):
                scan_result.append(future.result())

        return scan_result

class InteractionIcmpOs:

    @staticmethod
    def run():
        args_parser = ArgumentParser('icmp detector by os')
        args_parser.add_argument('-p', '--pdst', required=True, type=str)

        args = args_parser.parse_args()
        icmp_os = IcmpOs(args.pdst)
        result_list = icmp_os.start()
        for item in result_list:
            print(item)


if __name__ == '__main__':
    InteractionIcmpOs.run()





