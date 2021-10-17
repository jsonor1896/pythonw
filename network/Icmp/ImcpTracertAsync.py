import os
import re
import threading
import time

from scapy.layers.inet import ICMP, IP, traceroute, UDP
from scapy.sendrecv import sr, sr1
from scapy.volatile import RandInt, RandShort


class Route:

    def __init__(self, ttl, ip, time):
        self.ttl = ttl
        self.ip = ip
        self.time = time

    def sameIP(self, route):
        return self.ip == route.ip

    def print(self):
        if self.ip != '*':
            TXT_FORAMT = '{:<3} reach {:<15} {:.2f}ms'
            print(TXT_FORAMT.format(self.ttl, self.ip, self.time))
        else:
            print('{:<3} reach {:<15} {:<2}'.format(self.ttl, self.ip, self.time))


class IcmpTracertAsync:

    def __init__(self, pdst):
        self.pdst = pdst
        self.routes = {}
        self.ips = set()
        self.finished = False

    def matchIP(self, string):
        rule = r'((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})(\.((2(5[0-5]|[0-4]\d))|[0-1]?\d{1,2})){3}'
        result = re.finditer(rule, string)
        return list(result)[1].group()

    def getRouteIP(self, ttl):
        cmd = 'ping {host} -n 1 -w 3000 -i {ttl}'.format(host=self.pdst, ttl=ttl)

        start = time.time()
        txt = os.popen(cmd).read()
        inter = (time.time() - start) * 1000.0

        # 当出现超时状态时，丢包率往往时100%
        if '100%' in txt:
            route = Route(ttl, '*', '*')
            self.routes[ttl] = route
            return

        # 搜索返回值中的路由ip地址
        ip = self.matchIP(txt)
        if ip not in self.ips:
            self.ips.add(ip)
            route = Route(ttl, ip, inter)
            self.routes[ttl] = route

        # 到达目的地之后，TTL会正常显示，出现'TTL=数字'的字符信息
        if 'TTL=' in txt: self.finished = True

    def asyncGetRouteIP(self, ):
        threads = []
        for ttl in range(1, 18):
            th = threading.Thread(target=self.getRouteIP, args=(ttl,))
            th.start()
            threads.append(th)

        for thread in threads:
            thread.join()


if __name__ == '__main__':
    tracert = IcmpTracertAsync('www.baidu.com')
    tracert.asyncGetRouteIP()
    for key, route in tracert.routes.items():
      route.print()
