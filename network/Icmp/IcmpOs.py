# !/usr/bin/python
# -*- coding:utf-8 -*-
import os
import re
import time
from argparse import ArgumentParser


class IcmpOs:
    """
    通过调用windows命令ping实现功能

    对于系统命令而言，一般情况下如果调用成功，返回0，否则返回1
    """

    @classmethod
    def command(cls, host, count=1, timeout=1000, ttl=64, df=False, size=1510, callback=False):
        """
        获取指定参数的ping命令

        :param host: 目标主机
        :param count: 发送的数量
        :param timeout: 等待每次回复的超时时间
        :param ttl: 生存时间
        :param df: 在数据段中设置'DF'标志位
        :param size: 数据有效载荷的大小，单位字节
        :param callback: 是否有回显
        :return: 指定的ping命令
        """

        bk = '> NUL'
        if callback:
            bk = ''

        if df:
            cmd = 'ping {host} -n {count} -w {timeout} -f -l {size} {callback}'.format(
                host=host, count=count, timeout=timeout, size=size, callback=bk)
        else:
            cmd = 'ping {host} -n {count} -w {timeout} -i {ttl} {callback}'.format(
                host=host, count=count, timeout=timeout, ttl=ttl, callback=bk)

        return cmd

    @classmethod
    def alive(cls, host):
        """
        检查指定的主机是否存活

        :param host: 测试的目标主机
        :return: 如果主机存活，返回True，否则返回False
        """

        cmd = cls.command(host=host)
        code = os.system(cmd)

        return code == 0

    @classmethod
    def tracert(cls, host):
        """
        获取到达主机过程中经过的所有路由器信息

        :param host: 目标主机
        """

        WORD_RULE = r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}'
        TXT_FORAMT = '{:<3} reach {:<15} {:.2f}ms'

        for ttl in range(1, 32):
            cmd = cls.command(host=host, ttl=ttl, callback=True, timeout=3000)

            start = time.time()
            txt = os.popen(cmd).read()
            inter = (time.time() - start) * 1000.0

            # 当出现超时状态时，丢包率往往时100%
            if '100%' in txt:
                print(TXT_FORAMT.format(ttl, '*', inter))
                continue

            # 搜索返回值中的路由ip地址
            result = re.finditer(WORD_RULE, txt)
            print(TXT_FORAMT.format(ttl, list(result)[1].group(), inter))

            # 到达目的地之后，TTL会正常显示，出现'TTL=数字'的字符信息
            if 'TTL=' in txt: break

    @classmethod
    def mtu(cls, host='www.baidu.com', minmtu=1440, maxmtu=1510):
        """
        测试网络的mtu值，默认的测试范围是 [1510, 1440]

        :param host: 默认的测试主机是:www.baidu.com
        :param minmtu: 默认的最小mtu=1440
        :param maxmtu: 默认的最大mtu=1510
        :return: 当前网络的mtu值
        """

        for size in range(maxmtu - 28, minmtu - 28, -1):
            cmd = cls.command(host, df=True, size=size)
            resp = os.system(cmd)
            mtu = size + 28
            if resp > 0:
                print(f'[-] {mtu} bytes message send failed, the payload size is too larger for send')
            else:
                print(f'[+] {mtu} bytes message send success')
                return mtu


if __name__ == '__main__':
    parser = ArgumentParser(description='基于系统ping命令的icmp工具包')

    # 主机
    parser.add_argument('-p', '--host', help='目标主机', type=str, default='www.baidu.com')

    # mtu测试参数
    parser.add_argument('--min', help='最小mtu', default=1440, type=int)
    parser.add_argument('--max', help='最大mtu', default=1510, type=int)

    # 互斥量
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--tracert', help='路由路径监测', action='store_true')
    group.add_argument('--mtu', help='测试网络mtu值', action='store_true')

    args = parser.parse_args()

    if args.mtu:
        IcmpOs.mtu(args.host, args.min, args.max)
    elif args.tracert:
        IcmpOs.tracert(args.host)
    else:
        alive = IcmpOs.alive(args.host)
        print(args.host, alive)
